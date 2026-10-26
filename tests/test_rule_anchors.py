"""The free half of the eval suite: the rules the evals defend are still written where the engine reads them.

A paid eval (`evals/`) asks whether an agent obeys a rule; most regressions are cruder than that — an audit
moves a rule into a file nobody reads at that step, or renames the section a pointer names, and the rule is
gone without an error. Both are text facts, so they are checked here on every push, for nothing:

- every non-experiment eval case has its rule's anchor phrases, in files that are read at the step it fires;
- every «`file.md`, section «Title»» pointer between engine files lands on a heading or a bold entry.

An anchor is the rule's load-bearing sentence, matched after the markup is stripped and the whitespace
collapsed, so rewrapping a paragraph never fails it and rewording the rule always does. A failure means:
the rule moved (fix the anchor and check the new file is read at that step) or it was lost (restore it).

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVALS = REPO / "evals"
SKILL = "skills/qa/SKILL.md"

# Files the manager always has in front of it: SKILL.md is the skill itself, and an agent's instruction is
# its system prompt. Anything else holds a rule only if SKILL.md sends the reader there.
ALWAYS_READ = (SKILL, "agents/qa-manual.md", "agents/qa-analyst.md", "agents/qa-automator.md")

ANCHORS: dict[str, list[tuple[str, str]]] = {
    "profile-missing": [
        (SKILL, "No profile → do not start the session: suggest the user run `/qa-setup`"),
    ],
    "degradations-declared": [
        (SKILL, "apply the degradation from the table at the end of this file"),
        (SKILL, "| tracker | the input is only a free-form description from the user; ask them for the session's mode too (full cycle by default); the report's «tracker comment» is dropped"),
        (SKILL, "`none` — cases are not maintained at all: `qa-analyst` is not launched, the manual tester creates no case"),
        (SKILL, "| autotests | step 5 is skipped entirely"),
    ],
    "language-ru": [
        (SKILL, "The session's language is `language` from the profile"),
        (SKILL, "The engine's own instructions are in English, and that says nothing about the output language"),
        (SKILL, "make `Output language: <language>` the first line of every executor's prompt"),
        ("agents/qa-manual.md", "Your output language is the `Output language: <lang>` line of your prompt"),
        ("agents/qa-analyst.md", "Your output language is the `Output language: <lang>` line of your prompt"),
        ("agents/qa-automator.md", "Your output language is the `Output language: <lang>` line of your prompt"),
        ("skills/qa/templates/2-manual-task.md", "- Output language:"),
        ("skills/qa/templates/4-automator-task.md", "- Output language:"),
    ],
    "session-continuation": [
        (SKILL, "including the month archives"),
        (SKILL, "A session existed → this is a new round in the same folder: the folder is renamed to the current date"),
        (SKILL, "the report is not created anew — the same `99-report.md` is updated"),
        (SKILL, "Read `references/session-folder.md`, section «Continuing a session», before the round's first move"),
    ],
    "engine-clone-guard": [
        (SKILL, "but first check that `engine-clone` is a clone at all"),
        (SKILL, "its path is not inside the harness's install cache"),
        ("skills/qa/references/harness/claude-code.md", "a path inside `~/.claude/plugins/` is an installation, never a clone"),
        (SKILL, "Without a clone the lesson is written, not dropped — as a row of `.claude/qa-cube-feedback.md`"),
        (SKILL, "No version bump, no `plugin update`"),
    ],
    "feedback-layer": [
        (SKILL, "Read its open rows right after the profile (the «Closed» block is skipped"),
        (SKILL, "The profile and this file never carry the same rule — two layers"),
        (SKILL, "It is not rephrased into the profile to make it work sooner"),
        (SKILL, "no rule goes into both"),
    ],
}

POINTER = re.compile(r"`(?:\.\./)*(?:skills/qa/)?(?:references/|templates/)?([a-z0-9-]+\.md)`,?\s+(?:sections?\s+)?«([^»]+)»")
QUOTES = str.maketrans("", "", "«»\"“”")


def normalise(text: str) -> str:
    """Markup and line wrapping are not the rule: drop bold markers, collapse whitespace, ignore case."""
    return re.sub(r"\s+", " ", text.replace("**", "")).strip().lower()


def missing_anchors(text: str, phrases: list[str]) -> list[str]:
    body = normalise(text)
    return [p for p in phrases if normalise(p) not in body]


def titles(text: str) -> list[str]:
    """What a pointer may land on: a heading, or an entry's bold lead sentence."""
    heads = [re.sub(r"^#+\s*", "", line) for line in text.splitlines() if line.startswith("#")]
    bold = re.findall(r"\*\*(.+?)\*\*", text, flags=re.S)
    return [normalise(t).translate(QUOTES) for t in heads + bold]


