#!/usr/bin/env python3
"""Mechanical checks over a session's own files: leaked secrets, broken tables, oversized cells.

    check_session.py <sessions>/2026-09-14_acme-412-coupon/3-manual-result.md
    check_session.py <sessions>/2026-09-14_acme-412-coupon/          # the whole folder
    check_session.py --max-cell 850 --min-sections 3 <file> …

Six rules the engine states in prose and, until now, asked an agent to honour by eye:

- **no secret value goes into a session file.** The rule is repeated in four instructions because an
  instruction is the only thing that ever enforced it — and session folders are committed into the
  customer's repository and backed up off-site. A regex is not a guarantee either, but it is the kind
  of check that never gets tired on the ninth file of the round.
- **a table survives being copied into the tracker.** Step 6 says it outright: every row carries the
  same number of `|` as the separator row. A stray bar inside a cell shifts the columns and the
  damage is invisible in a rendered preview — the row simply reads as if the author wrote it that way.
- **a finding's cell stays under ~850 characters.** Past the limit the tracker's reader stops reading
  and the customer sends the report back to be shortened.
- **a `📎 <file>` marker names a readable file that exists in the folder's `screenshots/`.** The
  executor saves a screenshot under the candidate's name and the manager renames it to the finding's
  id when the report assigns one; a marker left pointing at the old name sends whoever files the bug
  looking for an attachment that is not there. The file itself is read too: the browser tool returns a
  plain screenshot as a JPEG shrunk to its image budget, and with a `scale` below 1 the captions in it
  are a few pixels tall — a JPEG under `MIN_SHOT_WIDTH` is that, and an extension that lies about the
  format is caught on the way.
- **no two files of a session folder share a number.** The numbering runs across the folder and is
  never reset, and round 2+ takes its names from `session.py next-file`; a round that counted by
  hand named three files `8-…` once, and the folder's order of work was gone with it. Checked only
  when the target is a folder; `0-session.md` and `99-report.md` sit outside the numbering.
- **every scenario of the brief has a heading in the manual result.** The brief's scenario table is
  keyed by ids in its `#` column, and the executor's sections carry them (`## S3 — …`, `## S2b + S6 — …`).
  A result's closing tables are written last, from the executor's context, and cite every step even
  when the file lost the sections — a scripted insertion once cut five of nine and the file still
  read as well-formed. Matched against the brief of the same round (`*-manual-task<suffix>.md`).

And one list that is not a verdict: the lines of a manual result that ask a question. An executor
raises questions next to the observation that prompted them, and the closing «open questions» is
usually assembled from the brief — so a self-raised one stays behind mid-file, unanswered. The
manager reads the list against the closing section; the script cannot tell an answered one.

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


# --- screenshots ---------------------------------------------------------------------------------

# A bare file name after the paperclip: the marker is language-neutral, and a plain «logo.png» in a
# finding about a broken image is the product's asset, not ours — so only the marker is resolved.
SCREENSHOT = re.compile(r"📎\s*`?([\w.-]+\.(?:png|jpe?g|webp))`?", re.I)

# A plain screenshot at `scale` 1 of a desktop viewport comes back 1200+ px wide; the ones taken at
# 0.5–0.7 came back 600–870, and their captions could not be read. A `zoom` is a lossless PNG at the
# display's pixel ratio (one or more pixels per CSS pixel) and is readable at any size, so only a JPEG is held to the width. Precedent: a round that
# switched to `scale` 0.5 against a tiled render kept it for every saved screenshot.
MIN_SHOT_WIDTH = 1000

EXTENSIONS = {"png": ("png",), "jpeg": ("jpg", "jpeg"), "webp": ("webp",)}


def image_info(path: Path) -> tuple[str, int] | None:
    """(format, width) from the file's own header — stdlib only, no PIL on a stock macOS."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return "png", int.from_bytes(data[16:20], "big")
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp", 0  # width varies by sub-format; the format is what is checked
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            # SOF0–SOF15 carry the frame size; C4 (DHT), C8 (JPG) and CC (DAC) share the range and do not
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                return "jpeg", int.from_bytes(data[i + 7:i + 9], "big")
            if marker in (0x01, 0xFF) or 0xD0 <= marker <= 0xD9:
                i += 2 if marker != 0xFF else 1
                continue
            i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
        return "jpeg", 0
    return None


