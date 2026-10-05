#!/usr/bin/env python3
"""The mechanical half of a session folder's housekeeping: file numbers, finding ids, the monthly sweep.

    session.py next-file <session folder> <role> <round>       # 8-manual-task-2.md
    session.py max-id <sessions> --prefix ABC-                   # the highest id assigned, and the next one
    session.py sweep <sessions> [--dry-run] [--today YYYY-MM-DD]
    session.py links <sessions>                                 # every path to a session folder resolves

Each of these was a paragraph of SKILL.md that the manager executed by hand, and each went wrong by hand
at least once: an id taken «from memory» that collided with one already assigned, a number counted after
the draft and so matching the manager's own fresh rows, a sweep whose `mv` took a second while fixing the
links it broke took two passes — and a third, because a clean grep had been read as proof that the
rewritten paths existed. The judgment stays with the manager (what a round is, which prefix the profile
uses, what a dead link should point at); what is the same every time is here.

Exit code 0 when the command did its job and found nothing wrong, 1 when it found something to fix (an
unresolved link, a folder it could not move), 2 on a usage error. Nothing here reads the project's
language: it works on file names, dates and the identifiers the engine never translates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

SESSION = re.compile(r"^(\d{4})-(\d{2})-\d{2}_.+")  # a session folder: <YYYY-MM-DD>_<source>-<slug>
MONTH = re.compile(r"^\d{4}-\d{2}$")                  # a month archive
NUMBERED = re.compile(r"^(\d+)-.+\.md$")
OUTSIDE_NUMBERING = {0, 99}                           # 0-session.md and 99-report.md are updated in place
FIRST_AFTER_OLD_SCHEME = 8                            # a folder of unnumbered files starts its new round here
PATH_CHARS = r"[\w.~/\-]"
MENTION = re.compile(rf"{PATH_CHARS}*\d{{4}}-\d{{2}}-\d{{2}}_{PATH_CHARS}+")


# --- next-file --------------------------------------------------------------------------------------

def next_number(names: list[str]) -> int:
    """The next free number in a folder whose files are `names`.

    The numbering runs across the whole folder and is never reset; 0 and 99 sit outside it. A folder that
    holds .md files with no number at all is from the old scheme, and its first new round starts at 8."""
    numbers = [int(m.group(1)) for n in names if (m := NUMBERED.match(n))]
    numbers = [n for n in numbers if n not in OUTSIDE_NUMBERING]
    if numbers:
        return max(numbers) + 1
    unnumbered = [n for n in names if n.endswith(".md") and not NUMBERED.match(n) and n != "README.md"]
    return FIRST_AFTER_OLD_SCHEME if unnumbered else 1


def next_file(names: list[str], role: str, round_: int) -> str:
    return f"{next_number(names)}-{role}-{round_}.md"


# --- max-id -----------------------------------------------------------------------------------------

def assigned_ids(text: str, prefix: str) -> list[int]:
    """Ids ASSIGNED in a report, not mentioned: `<ID> · <priority>` (the template's cell and its «Fixed»
    line), or an id that opens a table cell (a project format with its own id column). A brief's «start at
    N» or a «see ABC-12» in prose is a mention and does not count."""
    p = re.escape(prefix)
    found = re.findall(rf"(?<![\w-]){p}(\d+)\**\s*·", text)
    found += re.findall(rf"\|\s*\**{p}(\d+)\b", text)
    return [int(n) for n in found]


def reports(sessions: Path) -> list[Path]:
    """Every report under the sessions root, the month archives and the old scheme's names included."""
    return sorted(p for p in sessions.rglob("*.md") if "report" in p.name and p.is_file())


def max_id(sessions: Path, prefix: str) -> tuple[int, Path | None]:
    best, where = 0, None
    for path in reports(sessions):
        for n in assigned_ids(path.read_text(encoding="utf-8", errors="replace"), prefix):
            if n > best:
                best, where = n, path
    return best, where


# --- links ------------------------------------------------------------------------------------------

def repo_root(start: Path) -> Path:
    try:
        out = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def text_files(root: Path) -> list[Path]:
    """The markdown files a link to a session folder can live in: the project map, the profile, the
    knowledge base, the cases, the registries, the sessions themselves."""
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "*.md"],
                             capture_output=True, text=True, check=True).stdout.split("\n")
        return sorted(root / p for p in out if p and (root / p).is_file())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)


def _tokens(line: str) -> list[tuple[int, int, str]]:
    """Path-like mentions of a session folder: (start, end, text), a trailing full stop dropped."""
    out = []
    for m in MENTION.finditer(line):
        s = m.group(0).rstrip(".")
        if "/" not in s:  # a bare folder name is a mention in prose, not a path
            continue
        if s.startswith("//") or line[m.start() - 1: m.start()] in (">", "}", ":"):
            continue  # a URL, or a placeholder's tail: `<sessions>/2026-08-10_…`, `${S}/…`
        out.append((m.start(), m.start() + len(s), s))
    return out


def _resolve(token: str, base: Path, root: Path) -> tuple[Path, str] | None:
    """Where a path points, and the style it is written in: relative to its own file, or to the root."""
    candidates = [("file", base / token), ("root", root / token)]
    for style, path in candidates:
        if path.exists():
            return path.resolve(), style
    return None


