"""Tests for skills/qa-day/scripts/qa_day.py.

The digest is the one piece of real code the plugin ships, and all of it is parsing: session folders,
a passport written in the project's language, a report in the project's own format, legacy file names
from older schemes. None of that fails loudly — a parser that quietly stops recognising a file prints
a shorter digest, and a shorter digest looks exactly like a quiet day.

So the cases below are about the rules the skill file promises out loud (the day comes from the FOLDER
NAME, the task ids come from the folder name and the title only, both folder levels are walked, a
localized passport is parsed by structure rather than by caption) and about the shapes real projects
actually hold: old names, missing files, a profile with no `sessions:` key.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "qa-day" / "scripts" / "qa_day.py"

_spec = importlib.util.spec_from_file_location("qa_day", SCRIPT)
qa_day = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(qa_day)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class TempProject(unittest.TestCase):
    """A throwaway project root under a temp dir, with helpers for the pieces a session is made of."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "acme-shop"
        self.root.mkdir(parents=True)
        self.addCleanup(self._tmp.cleanup)

    def profile(self, body: str) -> None:
        write(self.root / ".claude" / "qa-profile.md", body)

    def session(self, folder: str, passport: str | None = None, report: str | None = None, sub: str = "") -> Path:
        base = self.root / "docs" / "test-sessions"
        if sub:
            base = base / sub
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        if passport is not None:
            write(path / "0-session.md", passport)
        if report is not None:
            write(path / "99-report.md", report)
        return path

    def digest(self, *args: str) -> str:
        """Run main() with argv and return everything it printed."""
        out = io.StringIO()
        argv = ["qa_day.py", *args, str(self.root)]
        with contextlib.redirect_stdout(out):
            old = qa_day.sys.argv
            qa_day.sys.argv = argv
            try:
                code = qa_day.main()
            finally:
                qa_day.sys.argv = old
        self.assertEqual(code, 0, out.getvalue())
        return out.getvalue()


# --- the project profile -------------------------------------------------------------------------


class ProfileTest(TempProject):
    def test_no_profile_falls_back_to_the_contract_default(self):
        got = qa_day.profile_of(self.root)
        self.assertEqual(got["sessions"], "docs/test-sessions/")
        self.assertIn("default", got["source"])
        self.assertEqual(got["language"], "")

    def test_reads_sessions_and_language(self):
        self.profile("## Capabilities\nsessions: qa/runs/\nlanguage: ru\n")
        got = qa_day.profile_of(self.root)
        self.assertEqual(got["sessions"], "qa/runs/")
        self.assertEqual(got["language"], "ru")

    def test_sessions_none_is_not_a_path(self):
        """`none` is a declaration that the capability is absent, not a folder called «none»."""
        self.profile("sessions: none\n")
        got = qa_day.profile_of(self.root)
        self.assertEqual(got["sessions"], "docs/test-sessions/")
        self.assertIn("no `sessions:` key", got["source"])

    def test_the_header_wins_over_later_prose(self):
        """A profile is prose around a header, and the prose says the word «sessions» all the time."""
        self.profile("sessions: qa/runs/\n\n## Sessions\nsessions: something the prose mentions\n")
        self.assertEqual(qa_day.profile_of(self.root)["sessions"], "qa/runs/")

    def test_trailing_comment_and_backticks_are_stripped(self):
        self.profile("sessions: `qa/runs/`   # where sessions live\n")
        self.assertEqual(qa_day.profile_of(self.root)["sessions"], "qa/runs/")


# --- finding the files a session is made of ------------------------------------------------------


