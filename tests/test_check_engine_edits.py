"""Tests for .github/scripts/check_engine_edits.py — the mechanical half of the review of an engine edit.

Each check fails in two ways: it misses the slip it exists for (the review then finds it by hand, which is
what the module was written to stop), or it fires on the engine's own prose and gets ignored. So the cases
come in pairs, caught and quiet, and the last test runs the counts over the catalogues as they stand.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / ".github" / "scripts" / "check_engine_edits.py"

_spec = importlib.util.spec_from_file_location("check_engine_edits", SCRIPT)
ce = importlib.util.module_from_spec(_spec)
sys.modules["check_engine_edits"] = ce
assert _spec.loader is not None
_spec.loader.exec_module(ce)


CATALOGUE = """# A catalogue

## Contents

**First group**

- an entry about apples

**Second group**

- an entry about pears

## First group

**Apples are red.** Precedent: an apple.

## Second group

**Pears are green.** Precedent: a pear.
"""


class Counts(unittest.TestCase):
    def test_ways_list_that_grew_is_caught(self):
        text = "- **The order** — one probe, read two ways: a · b · c\n"
        self.assertEqual(len(ce.count_problems(text, "x.md")), 1)

    def test_ways_list_that_matches_is_quiet(self):
        text = "- **The order** — one probe, read three ways: a · b · c\n"
        self.assertEqual(ce.count_problems(text, "x.md"), [])

    def test_ways_in_running_prose_is_quiet(self):
        # a comma list wraps across lines; only the one-line «·» index lists are counted
        text = "the mistake costs three ways: the evidence, the\nexecutor, and the report.\n"
        self.assertEqual(ce.count_problems(text, "x.md"), [])

    def test_a_quoted_count_is_an_example(self):
        text = "- *one*\n\nany count in words — «read eight ways: a · b», «all four still pay».\n"
        self.assertEqual(ce.count_problems(text, "x.md"), [])

    def test_entries_below_miscounted_is_caught(self):
        text = "### Family\n\n**Head.** The two entries below are shapes.\n\n**One.**\n\n**Two.**\n\n**Three.**\n"
        self.assertEqual(len(ce.count_problems(text, "x.md")), 1)

    def test_entries_below_stop_at_the_next_heading(self):
        text = "### Family\n\n**Head.** The two entries below are shapes.\n\n**One.**\n\n**Two.**\n\n### Next\n\n**Other.**\n"
        self.assertEqual(ce.count_problems(text, "x.md"), [])

    def test_all_n_still_against_the_list_above(self):
        text = "- *one*\n- *two*\n- *three*\n\nDone late, all four still pay.\n"
        self.assertEqual(len(ce.count_problems(text, "x.md")), 1)
        self.assertEqual(ce.count_problems(text.replace("four", "three"), "x.md"), [])


class Index(unittest.TestCase):
    def test_entry_without_an_index_line_is_caught(self):
        new = CATALOGUE.replace("**Apples are red.**", "**Apples are red.**\n\n**Apples fall.**")
        found = ce.index_problems(CATALOGUE, new, "x.md")
        self.assertEqual(len(found), 1)
        self.assertIn("First group", found[0])

    def test_entry_with_its_index_line_is_quiet(self):
        new = CATALOGUE.replace("**Apples are red.**", "**Apples are red.**\n\n**Apples fall.**")
        new = new.replace("- an entry about apples", "- an entry about apples\n- apples fall")
        self.assertEqual(ce.index_problems(CATALOGUE, new, "x.md"), [])

    def test_shape_added_inside_an_existing_line_is_quiet(self):
        new = CATALOGUE.replace("**Pears are green.**", "**Pears are green.**\n\n*And ripe ones are soft.*")
        new = new.replace("- an entry about pears", "- an entry about pears · a ripe one")
        self.assertEqual(ce.index_problems(CATALOGUE, new, "x.md"), [])

    def test_reworded_entry_is_quiet(self):
        new = CATALOGUE.replace("Apples are red.", "Apples are mostly red.")
        self.assertEqual(ce.index_problems(CATALOGUE, new, "x.md"), [])

    def test_index_without_groups_is_one_group(self):
        old = "## Contents\n\n- apples\n\n## Apples\n\n- **Red.**\n"
        new = old.replace("- **Red.**", "- **Red.**\n- **Round.**")
        self.assertEqual(len(ce.index_problems(old, new, "x.md")), 1)
        self.assertEqual(ce.index_problems(old, new.replace("- apples", "- apples, round"), "x.md"), [])


class Version(unittest.TestCase):
    def test_engine_edit_without_a_bump_is_caught(self):
        found = ce.version_problems(["skills/qa/SKILL.md"], "0.1.1", "0.1.1", False)
        self.assertEqual(len(found), 1)
        self.assertIn("bump", found[0])

    def test_bump_without_changelog_is_caught(self):
        found = ce.version_problems(["skills/qa/SKILL.md", ".claude-plugin/plugin.json"], "0.1.1", "0.1.2", False)
        self.assertEqual(len(found), 1)
        self.assertIn("CHANGELOG", found[0])

    def test_bump_with_changelog_is_quiet(self):
        self.assertEqual(ce.version_problems(["skills/qa/SKILL.md"], "0.1.1", "0.1.2", True), [])

    def test_edit_outside_the_engine_needs_no_bump(self):
        self.assertEqual(ce.version_problems([".github/scripts/x.py", "tests/t.py"], "0.1.1", "0.1.1", False), [])

    def test_bytecode_beside_an_engine_script_needs_no_bump(self):
        pyc = "skills/qa/scripts/__pycache__/check_session.cpython-312.pyc"
        self.assertEqual(ce.version_problems([pyc], "0.1.1", "0.1.1", False), [])

    def test_clean_tree_is_quiet(self):
        self.assertEqual(ce.version_problems([], "0.1.1", "0.1.1", False), [])


class RulesIndex(unittest.TestCase):
    HEAD = "# C\n\n## Contents\n\n**Every line below is the rule.**\n\n**Group**\n\n"
    def test_a_line_without_an_arrow_is_caught(self):
        text = self.HEAD + "- a shape named, no rule\n- a shape → what to do\n\n## Group\n\n**Entry.**\n"
        found = ce.index_rule_problems(text, "c.md")
        self.assertEqual(len(found), 1)
        self.assertIn(":9:", found[0])

    def test_lines_with_arrows_are_quiet(self):
        text = self.HEAD + "- a shape → what to do\n- **Family** — head → rule: shape → rule · shape → rule\n\n## Group\n\n**Entry.**\n"
        self.assertEqual(ce.index_rule_problems(text, "c.md"), [])

    def test_a_catalogue_without_the_marker_is_not_checked(self):
        text = "# C\n\n## Contents\n\n- a shape named, no rule\n\n## Group\n\n**Entry.**\n"
        self.assertEqual(ce.index_rule_problems(text, "c.md"), [])


class Budgets(unittest.TestCase):
    def test_a_listed_file_over_its_budget_is_caught(self):
        rel = "skills/qa/references/planning.md"
        found = ce.budget_problems("x" * (ce.BUDGETS[rel] + 1), rel)
        self.assertEqual(len(found), 1)
        self.assertIn("make room in the same edit", found[0])

    def test_a_listed_file_at_its_budget_is_quiet(self):
        rel = "skills/qa/references/planning.md"
        self.assertEqual(ce.budget_problems("x" * ce.BUDGETS[rel], rel), [])

    def test_an_unlisted_file_gets_the_default(self):
        rel = "skills/qa/references/a-new-catalogue.md"
        self.assertEqual(ce.budget_problems("x" * ce.DEFAULT_BUDGET, rel), [])
        self.assertEqual(len(ce.budget_problems("x" * (ce.DEFAULT_BUDGET + 1), rel)), 1)

    def test_every_budget_names_a_file_that_exists(self):
        # a renamed catalogue would silently fall back to the default and fail every edit
        self.assertEqual([rel for rel in ce.BUDGETS if not (REPO / rel).is_file()], [])


class Corpus(unittest.TestCase):
    def test_catalogues_as_they_stand_pass_the_counts(self):
        found = []
        for path in sorted(REPO.glob(ce.CATALOGUES)):
            found += ce.count_problems(path.read_text(), str(path.relative_to(REPO)))
        self.assertEqual(found, [])

    def test_rules_indexes_as_they_stand_carry_arrows(self):
        found = []
        for path in sorted(REPO.glob(ce.CATALOGUES)):
            found += ce.index_rule_problems(path.read_text(), str(path.relative_to(REPO)))
        self.assertEqual(found, [])

    def test_catalogues_and_agents_as_they_stand_fit_their_budgets(self):
        found = []
        for path in sorted([*REPO.glob(ce.CATALOGUES), *REPO.glob(ce.AGENTS)]):
            found += ce.budget_problems(path.read_text(), str(path.relative_to(REPO)))
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
