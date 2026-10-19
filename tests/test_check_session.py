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


# --- screenshots ------------------------------------------------------------------------------------


class ScreenshotTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        (self.dir / "screenshots").mkdir()
        (self.dir / "screenshots" / "ACME-12.png").write_bytes(b"")

    def shots(self, text: str) -> list[str]:
        return [m for _, m in check_session.scan_screenshots(text.splitlines(), self.dir)]

    def test_a_marker_whose_file_exists_is_quiet(self):
        self.assertEqual(self.shots("| **ACME-12 · Major** | FR-1 | broken *Tech.: 📎 ACME-12.png* |\n"), [])

    def test_a_marker_left_on_the_candidate_name_is_caught(self):
        """The rename at id assignment is the step that gets forgotten."""
        found = self.shots("*Tech.: 📎 c3.png*\n")
        self.assertEqual(len(found), 1)
        self.assertIn("c3.png", found[0])

    def test_a_marker_in_backticks_is_resolved_too(self):
        self.assertEqual(self.shots("📎 `ACME-12.png`\n"), [])
        self.assertTrue(self.shots("📎 `ACME-13.png`\n"))

    def test_an_image_named_without_the_marker_is_the_product_s_not_ours(self):
        self.assertEqual(self.shots("the page requests logo.png and gets a 404\n"), [])

    def test_a_placeholder_in_a_template_is_quiet(self):
        self.assertEqual(self.shots("*Tech.: …, 📎 <ID>.png*\n"), [])

    # Headers only: the checker reads the size from them and never decodes the picture.
    @staticmethod
    def png(width: int) -> bytes:
        return b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + width.to_bytes(4, "big") + (500).to_bytes(4, "big")

    @staticmethod
    def jpeg(width: int) -> bytes:
        app0 = b"\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 9  # a segment before the frame, as the tool writes it
        sof0 = b"\xff\xc0\x00\x11\x08" + (500).to_bytes(2, "big") + width.to_bytes(2, "big") + b"\x03" + b"\x00" * 9
        return b"\xff\xd8" + app0 + sof0 + b"\xff\xd9"

    def put(self, name: str, data: bytes) -> None:
        (self.dir / "screenshots" / name).write_bytes(data)

    def test_a_jpeg_shrunk_by_scale_is_caught(self):
        """The tool's plain screenshot at `scale` 0.6: 739 px wide, captions five pixels tall."""
        self.put("c1.jpg", self.jpeg(739))
        found = self.shots("📎 c1.jpg\n")
        self.assertEqual(len(found), 1)
        self.assertIn("739", found[0])
        self.assertIn("zoom", found[0])

    def test_a_jpeg_at_full_scale_is_quiet(self):
        self.put("c1.jpg", self.jpeg(1232))
        self.assertEqual(self.shots("📎 c1.jpg\n"), [])

    def test_a_small_zoom_is_quiet(self):
        """A `zoom` is a lossless PNG of a region — narrow, and readable."""
        self.put("c1.png", self.png(314))
        self.assertEqual(self.shots("📎 c1.png\n"), [])

    def test_a_jpeg_named_png_is_caught(self):
        self.put("c1.png", self.jpeg(1232))
        found = self.shots("📎 c1.png\n")
        self.assertEqual(len(found), 1)
        self.assertIn("JPEG under another extension", found[0])

    def test_jpg_and_jpeg_are_one_format(self):
        self.put("c1.jpeg", self.jpeg(1232))
        self.assertEqual(self.shots("📎 c1.jpeg\n"), [])


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


class FolderNumberingTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        for name in ("0-session.md", "1-plan.md", "2-manual-task.md", "3-manual-result.md", "7-retro.md", "99-report.md"):
            (self.dir / name).write_text("# x\n", encoding="utf-8")

    def test_a_round_that_counted_by_hand_is_caught(self):
        for name in ("8-plan-2.md", "8-manual-task-2.md", "8-manual-result-2.md"):
            (self.dir / name).write_text("# x\n", encoding="utf-8")
        found = check_session.scan_folder(self.dir)
        self.assertEqual(len(found), 1)
        self.assertIn("share the number 8", found[0])
        self.assertIn("next-file", found[0])

    def test_a_round_numbered_by_the_script_is_quiet(self):
        for name in ("8-plan-2.md", "9-manual-task-2.md", "10-manual-result-2.md"):
            (self.dir / name).write_text("# x\n", encoding="utf-8")
        self.assertEqual(check_session.scan_folder(self.dir), [])

    def test_the_meta_file_and_the_report_sit_outside_the_numbering(self):
        self.assertEqual(check_session.scan_folder(self.dir), [])

    def test_screenshots_and_issue_files_are_not_numbered_files(self):
        (self.dir / "screenshots").mkdir()
        (self.dir / "issue-B12.md").write_text("# x\n", encoding="utf-8")
        self.assertEqual(check_session.scan_folder(self.dir), [])


BRIEF = """# Brief

## Retest

| # | Requirement | Round 1 | What got in the way |
|---|---|---|---|
| R1 | the total is rounded | pass | — |

## Scenarios

| # | Scenario | Expected effect | Fixture | Identity |
|---|---|---|---|---|
| 0 | the refuting check | confirmed | — | qa-1 |
| S1 | the coupon applies once | the total drops once | cart A | qa-1 |
| S2 | a second apply is refused | 409, the total unchanged | cart A | qa-1 |
| S3 | the coupon on an empty cart | refused | cart B | qa-1 |
| N | <scenario> | <effect> | <fixture> | <who> |
"""