def dead_links(root: Path) -> list[str]:
    out = []
    for f in text_files(root):
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for _, _, token in _tokens(line):
                if _resolve(token, f.parent, root) is None:
                    out.append(f"{f.relative_to(root)}:{lineno}: {token} — no such path")
    return out


# --- sweep ------------------------------------------------------------------------------------------

def to_archive(sessions: Path, today: dt.date) -> list[tuple[Path, Path]]:
    """(folder, its place in the month archive) for every session folder in the root from a past month.
    The root keeps the current month; side-findings.md and the non-session folders are not touched."""
    current = (today.year, today.month)
    moves = []
    for d in sorted(sessions.iterdir()):
        m = SESSION.match(d.name)
        if d.is_dir() and m and (int(m.group(1)), int(m.group(2))) < current:
            moves.append((d, sessions / f"{m.group(1)}-{m.group(2)}" / d.name))
    return moves


def _moved(path: Path, moves: dict[Path, Path]) -> Path:
    for old, new in moves.items():
        if path == old or old in path.parents:
            return new / path.relative_to(old)
    return path


def rewrites(root: Path, moves: dict[Path, Path]) -> dict[Path, str]:
    """The new text of every file whose links the moves would break, each link kept in its own style:
    a link relative to its file stays relative (from the file's own new place), a root path stays one."""
    out = {}
    for f in text_files(root):
        f = f.resolve()
        text = f.read_text(encoding="utf-8", errors="replace")
        new_base = _moved(f, moves).parent
        lines = text.split("\n")
        changed = False
        for i, line in enumerate(lines):
            parts, last = [], 0
            for start, end, token in _tokens(line):
                hit = _resolve(token, f.parent, root)
                if hit is None:
                    continue
                target, style = hit
                new_target = _moved(target, moves)
                if new_target == target and new_base == f.parent:
                    continue
                rel = os.path.relpath(new_target, new_base if style == "file" else root.resolve())
                if token.endswith("/"):
                    rel += "/"
                if token.startswith("./") and not rel.startswith("."):
                    rel = "./" + rel
                if rel != token:
                    parts += [line[last:start], rel]
                    last = end
            if parts:
                lines[i] = "".join(parts) + line[last:]
                changed = True
        if changed:
            out[f] = "\n".join(lines)
    return out


def sweep(sessions: Path, today: dt.date, dry_run: bool) -> int:
    root = repo_root(sessions).resolve()
    sessions = sessions.resolve()
    moves, problems = {}, []
    for old, new in to_archive(sessions, today):
        if new.exists():
            problems.append(f"{new.relative_to(root)} already exists — {old.name} left in place")
        else:
            moves[old] = new
    if not moves:
        print("nothing to sweep")
    else:
        texts = rewrites(root, moves)
        for old, new in moves.items():
            print(f"{'would move' if dry_run else 'moved'}: {old.relative_to(root)} → {new.relative_to(root)}")
        for f in texts:
            print(f"{'would rewrite' if dry_run else 'rewrote'} links in: {_moved(f, moves).relative_to(root)}")
        if not dry_run:
            for f, text in texts.items():
                f.write_text(text, encoding="utf-8")
            for old, new in moves.items():
                new.parent.mkdir(exist_ok=True)
                old.rename(new)
    if moves:  # once per sweep, touched or not: a clean rewrite is not proof the paths exist
        problems += dead_links(root)
    for p in problems:
        print(f"  · {p}")
    return 1 if problems else 0


# --- cli --------------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    nf = sub.add_parser("next-file", help="the name of a round-2+ file in a session folder")
    nf.add_argument("folder", type=Path)
    nf.add_argument("role", help="manual-task, manual-result, plan, automator-task, retro, …")
    nf.add_argument("round", type=int)
    mi = sub.add_parser("max-id", help="the highest finding id assigned in any report")
    mi.add_argument("sessions", type=Path)
    mi.add_argument("--prefix", required=True, action="append", help="the profile's id prefix, e.g. ABC-")
    sw = sub.add_parser("sweep", help="move past months' sessions into their archives, fix the links")
    sw.add_argument("sessions", type=Path)
    sw.add_argument("--dry-run", action="store_true")
    sw.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    li = sub.add_parser("links", help="every path that names a session folder resolves")
    li.add_argument("sessions", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "next-file":
        if a.round < 2:
            print("round 1 takes the scheme's own names (1-plan.md, 2-manual-task.md, …)", file=sys.stderr)
            return 2
        if not a.folder.is_dir():
            print(f"no such folder: {a.folder}", file=sys.stderr)
            return 2
        print(next_file([p.name for p in a.folder.iterdir()], a.role, a.round))
        return 0
    if not a.sessions.is_dir():
        print(f"no such folder: {a.sessions}", file=sys.stderr)
        return 2
    if a.cmd == "max-id":
        for prefix in a.prefix:
            n, where = max_id(a.sessions, prefix)
            src = f" ({where.relative_to(a.sessions)})" if where else " (none assigned yet)"
            print(f"{prefix}: max {n}{src}, next {prefix}{n + 1}")
        return 0
    if a.cmd == "sweep":
        return sweep(a.sessions, a.today, a.dry_run)
    found = dead_links(repo_root(a.sessions).resolve())
    for p in found:
        print(f"  · {p}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
