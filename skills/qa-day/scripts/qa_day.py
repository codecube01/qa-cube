#!/usr/bin/env python3
"""A digest of qa-cube test sessions: what was tested on a date (or over the last N days), across one or several projects.

Reads only, writes nothing, and never leaves the session folders: the tracker, the queue of tasks and any personal notes are
somebody else's business (project skills), this script's whole contract is «the facts that already live in <sessions>/».

Usage (stdlib only, no dependencies):

    qa_day.py                               # today, the current repository
    qa_day.py ~/src/a ~/src/b               # today, two project roots
    qa_day.py --days 7 ~/src/a ~/src/b      # the last 7 days, ending today
    qa_day.py --date 2026-09-01              # one past day
    qa_day.py --task ACME-412 ~/src/a       # the freshest session on a task, whatever its date

Per root the sessions path comes from `<root>/.claude/qa-profile.md` (the `sessions:` key); no profile or no key — the
contract's default `docs/test-sessions/`. Nothing found is not an error: the root gets an honest note and the run carries on,
because a digest that dies on the first unconfigured project is a digest nobody runs twice.

The day of a session is the date in its FOLDER NAME (`<YYYY-MM-DD>_<source>-<slug>/`), never a file's mtime: by the engine's
convention the folder is named after the last round and a retest renames it. A session worked on today whose folder was not
renamed is therefore invisible here — deliberately, since mtime counts a stray typo fix as a round.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# The contract's default when the project has no profile yet.
DEFAULT_SESSIONS = "docs/test-sessions/"

# The current names first, then the names earlier schemes used — live projects hold both, and a round that ran under the old
# scheme is still a round that happened.
PASSPORT_NAMES = ("0-session.md", "session.md")
REPORT_NAMES = ("99-report.md", "report.md")

# The severity scale is an engine identifier and is never translated, so it is the one anchor in a localized report that a
# script may match on: the count of findings is the count of rows carrying one of these.
PRIORITIES = ("Blocker", "Critical", "Major", "Minor")

FOLDER_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(.+)$")
KEY_RE = re.compile(r"^[-*\s]*\*{0,2}(sessions|language)\*{0,2}\s*:\s*(.+)$", re.I)
TABLE_SEP_RE = re.compile(r"^\|[\s:|\-]+\|?\s*$")
# A task id as trackers shape them: a prefix plus a number — `ACME-412`, `acme-412`, or the `<prefix>#<number>` form.
ID_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9_]{0,15}[-#]\d+\b")

REGISTRY_MAX = 1000
TAIL_SECTIONS = 3
TAIL_MAX = 240


# --- small helpers -----------------------------------------------------------------------------------------------------


def oneline(text: str, limit: int) -> str:
    """Collapse to a single line and cut to `limit`, marking the cut."""
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_fences(lines: list[str]) -> list[str]:
    """Everything outside ``` fences. The report's last fenced block is the ready-made tracker comment — a retelling of the
    report rather than a fact of its own, and printing it would make the digest twice as long for nothing."""
    out: list[str] = []
    inside = False
    for line in lines:
        if line.strip().startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return out


def table_rows(lines: list[str]) -> list[str]:
    """The data rows of the first markdown table in `lines` — the header row and the `|---|` separator dropped."""
    block: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            block.append(stripped)
        elif block:
            break
    rows = [r for r in block if not TABLE_SEP_RE.match(r)]
    return rows[1:] if len(rows) > 1 else []


# --- the project profile -----------------------------------------------------------------------------------------------


def profile_of(root: Path) -> dict[str, str]:
    """`sessions` and `language` out of `<root>/.claude/qa-profile.md`, plus a note on where they came from.

    Only these two keys are read and no new key is introduced: the digest has to work the moment the plugin is installed,
    without a single extra question at onboarding.
    """
    out = {"sessions": DEFAULT_SESSIONS, "language": "", "source": "the contract's default (no profile)"}
    profile = root / ".claude" / "qa-profile.md"
    if not profile.is_file():
        return out
    out["source"] = ".claude/qa-profile.md"
    found: dict[str, str] = {}
    for line in read(profile).splitlines():
        match = KEY_RE.match(line)
        if not match:
            continue
        key = match.group(1).lower()
        if key in found:
            continue  # the header wins over any later prose that repeats the word
        value = match.group(2).split("#")[0].strip().strip("`").strip()
        if value:
            found[key] = value
    if found.get("sessions") and found["sessions"].lower() != "none":
        out["sessions"] = found["sessions"]
    else:
        out["source"] = ".claude/qa-profile.md (no `sessions:` key — the contract's default)"
    out["language"] = found.get("language", "")
    return out


