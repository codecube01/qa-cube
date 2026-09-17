#!/usr/bin/env python3
"""The single definition of «an identifier from a real project».

Used by validate-plugin.py (file contents), the git hooks (staged changes and commit
messages) and CI (commit messages, PR title and body). One definition, so the rule cannot
be enforced in one place and forgotten in another.

Standalone use:
    check_identifiers.py --text "Fix per ACME-303"     # a message
    check_identifiers.py --files a.md b.md              # file contents
    echo "…" | check_identifiers.py --stdin
Exits 1 and prints what it found.
"""

from __future__ import annotations

import argparse
import re
import sys

# A tracker id: ABC-123 (upper-case prefix) or service#456 (lower-case prefix).
PATTERN = re.compile(r"\b(?:[A-Z]{2,}-\d+|[a-z][a-z0-9]*#\d+)\b")

# Requirement markers and deliberately fictional examples are not references to a project.
ALLOWED_PREFIXES = ("FR-", "AC-", "API-", "ACME-", "ABC-")
ALLOWED_LITERALS = {"service#456"}

EXPLANATION = (
    "This looks like a task id from a real project. The engine is published outside the "
    "projects its lessons come from, so ids, environment hostnames, service, company and "
    "account names stay out of its files, commit messages, PR titles and PR bodies.\n"
    "Write the lesson by its mechanics instead: «precedent: a retest where the defect's "
    "symptom went stale together with the build»."
)


def find(text: str) -> list[str]:
    """Every disallowed identifier in the text, in order of appearance, deduplicated."""
    seen: list[str] = []
    for match in PATTERN.findall(text):
        if match.startswith(ALLOWED_PREFIXES) or match in ALLOWED_LITERALS:
            continue
        if match not in seen:
            seen.append(match)
    return seen


def scan_lines(text: str, label: str) -> list[str]:
    """Problems with line numbers, for file-shaped input."""
    out = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for found in find(line):
            out.append(f"{label}:{line_no}: `{found}`")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--text", help="check this string (a commit message, a PR title)")
    ap.add_argument("--files", nargs="*", default=[], help="check these files' contents")
    ap.add_argument("--stdin", action="store_true", help="check stdin")
    ap.add_argument("--label", default="input", help="name to show for --text/--stdin")
    args = ap.parse_args()

    problems: list[str] = []
    if args.text is not None:
        problems += [f"{args.label}: `{f}`" for f in find(args.text)]
    if args.stdin:
        problems += [f"{args.label}: `{f}`" for f in find(sys.stdin.read())]
    for path in args.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                problems += scan_lines(fh.read(), path)
        except (OSError, IsADirectoryError):
            continue

    if problems:
        print("✘ identifiers from a real project found:\n", file=sys.stderr)
        for p in problems:
            print(f"  · {p}", file=sys.stderr)
        print(f"\n{EXPLANATION}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
