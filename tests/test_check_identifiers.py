"""Tests for .github/scripts/check_identifiers.py — the definition of a leak from a real project.

The checker guards a public repository, and it fails in two ways. It can miss a leak — a stand's host,
a client's task id, a colleague's email — and nobody notices until the engine is in somebody else's
project. Or it can fire on the engine's own prose and code, full of `a.name`, `README.md` and
`FR-1` — and then it gets bypassed with --no-verify, which costs every check at once.

So the cases come in pairs, caught and quiet, plus one test that runs the checker over every tracked
file: the engine as it stands must pass, or a new detector is too greedy.

The leaks below are assembled from fragments (`j("PAY", "-303")`), so this file carries none of them
literally and passes the very checker it tests.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / ".github" / "scripts" / "check_identifiers.py"

_spec = importlib.util.spec_from_file_location("check_identifiers", SCRIPT)
ci = importlib.util.module_from_spec(_spec)
sys.modules["check_identifiers"] = ci
assert _spec.loader is not None
_spec.loader.exec_module(ci)


def j(*parts: str) -> str:
    return "".join(parts)


def kinds(text: str) -> list[str]:
    return [f.kind for f in ci.findings(text)]


class Caught(unittest.TestCase):
    """What must be caught — one family per test, so a failure names the family."""

    def assertCaught(self, text: str, kind: str) -> None:
        self.assertIn(kind, kinds(text), f"not caught as {kind!r}: {text!r}")

    def test_tracker_ids(self):
        for text in (j("Fix per PAY", "-303"), j("see AB2", "-45"), j("billing", "#77"),
                     j("group/project", "#12"), j("merged in web", "!34")):
            self.assertCaught(text, "a tracker id")

    def test_hosts_and_urls(self):
        self.assertCaught(j("https://", "stage.client-bank", ".ru/api/v1"), "a host or a URL")
        self.assertCaught(j("the host api.orders-", "internal", ".corp answers 502"), "a host")
        self.assertCaught(j("https://github.com/", "someorg/private-repo/pull/9"), "a host or a URL")
        self.assertCaught(j("http://", "grafana.tools", ".io/d/abc"), "a host or a URL")

    def test_email(self):
        self.assertCaught(j("ask ivan.petrov", "@", "clientbank", ".ru"), "an email address")
        self.assertCaught(j("logged in as p.ivanov", "@…"), "an email address")  # the domain elided, the person not

    def test_hosts_on_less_common_tlds(self):
        for text in (j("wiki.", "northwind", ".systems"), j("status.", "northwind", ".kg"), j("docs.", "northwind", ".digital"),
                     j("northwind", ".llc")):
            self.assertCaught(text, "a host")

    def test_legal_entities(self):
        for text in (j("ООО «", "Вектор-Сервис»"), j("ОсОО ", "Бета Плюс"), j("«Пётр ", "и КО»"), j("Northwind Trad", "ers L", "LC"),
                     j("АО «", "Северный Ветер»")):
            self.assertCaught(text, "a legal entity")

    def test_ip_addresses(self):
        self.assertCaught(j("10.12", ".0.5:8443"), "an IP address")
        self.assertCaught(j("185.10", ".2.3"), "an IP address")

    def test_home_paths(self):
        self.assertCaught(j("/Users/", "ivanp/Projects/shop"), "a home directory path")
        self.assertCaught(j("/home/", "deploy-bot/.ssh"), "a home directory path")

    def test_truncated_ids(self):
        self.assertCaught(j("deviceId 9c3e7a1f", "-…"), "a truncated entity id")
        self.assertCaught(j("0x4b7e91c2", "d5..."), "a truncated entity id")

    def test_entity_ids(self):
        self.assertCaught(j("3f2b8c1e-9a47-", "4d2e-b6c0-5e8f1a2d7b94"), "an entity id (UUID)")
        self.assertCaught(j("0x9f8e7d6c5b4a", "39281706f5e4d3c2b1a09f8e7d6c"), "an on-chain address")

    def test_secrets(self):
        self.assertTrue(any(k.startswith("a secret") for k in kinds(j("AKIA", "IOSFODNN7EXAMPLE"))))
        jwt = j("eyJ", "hbGciOiJIUzI1NiJ9", ".", "eyJzdWIiOiIxMjM0In0", ".", "c2lnbmF0dXJlLXZhbHVl")
        self.assertTrue(any(k.startswith("a secret") for k in kinds(jwt)))


class Quiet(unittest.TestCase):
    """What must stay quiet — the engine's own vocabulary."""

    def assertQuiet(self, text: str) -> None:
        self.assertEqual(ci.findings(text), [], f"fired on: {text!r}")

    def test_requirement_markers_and_fictional_examples(self):
        for text in ("FR-1", "NFR-3", "AC-2", "API-1", "ACME-412", "ABC-123", "service#456"):
            self.assertQuiet(text)

    def test_standards_that_share_the_shape(self):
        for text in ("UTF-8", "SHA-256", "ISO-8601", "RFC-5737", "CVE-2024-1234", "TLS-1"):
            self.assertQuiet(text)

    def test_own_repository(self):
        for text in ("codecube01/qa-cube#1", "https://github.com/codecube01/qa-cube/releases",
                     "https://raw.githubusercontent.com/codecube01/qa-cube/main/.claude-plugin/plugin.json",
                     "from PR #1"):
            self.assertQuiet(text)

    def test_code_that_looks_like_a_host(self):
        for text in ("`m.group(1)`", "`location.host`", "`dt.date.today()`", "`user.email`", "`this.store`", "`r.status`", "`a.name`", "README.md", "plugin.json", "`window.__ids`", "`e.extensions || {}`",
                     "`location.origin`", "`crypto.subtle`", "`r.data && r.data.x`", "`blob.text()`",
                     "check_session.py", "`e.id`", "`cache.extract`"):
            self.assertQuiet(text)

    def test_allowed_and_reserved_hosts(self):
        for text in ("http://localhost:8080", "https://shop.example.com/join", "tracker.example.com",
                     "https://keepachangelog.com/en/1.1.0/", "https://img.shields.io/badge/license-MIT-blue.svg",
                     "https://anthropic.com/claude-code/marketplace.schema.json", "api.test", "host.invalid"):
            self.assertQuiet(text)

    def test_allowed_emails(self):
        for text in ("Co-Authored-By: Claude <noreply@anthropic.com>", "someone@example.com", "user@…", "login as qa@…"):
            self.assertQuiet(text)

    def test_fictional_companies(self):
        for text in ("ООО «Рога и Копыта»", "Acme LLC", "ООО «Ромашка»", "Contoso Ltd"):
            self.assertQuiet(text)

    def test_versions_and_safe_addresses(self):
        for text in ("0.17.20", "v1.2.3", "127.0.0.1", "0.0.0.0", "192.0.2.10", "203.0.113.7"):
            self.assertQuiet(text)

    def test_placeholder_paths_and_ids(self):
        for text in ("/Users/you/project", "/home/runner/work", "/home/<user>/x",
                     "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "00000000-0000-0000-0000-000000000000",
                     "0x" + "0" * 40, "12345678-1234-1234-1234-123456789012", "aaaaaaaa-…", "12345678…"):
            self.assertQuiet(text)