class FileDiscoveryTest(TempProject):
    def test_current_names_win_over_legacy_ones(self):
        folder = self.session("2026-09-01_acme-412-x", passport="# S\n", report="# R\n")
        write(folder / "session.md", "# old passport\n")
        write(folder / "report.md", "# old report\n")
        self.assertEqual(qa_day.find_passport(folder).name, "0-session.md")
        self.assertEqual(qa_day.find_report(folder).name, "99-report.md")

    def test_legacy_names_are_still_found(self):
        folder = self.session("2026-09-01_acme-412-x")
        write(folder / "session.md", "# old passport\n")
        write(folder / "report.md", "# old report\n")
        self.assertEqual(qa_day.find_passport(folder).name, "session.md")
        self.assertEqual(qa_day.find_report(folder).name, "report.md")

    def test_numbered_legacy_reports_take_the_highest_number(self):
        """Older schemes numbered the report; the freshest round carries the biggest number."""
        folder = self.session("2026-09-01_acme-412-x")
        write(folder / "6-report.md", "# round 1\n")
        write(folder / "11-report-2.md", "# round 2\n")
        self.assertEqual(qa_day.find_report(folder).name, "11-report-2.md")

    def test_a_folder_without_either_file_is_not_an_error(self):
        folder = self.session("2026-09-01_acme-412-x")
        self.assertIsNone(qa_day.find_passport(folder))
        self.assertIsNone(qa_day.find_report(folder))


# --- parsing the passport ------------------------------------------------------------------------


PASSPORT_RU = """# Сессия: ACME-412 купон применяется дважды

- **Задачи:** ACME-412
- **Режим:** полный цикл
- **Статус:** баги

## Журнал раундов

| Раунд | Дата | Триггер | Итог |
|---|---|---|---|
| 1 | 2026-09-01 | первичная проверка | баги |
| 2 | 2026-09-14 | вернули в тестирование | исправлено |

## Сырой источник

- **это не поле шапки:** оно ниже первого `##` и попасть в шапку не должно
"""


class PassportTest(unittest.TestCase):
    def test_a_localized_passport_is_parsed_by_structure_not_by_caption(self):
        got = qa_day.parse_passport(PASSPORT_RU)
        self.assertEqual(got["title"], "Сессия: ACME-412 купон применяется дважды")
        self.assertEqual(len(got["header"]), 3)
        self.assertIn("**Статус:** баги", got["header"][2])

    def test_only_the_last_round_row_is_kept(self):
        got = qa_day.parse_passport(PASSPORT_RU)
        self.assertIn("вернули в тестирование", got["last_round"])
        self.assertNotIn("первичная проверка", got["last_round"])

    def test_header_stops_at_the_first_section(self):
        """The raw-source section repeats the `- **x:** y` shape; the header must not swallow it."""
        got = qa_day.parse_passport(PASSPORT_RU)
        self.assertFalse(any("не поле шапки" in line for line in got["header"]))

    def test_a_passport_without_a_round_log_is_not_an_error(self):
        got = qa_day.parse_passport("# S\n\n- **Status:** in progress\n")
        self.assertEqual(got["last_round"], "")
        self.assertEqual(len(got["header"]), 1)


# --- parsing the report --------------------------------------------------------------------------


REPORT = """# Report: coupon applied twice

**Current verdict (round 2):** bugs — one finding stands
**Method:** API

| Round | Date | Verdict |
|---|---|---|
| 1 | 2026-09-01 | bugs |

## Findings

| ID | Priority | What |
|---|---|---|
| F-1 | Critical | the discount is applied twice |
| F-2 | Major | the audit log misses the second application |
| F-3 | Major | the total is rounded the wrong way |

## Environment leftovers

Two test carts are left on the local environment, both named `eval-*`.

## Tracker comment

```
Verdict: bugs. 3 findings, see the report.
```
"""


class ReportTest(unittest.TestCase):
    def test_verdict_lines_are_the_bold_lines_above_the_first_section(self):
        got = qa_day.parse_report(REPORT)
        self.assertEqual(len(got["verdict"]), 2)
        self.assertTrue(got["verdict"][0].startswith("**Current verdict"))

    def test_findings_are_counted_off_the_untranslated_scale(self):
        got = qa_day.parse_report(REPORT)
        self.assertEqual(got["findings"], {"Critical": 1, "Major": 2})

    def test_a_row_is_counted_once_even_if_it_names_two_severities(self):
        text = "| F-1 | Critical | was Major before |\n"
        self.assertEqual(qa_day.parse_report(text)["findings"], {"Critical": 1})

    def test_the_fenced_tracker_comment_is_not_repeated_in_the_tail(self):
        """The comment is a retelling of the report; printing it would double the digest for nothing."""
        got = qa_day.parse_report(REPORT)
        joined = " ".join(got["tail"])
        self.assertIn("Environment leftovers", joined)
        self.assertNotIn("see the report", joined)

    def test_a_report_without_severities_is_not_an_error(self):
        got = qa_day.parse_report("# R\n\n**Verdict:** done\n")
        self.assertEqual(got["findings"], {})
        self.assertEqual(got["tail"], [])


