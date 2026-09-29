#!/usr/bin/env python3
"""Mechanical checks of an edit to the engine's own text — the part of a review that needs no judgment.

Most engine edits are made by the retro of a session running in another project, straight into an engine
clone, and the review that follows kept finding the same mechanical slips: a version bumped with no line in
CHANGELOG.md, an entry added to a catalogue with its «Contents» group left untouched, a count in the text
(«read seven ways», «all three still pay») that no longer matches its list. This module catches those, so the
review is left with what only a reader sees — a duplicate, a wrong address, a second precedent patched onto an
entry (the corpus holds dozens of legitimate riders with their own, so that one stays with the reviewer).

Two kinds of check:

* **counts** are read off the text as it stands, so they hold in CI on a clean tree too;
* **ratchets** compare the working tree with HEAD — «this edit made it worse». The catalogues are not 1:1
  with their indexes (a family is one index line), so a check of the whole text would either fail on the
  corpus or say nothing; a ratchet says exactly «the edit you are making». On a clean tree (CI) they are
  silent by construction.

validate-plugin.py calls `problems(ROOT)`; the functions below are pure and tested in
tests/test_check_engine_edits.py.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

NUMBERS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
_NUM = "|".join(NUMBERS)

# What an edit to these paths changes is what an installed copy runs, so it needs a patch bump.
ENGINE_PATHS = ("skills/", "agents/", "hooks/", "PROFILE-CONTRACT.md")
CATALOGUES = "skills/*/references/*.md"


# --- the text as it stands --------------------------------------------------------------------------

def _paragraphs(text: str) -> list[str]:
    return re.split(r"\n[ \t]*\n", text)


def _entries(paragraph: str) -> int:
    """Catalogue entries in a paragraph: one that opens with bold or italic, or each top-level list item
    that does (consecutive items sit in one paragraph)."""
    items = len(re.findall(r"^- \*", paragraph, re.M))
    return items or int(bool(re.match(r"\s*\*", paragraph)))


def _is_heading(paragraph: str) -> bool:
    return paragraph.lstrip().startswith("#")


def _unquoted(text: str) -> str:
    """A count inside «…» is an example being quoted, not a count of the text around it."""
    return re.sub(r"«[^»\n]*»", "«»", text)


def count_problems(text: str, rel: str) -> list[str]:
    """Counts written in words that must match what they count."""
    out: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = _unquoted(line)
        # «one probe, read eight ways: a · b · c»
        # (a comma list wraps across lines and is not counted; the «·» index lines are one line each)
        for m in re.finditer(rf"\b({_NUM})\s+ways:\s+([^\n]+)", line):
            if " · " not in m.group(2):
                continue
            items = len(m.group(2).split(" · "))
            if items != NUMBERS[m.group(1)]:
                out.append(f"{rel}:{lineno}: «{m.group(1)} ways» lists {items} item(s)")

    paras = _paragraphs(text)
    for i, para in enumerate(paras):
        lineno = text[: text.find(para)].count("\n") + 1
        # «The eight entries below» — the entries up to the next heading
        for m in re.finditer(rf"\b[Tt]he ({_NUM}) entries below\b", _unquoted(para)):
            n = 0
            for nxt in paras[i + 1:]:
                if _is_heading(nxt):
                    break
                n += _entries(nxt)
            if n != NUMBERS[m.group(1)]:
                out.append(f"{rel}:{lineno}: «the {m.group(1)} entries below» — {n} entries follow")
        # «all four still pay» — the items of the nearest list above
        for m in re.finditer(rf"\ball ({_NUM}) still\b", _unquoted(para)):
            n = 0
            for prev in reversed(paras[:i]):
                items = re.findall(r"^- ", prev, re.M)
                if items:
                    n += len(items)
                elif n:
                    break
            if n != NUMBERS[m.group(1)]:
                out.append(f"{rel}:{lineno}: «all {m.group(1)} still» — the list above has {n} item(s)")
    return out


# --- ratchets: the edit against HEAD ----------------------------------------------------------------

def _sections(text: str) -> dict[str, str]:
    """`## Name` → its body; the «Contents» section is split off by the caller."""
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def _index_groups(contents: str) -> dict[str, str]:
    """A «Contents» block's `**Group**` headings → their lines; no groups → one group named «»."""
    parts = re.split(r"^\*\*(.+?)\*\*$", contents, flags=re.M)
    if len(parts) == 1:
        return {"": contents}
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def index_problems(old: str, new: str, rel: str) -> list[str]:
    """A section that gained an entry must touch its index group (the whole index, where it has none).

    Not «one index line per entry»: a shape added to a family is one more `·` item inside a line that is
    already there. But an index that did not change at all while its section grew is always a miss.
    """
    old_s, new_s = _sections(old), _sections(new)
    if "Contents" not in new_s:
        return []
    old_idx = _index_groups(old_s.get("Contents", ""))
    new_idx = _index_groups(new_s["Contents"])
    out = []
    for name, body in new_s.items():
        if name == "Contents":
            continue
        grew = sum(map(_entries, _paragraphs(body))) - sum(map(_entries, _paragraphs(old_s.get(name, ""))))
        if grew <= 0:
            continue
        group = name if name in new_idx else ("" if "" in new_idx else None)
        if group is None:
            continue  # a section the index does not list at all — not this check's business
        if new_idx[group] == old_idx.get(group):
            where = f"its «{name}» group" if group else "it"
            out.append(f"{rel}: section «{name}» gained {grew} entr{'y' if grew == 1 else 'ies'}, "
                       f"but the «Contents» index does not mention {where} — add the index line")
    return out