# --- the session's own files -------------------------------------------------------------------------------------------


def find_passport(folder: Path) -> Path | None:
    for name in PASSPORT_NAMES:
        if (folder / name).is_file():
            return folder / name
    return None


def find_report(folder: Path) -> Path | None:
    for name in REPORT_NAMES:
        if (folder / name).is_file():
            return folder / name
    # Legacy schemes numbered the report (`6-report.md`, `report-2.md`): take the highest number, i.e. the freshest.
    candidates = [p for p in sorted(folder.glob("*report*.md")) if p.is_file()]
    if not candidates:
        return None

    def rank(path: Path) -> tuple[int, str]:
        digits = re.match(r"^(\d+)", path.name)
        return (int(digits.group(1)) if digits else -1, path.name)

    return sorted(candidates, key=rank)[-1]


def parse_passport(text: str) -> dict:
    """Title, header block and the last row of the round log.

    The passport is written in the project's language, so nothing here matches a field's caption: what is matched is the
    template's structure — the `- **field:** value` rows above the first `##`, then the first table after them. The values
    are printed verbatim and read by the agent, which is what makes the digest language-agnostic.
    """
    lines = text.splitlines()
    title = ""
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            start = i + 1
            break
    header: list[str] = []
    body_at = len(lines)
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith("## "):
            body_at = i
            break
        if re.match(r"^\s*-\s+\*\*", line):
            header.append(line.strip())
    rows = table_rows(lines[body_at:])
    return {"title": title, "header": header, "last_round": rows[-1] if rows else ""}


def parse_report(text: str) -> dict:
    """The verdict lines, the count of findings by severity and the report's tail sections.

    The report's section titles are localized too, so they are taken by position and by heuristic rather than by caption:
    the findings are counted off the untranslated severity scale, and the tail sections (leftovers on the environment, open
    questions) are printed with their own headings for the agent to read. A section that is absent is simply absent — a
    project format that has no such section must not break the run.
    """
    lines = text.splitlines()
    cut = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    verdict = [l.strip() for l in lines[:cut] if l.strip().startswith("**")]

    counts: dict[str, int] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or TABLE_SEP_RE.match(stripped):
            continue
        for priority in PRIORITIES:
            if re.search(rf"\b{priority}\b", stripped):
                counts[priority] = counts.get(priority, 0) + 1
                break

    sections: list[tuple[str, list[str]]] = []
    heading = ""
    body: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if heading:
                sections.append((heading, body))
            heading, body = line[3:].strip(), []
        elif heading:
            body.append(line)
    if heading:
        sections.append((heading, body))

    tail: list[str] = []
    for name, content in reversed(sections):
        if len(tail) >= TAIL_SECTIONS:
            break
        prose = [l.strip() for l in strip_fences(content) if l.strip() and not l.strip().startswith(("|", "_"))]
        if not prose:
            continue
        tail.append(f"{name} → {oneline(' '.join(prose), TAIL_MAX)}")
    return {"verdict": verdict, "findings": counts, "tail": list(reversed(tail))}


# --- walking the sessions ----------------------------------------------------------------------------------------------


