"""Tests for skills/qa/scripts/transcripts.py — the retro's numbers from the transcripts on disk.

The fixture is a fake `~/.claude/projects`: a manager that writes into the session folder, an executor whose prompt
names it, a later session that only reads the folder, and one that moves it in a sweep. A case here is a way the
numbers came out wrong on real transcripts: a streamed message counted twice, a reader taken for the manager, an
executor resumed three days later reported as three days of work, a renamed folder losing its round 1 — and, for
«where the context went», a share computed from characters instead of the measured growth (a one-off measurement put
the instructions at half their real share that way).

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


def call(minute: int, msg_id: str, context: int, out: int = 0, thinking: int = 0, *calls: tuple[str, str, dict]) -> dict:
    e = assistant(minute, msg_id, *calls, context=context, out=out)
    e["message"]["usage"]["output_tokens_details"] = {"thinking_tokens": thinking}
    return e


class WhereItWent(Fixture):
    """Every call's context split by what put it there — measured by the growth between calls, not by a guess of
    characters per token; the sum over calls is the processed context, which is what a session pays."""

    def test_growth_goes_to_what_came_back_and_output_stays(self):
        engine = "/plugins/cache/qa-cube/qa-cube/0.1.0/skills/qa/references/planning.md"
        write(self.proj / "s" / "subagents" / "agent-a.jsonl", [
            prompt(0, f"folder 2026-10-01_{SLUG}"),
            call(1, "a", 1000, 100, 0, ("t1", "Read", {"file_path": engine})), result(1, "t1", "x" * 300),
            call(2, "b", 1500, 50, 0, ("t2", "Read", {"file_path": "/repo/.claude/qa-profile.md"})), result(2, "t2", "y" * 900),
            call(3, "c", 1750),
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(s.processed, 1000 + 1500 + 1750)
        P = transcripts
        self.assertEqual({k: round(v) for k, v in s.parts.items() if v},
                         {P.START: 3000, P.OUTPUT: 250, P.ENGINE: 800, P.PROFILE: 200})   # 300 chars became 400 tokens: measured, not guessed

    def test_a_drop_takes_thinking_first(self):
        write(self.proj / "s" / "subagents" / "agent-b.jsonl", [
            prompt(0, f"folder 2026-10-01_{SLUG}"),
            call(1, "a", 1000, 300, 200, ("t1", "Read", {"file_path": f"{self.folder}/1-plan.md"})), result(1, "t1", "p" * 500),
            call(2, "b", 1800),
            prompt(3, "a new user turn: the earlier thinking is stripped"),
            call(4, "c", 1600),
        ])
        [s] = transcripts.collect(self.root, self.folder)
        P = transcripts
        self.assertEqual(round(s.parts[P.OWN]), 500 + 500)     # the plan stays whole in b and in c
        self.assertEqual(round(s.parts[P.OUTPUT]), 300 + 100)  # b holds thinking and text, c only the text

    def test_a_drop_below_the_start_shrinks_the_start(self):
        write(self.proj / "s" / "subagents" / "agent-d.jsonl", [
            prompt(0, f"folder 2026-10-01_{SLUG}"),
            call(1, "a", 1000, 100), call(2, "b", 600),
        ])
        [s] = transcripts.collect(self.root, self.folder)
        self.assertEqual(round(sum(s.parts.values())), s.processed)   # the shares never add up to more than was sent

    def test_targets(self):
        other = self.folder.parent / "2026-09-20_acme-300-old"
        T, P = transcripts.target, transcripts
        cases = {
            ("Read", f"{self.folder}/3-manual-result.md"): P.OWN,
            ("Read", f"{other}/3-manual-result.md"): P.OTHER_SESSIONS,
            ("Read", f"{self.folder.parent}/environment-state.md"): P.OTHER_SESSIONS,
            ("Read", "/repo/.claude/qa-profile/browser.md"): P.PROFILE,
            ("Read", "/repo/.claude/qa-cube-feedback.md"): P.PROFILE,     # not the engine, though it says qa-cube
            ("Read", "/repo/docs/knowledge/payments.md"): P.PROFILE,
            ("Read", "/opt/claude/plugins/cache/qa-cube/qa-cube/0.1.0/skills/qa/SKILL.md"): P.ENGINE,
            ("Bash", "curl -s https://api.example.test/v1/orders"): P.WORK,
            ("Bash", f"curl -s https://api.example.test/{self.folder.parent.name}/42"): P.WORK,   # an API path, not the folder
            ("Bash", f"cat {self.folder.parent.name}/2026-09-20_acme-300-old/1-plan.md"): P.OTHER_SESSIONS,
            ("Bash", "grep -rn knowledge /opt/claude/plugins/cache/qa-cube/qa-cube/0.1.0/skills/qa/"): P.ENGINE,
            ("Read", "/repo/docs/product-knowledge.md"): P.WORK,
        }
        for (name, aim), want in cases.items():
            key = "file_path" if name == "Read" else "command"
            self.assertEqual(T({"name": name, "input": {key: aim}}, self.folder), want, aim)

    def test_the_table_is_printed_with_processed_and_a_total(self):
        write(self.proj / "m.jsonl", [
            call(1, "a", 2000, 10, 0, ("t1", "Write", {"file_path": f"{self.folder}/1-plan.md", "content": "x"})),
            result(1, "t1", "ok"), call(2, "b", 2100),
        ])
        write(self.proj / "s" / "subagents" / "agent-c.jsonl", [prompt(0, f"folder 2026-10-01_{SLUG}"), call(1, "a", 900)])
        code, out = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("| processed |", out)
        self.assertIn("4k |", out)                     # the manager's 2000 + 2100
        self.assertRegex(out, r"\n\| all \| \d+% \|")


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
