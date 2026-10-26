"""Tests for skills/qa/scripts/session.py — file numbers, finding ids, the monthly sweep.

Each command replaces a paragraph the manager used to execute by hand, so a case here is a way that paragraph
went wrong: a number counted from the wrong files, an id read off a mention, a link rewritten into the wrong
style or left pointing at a path that no longer exists. The sweep runs on a real temporary git repository,
because «which files can hold a link» is answered by git.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "qa" / "scripts" / "session.py"

_spec = importlib.util.spec_from_file_location("session", SCRIPT)
session = importlib.util.module_from_spec(_spec)
sys.modules["session"] = session
assert _spec.loader is not None
_spec.loader.exec_module(session)

AUG = "2026-08-10_acme-412-coupon"
AUG2 = "2026-08-11_acme-415-refund"
SEP = "2026-09-02_acme-430-cart"
OCT = "2026-10-01_acme-441-promo"
TODAY = dt.date(2026, 10, 5)


class NextFile(unittest.TestCase):
    def test_round_two_continues_after_the_scheme(self):
        names = ["0-session.md", "1-plan.md", "2-manual-task.md", "3-manual-result.md", "7-retro.md", "99-report.md"]
        self.assertEqual(session.next_file(names, "manual-task", 2), "8-manual-task-2.md")

    def test_the_numbering_is_never_reset(self):
        names = ["0-session.md", "7-retro.md", "8-manual-task-2.md", "9-manual-result-2.md", "99-report.md"]
        self.assertEqual(session.next_file(names, "retro", 2), "10-retro-2.md")

    def test_report_and_meta_sit_outside_the_numbering(self):
        self.assertEqual(session.next_number(["0-session.md", "99-report.md"]), 1)

    def test_an_old_scheme_folder_starts_at_eight(self):
        self.assertEqual(session.next_number(["session.md", "report.md", "task-manual.md"]), 8)

    def test_an_old_scheme_folder_after_the_two_renames_still_starts_at_eight(self):
        self.assertEqual(session.next_number(["0-session.md", "99-report.md", "task-manual.md"]), 8)

    def test_a_readme_and_screenshots_are_not_the_old_scheme(self):
        self.assertEqual(session.next_number(["0-session.md", "README.md", "screenshots"]), 1)

    def test_round_one_is_refused(self):
        with tempfile.TemporaryDirectory() as d, redirect_stdout(io.StringIO()):
            self.assertEqual(session.main(["next-file", d, "plan", "1"]), 2)


class MaxId(unittest.TestCase):
    def test_the_template_cell_is_an_assignment(self):
        self.assertEqual(session.assigned_ids("| **ABC-12 · Major** | FR-1 | text |", "ABC-"), [12, 12])

    def test_an_id_column_of_the_projects_own_format_is_an_assignment(self):
        self.assertEqual(session.assigned_ids("| ABC-7 | Major | text |", "ABC-"), [7])

    def test_the_fixed_line_is_an_assignment(self):
        self.assertEqual(session.assigned_ids("Fixed: ABC-9 · Minor — the filter", "ABC-"), [9])

    def test_a_mention_in_prose_is_not(self):
        self.assertEqual(session.assigned_ids("see ABC-40; numbering starts at ABC-50 in the brief", "ABC-"), [])

    def test_another_prefix_ending_the_same_way_is_not(self):
        self.assertEqual(session.assigned_ids("Z" + "ABC-3 · Major", "ABC-"), [])

    def test_the_maximum_spans_the_month_archives_and_the_old_names(self):
        with tempfile.TemporaryDirectory() as d:
            s = Path(d)
            (s / AUG).mkdir()
            (s / AUG / "99-report.md").write_text("| **ABC-5 · Minor** | FR-1 | x |\n")
            (s / "2026-07" / "2026-07-01_acme-400-old").mkdir(parents=True)
            (s / "2026-07" / "2026-07-01_acme-400-old" / "report.md").write_text("| **ABC-31 · Major** | FR-2 | x |\n")
            (s / OCT).mkdir()
            (s / OCT / "2-manual-task.md").write_text("assign from ABC-90 on\n")  # a brief, not a report
            n, where = session.max_id(s, "ABC-")
            self.assertEqual(n, 31)
            self.assertEqual(where.name, "report.md")

    def test_an_id_living_only_in_the_side_findings_registry_counts(self):
        with tempfile.TemporaryDirectory() as d:
            s = Path(d)
            (s / AUG).mkdir()
            (s / AUG / "99-report.md").write_text("| **ABC-5 · Minor** | FR-1 | x |\n")
            (s / "side-findings.md").write_text("| **ABC-9** | Minor | **Area \\ moved here from a report** |\n")
            n, where = session.max_id(s, "ABC-")
            self.assertEqual(n, 9)
            self.assertEqual(where.name, "side-findings.md")


class Sweep(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.s = self.root / "docs" / "test-sessions"
        for name in (AUG, AUG2, SEP, OCT):
            (self.s / name).mkdir(parents=True)
            (self.s / name / "99-report.md").write_text(f"# {name}\n")
        (self.s / "side-findings.md").write_text("| date | finding |\n")
        # a root path, from the project map
        (self.root / "CLAUDE.md").write_text(f"Sample report: `docs/test-sessions/{AUG}/99-report.md`.\n")
        # the registry, relative to itself
        (self.s / "README.md").write_text(f"| ACME-412 | done | `{AUG}/` |\n| ACME-441 | done | `{OCT}/` |\n")
        # a session that moves, pointing at another that moves to a different month
        (self.s / SEP / "0-session.md").write_text(f"Round 1: [report](../{AUG}/99-report.md)\n")
        # two sessions of the same month pointing at each other: the link survives the move unchanged
        (self.s / AUG2 / "0-session.md").write_text(f"Related: ../{AUG}/99-report.md\n")
        # a session that stays, pointing at one that moves
        (self.s / OCT / "0-session.md").write_text(f"Previous: ../{SEP}/99-report.md and a placeholder <sessions>/2026-08-10_…\n")

    def tearDown(self):
        self._tmp.cleanup()

    def run_sweep(self, *extra):
        out = io.StringIO()
        with redirect_stdout(out):
            code = session.sweep(self.s, TODAY, dry_run="--dry-run" in extra)
        return code, out.getvalue()

    def test_past_months_move_into_their_archives_and_the_current_one_stays(self):
        code, out = self.run_sweep()
        self.assertEqual(code, 0, out)
        self.assertTrue((self.s / "2026-08" / AUG).is_dir())
        self.assertTrue((self.s / "2026-08" / AUG2).is_dir())
        self.assertTrue((self.s / "2026-09" / SEP).is_dir())
        self.assertTrue((self.s / OCT).is_dir())
        self.assertTrue((self.s / "side-findings.md").is_file())

    def test_every_link_keeps_its_own_style(self):
        self.run_sweep()
        self.assertIn(f"`docs/test-sessions/2026-08/{AUG}/99-report.md`", (self.root / "CLAUDE.md").read_text())
        registry = (self.s / "README.md").read_text()
        self.assertIn(f"`2026-08/{AUG}/`", registry)
        self.assertIn(f"`{OCT}/`", registry)
        self.assertIn(f"(../../2026-08/{AUG}/99-report.md)", (self.s / "2026-09" / SEP / "0-session.md").read_text())
        self.assertIn(f"Related: ../{AUG}/99-report.md", (self.s / "2026-08" / AUG2 / "0-session.md").read_text())
        self.assertIn(f"Previous: ../2026-09/{SEP}/99-report.md", (self.s / OCT / "0-session.md").read_text())

    def test_a_dry_run_changes_nothing(self):
        before = (self.root / "CLAUDE.md").read_text()
        code, out = self.run_sweep("--dry-run")
        self.assertEqual(code, 0, out)
        self.assertIn("would move", out)
        self.assertTrue((self.s / AUG).is_dir())
        self.assertEqual((self.root / "CLAUDE.md").read_text(), before)

    def test_a_dead_link_is_reported_even_when_the_sweep_did_not_touch_it(self):
        (self.root / "notes.md").write_text("Lost: docs/test-sessions/2026-06-01_acme-300-gone/99-report.md\n")
        code, out = self.run_sweep()
        self.assertEqual(code, 1)
        self.assertIn("notes.md:1: docs/test-sessions/2026-06-01_acme-300-gone/99-report.md", out)

    def test_a_folder_already_in_the_archive_is_left_in_place(self):
        (self.s / "2026-08" / AUG).mkdir(parents=True)
        code, out = self.run_sweep()
        self.assertEqual(code, 1)
        self.assertIn("already exists", out)
        self.assertTrue((self.s / AUG).is_dir())

    def test_a_second_sweep_has_nothing_to_do(self):
        self.run_sweep()
        code, out = self.run_sweep()
        self.assertEqual(code, 0, out)
        self.assertIn("nothing to sweep", out)


class Shot(unittest.TestCase):
    """The rename and the markers are one move: the marker left behind is the half that was forgotten."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        (self.dir / "screenshots").mkdir()
        (self.dir / "screenshots" / "c3-2.png").write_bytes(b"png")
        (self.dir / "screenshots" / "c13-2.png").write_bytes(b"png")
        (self.dir / "9-manual-result-2.md").write_text(
            "- the total doubles 📎 c3-2.png\n- another 📎 `c3-2.png`\n- unrelated 📎 c13-2.png\n", encoding="utf-8")

    def test_the_file_takes_the_id_and_keeps_the_round_suffix(self):
        code, out = session.rename_shot(self.dir, "c3-2", "ABC-15")
        self.assertEqual(code, 0, out)
        self.assertTrue((self.dir / "screenshots" / "ABC-15-2.png").is_file())
        self.assertFalse((self.dir / "screenshots" / "c3-2.png").exists())
        self.assertIn("📎 ABC-15-2.png", out[-1])

    def test_every_marker_follows_and_a_longer_name_is_left_alone(self):
        session.rename_shot(self.dir, "c3-2", "ABC-15")
        text = (self.dir / "9-manual-result-2.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("ABC-15-2.png"), 2)
        self.assertIn("📎 c13-2.png", text)

    def test_a_marker_that_ends_a_sentence_follows_too(self):
        (self.dir / "3-manual-result.md").write_text(
            "the window is empty. 📎 c3-2.png. A control run followed.\nnot a marker: 📎 c3-2.png.bak\n", encoding="utf-8")
        session.rename_shot(self.dir, "c3-2", "ABC-15")
        text = (self.dir / "3-manual-result.md").read_text(encoding="utf-8")
        self.assertIn("📎 ABC-15-2.png. A control", text)
        self.assertIn("📎 c3-2.png.bak", text)

    def test_a_missing_candidate_changes_nothing(self):
        code, _ = session.rename_shot(self.dir, "c4-2", "ABC-15")
        self.assertEqual(code, 1)
        self.assertIn("c3-2.png", (self.dir / "9-manual-result-2.md").read_text(encoding="utf-8"))

    def test_an_id_already_taken_by_a_file_is_refused(self):
        (self.dir / "screenshots" / "ABC-15-2.png").write_bytes(b"png")
        code, _ = session.rename_shot(self.dir, "c3-2", "ABC-15")
        self.assertEqual(code, 1)
        self.assertTrue((self.dir / "screenshots" / "c3-2.png").is_file())

    def test_not_a_candidate_name_is_a_usage_error(self):
        self.assertEqual(session.rename_shot(self.dir, "shot-1", "ABC-15")[0], 2)


if __name__ == "__main__":
    unittest.main()