class Session:
    def __init__(self, folder: Path) -> None:
        self.folder = folder
        match = FOLDER_RE.match(folder.name)
        self.date = match.group(1) if match else ""
        self.slug = match.group(2) if match else folder.name
        self.passport_path = find_passport(folder)
        self.report_path = find_report(folder)
        self.passport = parse_passport(read(self.passport_path)) if self.passport_path else None
        self.report = parse_report(read(self.report_path)) if self.report_path else None

    @property
    def tasks(self) -> list[str]:
        """The session's task ids: the folder name (the main task) plus the passport's title (a multi-task session names
        the rest there). Deliberately NOT the whole passport — its body lists parent tasks, neighbors and past rounds, and
        that noise would make every digest line claim half the tracker."""
        found: list[str] = []
        for text in (self.slug, (self.passport or {}).get("title", "")):
            for hit in ID_RE.findall(text or ""):
                if hit.lower() not in [f.lower() for f in found]:
                    found.append(hit)
        return found


def iter_sessions(sessions_dir: Path) -> list[Session]:
    """Session folders at both levels: the root of `<sessions>/` holds what is alive, its subfolders the month archives."""
    out: list[Session] = []
    if not sessions_dir.is_dir():
        return out
    for entry in sorted(sessions_dir.iterdir()):
        if not entry.is_dir():
            continue
        if FOLDER_RE.match(entry.name):
            out.append(Session(entry))
            continue
        for nested in sorted(entry.iterdir()):
            if nested.is_dir() and FOLDER_RE.match(nested.name):
                out.append(Session(nested))
    return out


def registry_lines(sessions_dir: Path, folder_name: str) -> list[str]:
    """The session's row in `<sessions>/README.md` — the engine keeps one line per session there."""
    readme = sessions_dir / "README.md"
    if not readme.is_file():
        return []
    try:
        return [oneline(l, REGISTRY_MAX) for l in read(readme).splitlines() if folder_name in l]
    except OSError:
        return []


# --- printing ----------------------------------------------------------------------------------------------------------


def print_session(session: Session, sessions_dir: Path, root: Path) -> None:
    try:
        shown = session.folder.relative_to(root)
    except ValueError:
        shown = session.folder
    print(f"\n--- {session.folder.name}")
    print(f"  path:     {shown}")
    print(f"  tasks:    {', '.join(session.tasks) if session.tasks else '(none in the folder name or the title)'}")
    if session.passport:
        print(f"  passport: {session.passport_path.name}")
        if session.passport["title"]:
            print(f"    title:  {session.passport['title']}")
        for line in session.passport["header"]:
            print(f"    {line}")
        if session.passport["last_round"]:
            print(f"    last round: {session.passport['last_round']}")
        else:
            print("    note: no round log in the passport")
    else:
        print("  note: no passport file (0-session.md / session.md) — status unknown")
    if session.report:
        print(f"  report:   {session.report_path.name}")
        for line in session.report["verdict"]:
            print(f"    {line}")
        counts = session.report["findings"]
        if counts:
            total = sum(counts.values())
            breakdown = ", ".join(f"{k} {v}" for k, v in counts.items() if v)
            print(f"    findings: {total} ({breakdown})")
        else:
            print("    findings: none listed by severity")
        for line in session.report["tail"]:
            print(f"    tail: {line}")
    else:
        print("  note: no report file (99-report.md / report.md) — the round may still be running")
    for line in registry_lines(sessions_dir, session.folder.name):
        print(f"  registry: {line}")


def print_root_header(root: Path, profile: dict, sessions_dir: Path) -> None:
    print(f"\n=== project: {root.name}  ({root})")
    print(f"  sessions: {sessions_dir}  [from {profile['source']}]")
    if profile["language"]:
        print(f"  language: {profile['language']}")


# --- modes -------------------------------------------------------------------------------------------------------------


