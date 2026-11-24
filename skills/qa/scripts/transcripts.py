#!/usr/bin/env python3
"""What the session's transcripts say happened — the retro's numbers, not anybody's memory of them.

    transcripts.py <session folder>                 # one row per manager and executor transcript, where each one's context went, then the notes
    transcripts.py <session folder> --root <dir>    # transcripts kept somewhere other than ~/.claude/projects

The retro is written from the manager's memory and the executors' own retro sections, and both are summaries
written by the party being reviewed — the very thing acceptance says not to trust. The transcripts on disk are
the record, but an executor's runs to megabytes (screenshots, page dumps), so nobody reads one. This reads all
of them and prints a screen: who ran how long, how large their context grew, what failed, what was refused,
what was retried after failing, and where the context was compacted. What it means is the retro's call.

A transcript belongs to the session when it names the folder's slug — the name without its date, since a
continued session renames the folder to the current date: an executor by its prompt, a manager by a write into
the folder or a launch that names it (reading the folder is not enough — a later session may only consult it).
A manager is counted from its first such line, its time is the sum of its turns (the user's pauses excluded).

The cost of a transcript is its processed context — every call re-sends the whole context, so the sum over calls,
not the peak, is what a session pays (and why a long tail at a large context costs more than the plan did). Where it
went is measured, not guessed from characters: between two calls the context grows by the first call's output (its
usage) plus what came back, and that growth is split among the items that came back by their characters, within that
gap only. A drop (compaction, thinking stripped at a new user turn) removes thinking first, then scales the rest.

Exit code 0 when transcripts were found, 1 when none were, 2 on a usage error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

DATED = re.compile(r"^\d{4}-\d{2}-\d{2}_")
WRITES = {"Write", "Edit", "MultiEdit", "NotebookEdit"}   # by `file_path`
LAUNCHES = {"Agent", "Task"}                            # by `prompt`
REPEAT_AT = 3   # the same call answered the same way this many times is worth a look
IDLE_MS = 15 * 60 * 1000   # a gap longer than this is a pause (resumed later), not work
SHOWN = 3       # notes per kind per transcript
IMAGE_CHARS = 9000   # an image in a tool result weighs about as much as this much text

# Where the context went: the columns of the second table, in order.
START, ENGINE, PROFILE, OWN, OTHER_SESSIONS, OUTPUT, WORK = (
    "start", "engine", "profile+KB", "this session", "other sessions", "model output", "product & other")
PARTS = (START, ENGINE, PROFILE, OWN, OTHER_SESSIONS, OUTPUT, WORK)
_ENGINE = re.compile(r"qa-cube|/skills/qa/|/agents/qa-")
_FEEDBACK = re.compile(r"qa-cube-feedback\.md")   # the project's file, though its name says qa-cube
_PROFILE = re.compile(r"\.claude/qa-profile|(^|[\s'\"/=])knowledge[\w-]*(/|$|[\s'\"])", re.I)   # the profile, the KB as a directory


def mentions_dir(aim: str, d: Path) -> bool:
    """`aim` names a path inside `d` — in full, or relative through `d`'s own name as a whole path component.
    A URL never counts: an API's `/sessions/` is not the sessions folder."""
    if str(d) in aim:
        return True
    return any("://" not in tok and (tok.startswith(f"{d.name}/") or f"/{d.name}/" in tok)
               for tok in re.split(r"[\s'\"=]+", aim))


def slug_of(folder: Path) -> str:
    return DATED.sub("", folder.name)