# --- the session's task ids ----------------------------------------------------------------------


class TaskIdTest(TempProject):
    def test_ids_come_from_the_folder_name_and_the_title_only(self):
        """Reading them out of the whole passport once reported six tasks for one session."""
        folder = self.session(
            "2026-09-01_acme-412-coupon",
            passport="# Session: ACME-412 and ACME-777\n\n- **Parent:** ACME-100\n\n## Raw\n\nsee ACME-999\n",
        )
        got = qa_day.Session(folder).tasks
        self.assertIn("acme-412", [t.lower() for t in got])
        self.assertIn("ACME-777", got)
        self.assertNotIn("ACME-100", got)
        self.assertNotIn("ACME-999", got)

    def test_the_same_id_in_both_places_is_not_listed_twice(self):
        folder = self.session("2026-09-01_acme-412-coupon", passport="# Session: ACME-412\n")
        self.assertEqual(len(qa_day.Session(folder).tasks), 1)

    def test_a_session_with_no_id_anywhere_is_not_an_error(self):
        folder = self.session("2026-09-01_rbac-review", passport="# An initiative run\n")
        self.assertEqual(qa_day.Session(folder).tasks, [])


# --- walking the folders -------------------------------------------------------------------------


class WalkTest(TempProject):
    def test_both_levels_are_walked(self):
        """The root holds what is alive, the month folders hold closed history — a one-level walk
        loses everything from the previous month."""
        self.session("2026-09-01_acme-1-alive", passport="# a\n")
        self.session("2026-08-10_acme-2-archived", passport="# b\n", sub="2026-08")
        names = sorted(s.folder.name for s in qa_day.iter_sessions(self.root / "docs" / "test-sessions"))
        self.assertEqual(names, ["2026-08-10_acme-2-archived", "2026-09-01_acme-1-alive"])

    def test_folders_that_are_not_sessions_are_ignored(self):
        self.session("2026-09-01_acme-1-alive", passport="# a\n")
        (self.root / "docs" / "test-sessions" / "attachments").mkdir(parents=True)
        write(self.root / "docs" / "test-sessions" / "side-findings.md", "# side\n")
        got = qa_day.iter_sessions(self.root / "docs" / "test-sessions")
        self.assertEqual([s.folder.name for s in got], ["2026-09-01_acme-1-alive"])

    def test_a_missing_sessions_directory_returns_nothing(self):
        self.assertEqual(qa_day.iter_sessions(self.root / "nope"), [])


# --- the window, end to end ----------------------------------------------------------------------