def scan_screenshots(lines: list[str], folder: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for n, line in enumerate(lines, 1):
        for match in SCREENSHOT.finditer(line):
            name = match.group(1)
            path = folder / "screenshots" / name
            if not path.is_file():
                out.append(
                    (n, f"`📎 {name}` has no file in `screenshots/` — a candidate's screenshot is renamed "
                        f"to the finding's id when the id is assigned; `session.py shot` renames it and its markers together")
                )
                continue
            info = image_info(path)
            if info is None:
                continue  # an empty or unknown file: nothing to measure, and the marker itself resolves
            fmt, width = info
            if name.rsplit(".", 1)[-1].lower() not in EXTENSIONS[fmt]:
                out.append(
                    (n, f"`{name}` is a {fmt.upper()} under another extension — keep the extension the "
                        f"tool's file came with, and fix the marker")
                )
            if fmt == "jpeg" and 0 < width < MIN_SHOT_WIDTH:
                out.append(
                    (n, f"`{name}` is a JPEG {width} px wide — a screenshot shrunk past reading (a `scale` "
                        f"below 1); retake it as a `zoom` of the region with `save_to_disk` (a lossless PNG)")
                )
    return out


# --- scenarios against the brief ----------------------------------------------------------------

# An id in the brief's `#` column: a short prefix in any script, a number, an optional letter — S3, B12,
# 7, S2b. The template's placeholders (`N`, `N+1`) are not ids and are skipped.
SCENARIO_ID = re.compile(r"[^\W\d_]{0,3}\d+[^\W\d_]?")
RANGE = re.compile(r"([^\W\d_]{0,3})(\d+)\s*[–-]\s*([^\W\d_]{0,3})(\d+)")
MANUAL_RESULT = re.compile(r"^\d+-manual-result(.*)\.md$")
# Executors stamp their headings with the time and the date; `(11:02–11:05)` read as a range would
# vouch for scenarios 2 to 11, so both are cut out before the words are taken.
CLOCK = re.compile(r"\d{4}-\d{2}-\d{2}(?:T[\d:.]+Z?)?|\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?Z?")


def brief_scenario_ids(lines: list[str]) -> list[str]:
    """Ids of the brief's LAST table keyed by `#` with four columns or more. The template puts the
    scenarios last; a retest table of the previous round's verdicts and a hypotheses table come before
    it and are narrower in older briefs, which is how their ids are kept out."""
    tables: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        s = line.strip()
        if s.startswith("|") and current is None and not SEPARATOR.match(s):
            cells = split_cells(s)
            if cells and cells[0].strip() == "#" and len(cells) >= 4:
                current = []
                tables.append(current)
            continue
        if current is not None and s.startswith("|"):
            if not SEPARATOR.match(s):
                cell = split_cells(s)[0].strip() if split_cells(s) else ""
                if SCENARIO_ID.fullmatch(cell):
                    current.append(cell)
            continue
        current = None
    return tables[-1] if tables else []


def heading_tokens(lines: list[str]) -> set[str]:
    """Every word of every heading, lowercased, with `S1–S4` unfolded — an id is found anywhere in the
    heading, because executors write it first (`## S3 — …`), after a word (`## Scenario 3`) or in
    brackets with the others run in the same pass."""
    tokens: set[str] = set()
    fenced = False
    for line in lines:
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or not re.match(r"^#{2,4} ", line):
            continue
        line = CLOCK.sub(" ", line)
        tokens.update(w.lower() for w in re.findall(r"[^\W_]+", line))
        for pa, a, pb, b in RANGE.findall(line):
            if (not pb or pa.lower() == pb.lower()) and 0 < int(b) - int(a) <= 50:
                tokens.update(f"{pa}{k}".lower() for k in range(int(a), int(b) + 1))
    return tokens


def scan_scenarios(lines: list[str], path: Path) -> list[tuple[int, str]]:
    m = MANUAL_RESULT.match(path.name)
    if not m:
        return []
    briefs = sorted(path.parent.glob(f"*-manual-task{m.group(1)}.md"),
                    key=lambda b: int(b.name.split("-", 1)[0]) if b.name.split("-", 1)[0].isdigit() else 0)
    if not briefs:
        return []
    brief = briefs[-1]
    ids = brief_scenario_ids(brief.read_text(encoding="utf-8", errors="replace").splitlines())
    tokens = heading_tokens(lines)
    out: list[tuple[int, str]] = []
    for sid in ids:
        low = sid.lower()
        # S7 is also found as S7a / S7b: a scenario split into parts keeps its id with a letter
        if low in tokens or any(re.fullmatch(re.escape(low) + r"[^\W\d_]", t) for t in tokens):
            continue
        out.append(
            (1, f"scenario {sid} of {brief.name} has no heading — the section is missing (send it back while the "
                f"executor's context is alive) or it ran inside another (that heading names every id it ran)")
        )
    return out


# --- questions raised mid-file -------------------------------------------------------------------


def scan_questions(lines: list[str]) -> list[tuple[int, str]]:
    """Lines that ask something, outside code and URLs — a list for the manager, not a verdict."""
    out: list[tuple[int, str]] = []
    fenced = False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        prose = re.sub(r"https?://\S+", "", re.sub(r"`[^`]*`", "", line))
        if "?" in prose:
            text = " ".join(line.split())
            out.append((n, text if len(text) <= 120 else text[:117] + "…"))
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
    problems = (scan_secrets(lines) + scan_tables(lines, max_cell) + scan_structure(lines, sections_needed)
                + scan_screenshots(lines, path.parent) + scan_scenarios(lines, path))
    return [f"{path}:{n}: {message}" for n, message in sorted(problems)]


def question_notes(path: Path) -> list[str]:
    if not MANUAL_RESULT.match(path.name):
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [f"{path}:{n}: {text}" for n, text in scan_questions(lines)]


NUMBERED = re.compile(r"^(\d+)-.+\.md$")
OUTSIDE_NUMBERING = {0, 99}


def scan_folder(folder: Path) -> list[str]:
    """Two files of one session folder carrying the same number."""
    by_number: dict[int, list[str]] = {}
    for p in sorted(folder.iterdir()):
        m = NUMBERED.match(p.name)
        if m and p.is_file() and int(m.group(1)) not in OUTSIDE_NUMBERING:
            by_number.setdefault(int(m.group(1)), []).append(p.name)
    return [f"{folder}: files {', '.join(names)} share the number {n} — the numbering runs across the "
            f"folder; name round-2+ files with `session.py next-file`, one call per file"
            for n, names in sorted(by_number.items()) if len(names) > 1]


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
    notes: list[str] = []
    for target in args.targets:
        if Path(target).expanduser().is_dir():
            problems.extend(scan_folder(Path(target).expanduser()))
    for path in files:
        problems.extend(check_file(path, args.max_cell, 0 if args.no_structure else args.min_sections))
        notes.extend(question_notes(path))

    if notes:
        print("Questions raised in the file — each one answered, or carried into the closing open questions?\n")
        for note in notes:
            print(f"  ? {note}")
        print()
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
