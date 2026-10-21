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
    text = re.sub(r"[*`_]", "", text)
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
