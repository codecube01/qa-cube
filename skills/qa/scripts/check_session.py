#!/usr/bin/env python3
"""Mechanical checks over a session's own files: leaked secrets, broken tables, oversized cells.

    check_session.py <sessions>/2026-09-14_acme-412-coupon/3-manual-result.md
    check_session.py <sessions>/2026-09-14_acme-412-coupon/          # the whole folder
    check_session.py --max-cell 850 --min-sections 3 <file> …

Three rules the engine states in prose and, until now, asked an agent to honour by eye:

- **no secret value goes into a session file.** The rule is repeated in four instructions because an
  instruction is the only thing that ever enforced it — and session folders are committed into the
  customer's repository and backed up off-site. A regex is not a guarantee either, but it is the kind
  of check that never gets tired on the ninth file of the round.
- **a table survives being copied into the tracker.** Step 6 says it outright: every row carries the
  same number of `|` as the separator row. A stray bar inside a cell shifts the columns and the
  damage is invisible in a rendered preview — the row simply reads as if the author wrote it that way.
- **a finding's cell stays under ~850 characters.** Past the limit the tracker's reader stops reading
  and the customer sends the report back to be shortened.

Exit code 0 when nothing was found, 1 when something was. Every problem is printed as
`file:line: what`, so the output pastes straight into a result file.

Nothing here understands the project's language: section names, verdicts and headings are written in
whatever `language` the profile declares, so every check rests on structure and on identifiers the
engine never translates. What cannot be checked that way is not checked at all — a validator that
guesses at meaning would be worse than none, because it would be believed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_CELL = 850
MIN_SECTIONS = 3

# --- secrets -------------------------------------------------------------------------------------

# The masked forms the engine mandates, plus the shapes a placeholder takes in practice. A value
# matching any of these is not a leak — it is the rule being followed.
MASKED = re.compile(
    r"""^(?:
        <[^>]*>            # <TOKEN>, <your password here>
      | \{\{[^}]*\}\}      # {{ token }}
      | \$\{?[A-Za-z_][A-Za-z0-9_]*\}?   # $TOKEN, ${TOKEN}
      | \*{3,}             # ***
      | x{3,}              # xxx
      | \.{3,}|…           # ...
      | (?:TODO|TBD|REDACTED|MASKED|HIDDEN|SECRET|CHANGEME|null|none|N/?A)
      | ['"](?:\s*)['"]    # empty string
    )$""",
    re.X | re.I,
)

# A value assigned to a secret-shaped key. The key list is deliberately short: every extra word costs
# a false positive on prose, and prose is what session files are mostly made of.
ASSIGNED = re.compile(
    r"""(?P<key>\b(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key
        |private[_-]?key|authorization|credential)s?\b)
        \s*[:=]\s*
        (?P<value>\S+)""",
    re.X | re.I,
)

# What a credential VALUE looks like, as opposed to a word of prose. Both halves matter: the engine's
# own verdict vocabulary («pass», «fail») and sentences like «token: expired» are the exact shapes a
# looser rule fires on, and a check that cries wolf on correct work gets switched off within a week.
# Precedent: the first version flagged the phrase «a wall the executor cannot pass: signing in a
# wallet» in the engine's own lesson catalogue.
CREDENTIAL_VALUE = re.compile(r"^[A-Za-z0-9._~+/=-]{8,}$")

# Shapes that are a secret whatever they are assigned to.
SHAPES: list[tuple[str, re.Pattern[str]]] = [
    ("a JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}")),
    ("a private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("an AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("a GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("a Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("a bearer value", re.compile(r"\bBearer\s+(?!<)[A-Za-z0-9._~+/-]{16,}")),
    (
        "a one-time link (a magic link or an invite is a credential too)",
        re.compile(r"https?://\S*[?&](?:token|code|key|secret|invite|otp)=(?!<)[A-Za-z0-9._~+/-]{12,}", re.I),
    ),
]

def scan_secrets(lines: list[str]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for n, line in enumerate(lines, 1):
        for what, pattern in SHAPES:
            if pattern.search(line):
                out.append((n, f"looks like {what} — mask it and keep the value in the profile's `secrets` source"))
        for match in ASSIGNED.finditer(line):
            value = match.group("value").strip("`'\",;)")
            if MASKED.match(value) or value.startswith("<") or value.endswith(">"):
                continue
            if not CREDENTIAL_VALUE.match(value):
                continue
            if not (any(c.isdigit() for c in value) and any(c.isalpha() for c in value)):
                continue  # letters AND digits: prose is one or the other
            key = match.group("key")
            out.append(
                (n, f"`{key}` is followed by what looks like a real value — mask it (`{key}: <…>`) "
                    f"and reference the profile's `secrets` source instead")
            )
    # one problem per line is enough to act on; more is noise
    seen: set[int] = set()
    unique: list[tuple[int, str]] = []
    for n, message in out:
        if n in seen:
            continue
        seen.add(n)
        unique.append((n, message))
    return unique


# --- tables --------------------------------------------------------------------------------------

SEPARATOR = re.compile(r"^\|[\s:|\-]+\|?\s*$")


def split_cells(row: str) -> list[str]:
    """Cells of a markdown row, honouring `\\|` as an escaped bar (which does NOT break the table)."""
    parts = re.split(r"(?<!\\)\|", row.strip())
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return parts


def scan_tables(lines: list[str], max_cell: int) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    block: list[tuple[int, str]] = []
    fenced = False

    def flush(rows: list[tuple[int, str]]) -> None:
        sep = next((i for i, (_, text) in enumerate(rows) if SEPARATOR.match(text)), None)
        if sep is None:
            return  # a run of `|` lines that is not a table — a diagram, a quoted log
        width = len(split_cells(rows[sep][1]))
        for n, text in rows:
            if SEPARATOR.match(text):
                continue
            cells = split_cells(text)
            if len(cells) != width:
                out.append(
                    (n, f"the row has {len(cells)} cell(s) against the separator's {width} — "
                        f"an unescaped `|` inside a cell shifts the columns silently; write it as `\\|` or use a word")
                )
            for cell in cells:
                if len(cell.strip()) > max_cell:
                    out.append(
                        (n, f"a cell is {len(cell.strip())} characters, over the {max_cell} limit — "
                            f"the tracker's reader stops before the end; move the workings to the result file")
                    )
                    break

    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.strip().startswith("|"):
            block.append((n, line))
            continue
        if block:
            flush(block)
            block = []
    if block:
        flush(block)
    return out


# --- structure -----------------------------------------------------------------------------------


def scan_structure(lines: list[str], min_sections: int) -> list[tuple[int, str]]:
    """Section COUNT only. The engine names the sections in the project's language, so matching a
    caption would break every non-English project — and a check that fires on correct work is worse
    than no check at all."""
    fenced = False
    sections = 0
    for line in lines:
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced and line.startswith("## "):
            sections += 1
    if sections < min_sections:
        return [(1, f"{sections} section(s) of the {min_sections} the file scheme expects — "
                    f"a result carries «Summary», «Product findings» and «Executor retro» at the very least")]
    return []


# --- driver --------------------------------------------------------------------------------------


def check_file(path: Path, max_cell: int, min_sections: int) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"{path}: cannot read — {exc}"]
    # The section-count rule describes a RESULT file; plans, briefs, retros and the report have
    # their own templates and legitimately carry fewer sections. Pointed at a whole session folder
    # the check would fire on every one of them, so it is scoped by the file scheme's own naming —
    # `*-manual-result*.md`, `*-automator-result*.md` — which is English by construction and does
    # not depend on the session's language.
    sections_needed = min_sections if "result" in path.stem.lower() else 0
    problems = scan_secrets(lines) + scan_tables(lines, max_cell) + scan_structure(lines, sections_needed)
    return [f"{path}:{n}: {message}" for n, message in sorted(problems)]


def collect(targets: list[str]) -> list[Path]:
    out: list[Path] = []
    for target in targets:
        path = Path(target).expanduser()
        if path.is_dir():
            out.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            out.append(path)
        else:
            print(f"note: {path} is neither a file nor a directory — skipped")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical checks over a qa-cube session's files.")
    parser.add_argument("targets", nargs="+", help="markdown files, or a session folder")
    parser.add_argument("--max-cell", type=int, default=MAX_CELL, help=f"table cell limit (default {MAX_CELL})")
    parser.add_argument("--min-sections", type=int, default=MIN_SECTIONS, help=f"default {MIN_SECTIONS}")
    parser.add_argument("--no-structure", action="store_true", help="skip the section-count check")
    args = parser.parse_args()

    files = collect(args.targets)
    if not files:
        print("note: nothing to check")
        return 0

    problems: list[str] = []
    for path in files:
        problems.extend(check_file(path, args.max_cell, 0 if args.no_structure else args.min_sections))

    if not problems:
        print(f"ok: {len(files)} file(s) checked, nothing found")
        return 0
    print(f"✘ {len(problems)} problem(s) in {len(files)} file(s):\n")
    for problem in problems:
        print(f"  · {problem}")
    print("\nSecrets: mask the value and reference the profile's `secrets` source — session folders are")
    print("committed and backed up. Tables: they get copied into the tracker whole.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
