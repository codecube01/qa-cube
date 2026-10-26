"""Tests for skills/qa/scripts/transcripts.py — the retro's numbers from the transcripts on disk.

The fixture is a fake `~/.claude/projects`: a manager that writes into the session folder, an executor whose prompt
names it, a later session that only reads the folder, and one that moves it in a sweep. A case here is a way the
numbers came out wrong on real transcripts: a streamed message counted twice, a reader taken for the manager, an
executor resumed three days later reported as three days of work, a renamed folder losing its round 1.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "qa" / "scripts" / "transcripts.py"

_spec = importlib.util.spec_from_file_location("transcripts", SCRIPT)
transcripts = importlib.util.module_from_spec(_spec)
sys.modules["transcripts"] = transcripts
assert _spec.loader is not None
_spec.loader.exec_module(transcripts)

SLUG = "acme-412-cart"


def ts(minute: int) -> str:
    return f"2026-10-01T10:{minute:02d}:00.000Z" if minute < 60 else f"2026-10-0{1 + minute // 1440}T{minute % 1440 // 60:02d}:{minute % 60:02d}:00.000Z"


def assistant(minute: int, msg_id: str, *calls: tuple[str, str, dict], context: int = 1000, out: int = 10) -> dict:
    content = [{"type": "tool_use", "id": cid, "name": name, "input": inp} for cid, name, inp in calls] or [{"type": "text", "text": "ok"}]
    usage = {"input_tokens": 2, "cache_creation_input_tokens": 0, "cache_read_input_tokens": context - 2, "output_tokens": out}
    return {"type": "assistant", "timestamp": ts(minute), "message": {"id": msg_id, "model": "claude-test-1", "usage": usage, "content": content}}


def result(minute: int, cid: str, text: str, error: bool = False, denial: str | None = None) -> dict:
    entry = {"type": "user", "timestamp": ts(minute),
             "message": {"content": [{"type": "tool_result", "tool_use_id": cid, "content": text, "is_error": error}]}}
    if denial:
        entry["toolDenialKind"] = denial
    return entry


def prompt(minute: int, text: str) -> dict:
    return {"type": "user", "timestamp": ts(minute), "message": {"content": text}}


def write(path: Path, entries: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(e) + "\n" for e in entries))
    return path


class Fixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.root = base / "projects"
        self.folder = base / "repo" / "docs" / "test-sessions" / f"2026-10-01_{SLUG}"
        self.folder.mkdir(parents=True)
        self.proj = self.root / transcripts.mangle(base / "repo")
        self.proj.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = transcripts.main([str(self.folder), "--root", str(self.root), *args])
        return code, buf.getvalue()


class Membership(Fixture):
    def test_manager_counts_from_its_first_write_into_the_folder(self):
        write(self.proj / "m1.jsonl", [
            prompt(0, "unrelated work before the session"),
            assistant(1, "a", ("t0", "Bash", {"command": "ls"}), context=900_000),
            assistant(5, "b", ("t1", "Write", {"file_path": f"{self.folder}/0-session.md", "content": "x"}), context=5000),
            result(6, "t1", "ok"),
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(s.who, "manager m1")
        self.assertEqual(s.peak, 5000)            # the 900k before the session is not its context
        self.assertEqual(sum(s.tools.values()), 1)

    def test_a_reader_and_a_sweep_are_not_managers(self):
        write(self.proj / "reader.jsonl", [
            assistant(1, "a", ("t1", "Bash", {"command": f"grep -n FR-1 docs/test-sessions/2026-10-01_{SLUG}/99-report.md"})),
            assistant(2, "b", ("t2", "Read", {"file_path": f"{self.folder}/99-report.md"})),
        ])
        write(self.proj / "sweep.jsonl", [
            assistant(1, "a", ("t1", "Bash", {"command": f"mv 2026-10-01_{SLUG} 2026-10/"})),
            assistant(2, "b", ("t2", "Edit", {"file_path": "/repo/docs/test-sessions/README.md",
                                              "old_string": f"2026-10-01_{SLUG}", "new_string": f"2026-10/2026-10-01_{SLUG}"})),
        ])
        self.assertEqual(transcripts.collect(self.root, self.folder), [])

    def test_executor_found_by_its_prompt_even_after_the_folder_was_renamed(self):
        # round 2 renames the folder to the current date; round 1's executor named the old one
        renamed = self.folder.with_name(f"2026-10-05_{SLUG}")
        self.folder.rename(renamed)
        self.folder = renamed
        ex = write(self.proj / "sess" / "subagents" / "agent-x.jsonl", [
            prompt(0, f"Session folder: /repo/docs/test-sessions/2026-10-01_{SLUG}/\nBrief: 2-manual-task.md"),
            assistant(1, "a"),
        ])
        ex.with_suffix(".meta.json").write_text(json.dumps({"agentType": "qa-cube:qa-manual", "description": "round 1"}))
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(s.who, "qa-manual «round 1»")

    def test_manager_of_a_moved_project_is_found_through_its_executor(self):
        # the project's directory changed; its old transcripts sit under the old path's name
        old = self.root / "-old-checkout"
        write(old / "mgr.jsonl", [assistant(1, "a", ("t1", "Agent", {"prompt": f"folder 2026-10-01_{SLUG}"}))])
        write(old / "subagents" / "agent-y.jsonl", [prompt(2, f"folder 2026-10-01_{SLUG}"), assistant(3, "b")])
        self.assertEqual(sorted(s.who for s in transcripts.collect(self.root, self.folder)), ["manager mgr", "subagent"])


class Numbers(Fixture):
    def test_streamed_message_is_counted_once_and_peak_is_the_largest_context(self):
        write(self.proj / "m.jsonl", [
            assistant(1, "a", ("t1", "Write", {"file_path": f"{self.folder}/1-plan.md"}), context=3000, out=1),
            assistant(1, "a", context=3000, out=40),   # the same message, its last line carries the total
            assistant(2, "b", context=7000, out=60),
            {"type": "system", "subtype": "turn_duration", "durationMs": 120000, "timestamp": ts(3)},
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual((s.peak, s.output, s.active_ms), (7000, 100, 120000))

    def test_errors_denials_retries_and_compaction(self):
        call = ("Bash", {"command": "curl -s localhost"})
        write(self.proj / "m.jsonl", [
            assistant(1, "a", ("t1", "Write", {"file_path": f"{self.folder}/1-plan.md"})),
            assistant(2, "b", ("t2", *call)), result(2, "t2", "connection refused", error=True),
            assistant(3, "c", ("t3", *call)), result(3, "t3", "200"),
            assistant(4, "d", ("t4", "Navigate", {"url": "x"})), result(4, "t4", "blocked", error=True, denial="permission-rule"),
            {"type": "system", "subtype": "compact_boundary", "timestamp": ts(5), "compactMetadata": {"preTokens": 391000}},
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(s.errors, 1)
        self.assertEqual(dict(s.denied), {"Navigate": 1})
        self.assertEqual(list(s.retried.values()), [1])
        self.assertEqual(s.compactions, [391000])

    def test_same_call_counts_as_repeat_only_with_the_same_answer(self):
        calls = []
        for i, answer in enumerate(["a", "b", "c", "same", "same", "same"]):
            calls += [assistant(i + 1, f"m{i}", (f"t{i}", "Shot", {"tab": 1})), result(i + 1, f"t{i}", answer)]
        write(self.proj / "m.jsonl", [assistant(0, "w", ("tw", "Write", {"file_path": f"{self.folder}/x.md"})), *calls])
        code, out = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(len(re.findall(r"same call, same answer ×3: Shot", out)), 1)

    def test_executor_resumed_days_later_reports_its_work_not_the_wall_clock(self):
        write(self.proj / "s" / "subagents" / "agent-z.jsonl", [
            prompt(0, f"folder 2026-10-01_{SLUG}"), assistant(10, "a"),
            prompt(3000, "resume"), assistant(3005, "b"),
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(s.active_ms, 15 * 60_000)
        self.assertEqual(len(s.pauses), 1)


class Cli(Fixture):
    def test_nothing_found_exits_1(self):
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stdout(io.StringIO()):
            self.assertEqual(transcripts.main([str(self.folder), "--root", str(self.root)]), 1)

    def test_missing_folder_exits_2(self):
        self.assertEqual(transcripts.main([str(self.folder / "nope"), "--root", str(self.root)]), 2)

    def test_executors_without_a_manager_say_why(self):
        write(self.proj / "s" / "subagents" / "agent-q.jsonl", [prompt(0, f"folder 2026-10-01_{SLUG}"), assistant(1, "a")])
        code, out = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("cleanupPeriodDays", out)


class Exit(unittest.TestCase):
    def test_a_missing_transcript_root_is_none_found_not_a_usage_error(self):
        folder = Path(tempfile.mkdtemp())
        self.assertEqual(transcripts.main([str(folder), "--root", str(folder / "no-such-dir")]), 1)


if __name__ == "__main__":
    unittest.main()
