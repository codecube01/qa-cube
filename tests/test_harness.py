"""The harness and browser adapters: the rules that keep the engine portable are written where they are read.

The engine's body names an action by its role and sends the reader to the adapter of the harness (or the
browser tool) the session runs in. These are text facts, checked like `test_rule_anchors.py`: an anchor is a
load-bearing sentence matched after the markup is stripped and the whitespace collapsed, so rewrapping never
fails a test and rewording the rule always does.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARNESS = REPO / "skills/qa/references/harness"


def plain(text: str) -> str:
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text)


def read(rel: str) -> str:
    return plain((REPO / rel).read_text())


class Harness(unittest.TestCase):
    def test_no_subagents_fallback_is_written(self):
        text = read("skills/qa/references/harness/README.md")
        self.assertIn("no subagents → the manager runs the roles itself", text)
        self.assertIn("no context isolation", text)

    def test_every_adapter_is_listed_in_the_readme(self):
        readme = read("skills/qa/references/harness/README.md")
        adapters = sorted(p.name for p in HARNESS.glob("*.md") if p.name != "README.md")
        self.assertEqual([a for a in adapters if a not in readme], [])

    def test_engine_update_command_comes_from_adapter(self):
        skill = read("skills/qa/SKILL.md")
        self.assertNotIn("claude plugin", skill)
        self.assertIn("then the adapter's «Updating the engine from a clone»", skill)
        self.assertNotIn("claude plugin", read("skills/qa/references/engine-edits.md"))
        generic = read("skills/qa/references/harness/generic.md")
        self.assertIn("Updating the engine from a clone No known command: commit the edit in the clone", generic)


def section(rel: str, heading: str) -> str:
    text = (REPO / rel).read_text()
    m = re.search(rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return plain(m.group(1)) if m else ""


class Browser(unittest.TestCase):
    def test_playwriter_preflight_names_the_users_action(self):
        pre = section("skills/qa/references/browser/playwriter.md", "## Preflight")
        self.assertIn("extension is not connected", pre)
        self.assertIn("do not launch the executor", pre)

    def test_the_techniques_send_the_reader_to_the_tool_adapter(self):
        text = read("skills/qa/references/browser-techniques.md")
        self.assertIn("are in browser/<tool>.md, named by the profile's browser", text)
        self.assertNotIn("[BLOCKED", text)

    def test_legacy_browser_values_read_as_claude_in_chrome(self):
        self.assertIn("default and dedicated, written before the tool was named, read as claude-in-chrome",
                      read("PROFILE-CONTRACT.md"))
        self.assertIn("default/dedicated → claude-in-chrome", read("skills/qa/SKILL.md"))

    def test_unavailable_browser_tool_falls_back_to_playwriter(self):
        skill = read("skills/qa/SKILL.md")
        self.assertIn("the profile's browser tool cannot run in this harness", skill)
        self.assertIn("Playwriter instead, said in the session's first message and in the report", skill)
        self.assertIn("the API scenarios still run", skill)

    def test_setup_recommends_playwriter_and_checks_it_live(self):
        setup = read("skills/qa-setup/SKILL.md")
        self.assertIn("Playwriter (Recommended)", setup)
        self.assertIn("the browser: through the chosen tool, open a tab and read its URL and title", setup)
        self.assertIn("the browser tool is a channel too", setup)


class ReviewFixes(unittest.TestCase):
    def test_claude_code_is_told_by_agent_or_task_and_askuserquestion(self):
        readme = read("skills/qa/references/harness/README.md")
        self.assertIn("Agent or Task with a subagent_type parameter, AskUserQuestion", readme)
        self.assertIn("task with a subagent_type parameter, skill, and no AskUserQuestion", readme)

    def test_claude_code_plugin_root_is_taken_from_the_base_directory(self):
        root = section("skills/qa/references/harness/claude-code.md", "## Plugin root")
        self.assertIn("Two directories above the «Base directory for this skill»", root)

    def test_preflight_reads_the_tool_adapter_first(self):
        self.assertIn("against the browser tool adapter's «Preflight», then the profile's checklist", read("skills/qa/SKILL.md"))
        self.assertIn("command not found", section("skills/qa/references/browser/playwriter.md", "## Preflight"))

    def test_a_bump_moves_both_manifests(self):
        self.assertIn("bump the patch version in <engine-clone>/.claude-plugin/plugin.json and .codex-plugin/plugin.json",
                      read("skills/qa/SKILL.md"))
        self.assertNotIn("bump the patch version", read("skills/qa/references/harness/claude-code.md"))
        self.assertIn(".codex-plugin/plugin.json", read("skills/qa/references/engine-edits.md"))

    def test_moved_entries_point_where_they_now_live(self):
        cic = read("skills/qa/references/browser/claude-in-chrome.md")
        self.assertNotIn("under «Your tab must be the ACTIVE one»", cic)
        self.assertNotIn("«A full id is never reconstructed» above", cic)
        self.assertIn("../harness/<name>.md", read("skills/qa/references/browser/playwright-mcp.md"))

    def test_setup_offers_playwriter_to_a_legacy_profile(self):
        self.assertIn("browser is default or dedicated → offer Playwriter", read("skills/qa-setup/SKILL.md"))


class SharedRules(unittest.TestCase):
    """A rule repeated where each reader meets it — kept in step, so an edit to one copy cannot quietly drop the others."""

    FRESH_TAB = ("skills/qa/SKILL.md", "skills/qa/references/manual-brief.md", "skills/qa/templates/2-manual-task.md",
                 "agents/qa-manual.md")

    def test_a_dead_verdict_needs_a_new_tab_for_every_recheck(self):
        self.assertEqual([p for p in self.FRESH_TAB if "every re-check" not in read(p)], [])
        brief = read("skills/qa/references/manual-brief.md")
        self.assertGreaterEqual(brief.count("every re-check"), 2)  # the index line and the entry

    def test_the_page_secret_route_is_in_every_browser_adapter(self):
        for tool in ("playwriter", "claude-in-chrome", "playwright-mcp"):
            self.assertIn("A secret captured only in the page", read(f"skills/qa/references/browser/{tool}.md"), tool)


class Manifests(unittest.TestCase):
    def test_codex_manifest_version_matches(self):
        import json
        claude = (REPO / ".claude-plugin/plugin.json").read_text()
        codex = (REPO / ".codex-plugin/plugin.json").read_text()
        self.assertEqual(json.loads(codex)["version"], json.loads(claude)["version"])
        self.assertEqual(json.loads(codex)["skills"], "./skills/")
        self.assertTrue(codex.endswith("\n"))

    def test_every_install_route_the_readme_names_exists(self):
        readme = (REPO / "README.md").read_text()
        self.assertIn("## Install", readme)
        for rel in ("INSTALL.md", ".opencode/INSTALL.md"):
            self.assertTrue((REPO / rel).is_file(), rel)
            self.assertIn(rel, readme)


if __name__ == "__main__":
    unittest.main()
