#!/usr/bin/env python3
"""What the session's transcripts say happened — the retro's numbers, not anybody's memory of them.

    transcripts.py <session folder>                 # one row per manager and executor transcript, then the notes
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


def read(path: Path, who: str, slug: str | None = None) -> Stats | None:
    """Stats of one transcript; with `slug`, a manager's, counted from its first line that works on the folder."""
    s = Stats(who, path)
    started = slug is None
    usage: dict[str, dict] = {}
    model: dict[str, str] = {}
    pending: dict[str, str] = {}   # tool_use id → its call
    failed: set[str] = set()
    for entry in lines(path):
        if not started:
            if entry.get("type") != "assistant" or not names_folder(entry, slug):
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
        if slug in first_prompt(t) and (s := read(t, executor_label(t))) is not None:
            found.append(s)
            dirs.add(t.parent.parent if t.parent.parent.parent == root else t.parent.parent.parent)
    for d in sorted(dirs):
        for t in sorted(d.glob("*.jsonl")):
            if (s := read(t, f"manager {t.stem[:8]}", slug)) is not None:
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


def render(found: list[Stats], folder: Path) -> list[str]:
    out = [f"Transcripts of {folder.name}: {sum(s.who.startswith('manager') for s in found)} manager, "
           f"{sum(not s.who.startswith('manager') for s in found)} subagent",
           "",
           "| # | who | model | started | time | context peak | output | tool calls | errors | refused | compacted |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(found, 1):
        comp = ", ".join(f"at {k(p)}" for p in s.compactions) or "—"
        top = s.models.most_common(1)[0][0].removeprefix("claude-") if s.models else "?"
        out.append(f"| {i} | {s.who} | {top} | {when(s.first)} | {minutes(s.active_ms)} | {k(s.peak)} | {k(s.output)} | "
                   f"{sum(s.tools.values())} | {s.errors} | {sum(s.denied.values())} | {comp} |")
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