class Denylist(unittest.TestCase):
    """The private names — the only detector that knows real ones."""

    def setUp(self):
        self._saved = os.environ.get(ci.DENYLIST_ENV)
        os.environ[ci.DENYLIST_ENV] = "Contoso Bank, Фабрикам"
        ci._DENYLIST_PATTERNS = None  # re-read the environment

    def tearDown(self):
        if self._saved is None:
            os.environ.pop(ci.DENYLIST_ENV, None)
        else:
            os.environ[ci.DENYLIST_ENV] = self._saved
        ci._DENYLIST_PATTERNS = None

    def test_every_spelling_is_caught(self):
        for text in ("Contoso Bank", "contoso-bank", "ContosoBank", "contoso_bank", "stage.contoso.bank"):
            self.assertIn("a name from the private denylist", kinds(text), text)

    def test_cyrillic_terms(self):
        self.assertIn("a name from the private denylist", kinds("отчёт для Фабрикам"))

    def test_a_longer_word_is_not_the_term(self):
        self.assertNotIn("a name from the private denylist", kinds("contosobanking"))

    def test_a_quoted_term_is_matched_as_written(self):
        os.environ[ci.DENYLIST_ENV] = '"find-logs"'
        ci._DENYLIST_PATTERNS = None
        self.assertIn("a name from the private denylist", kinds("the find-logs skill"))
        self.assertNotIn("a name from the private denylist", kinds("find logs by trace id"))

    def test_a_star_drops_the_boundary(self):
        os.environ[ci.DENYLIST_ENV] = "fabrik*"
        ci._DENYLIST_PATTERNS = None
        for text in ("FABRIKUSDT", "fabrikdev", "fabrik-iss"):
            self.assertIn("a name from the private denylist", kinds(text), text)
        self.assertNotIn("a name from the private denylist", kinds("prefabrik"))

    def test_the_output_is_masked(self):
        shown = [f.shown for f in ci.findings("ContosoBank")]
        self.assertTrue(shown)
        self.assertNotIn("ContosoBank", " ".join(shown))


