"""Tests for skills/qa/scripts/check_session.py.

A checker over somebody else's writing has two ways to fail, and only one of them is visible. It can
miss a leaked token — and nobody finds out until the repository is shared. Or it can fire on correct
work — and then it is switched off within a week, which costs both checks at once.

So the cases come in pairs: what must be caught, and what must stay quiet. The quiet half is the
bigger one on purpose — session files are mostly prose, written in the project's own language, and
prose is where a secret-shaped regex goes wrong.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "qa" / "scripts" / "check_session.py"

_spec = importlib.util.spec_from_file_location("check_session", SCRIPT)
check_session = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(check_session)


def secrets(text: str) -> list[str]:
    return [m for _, m in check_session.scan_secrets(text.splitlines())]


def tables(text: str, max_cell: int = 850) -> list[str]:
    return [m for _, m in check_session.scan_tables(text.splitlines(), max_cell)]


# --- secrets: what must be caught -----------------------------------------------------------------


class SecretsCaughtTest(unittest.TestCase):
    def test_a_password_with_a_real_looking_value(self):
        self.assertTrue(secrets("password: hunter2xyz\n"))

    def test_a_bearer_header(self):
        self.assertTrue(secrets("Authorization: Bearer abcdefghijklmnop0123456789\n"))

    def test_a_jwt_anywhere_in_the_line(self):
        jwt = "eyJhbGciOi.eyJzdWIiOjEyMw.SflKxwRJSMeK"
        self.assertTrue(secrets(f"the response carried {jwt} in the body\n"))

    def test_a_private_key_block(self):
        self.assertTrue(secrets("-----BEGIN RSA PRIVATE KEY-----\n"))

    def test_a_cloud_key_id(self):
        self.assertTrue(secrets("AKIAIOSFODNN7EXAMPLE\n"))

    def test_a_forge_token(self):
        self.assertTrue(secrets("ghp_16CharactersAndThenSomeMore0123\n"))

    def test_a_one_time_link_is_a_credential_too(self):
        """Even one the executor requested themselves — the engine says so in as many words."""
        self.assertTrue(secrets("Invite: https://shop.example.com/join?token=Ab3xY9kLmN0pQr5s\n"))

    def test_one_line_yields_one_problem_not_four(self):
        line = "password: hunter2xyz token: Ab3xY9kLmN0pQr5s\n"
        self.assertEqual(len(secrets(line)), 1)


# --- secrets: what must stay quiet ----------------------------------------------------------------


class SecretsQuietTest(unittest.TestCase):
    def test_the_masked_forms_the_engine_mandates(self):
        text = (
            "Authorization: <TOKEN>\n"
            "password: ***\n"
            "api_key: $ACME_API_KEY\n"
            "token: ${SHOP_TOKEN}\n"
            "secret: TODO\n"
            "password: <your password here>\n"
        )
        self.assertEqual(secrets(text), [])

    def test_prose_that_merely_uses_the_words(self):
        """The shape a looser rule fires on — and the engine's own verdict vocabulary lives here."""
        text = (
            "a wall the executor cannot pass: signing in a wallet\n"
            "token: expired\n"
            "FR-2 — verdict: pass\n"
            "the password field is required\n"
            "credentials: the profile's secrets source\n"
        )
        self.assertEqual(secrets(text), [])

    def test_a_value_of_letters_only_is_not_treated_as_a_credential(self):
        """A deliberate trade: letters-and-digits is the shape of a token, and demanding less would
        put every «token: missing» in the report."""
        self.assertEqual(secrets("token: missingvalue\n"), [])

    def test_a_short_value_is_not_a_credential(self):
        self.assertEqual(secrets("pwd: 12ab\n"), [])


# --- tables ---------------------------------------------------------------------------------------


GOOD_TABLE = """| № | Requirement | Description |
|---|---|---|
| B-1 | FR-2 | the total is wrong |
| B-2 | FR-3 | fine |
"""


