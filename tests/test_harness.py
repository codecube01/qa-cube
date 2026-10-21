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


if __name__ == "__main__":
    unittest.main()