class FileScopes(unittest.TestCase):
    """Waivers are per file and per family, never wholesale."""

    def test_fixtures_keep_fake_secrets_but_not_real_ids(self):
        secret = j("AKIA", "IOSFODNN7EXAMPLE")
        self.assertEqual(ci.scan_lines(secret, "tests/test_x.py"), [])
        self.assertTrue(ci.scan_lines(secret, "skills/qa/SKILL.md"))
        self.assertTrue(ci.scan_lines(j("PAY", "-303"), "tests/test_x.py"))

    def test_only_the_exact_definitions_file_is_exempt(self):
        # a suffix match once waived the checker's own test file wholesale
        patch = "\n".join(["+++ b/tests/test_check_identifiers.py", "+" + j("see PAY", "-303")])
        self.assertTrue(ci.scan_patch(patch))
        patch = "\n".join(["+++ b/.github/scripts/check_identifiers.py", "+" + j("see PAY", "-303")])
        self.assertEqual(ci.scan_patch(patch), [])  # a shape example, waived
        patch = "\n".join(["+++ b/.github/scripts/check_identifiers.py", "+# " + j("9c3e7a1f", "-…")])
        self.assertTrue(ci.scan_patch(patch))  # a real-looking id is never an example

    def test_a_diff_is_judged_per_file(self):
        patch = "\n".join([
            "+++ b/tests/test_x.py",
            "+" + j("AKIA", "IOSFODNN7EXAMPLE"),
            "+++ b/agents/qa-manual.md",
            "+" + j("see PAY", "-303"),
        ])
        problems = ci.scan_patch(patch)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("agents/qa-manual.md", problems[0])


class HistoryBaseline(unittest.TestCase):
    """Accepted history findings are stored as hashes — the baseline must name nothing."""

    def test_the_key_hides_the_value(self):
        key = ci._baseline_key("0123abcd", "skills/qa/SKILL.md", j("secret-", "name"))
        self.assertNotIn("secret", key)
        self.assertEqual(len(key), 24)
        self.assertNotEqual(key, ci._baseline_key("0123abcd", "skills/qa/SKILL.md", j("other-", "name")))


class TheEngineAsItStands(unittest.TestCase):
    """Every tracked file passes — the regression guard against a greedy detector."""

    def test_tracked_files_are_clean(self):
        tracked = subprocess.run(["git", "-C", str(REPO), "ls-files"], capture_output=True, text=True, check=True).stdout.split()
        problems = []
        for rel in tracked:
            path = REPO / rel
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            problems += ci.scan_lines(text, rel)
        self.assertEqual(problems, [], "\n".join(problems[:20]))

    def test_the_denylist_file_is_never_tracked(self):
        tracked = subprocess.run(["git", "-C", str(REPO), "ls-files", ci.DENYLIST_FILE.name],
                                 capture_output=True, text=True, check=True).stdout.strip()
        self.assertEqual(tracked, "", "the private denylist is in git — it IS the leak it guards against")


if __name__ == "__main__":
    sys.exit(unittest.main())