class TableTest(unittest.TestCase):
    def test_a_well_formed_table_is_quiet(self):
        self.assertEqual(tables(GOOD_TABLE), [])

    def test_an_unescaped_bar_inside_a_cell_is_caught(self):
        """The damage is invisible in a rendered preview — the row just reads as written."""
        broken = GOOD_TABLE.replace("the total is wrong", "the columns ID | Name | Status are swapped")
        found = tables(broken)
        self.assertEqual(len(found), 1)
        self.assertIn("5 cell(s) against the separator's 3", found[0])

    def test_an_escaped_bar_is_allowed(self):
        ok = GOOD_TABLE.replace("the total is wrong", r"the columns ID \| Name are swapped")
        self.assertEqual(tables(ok), [])

    def test_an_oversized_cell_is_caught_once_per_row(self):
        big = GOOD_TABLE.replace("the total is wrong", "x" * 900)
        found = tables(big)
        self.assertEqual(len(found), 1)
        self.assertIn("over the 850 limit", found[0])

    def test_the_limit_is_configurable(self):
        text = GOOD_TABLE.replace("the total is wrong", "x" * 100)
        self.assertEqual(tables(text, max_cell=850), [])
        self.assertTrue(tables(text, max_cell=50))

    def test_bars_inside_a_fenced_block_are_not_a_table(self):
        """A quoted log or a tracker comment often holds `|` — and neither is a table."""
        text = "```\n| not | a | table |\n| at | all\n```\n"
        self.assertEqual(tables(text), [])

    def test_a_run_of_bar_lines_without_a_separator_is_left_alone(self):
        self.assertEqual(tables("| just | some | bars |\n| and | more | bars |\n"), [])


# --- structure --------------------------------------------------------------------------------------


class StructureTest(unittest.TestCase):
    def test_too_few_sections_is_reported(self):
        found = check_session.scan_structure("# R\n\n## Summary\n".splitlines(), 3)
        self.assertEqual(len(found), 1)
        self.assertIn("1 section(s)", found[0][1])

    def test_sections_in_any_language_count(self):
        """Nothing here matches a caption: the files are written in the project's language."""
        text = "# Результат\n\n## Итог\n\n## Находки по продукту\n\n## Ретро исполнителя\n"
        self.assertEqual(check_session.scan_structure(text.splitlines(), 3), [])

    def test_headings_inside_a_fence_do_not_count(self):
        text = "# R\n\n## Summary\n\n```\n## not a heading\n## nor this\n```\n"
        self.assertEqual(len(check_session.scan_structure(text.splitlines(), 3)), 1)


# --- the driver ---------------------------------------------------------------------------------


class DriverTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_a_clean_file_produces_no_problems(self):
        path = self.write("ok.md", "# R\n\n## A\n\n## B\n\n## C\n" + GOOD_TABLE)
        self.assertEqual(check_session.check_file(path, 850, 3), [])

    def test_problems_are_printed_as_file_line_message(self):
        path = self.write("bad.md", "# R\n\n## A\n\n## B\n\n## C\n\npassword: hunter2xyz\n")
        found = check_session.check_file(path, 850, 3)
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0].startswith(f"{path}:9:"))

    def test_a_folder_target_collects_markdown_only(self):
        self.write("a.md", "# a\n")
        self.write("b.md", "# b\n")
        (self.dir / "notes.txt").write_text("password: hunter2xyz\n", encoding="utf-8")
        collected = check_session.collect([str(self.dir)])
        self.assertEqual(sorted(p.name for p in collected), ["a.md", "b.md"])

    def test_a_missing_target_is_skipped_not_fatal(self):
        self.assertEqual(check_session.collect([str(self.dir / "nope.md")]), [])

    def test_structure_is_only_required_of_a_result_file(self):
        """Plans, briefs, retros and the report have templates of their own and legitimately carry
        fewer sections — pointed at a whole session folder, the rule would fire on every one."""
        plan = self.write("1-plan.md", "# Plan\n\n## Scenarios\n")
        self.assertEqual(check_session.check_file(plan, 850, 3), [])
        result = self.write("3-manual-result.md", "# Result\n\n## Scenarios\n")
        self.assertTrue(check_session.check_file(result, 850, 3))
        self.assertEqual(check_session.check_file(result, 850, 0), [])


class EngineFilesTest(unittest.TestCase):
    """The engine's own corpus is the largest body of correct prose available, and it is full of the
    shapes this checker hunts: masked credentials, wide tables, long cells. A false positive here is
    a false positive in every session."""

    def test_the_engine_corpus_is_quiet(self):
        targets = [
            REPO / "skills" / "qa" / "references",
            REPO / "skills" / "qa" / "templates",
            REPO / "agents",
        ]
        problems: list[str] = []
        for path in check_session.collect([str(t) for t in targets]):
            problems.extend(check_session.check_file(path, 850, 0))
        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