def unresolved_pointers(text: str, targets: dict[str, str]) -> list[str]:
    bad = []
    for name, title in POINTER.findall(re.sub(r"\s+", " ", text)):
        if name not in targets:
            continue  # a project's profile subfile or a file outside the engine
        wanted = normalise(title).translate(QUOTES)
        if not any(wanted in t for t in titles(targets[name])):
            bad.append(f"{name} «{title}»")
    return bad


def engine_files() -> dict[str, Path]:
    paths = list((REPO / "skills/qa").rglob("*.md")) + list((REPO / "agents").glob("*.md"))
    return {p.relative_to(REPO).as_posix(): p for p in paths}


def eval_cases() -> set[str]:
    cases = set()
    for case in EVALS.glob("*/case.yaml"):
        if not re.search(r"^tags:.*\bexperiment\b", case.read_text(), flags=re.M):
            cases.add(case.parent.name)
    return cases


class Helpers(unittest.TestCase):
    def test_rewrapped_bold_rule_still_matches(self):
        text = "No profile → **do not\n  start** the session."
        self.assertEqual(missing_anchors(text, ["no profile → do not start the session"]), [])

    def test_reworded_rule_is_caught(self):
        text = "No profile → consider starting the session."
        self.assertEqual(len(missing_anchors(text, ["No profile → do not start the session"])), 1)

    def test_pointer_to_bold_entry_resolves(self):
        targets = {"a.md": "## Group\n\n**«The design has no such screen» is true only of the canvas.** Text.\n"}
        text = "see `references/a.md`, «The design has no such screen»"
        self.assertEqual(unresolved_pointers(text, targets), [])

    def test_pointer_to_renamed_section_is_caught(self):
        targets = {"a.md": "## Continuing a round\n"}
        text = "read `references/a.md`, section «Continuing a session», first"
        self.assertEqual(unresolved_pointers(text, targets), ["a.md «Continuing a session»"])

    def test_pointer_outside_the_engine_is_ignored(self):
        text = "the profile's `browser.md`, «Login» section"
        self.assertEqual(unresolved_pointers(text, {}), [])


class EvalRules(unittest.TestCase):
    def test_every_eval_case_has_anchors(self):
        # A new case without anchors is defended only by a paid run; an anchor set without a case is stale.
        self.assertEqual(eval_cases(), set(ANCHORS))

    def test_anchors_present(self):
        for case, anchors in ANCHORS.items():
            for path, phrase in anchors:
                with self.subTest(case=case, file=path):
                    self.assertEqual(missing_anchors((REPO / path).read_text(), [phrase]), [], phrase)

    def test_anchor_files_are_read(self):
        # A rule in a reference SKILL.md never names is a rule in a drawer.
        skill = (REPO / SKILL).read_text()
        for case, anchors in ANCHORS.items():
            for path, _ in anchors:
                if path in ALWAYS_READ:
                    continue
                with self.subTest(case=case, file=path):
                    self.assertIn(Path(path).name, skill)


class Pointers(unittest.TestCase):
    def test_every_section_pointer_resolves(self):
        files = engine_files()
        targets = {p.name: p.read_text() for p in files.values()}
        for rel, path in sorted(files.items()):
            with self.subTest(file=rel):
                self.assertEqual(unresolved_pointers(path.read_text(), targets), [])


if __name__ == "__main__":
    unittest.main()