class WindowTest(TempProject):
    def test_the_day_comes_from_the_folder_name_not_from_mtime(self):
        """The rule the skill file states out loud: a digest built on mtimes counts a typo fix in an
        old report as today's work, and the day's list stops matching what the person actually ran."""
        folder = self.session("2026-09-01_acme-412-x", passport="# S\n", report="# R\n\n**Verdict:** done\n")
        now = dt.datetime(2026, 9, 14, 12, 0).timestamp()
        for path in folder.rglob("*"):
            os.utime(path, (now, now))
        self.assertIn("no session folder is dated in this window", self.digest("--date", "2026-09-14"))
        # and the same folder IS in the window its NAME points at, mtimes notwithstanding
        self.assertIn("2026-09-01_acme-412-x", self.digest("--date", "2026-09-01"))

    def test_a_multi_day_window_includes_both_ends(self):
        self.session("2026-09-08_acme-1-a", passport="# a\n")
        self.session("2026-09-14_acme-2-b", passport="# b\n")
        out = self.digest("--date", "2026-09-14", "--days", "7")
        self.assertIn("2026-09-08_acme-1-a", out)
        self.assertIn("2026-09-14_acme-2-b", out)
        self.assertIn("total: 2 session(s)", out)

    def test_a_session_outside_the_window_is_left_out(self):
        self.session("2026-09-01_acme-1-a", passport="# a\n")
        out = self.digest("--date", "2026-09-14", "--days", "7")
        self.assertNotIn("2026-09-01_acme-1-a", out)

    def test_a_project_without_sessions_gets_a_note_and_the_run_carries_on(self):
        out = self.digest("--date", "2026-09-14")
        self.assertIn("no sessions directory here", out)
        self.assertIn("total: 0 session(s)", out)

    def test_a_folder_without_a_passport_is_reported_honestly(self):
        self.session("2026-09-14_acme-412-x")
        out = self.digest("--date", "2026-09-14")
        self.assertIn("no passport file", out)
        self.assertIn("no report file", out)

    def test_the_registry_row_is_shown(self):
        self.session("2026-09-14_acme-412-x", passport="# S\n")
        write(
            self.root / "docs" / "test-sessions" / "README.md",
            "| ACME-412 | 2026-09-14 | bugs | 2026-09-14_acme-412-x |\n",
        )
        self.assertIn("registry:", self.digest("--date", "2026-09-14"))


# --- the task lookup -----------------------------------------------------------------------------


class TaskLookupTest(TempProject):
    def test_found_by_folder_name(self):
        self.session("2026-09-01_acme-412-coupon", passport="# Session: ACME-412\n")
        out = self.digest("--task", "acme-412")
        self.assertIn("found by: the folder name", out)
        self.assertIn("2026-09-01_acme-412-coupon", out)

    def test_found_inside_a_multi_task_session_by_grep(self):
        """Without the second pass the answer is «there was no session» — worse than a slower search."""
        self.session("2026-09-01_acme-412-coupon", passport="# Session: ACME-412\n\n## Raw\n\nalso ACME-900 here\n")
        out = self.digest("--task", "ACME-900")
        self.assertIn("a grep of the passports", out)
        self.assertIn("2026-09-01_acme-412-coupon", out)

    def test_the_freshest_of_several_candidates_is_shown(self):
        self.session("2026-08-01_acme-412-old", passport="# Session: ACME-412\n", sub="2026-08")
        self.session("2026-09-01_acme-412-new", passport="# Session: ACME-412\n")
        out = self.digest("--task", "ACME-412")
        self.assertIn("2 candidate(s), showing the freshest", out)
        self.assertIn("--- 2026-09-01_acme-412-new", out)

    def test_nothing_found_is_not_an_error(self):
        self.session("2026-09-01_acme-412-coupon", passport="# Session: ACME-412\n")
        self.assertIn("no session found", self.digest("--task", "ACME-000"))


# --- argument handling ---------------------------------------------------------------------------


class ArgumentTest(TempProject):
    def _main(self, argv: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        old = qa_day.sys.argv
        qa_day.sys.argv = ["qa_day.py", *argv]
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
                return qa_day.main(), out.getvalue()
        finally:
            qa_day.sys.argv = old

    def test_a_bad_date_is_refused_with_exit_2(self):
        code, out = self._main(["--date", "14.09.2026", str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("not a YYYY-MM-DD date", out)

    def test_days_below_one_is_refused_with_exit_2(self):
        code, out = self._main(["--days", "0", str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("--days must be 1 or more", out)

    def test_a_root_that_is_not_a_directory_is_skipped_not_fatal(self):
        self.session("2026-09-14_acme-1-a", passport="# a\n")
        code, out = self._main(["--date", "2026-09-14", str(self.root / "nope"), str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("is not a directory — skipped", out)
        self.assertIn("2026-09-14_acme-1-a", out)

    def test_no_readable_root_at_all_is_still_exit_0(self):
        code, out = self._main([str(self.root / "nope")])
        self.assertEqual(code, 0)
        self.assertIn("no readable project root", out)


if __name__ == "__main__":
    unittest.main()