def run_window(roots: list[Path], end: dt.date, days: int) -> int:
    start = end - dt.timedelta(days=days - 1)
    window = f"{start.isoformat()}" if days == 1 else f"{start.isoformat()} … {end.isoformat()}"
    print(f"qa-cube day digest · window: {window} ({days} day(s)) · projects: {len(roots)}")
    total = 0
    for root in roots:
        profile = profile_of(root)
        sessions_dir = (root / profile["sessions"]).resolve()
        print_root_header(root, profile, sessions_dir)
        if not sessions_dir.is_dir():
            print("  note: no sessions directory here — nothing to digest for this project")
            continue
        try:
            sessions = iter_sessions(sessions_dir)
        except OSError as exc:
            print(f"  note: cannot read the sessions directory — {exc}")
            continue
        picked = [s for s in sessions if s.date and start.isoformat() <= s.date <= end.isoformat()]
        if not picked:
            print(f"  note: no session folder is dated in this window ({len(sessions)} session folder(s) in total)")
            continue
        for session in sorted(picked, key=lambda s: (s.date, s.folder.name), reverse=True):
            try:
                print_session(session, sessions_dir, root)
            except OSError as exc:
                print(f"\n--- {session.folder.name}\n  note: cannot read this session — {exc}")
        total += len(picked)
    print(f"\ntotal: {total} session(s) in the window across {len(roots)} project(s)")
    return 0


def run_task(roots: list[Path], task: str) -> int:
    """The freshest session on a task id — by folder name first, then by a grep of the passports.

    Two passes, because one folder can carry several tasks: a multi-task session is named after one of them, and the others
    are findable only inside the passport. Without the second pass the answer to «how did the session on this task end» is
    «there was none», which is worse than a slow search.
    """
    print(f"qa-cube session lookup · task: {task} · projects: {len(roots)}")
    by_name: list[tuple[Session, Path, Path]] = []
    by_grep: list[tuple[Session, Path, Path]] = []
    needle = task.lower()
    for root in roots:
        profile = profile_of(root)
        sessions_dir = (root / profile["sessions"]).resolve()
        print_root_header(root, profile, sessions_dir)
        if not sessions_dir.is_dir():
            print("  note: no sessions directory here")
            continue
        try:
            sessions = iter_sessions(sessions_dir)
        except OSError as exc:
            print(f"  note: cannot read the sessions directory — {exc}")
            continue
        for session in sessions:
            slug = session.slug.lower()
            if slug == needle or slug.startswith(needle + "-") or needle in [t.lower() for t in session.tasks]:
                by_name.append((session, sessions_dir, root))
            elif session.passport_path and needle in read(session.passport_path).lower():
                by_grep.append((session, sessions_dir, root))
        print(f"  scanned: {len(sessions)} session folder(s)")

    hits = by_name or by_grep
    how = "the folder name / the passport title" if by_name else "a grep of the passports (a multi-task session)"
    if not hits:
        print(f"\nnote: no session found for `{task}` — neither in folder names nor in the passports")
        return 0
    hits.sort(key=lambda hit: (hit[0].date, hit[0].folder.name), reverse=True)
    session, sessions_dir, root = hits[0]
    print(f"\nfound by: {how} · {len(hits)} candidate(s), showing the freshest")
    print_session(session, sessions_dir, root)
    for other, _, _ in hits[1:]:
        print(f"  also: {other.folder}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A digest of qa-cube test sessions for a date (or the last N days), across one or several projects.",
    )
    parser.add_argument("roots", nargs="*", help="project roots; none given — the current directory")
    parser.add_argument("--date", help="the window's last day, YYYY-MM-DD (default: today)")
    parser.add_argument("--days", type=int, default=1, help="how many days back the window covers, including --date")
    parser.add_argument("--task", help="secondary mode: find the freshest session on this task id, at any date")
    args = parser.parse_args()

    roots = [Path(r).expanduser().resolve() for r in (args.roots or ["."])]
    missing = [r for r in roots if not r.is_dir()]
    for root in missing:
        print(f"note: {root} is not a directory — skipped")
    roots = [r for r in roots if r.is_dir()]
    if not roots:
        print("note: no readable project root — nothing to do")
        return 0

    if args.task:
        return run_task(roots, args.task)

    try:
        end = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    except ValueError:
        print(f"error: --date `{args.date}` is not a YYYY-MM-DD date", file=sys.stderr)
        return 2
    if args.days < 1:
        print("error: --days must be 1 or more", file=sys.stderr)
        return 2
    return run_window(roots, end, args.days)


if __name__ == "__main__":
    sys.exit(main())
