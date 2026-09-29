#!/usr/bin/env python3
"""Structural checks for the qa-cube plugin.

Run from the repo root: python3 .github/scripts/validate-plugin.py
Exits non-zero and prints every problem it found, so one run tells the whole story.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
problems: list[str] = []


def fail(msg: str) -> None:
    problems.append(msg)


def load_json(rel: str) -> dict | None:
    path = ROOT / rel
    if not path.exists():
        fail(f"{rel}: missing")
        return None
    text = path.read_text()
    # A retro edit that rewrites the file by hand tends to drop the final newline;
    # it has happened twice, so it is a check rather than a note.
    if not text.endswith("\n"):
        fail(f"{rel}: no trailing newline at end of file")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"{rel}: invalid JSON — {exc}")
        return None


def frontmatter(path: Path) -> dict[str, str] | None:
    """Parse the leading --- block. Only the flat key: value pairs we care about."""
    text = path.read_text()
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: no frontmatter block")
        return None
    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)}: frontmatter block is not closed")
        return None
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


# --- plugin.json -------------------------------------------------------------
plugin = load_json(".claude-plugin/plugin.json")
version = None
if plugin:
    for key in ("name", "description", "version"):
        if not plugin.get(key):
            fail(f"plugin.json: `{key}` is missing or empty")
    version = plugin.get("version")
    if version and not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"plugin.json: version `{version}` is not MAJOR.MINOR.PATCH")

# --- marketplace.json --------------------------------------------------------
market = load_json(".claude-plugin/marketplace.json")
if market and plugin:
    entries = market.get("plugins") or []
    if not entries:
        fail("marketplace.json: the `plugins` list is empty")
    names = [e.get("name") for e in entries]
    if plugin.get("name") not in names:
        fail(f"marketplace.json: no entry for plugin `{plugin.get('name')}` (found {names})")

# --- hooks -------------------------------------------------------------------
hooks = load_json("hooks/hooks.json")
if hooks:
    # json.dumps re-escapes the quotes the hook commands wrap their paths in, so the
    # path stops at a backslash as well as at a quote or whitespace.
    referenced = set(re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([^\"\s\\]+)", json.dumps(hooks)))
    if not referenced:
        fail("hooks.json: no ${CLAUDE_PLUGIN_ROOT}-relative commands found")
    for rel in sorted(referenced):
        target = ROOT / rel
        if not target.exists():
            fail(f"hooks.json points at {rel}, which does not exist")
        elif rel.endswith(".sh") and not target.stat().st_mode & 0o111:
            fail(f"{rel}: referenced by hooks.json but not executable (chmod +x)")

# --- skills and agents -------------------------------------------------------
skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
if not skill_files:
    fail("skills/: no SKILL.md found")
for path in skill_files:
    meta = frontmatter(path)
    if meta is None:
        continue
    if not meta.get("description"):
        fail(f"{path.relative_to(ROOT)}: frontmatter has no `description`")
    expected = path.parent.name
    if meta.get("name") != expected:
        fail(f"{path.relative_to(ROOT)}: frontmatter name `{meta.get('name')}` != directory `{expected}`")

agent_files = sorted((ROOT / "agents").glob("*.md"))
if not agent_files:
    fail("agents/: no agent files found")
for path in agent_files:
    meta = frontmatter(path)
    if meta is None:
        continue
    if not meta.get("description"):
        fail(f"{path.relative_to(ROOT)}: frontmatter has no `description`")
    if meta.get("name") != path.stem:
        fail(f"{path.relative_to(ROOT)}: frontmatter name `{meta.get('name')}` != file name `{path.stem}`")

# --- templates referenced by the engine --------------------------------------
qa_skill = ROOT / "skills/qa/SKILL.md"
if qa_skill.exists():
    text = qa_skill.read_text()
    for rel in sorted(set(re.findall(r"`templates/([\w.\-]+\.md)`", text))):
        if not (qa_skill.parent / "templates" / rel).exists():
            fail(f"skills/qa/SKILL.md references templates/{rel}, which does not exist")
    # every session file the engine names in its file-scheme block must have a template
    block = re.search(r"```\n(0-session\.md.*?)```", text, re.S)
    if block:
        named = re.findall(r"^(\d+[\w\-]*\.md)", block.group(1), re.M)
        have = {p.name for p in (qa_skill.parent / "templates").glob("*.md")}
        for name in named:
            # result files are written by the executors and have no template on purpose
            if "result" in name:
                continue
            if name not in have:
                fail(f"skills/qa/SKILL.md's file scheme names {name}, but templates/{name} is missing")

# --- reference catalogues the engine points at -------------------------------
# SKILL.md holds the procedure and delegates the situational lessons to
# references/*.md. A pointer to a file that does not exist silently costs the
# manager the whole catalogue, and a catalogue with no contents list gets read
# with `head` instead of whole — so both are checked, not trusted.
if qa_skill.exists():
    text = qa_skill.read_text()
    for rel in sorted(set(re.findall(r"`references/([\w.\-]+\.md)`", text))):
        ref = qa_skill.parent / "references" / rel
        if not ref.exists():
            fail(f"skills/qa/SKILL.md references references/{rel}, which does not exist")
        elif len(ref.read_text().splitlines()) > 100 and "## Contents" not in ref.read_text():
            fail(f"skills/qa/references/{rel}: over 100 lines and no «## Contents» section")
    # The step-3 and step-4 lesson corpora once grew to half of SKILL.md, and the
    # manager paid for all of them in every session — including the ones where not a
    # single lesson applied. Situational lessons belong in references/, not here.
    # The budget is in characters, not lines: line count moves when the file is
    # rewrapped, while what the manager actually pays for is the token count.
    size = len(text)
    if size > 66_000:
        fail(
            f"skills/qa/SKILL.md: {size} characters (budget 66000, ~16.5k tokens) — move "
            f"situational lessons into skills/qa/references/ and leave the procedure here"
        )

# --- subagent_type values must match real agents -----------------------------
if qa_skill.exists():
    declared = {p.stem for p in agent_files}
    for used in sorted(set(re.findall(r'subagent_type: "([\w\-]+)"', qa_skill.read_text()))):
        if used not in declared:
            fail(f"skills/qa/SKILL.md launches subagent_type `{used}`, but agents/{used}.md does not exist")

# --- the contract version must agree with its own example --------------------
contract = ROOT / "PROFILE-CONTRACT.md"
if not contract.exists():
    fail("PROFILE-CONTRACT.md: missing")
else:
    text = contract.read_text()
    current = re.search(r"current version is \*\*(\d+)\*\*", text)
    if not current:
        fail("PROFILE-CONTRACT.md: cannot find the «current version is **N**» line")
    else:
        n = current.group(1)
        examples = set(re.findall(r"^contract-version:\s*(\d+)", text, re.M))
        stale = {e for e in examples if e != n}
        if stale:
            fail(
                f"PROFILE-CONTRACT.md: current version is {n}, but the examples say "
                f"contract-version: {', '.join(sorted(stale))} — bump them together"
            )
        if not re.search(rf"^\|\s*{n}\s*\|", text, re.M):
            fail(f"PROFILE-CONTRACT.md: version {n} has no row in the version-history table")

# --- no identifiers from real projects ---------------------------------------
# The engine is published outside the projects it is written in, so nothing from a
# client's project may travel with it: task ids, hosts, addresses, entity ids, secrets,
# private names. Lessons are anonymised: the mechanics stay, the address goes. Session
# files, project profiles and project knowledge bases are unaffected — they live inside
# their project. The definition of «a leak» lives in check_identifiers.py, shared with
# the git hooks and the CI jobs that read commit messages, PR metadata and history.
sys.path.insert(0, str(Path(__file__).parent))
from check_identifiers import DENYLIST_FILE, scan_lines  # noqa: E402

# Only git-tracked files can leak: what .gitignore keeps out (docs/, CLAUDE.md,
# .superpowers/, the private denylist) stays on this machine and may name what it needs.
# Every tracked text file is read — a workflow or a fixture leaks as well as a lesson.
try:
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    engine_files = [ROOT / rel for rel in tracked]
except (subprocess.CalledProcessError, FileNotFoundError):
    # no git available (a tarball, say) — fall back to walking the tree
    engine_files = [
        p
        for p in ROOT.rglob("*")
        if p.is_file()
        and not any(part in {".git", "docs", ".superpowers"} for part in p.parts)
        and p.name not in {"CLAUDE.md", DENYLIST_FILE.name}
    ]
    tracked = []
if DENYLIST_FILE.name in tracked:
    fail(f"{DENYLIST_FILE.name} is tracked by git — the private denylist IS the leak it guards "
         f"against: `git rm --cached {DENYLIST_FILE.name}` and rewrite the history that carries it")
# A real document (a charter, a licence, a passport scan, a screenshot of a client's screen) is the
# worst leak of all and no text check reads it — so the engine carries no documents or images at
# all, unless one is added to this list on purpose.
DOCUMENT_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".odt", ".ods", ".rtf", ".png", ".jpg",
                     ".jpeg", ".gif", ".webp", ".heic", ".tif", ".tiff", ".bmp", ".zip", ".rar", ".7z"}
ALLOWED_DOCUMENTS: set[str] = set()
for rel in tracked:
    if Path(rel).suffix.lower() in DOCUMENT_SUFFIXES and rel not in ALLOWED_DOCUMENTS:
        fail(f"{rel}: a document or an image in the engine — no text check can read it for a "
             f"client's data; remove it, or list it in ALLOWED_DOCUMENTS on purpose")
for path in sorted(engine_files):
    if not path.is_file():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue  # a binary file: an image, an archive
    for problem in scan_lines(text, str(path.relative_to(ROOT))):
        fail(f"{problem} — anonymise it (keep the mechanics, drop the address)")

# --- the edit itself: counts in the text, and ratchets against HEAD ----------
# A retro edits the engine from another project's session and never sees this
# repository's own review rules; the mechanical half of that review lives in
# check_engine_edits.py (version bump, CHANGELOG, index groups, counts in words).
from check_engine_edits import problems as edit_problems  # noqa: E402

for problem in edit_problems(ROOT):
    fail(problem)

# --- report ------------------------------------------------------------------
if problems:
    print(f"✘ {len(problems)} problem(s) found:\n")
    for p in problems:
        print(f"  · {p}")
    sys.exit(1)

print(
    f"✔ plugin {plugin.get('name')} {version}: "
    f"{len(skill_files)} skill(s), {len(agent_files)} agent(s), structure is consistent"
)