def mangle(path: Path) -> str:
    """The directory name Claude Code gives a working directory's transcripts."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def project_dirs(root: Path, folder: Path) -> list[Path]:
    """The transcript directories of every working directory the session could have run from."""
    real = folder.resolve()   # a symlinked path (macOS `/var` → `/private/var`) is named either way
    names = {mangle(p) for p in (folder, *folder.parents, real, *real.parents)}
    slug = mangle(Path(slug_of(folder)))
    return sorted(d for d in root.iterdir() if d.is_dir() and (d.name in names or slug in d.name))


@dataclass
class Stats:
    who: str
    path: Path
    first: str = ""
    last: str = ""
    active_ms: int = 0
    peak: int = 0
    output: int = 0
    tools: Counter = field(default_factory=Counter)
    errors: int = 0
    denied: Counter = field(default_factory=Counter)
    retried: Counter = field(default_factory=Counter)
    repeats: Counter = field(default_factory=Counter)
    pauses: list[int] = field(default_factory=list)
    compactions: list[int] = field(default_factory=list)
    models: Counter = field(default_factory=Counter)
    processed: int = 0
    parts: Counter = field(default_factory=Counter)   # PARTS → tokens summed over calls


def lines(path: Path):
    with path.open(errors="replace") as fh:
        for raw in fh:
            try:
                yield json.loads(raw)
            except json.JSONDecodeError:
                continue


def blocks(entry: dict) -> list[dict]:
    content = (entry.get("message") or {}).get("content")
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def first_prompt(path: Path) -> str:
    for entry in lines(path):
        if entry.get("type") == "user":
            content = entry["message"].get("content")
            return content if isinstance(content, str) else " ".join(b.get("text", "") for b in blocks(entry))
    return ""


def call_key(block: dict) -> str:
    return f"{block.get('name')} {json.dumps(block.get('input'), sort_keys=True, ensure_ascii=False)}"


def names_folder(entry: dict, slug: str) -> bool:
    """A manager's line that works ON the folder: a write into it or a launch that names it.

    Not a shell command and not an edit elsewhere that mentions the folder: a later session's monthly sweep
    moves it with `mv` and rewrites the links to it in other sessions' files, and is no part of this one."""
    for b in blocks(entry):
        if b.get("type") != "tool_use" or not isinstance(b.get("input"), dict):
            continue
        if b.get("name") in WRITES and slug in str(b["input"].get("file_path", "")):
            return True
        if b.get("name") in LAUNCHES and slug in str(b["input"].get("prompt", "")):
            return True
    return False


def target(block: dict, folder: Path | None) -> str:
    """Which column of «where the context went» a tool's result belongs to, by what the call was aimed at."""
    inp = block.get("input") if isinstance(block.get("input"), dict) else {}
    aim = " ".join(str(inp.get(k, "")) for k in ("file_path", "command", "path", "pattern", "skill"))
    if _FEEDBACK.search(aim):
        return PROFILE
    if block.get("name") == "Skill" or _ENGINE.search(aim):
        return ENGINE
    if _PROFILE.search(aim):
        return PROFILE
    if folder is not None and slug_of(folder) in aim:
        return OWN
    if folder is not None and mentions_dir(aim, folder.parent):
        return OTHER_SESSIONS
    return WORK


def size(block: dict) -> int:
    content = block.get("content")
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(str(b.get("text", ""))) + (IMAGE_CHARS if b.get("type") == "image" else 0)
                   for b in content if isinstance(b, dict))
    return 0


class Ledger:
    """What the context of the next call is made of, kept call by call (the module docstring says how)."""

    def __init__(self):
        self.base: int | None = None
        self.held = Counter()
        self.thinking = 0.0
        self.incoming = Counter()   # what came back since the last call, in characters

    def call(self, context: int) -> Counter:
        """The composition of this call's context, in tokens."""
        if self.base is None:
            self.base = context
        else:
            gap = context - self.base - sum(self.held.values()) - self.thinking
            if gap < 0:
                cut = min(self.thinking, -gap)
                self.thinking -= cut
                rest = -gap - cut
                total = sum(self.held.values())
                if rest and total:
                    keep = max(0.0, 1 - rest / total)
                    for k in self.held:
                        self.held[k] *= keep
                if rest > total:   # below the first call's size: what is left of the start shrinks too
                    self.base = max(0, self.base - (rest - total))
            elif gap:
                came = sum(self.incoming.values())
                for k, v in (self.incoming.items() if came else [(WORK, 1)]):
                    self.held[k] += gap * v / (came or 1)
        self.incoming = Counter()
        now = Counter(self.held)
        now[START] += self.base
        now[OUTPUT] += self.thinking
        return now

    def output(self, usage: dict) -> None:
        """A call's output stays in the context: its thinking (dropped first when the context shrinks) and the rest."""
        out = int(usage.get("output_tokens") or 0)
        think = min(out, int((usage.get("output_tokens_details") or {}).get("thinking_tokens") or 0))
        self.thinking += think
        self.held[OUTPUT] += out - think