class ScenarioHeadingsTest(unittest.TestCase):
    """Scenario ids are identifiers, so the match is language-neutral; the quiet cases are the ways
    executors actually write headings."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        (self.dir / "2-manual-task.md").write_text(BRIEF, encoding="utf-8")

    def missing(self, result: str, name: str = "3-manual-result.md") -> list[str]:
        path = self.dir / name
        path.write_text(result, encoding="utf-8")
        found = check_session.scan_scenarios(result.splitlines(), path)
        return [m.split()[1] for _, m in found]

    def test_the_brief_s_scenario_table_is_the_last_one_keyed_by_hash(self):
        self.assertEqual(check_session.brief_scenario_ids(BRIEF.splitlines()), ["0", "S1", "S2", "S3"])

    def test_a_result_cut_after_its_first_sections_is_caught(self):
        result = "## 0. Fingerprint\n\n## S1 — applies once — pass\n\n## Summary\n"
        self.assertEqual(self.missing(result), ["S2", "S3"])

    def test_every_id_in_a_heading_of_its_own_is_quiet(self):
        result = "## 0. Fingerprint\n## S1 — once\n## S2. twice\n## Сценарий S3 — пустая корзина\n"
        self.assertEqual(self.missing(result), [])

    def test_ids_run_together_in_one_heading_are_quiet(self):
        result = "## 0 — fingerprint\n## S1 + S2 (one cart) — pass\n### S3 (inside the same pass)\n"
        self.assertEqual(self.missing(result), [])

    def test_a_range_in_a_heading_is_unfolded(self):
        result = "## 0. Fingerprint (12:01–12:03)\n## S1–S3. The coupon\n"
        self.assertEqual(self.missing(result), [])

    def test_a_scenario_split_into_parts_keeps_its_id(self):
        result = "## 0\n## S1\n## S2a — first apply\n## S2b — second apply\n## S3\n"
        self.assertEqual(self.missing(result), [])

    def test_a_number_inside_a_timestamp_is_not_an_id(self):
        result = "## S1 (10:03:00)\n## S2\n## S3\n"
        self.assertEqual(self.missing(result), ["0"])

    def test_a_clock_range_in_a_heading_vouches_for_no_numbered_scenario(self):
        brief = BRIEF.replace("| S1 |", "| 1 |").replace("| S2 |", "| 2 |").replace("| S3 |", "| 3 |")
        (self.dir / "2-manual-task.md").write_text(brief, encoding="utf-8")
        result = "## 0. Fingerprint (2026-10-08T11:01:00Z)\n## 1 — once (11:02–11:05 UTC)\n"
        self.assertEqual(self.missing(result), ["2", "3"])

    def test_a_bare_numbered_brief_is_answered_by_s_prefixed_headings(self):
        brief = BRIEF.replace("| S1 |", "| 1 |").replace("| S2 |", "| 2 |").replace("| S3 |", "| 3 |")
        (self.dir / "2-manual-task.md").write_text(brief, encoding="utf-8")
        result = "## S0 — fingerprint\n## S1 — base\n## S2a — part\n"
        self.assertEqual(self.missing(result), ["3"])

    def test_a_bare_id_with_a_letter_in_any_script_is_answered_by_an_s_prefixed_heading(self):
        brief = BRIEF.replace("| S1 |", "| 0а |")
        (self.dir / "2-manual-task.md").write_text(brief, encoding="utf-8")
        result = "## S0а — snapshot\n## S2\n## S3\n"
        self.assertEqual(self.missing(result), [])

    def test_a_round_two_result_is_matched_against_the_round_two_brief(self):
        (self.dir / "8-manual-task-2.md").write_text(BRIEF.replace("| S3 |", "| S4 |"), encoding="utf-8")
        result = "## 0\n## S1\n## S2\n## S3\n"
        self.assertEqual(self.missing(result, "9-manual-result-2.md"), ["S4"])

    def test_no_brief_or_no_scenario_table_is_quiet(self):
        (self.dir / "2-manual-task.md").write_text("# Brief\n\n- scenario one\n", encoding="utf-8")
        self.assertEqual(self.missing("## Summary\n"), [])
        self.assertEqual(self.missing("## Summary\n", "5-automator-result.md"), [])


class QuestionNotesTest(unittest.TestCase):
    def test_a_question_in_prose_is_listed(self):
        found = check_session.scan_questions(["## S2", "how did this cart get a second coupon?", "ok"])
        self.assertEqual([n for n, _ in found], [2])

    def test_code_and_urls_are_not_questions(self):
        lines = ["`GET /cart?id=7`", "https://shop.example.com/cart?id=7", "```", "a ? b", "```"]
        self.assertEqual(check_session.scan_questions(lines), [])

    def test_notes_are_only_taken_from_a_manual_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "1-plan.md"
            plan.write_text("why this order?\n", encoding="utf-8")
            self.assertEqual(check_session.question_notes(plan), [])


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