def version_problems(changed: list[str], old_version: str | None, new_version: str | None,
                     changelog_changed: bool) -> list[str]:
    out = []
    if old_version is None:
        return out
    # bytecode an import leaves beside a script is no edit (CI imports check_session.py before this runs)
    engine = [p for p in changed if p.startswith(ENGINE_PATHS) and "__pycache__/" not in p and not p.endswith(".pyc")]
    if engine and new_version == old_version:
        out.append(f"the engine changed ({', '.join(engine[:3])}{'…' if len(engine) > 3 else ''}) but "
                   f".claude-plugin/plugin.json is still {old_version} — bump the patch version, or the "
                   f"edit never reaches an installed copy")
    if new_version != old_version and not changelog_changed:
        out.append(f"the version moved {old_version} → {new_version} but CHANGELOG.md is untouched — "
                   f"add a 2–3 line entry under [Unreleased]")
    return out


# --- wiring -----------------------------------------------------------------------------------------

def _git(root: Path, *args: str) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                              check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _head(root: Path, rel: str) -> str:
    return _git(root, "show", f"HEAD:{rel}") or ""


def problems(root: Path) -> list[str]:
    out: list[str] = []
    for path in sorted(root.glob(CATALOGUES)):
        out += count_problems(path.read_text(), str(path.relative_to(root)))

    if _git(root, "rev-parse", "--verify", "-q", "HEAD") is None:
        return out  # no git, or no commit yet — nothing to ratchet against
    changed = (_git(root, "diff", "--name-only", "HEAD") or "").split()
    changed += (_git(root, "ls-files", "--others", "--exclude-standard") or "").split()
    if not changed:
        return out

    for rel in changed:
        path = root / rel
        if not path.is_file() or path.suffix != ".md":
            continue
        new, old = path.read_text(), _head(root, rel)
        if path.match(CATALOGUES):
            out += index_problems(old, new, rel)

    def version(text: str) -> str | None:
        try:
            return json.loads(text).get("version")
        except (json.JSONDecodeError, AttributeError):
            return None

    plugin = root / ".claude-plugin/plugin.json"
    out += version_problems(changed, version(_head(root, ".claude-plugin/plugin.json")),
                            version(plugin.read_text()) if plugin.exists() else None,
                            "CHANGELOG.md" in changed)
    return out


if __name__ == "__main__":
    import sys
    found = problems(Path(__file__).resolve().parents[2])
    for p in found:
        print(f"  · {p}")
    sys.exit(1 if found else 0)