def read(path: Path, who: str, slug: str | None = None, folder: Path | None = None) -> Stats | None:
    """Stats of one transcript; with `slug`, a manager's, counted from its first line that works on the folder.
    `folder` sorts what the transcript read into this session's files, other sessions' and the rest."""
    s = Stats(who, path)
    started = slug is None
    usage: dict[str, dict] = {}
    model: dict[str, str] = {}
    pending: dict[str, str] = {}   # tool_use id → its call
    aimed: dict[str, str] = {}     # tool_use id → the column its result goes to
    failed: set[str] = set()
    ledger = Ledger()
    every: dict[str, dict] = {}   # every call's usage, before the start too: the ledger needs the whole history
    last_id = ""
    for entry in lines(path):
        kind = entry.get("type")
        msg = entry.get("message") or {}
        if kind == "assistant" and msg.get("id") and msg.get("usage"):
            if msg["id"] not in every:   # a new call: the previous one's output is in, its growth is measurable now
                if last_id:
                    ledger.output(every[last_id])
                context = sum(int(msg["usage"].get(k) or 0) for k in
                              ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
                now = ledger.call(context)
                if started or names_folder(entry, slug):
                    s.parts.update(now)
                    s.processed += context
                last_id = msg["id"]
            every[msg["id"]] = msg["usage"]
            for b in blocks(entry):
                if b.get("type") == "tool_use":
                    aimed.setdefault(b.get("id"), target(b, folder))
        elif kind == "user" and last_id:
            content = msg.get("content")
            texts = [content] if isinstance(content, str) else [b.get("text", "") for b in blocks(entry) if b.get("type") == "text"]
            for t in texts:
                ledger.incoming[ENGINE if "qa-cube" in t and "Base directory for this skill" in t else WORK] += len(t)
            for b in blocks(entry):
                if b.get("type") == "tool_result":
                    ledger.incoming[aimed.get(b.get("tool_use_id"), WORK)] += size(b)
        if not started:
            if kind != "assistant" or not names_folder(entry, slug):
                continue
            started = True
        ts = entry.get("timestamp")
        if ts:
            if s.last and slug is None:
                gap = span_ms(s.last, ts)
                if gap > IDLE_MS:
                    s.pauses.append(gap)
                else:
                    s.active_ms += max(gap, 0)
            s.first = s.first or ts
            s.last = ts
        kind = entry.get("type")
        if kind == "system":
            if entry.get("subtype") == "turn_duration":
                s.active_ms += int(entry.get("durationMs") or 0)
            elif entry.get("subtype") == "compact_boundary":
                s.compactions.append(int((entry.get("compactMetadata") or {}).get("preTokens") or 0))
        elif kind == "assistant":
            msg = entry.get("message") or {}
            if msg.get("id") and msg.get("usage"):
                usage[msg["id"]] = msg["usage"]   # a message is streamed over several lines; the last carries the total
                model[msg["id"]] = msg.get("model") or "?"
            for b in blocks(entry):
                if b.get("type") == "tool_use" and b.get("id") not in pending:
                    key = call_key(b)
                    pending[b["id"]] = key
                    s.tools[b.get("name")] += 1
                    if key in failed:
                        s.retried[key] += 1
        elif kind == "user":
            for b in blocks(entry):
                if b.get("type") == "tool_result":
                    answer = json.dumps(b.get("content"), sort_keys=True, ensure_ascii=False)
                    s.repeats[(pending.get(b.get("tool_use_id"), "?"), hash(answer))] += 1
                if b.get("type") == "tool_result" and b.get("is_error"):
                    if entry.get("toolDenialKind"):
                        s.denied[pending.get(b.get("tool_use_id"), "?").split(" ", 1)[0]] += 1
                    else:
                        s.errors += 1
                    failed.add(pending.get(b.get("tool_use_id"), ""))
    if not started:
        return None
    for u in usage.values():
        s.peak = max(s.peak, sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")))
        s.output += int(u.get("output_tokens") or 0)
    s.models = Counter(model.values())
    return s


def span_ms(first: str, last: str) -> int:
    if not first or not last:
        return 0
    return int((parse(last) - parse(first)).total_seconds() * 1000)


def parse(ts: str) -> dt.datetime:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def executor_label(path: Path) -> str:
    meta = path.with_suffix(".meta.json")
    try:
        m = json.loads(meta.read_text())
    except (OSError, json.JSONDecodeError):
        return "subagent"
    kind = str(m.get("agentType") or "subagent").split(":")[-1]
    desc = str(m.get("description") or "").strip()
    return f"{kind} «{desc}»" if desc else kind


def collect(root: Path, folder: Path) -> list[Stats]:
    """Executors are found anywhere (a prompt is one line to read); managers in the directories of the working
    directories above the folder and of the executors found — a project that moved keeps its old transcripts
    under its old path's name."""
    slug = slug_of(folder)
    found: list[Stats] = []
    dirs = set(project_dirs(root, folder))
    for t in sorted({*root.glob("*/subagents/*.jsonl"), *root.glob("*/*/subagents/*.jsonl")}):
        if slug in first_prompt(t) and (s := read(t, executor_label(t), folder=folder)) is not None:
            found.append(s)
            dirs.add(t.parent.parent if t.parent.parent.parent == root else t.parent.parent.parent)
    for d in sorted(dirs):
        for t in sorted(d.glob("*.jsonl")):
            if (s := read(t, f"manager {t.stem[:8]}", slug, folder)) is not None:
                found.append(s)
    return sorted(found, key=lambda s: s.first)


def k(n: int) -> str:
    return f"{n / 1000:.0f}k" if n >= 1000 else str(n)


def minutes(ms: int) -> str:
    m = round(ms / 60000)
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


def when(ts: str) -> str:
    return parse(ts).astimezone().strftime("%m-%d %H:%M") if ts else "?"


def short(key: str, width: int = 90) -> str:
    return key if len(key) <= width else key[: width - 1] + "…"


def where_it_went(found: list[Stats]) -> list[str]:
    """The second table: each transcript's processed context split by what put it there, in percent."""
    def row(label: str, parts: Counter) -> str:
        total = sum(parts.values()) or 1
        return f"| {label} | " + " | ".join(f"{100 * parts[p] / total:.0f}%" for p in PARTS) + " |"
    head = ["Where the context went (share of each transcript's processed context; «start» is its first call: system prompt, "
            "tools, agent file, launch prompt):", "",
            "| # | " + " | ".join(PARTS) + " |", "|---|" + "---|" * len(PARTS)]
    rows = [row(f"{i}", s.parts) for i, s in enumerate(found, 1) if s.processed]
    total = sum((s.parts for s in found), Counter())
    return head + rows + ([row("all", total)] if len(rows) > 1 else [])


def render(found: list[Stats], folder: Path) -> list[str]:
    out = [f"Transcripts of {folder.name}: {sum(s.who.startswith('manager') for s in found)} manager, "
           f"{sum(not s.who.startswith('manager') for s in found)} subagent",
           "",
           "| # | who | model | started | time | context peak | processed | output | tool calls | errors | refused | compacted |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(found, 1):
        comp = ", ".join(f"at {k(p)}" for p in s.compactions) or "—"
        top = s.models.most_common(1)[0][0].removeprefix("claude-") if s.models else "?"
        out.append(f"| {i} | {s.who} | {top} | {when(s.first)} | {minutes(s.active_ms)} | {k(s.peak)} | {k(s.processed)} | {k(s.output)} | "
                   f"{sum(s.tools.values())} | {s.errors} | {sum(s.denied.values())} | {comp} |")
    out += ["", *where_it_went(found)]
    notes = []
    for i, s in enumerate(found, 1):
        if s.denied:
            notes.append(f"#{i} refused: " + ", ".join(f"{t} ×{n}" for t, n in s.denied.most_common(SHOWN)))
        for key, n in s.retried.most_common(SHOWN):
            notes.append(f"#{i} retried after failing ×{n}: {short(key)}")
        for (key, _), n in [(key, n) for key, n in s.repeats.most_common() if n >= REPEAT_AT][:SHOWN]:
            notes.append(f"#{i} same call, same answer ×{n}: {short(key)}")
        if s.pauses:
            notes.append(f"#{i} paused ×{len(s.pauses)} (longest {minutes(max(s.pauses))}), not counted in its time")
    if found and not any(s.who.startswith("manager") for s in found):
        notes.append("no manager transcript found — Claude Code deletes transcripts after `cleanupPeriodDays` (30 by default)")
    if notes:
        out += ["", "Notes (facts to read, not verdicts):", *(f"- {n}" for n in notes)]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("folder", type=Path, help="the session folder")
    ap.add_argument("--root", type=Path, default=Path.home() / ".claude" / "projects",
                    help="where Claude Code keeps transcripts")
    a = ap.parse_args(argv)
    folder = a.folder.absolute()
    if not folder.is_dir():
        print(f"no such folder: {folder}", file=sys.stderr)
        return 2
    if not a.root.is_dir():  # another harness: no Claude Code transcripts at all — «none found», not a usage error
        print(f"no transcripts: {a.root} does not exist", file=sys.stderr)
        return 1
    found = collect(a.root, folder)
    if not found:
        print(f"no transcript names {slug_of(folder)} under {a.root}", file=sys.stderr)
        return 1
    print("\n".join(render(found, folder)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
