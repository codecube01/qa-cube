#!/usr/bin/env python3
"""The single definition of «an identifier from a real project».

Used by validate-plugin.py (file contents), the git hooks (staged changes, file and branch names,
commit messages) and CI (commit messages, PR title and body, the tag). One definition, so the rule
cannot be enforced in one place and forgotten in another.

What counts as a leak — each family is a separate detector below:
  · a tracker id           ABC-123, AB2-45, service#456, group/project#12, project!34
  · a host or a URL        anything outside the allow-list: a stand, a client's repo, an internal host
  · an email address       outside the allow-list (noreply trailers, example domains), or with its domain elided
  · a legal entity         a legal form beside a name: «ООО «…»», «ОсОО …», «… LLC», «… и КО»
  · an IP address          anything but loopback and the documentation ranges
  · a home directory path  /Users/<name>/…, /home/<name>/… — it names a person and a machine
  · a real entity id       a random-looking UUID or on-chain address copied from an environment
  · a secret               the shapes check_session.py knows (JWT, cloud keys, tokens, one-time links)
  · a private name         a company, client, service or person from the local denylist

The private denylist is the only detector that knows real names, so it never lives in git: one term
per line in `.identifiers.local` at the repo root (git-ignored), and/or the `QA_CUBE_DENYLIST`
environment variable (newline- or comma-separated; in CI, a repository secret). Its hits are printed
masked — a public CI log must not publish the list it is enforcing.

Standalone use:
    check_identifiers.py --text "Fix per ACME-303"     # a message
    check_identifiers.py --files a.md b.md              # file contents
    echo "…" | check_identifiers.py --stdin
    git diff --cached -U0 | check_identifiers.py --diff  # the added lines, each under its own file
    check_identifiers.py --history                      # audit every commit message and every added line ever
    check_identifiers.py --accept-history               # baseline what is published and judged, by hash
Exits 1 and prints what it found.
"""

from __future__ import annotations

import argparse
import importlib.util
import ipaddress
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
DENYLIST_FILE = ROOT / ".identifiers.local"
DENYLIST_ENV = "QA_CUBE_DENYLIST"


class Finding(NamedTuple):
    kind: str   # which family caught it — shown to the reader
    shown: str  # what to print; masked for the private denylist


# --- tracker ids -------------------------------------------------------------------------------

# Jira-like keys (a digit may follow the first letter: AB2-45), lower-case service refs, and
# GitLab/GitHub refs with a path (group/project#12, project!34 for a merge request).
TRACKER = re.compile(
    r"(?<![\w/-])(?:"
    r"[A-Z][A-Z0-9_]+-\d+"
    r"|[a-z][a-z0-9_.-]*(?:/[a-z0-9_.-]+)*#\d+"
    r"|[a-z][a-z0-9_.-]*(?:/[a-z0-9_.-]+)*!\d+"
    r")(?![\w-])"
)
# Requirement markers, deliberately fictional examples, and standards that share the shape.
ALLOWED_PREFIXES = (
    "FR-", "NFR-", "AC-", "API-", "ACME-", "ABC-",
    "UTF-", "SHA-", "ISO-", "RFC-", "TLS-", "HTTP-", "AES-", "CVE-",
)
ALLOWED_LITERALS = {"service#456"}
OWN_REPO = "codecube01/qa-cube"


def _trackers(text: str) -> list[Finding]:
    out = []
    for m in TRACKER.finditer(text):
        value = m.group(0)
        if value.startswith(ALLOWED_PREFIXES) or value in ALLOWED_LITERALS:
            continue
        if value.startswith(OWN_REPO):
            continue  # the engine's own issues and pull requests
        out.append(Finding("a tracker id", value))
    return out


# --- hosts and URLs ----------------------------------------------------------------------------

# Hosts the engine may name. Everything else is a stand, a client, or somebody's internal network.
ALLOWED_HOSTS = {
    "localhost", "anthropic.com", "claude.com", "claude.ai", "docs.anthropic.com",
    "keepachangelog.com", "semver.org", "img.shields.io",
}
# Reserved for documentation (RFC 2606 / RFC 6761): never anybody's real host.
RESERVED_SUFFIXES = ("example.com", "example.org", "example.net", ".example", ".test", ".invalid")
# Hosts that are fine only for the engine's own repository — a client's repo there is a leak.
OWN_REPO_HOSTS = {"github.com", "raw.githubusercontent.com", "gitlab.com"}

URL = re.compile(r"\bhttps?://[^\s)\"'<>`\]]+", re.I)
# A bare host: labels plus a TLD real hosts use. TLDs that are also file extensions or code
# (.md .py .sh .rs .pl .pm .ps .ms .ml .mo .so .cc .tf .sv .am .ac .in .is .it .to .do .as .at
# .be .no .id .me .name .link .page .data) are left out on purpose — `a.name`, `README.md` and
# `row.user.id` are not hosts; such a host is still caught inside a URL or an email.
# gTLDs that double as everyday property or method names (group, host, email, store, today,
# live, work, team, company, network, media, one, top, space, shop, bank…) are left out too —
# `m.group(1)`, `location.host` and `date.today()` must stay quiet.
GTLDS = (
    "com net org info biz pro xyz online site tech dev app cloud io ai co "
    "systems digital solutions finance financial agency studio ventures consulting software "
    "llc inc ltd gmbh internal local corp lan intra intranet"
).split()
CCTLDS = (
    "ru su kg kz uz ua by tj tm ge az ee lv lt de uk us eu nl fr ch se fi dk cz sk hu ro bg rs "
    "es pt gr il tr ae sa qa sg hk jp cn kr tw vn th my ph ca au nz br ar mx cl pe"
).split()
BARE_HOST = re.compile(
    r"(?<![\w@/.-])((?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"(?:" + "|".join(sorted(set(GTLDS + CCTLDS), key=len, reverse=True)) + r"))"
    r"(?![\w-])",
    re.I,
)


def _host_allowed(host: str, path: str = "") -> bool:
    host = host.lower().rstrip(".")
    if host in ALLOWED_HOSTS or host.endswith(RESERVED_SUFFIXES):
        return True
    if host == "img.shields.io":
        return True
    if host in OWN_REPO_HOSTS:
        return path.lstrip("/").startswith(OWN_REPO) or path in ("", "/")
    return False


def _hosts(text: str) -> list[Finding]:
    out = []
    spans = []
    for m in URL.finditer(text):
        spans.append(m.span())
        parts = urlsplit(m.group(0))
        host = (parts.hostname or "").lower()
        if host and _is_ip(host):
            continue  # the IP detector owns it
        if host and not _host_allowed(host, parts.path):
            out.append(Finding("a host or a URL", m.group(0).rstrip(".,;:")))
    for m in BARE_HOST.finditer(text):
        if any(a <= m.start() < b for a, b in spans):
            continue  # already judged as part of a URL
        if not _host_allowed(m.group(1)):
            out.append(Finding("a host", m.group(1)))
    return out


# --- email addresses ---------------------------------------------------------------------------

EMAIL = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![\w-])")
ALLOWED_EMAIL_DOMAINS = {"anthropic.com", "users.noreply.github.com"}


# «a.name@…» — the domain elided, the person still named. Placeholders stay quiet.
ELIDED_EMAIL = re.compile(r"(?<![\w.+-])([A-Za-z0-9._%+-]+)@(?:…|\.{3}|\*{2,}|x{3,})")
PLACEHOLDER_LOCALS = {"user", "name", "you", "someone", "email", "test", "qa", "login", "admin", "me", "x", "xxx"}


def _emails(text: str) -> list[Finding]:
    out = [Finding("an email address", m.group(0)) for m in ELIDED_EMAIL.finditer(text)
           if m.group(1).lower().split("+")[0] not in PLACEHOLDER_LOCALS]
    for m in EMAIL.finditer(text):
        domain = m.group(1).lower()
        if domain in ALLOWED_EMAIL_DOMAINS or domain.endswith(RESERVED_SUFFIXES):
            continue
        out.append(Finding("an email address", m.group(0)))
    return out


# --- legal entities --------------------------------------------------------------------------

# A legal form with a name beside it — «ООО «Name»», «ОсОО Name», «Name LLC» — is how a real
# counterparty lands in a precedent. The engine's own fictional companies are allowed by name.
LEGAL_FORMS_RU = r"(?:ООО|ОсОО|ОАО|ЗАО|ПАО|НАО|АО|ИП|НКО|ГУП|МУП|ТОО|ЧП)"
LEGAL_ENTITY = re.compile(
    r"(?<![\w-])" + LEGAL_FORMS_RU + r"\s*[«\"„“]?\s*[A-ZА-ЯЁ][\wА-Яа-яЁё&.\- ]{1,40}"
    r"|[«\"„“][A-ZА-ЯЁ][^»\"”]{1,40}\s(?:и\s+К[Оо]|&\s*Co)\.?[»\"”]"
    r"|(?<![\w-])[A-Z][\w&.\-]*(?:\s+[A-Z][\w&.\-]*){0,3},?\s+(?:LLC|Ltd|GmbH|Inc|JSC|LLP|PLC|OOO|S\.A\.|B\.V\.)(?![\w-])"
)
FICTIONAL_COMPANIES = ("acme", "contoso", "example", "рога и копыта", "ромашка", "тест банк")


def _legal_entities(text: str) -> list[Finding]:
    out = []
    for m in LEGAL_ENTITY.finditer(text):
        value = m.group(0).strip()
        if any(name in value.lower() for name in FICTIONAL_COMPANIES):
            continue
        out.append(Finding("a legal entity", value))
    return out


# --- IP addresses ------------------------------------------------------------------------------

IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.]*\d)")
DOC_NETWORKS = [ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")]


def _is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _ips(text: str) -> list[Finding]:
    out = []
    for m in IPV4.finditer(text):
        try:
            ip = ipaddress.ip_address(m.group(0))
        except ValueError:
            continue  # 999.1.1.1 — a version string, not an address
        if ip.is_loopback or ip.is_unspecified or any(ip in n for n in DOC_NETWORKS):
            continue
        if str(ip) == "255.255.255.255":
            continue
        out.append(Finding("an IP address", m.group(0)))
    return out


# --- home directory paths ----------------------------------------------------------------------

HOME = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\+Users\\+)(?!you\b|user\b|username\b|me\b|runner\b|<)[A-Za-z0-9._-]+")


def _homes(text: str) -> list[Finding]:
    return [Finding("a home directory path", m.group(0)) for m in HOME.finditer(text)]


# --- real entity ids ---------------------------------------------------------------------------

UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
CHAIN_ADDRESS = re.compile(r"\b0x[0-9a-fA-F]{40}\b")


def _random_looking(value: str, distinct: int = 8) -> bool:
    """A placeholder repeats a few characters (aaaaaaaa-bbbb-…, 0000…) or counts (1234…); a real id is
    random, and a random hex string of this length carries both letters and digits all but always."""
    digits = re.sub(r"[^0-9a-f]", "", value.lower().removeprefix("0x"))
    return len(set(digits)) >= distinct and re.search(r"[a-f]", digits) is not None and re.search(r"\d", digits) is not None


# «<8 hex>-…» — an id shortened by hand is still the head of a real one.
TRUNCATED_ID = re.compile(r"(?<![\w-])(?:0x)?[0-9a-fA-F]{8,}-?(?:…|\.{3})")


def _entity_ids(text: str) -> list[Finding]:
    out = [Finding("a truncated entity id", m.group(0)) for m in TRUNCATED_ID.finditer(text) if _random_looking(m.group(0), 5)]
    out += [Finding("an entity id (UUID)", m.group(0)) for m in UUID.finditer(text) if _random_looking(m.group(0))]
    out += [Finding("an on-chain address", m.group(0)) for m in CHAIN_ADDRESS.finditer(text) if _random_looking(m.group(0))]
    return out


# --- secrets -----------------------------------------------------------------------------------

def _load_secret_shapes() -> list[tuple[str, re.Pattern[str]]]:
    """The shapes live in check_session.py, which guards session files; one definition for both."""
    script = ROOT / "skills" / "qa" / "scripts" / "check_session.py"
    spec = importlib.util.spec_from_file_location("check_session", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load the secret shapes from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("check_session", module)
    spec.loader.exec_module(module)
    return module.SHAPES


SECRET_SHAPES = _load_secret_shapes()


def _secrets(text: str) -> list[Finding]:
    out = []
    for what, pattern in SECRET_SHAPES:
        for m in pattern.finditer(text):
            out.append(Finding(f"a secret ({what.split(' (')[0].removeprefix('a ').removeprefix('an ')})", _mask(m.group(0))))
    return out


# --- the private denylist ----------------------------------------------------------------------

def load_denylist() -> list[str]:
    terms: list[str] = []
    if DENYLIST_FILE.is_file():
        for line in DENYLIST_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line)
    for chunk in re.split(r"[\n,]", os.environ.get(DENYLIST_ENV, "")):
        if chunk.strip():
            terms.append(chunk.strip())
    return terms


def _term_pattern(term: str) -> re.Pattern[str]:
    """«Acme Corp» also catches acme-corp, acme_corp, AcmeCorp and acme.corp. A `*` at either end
    drops that word boundary: «acme*» catches ACMEUSDT and acmedev, «*acme» catches superacme.
    A term in double quotes is matched as written (case aside): «"find-logs"» catches a skill
    name and leaves the English phrase «find logs» alone."""
    if len(term) > 2 and term.startswith('"') and term.endswith('"'):
        return re.compile(r"(?<!\w)" + re.escape(term[1:-1]) + r"(?!\w)", re.I)
    head = "" if term.startswith("*") else r"(?<!\w)"
    tail = "" if term.endswith("*") else r"(?!\w)"
    tokens = [re.escape(t) for t in re.split(r"[\W_]+", term.strip("*")) if t]
    return re.compile(head + r"[\W_]*".join(tokens) + tail, re.I)


def _mask(value: str) -> str:
    if len(value) <= 2:
        return "*" * len(value)
    return value[0] + "*" * (len(value) - 2) + value[-1]


_DENYLIST_PATTERNS: list[re.Pattern[str]] | None = None


def _denylisted(text: str) -> list[Finding]:
    global _DENYLIST_PATTERNS
    if _DENYLIST_PATTERNS is None:
        _DENYLIST_PATTERNS = [_term_pattern(t) for t in load_denylist() if re.search(r"\w", t)]
    return [Finding("a name from the private denylist", _mask(m.group(0)))
            for p in _DENYLIST_PATTERNS for m in p.finditer(text)]


# --- the definition ----------------------------------------------------------------------------

DETECTORS = [_trackers, _hosts, _emails, _legal_entities, _ips, _homes, _entity_ids, _secrets, _denylisted]


def findings(text: str, skip: frozenset[str] = frozenset()) -> list[Finding]:
    """Every leak in the text, in detector order, deduplicated. `skip` names detector families to
    leave out (by function name without the underscore) — used for test fixtures only."""
    seen: list[Finding] = []
    for detector in DETECTORS:
        if detector.__name__.lstrip("_") in skip:
            continue
        for f in detector(text):
            if f not in seen:
                seen.append(f)
    return seen


def find(text: str) -> list[str]:
    """What findings() found, as printable strings — the interface the callers had before."""
    return [f.shown for f in findings(text)]


# The definitions file must show the SHAPES it catches (a tracker id, a host, an email, a legal
# form) — those families are waived there and nowhere else. Real names, real-looking ids, IPs, home
# paths and secrets are never needed as examples, so they are checked in it like anywhere: a
# wholesale exemption once let a real device id and a real skill name sit in its comments.
DEFINITION_WAIVER = frozenset({"trackers", "hosts", "emails", "legal_entities"})


def skip_for(path: str) -> frozenset[str]:
    """Test fixtures carry fake secrets on purpose — a checker needs something to catch. Only the
    secret family is waived there, and only there; every other family still applies."""
    if path in EXEMPT_PATHS:
        return DEFINITION_WAIVER
    return frozenset({"secrets"}) if path.startswith("tests/") or "/tests/" in path else frozenset()


def scan_lines(text: str, label: str) -> list[str]:
    """Problems with line numbers, for file-shaped input."""
    skip = skip_for(label)
    out = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for f in findings(line, skip):
            out.append(f"{label}:{line_no}: {f.kind} `{f.shown}`")
    return out


# What is published or about to be: the current branch and every remote branch. Local-only refs
# (a backup made before an anonymisation, say) never left the machine and are not judged.
PUBLISHED_REFS = ("HEAD", "--remotes")

# Findings already published that cannot be taken back without rewriting a public history — kept
# as hashes of (commit, file, value), so the list names nothing. A new leak is never in it; the
# list is written only by `--accept-history`, deliberately, after the leak was judged.
BASELINE_FILE = Path(__file__).with_name("history-accepted.txt")
# Exact paths, never a suffix: `endswith("check_identifiers.py")` once waived the checker's own test
# file wholesale — its fixtures went unchecked by --diff, --history and the tree test alike. These
# files get the partial DEFINITION_WAIVER below, never a pass.
EXEMPT_PATHS = {".github/scripts/check_identifiers.py", ".github/scripts/history-accepted.txt"}


def _baseline_key(sha: str, where: str, value: str) -> str:
    import hashlib
    return hashlib.sha256(f"{sha}\0{where}\0{value}".encode()).hexdigest()[:24]


def _load_baseline() -> set[str]:
    if not BASELINE_FILE.is_file():
        return set()
    return {line.split()[0] for line in BASELINE_FILE.read_text().splitlines() if line.strip() and not line.startswith("#")}


def scan_history(accept: bool = False) -> list[str]:
    """Every commit message and every line ever added on the published refs — the audit of what
    is already out. Slow on a big repo, instant on this one. Findings in the baseline are skipped;
    with `accept`, every current finding is added to it instead of being reported."""
    raw: list[tuple[str, str, str, Finding]] = []  # (sha, where, value, finding)
    log = subprocess.run(["git", "-C", str(ROOT), "log", *PUBLISHED_REFS, "--format=%x00%H%n%B"],
                         capture_output=True, text=True, check=True).stdout
    for entry in log.split("\x00"):
        if not entry.strip():
            continue
        sha, _, body = entry.partition("\n")
        for f, value in _findings_with_values(body):
            raw.append((sha, "message", value, f))
    patch = subprocess.run(["git", "-C", str(ROOT), "log", *PUBLISHED_REFS, "-p", "--format=%x00%H", "--no-color"],
                           capture_output=True, text=True, check=True, errors="replace").stdout
    for entry in patch.split("\x00"):
        if not entry.strip():
            continue
        sha, _, diff = entry.partition("\n")
        for where, f, value in _patch_findings(diff):
            raw.append((sha, where, value, f))
    baseline = _load_baseline()
    fresh = [(sha, where, value, f) for sha, where, value, f in raw if _baseline_key(sha, where, value) not in baseline]
    if accept:
        with BASELINE_FILE.open("a") as fh:
            if not BASELINE_FILE.stat().st_size:
                fh.write("# check_identifiers.py --accept-history: published findings accepted on purpose,\n"
                         "# as hashes of (commit, file, value) — the list itself names nothing\n")
            for sha, where, value, f in fresh:
                fh.write(f"{_baseline_key(sha, where, value)}  {sha[:10]} {where}: {f.kind}\n")
        return []
    return [f"commit {sha[:10]} {where}: {f.kind} `{f.shown}`" for sha, where, value, f in fresh]


def _findings_with_values(text: str, skip: frozenset[str] = frozenset()) -> list[tuple[Finding, str]]:
    """findings() plus the raw matched value — the baseline hashes the value, never prints it."""
    out = []
    for f in findings(text, skip):
        out.append((f, f.shown if "*" not in f.shown else text))
    return out


def _patch_findings(patch: str) -> list[tuple[str, Finding, str]]:
    out = []
    current = ""
    for line in patch.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else ""
        elif line.startswith("+") and not line.startswith("+++"):
            for f, value in _findings_with_values(line[1:], skip_for(current)):
                out.append((current, f, value))
    return out


def scan_patch(patch: str, prefix: str = "") -> list[str]:
    """The added lines of a unified diff, each judged under the path of its own file — so a test
    fixture keeps its waiver and the definitions file is not judged against itself."""
    return [f"{prefix}{where}: {f.kind} `{f.shown}`" for where, f, _ in _patch_findings(patch)]


EXPLANATION = (
    "This looks like it comes from a real project. The engine is published outside the projects "
    "its lessons come from, so task ids, hosts, addresses, entity ids, secrets and the names of "
    "companies, services, clients and accounts stay out of its files, file names, branch names, "
    "commit messages, PR titles and bodies.\n"
    "Write the lesson by its mechanics instead: «precedent: a retest where the defect's "
    "symptom went stale together with the build»."
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--text", help="check this string (a commit message, a PR title)")
    ap.add_argument("--files", nargs="*", default=[], help="check these files' contents")
    ap.add_argument("--stdin", action="store_true", help="check stdin")
    ap.add_argument("--diff", action="store_true", help="check the added lines of a unified diff on stdin, per file")
    ap.add_argument("--history", action="store_true", help="audit every commit message and added line in git history")
    ap.add_argument("--accept-history", action="store_true",
                    help="add every current history finding to the baseline (after judging them — they are published)")
    ap.add_argument("--label", default="input", help="name to show for --text/--stdin")
    args = ap.parse_args()

    problems: list[str] = []
    if args.text is not None:
        problems += [f"{args.label}: {f.kind} `{f.shown}`" for f in findings(args.text)]
    if args.stdin:
        problems += [f"{args.label}: {f.kind} `{f.shown}`" for f in findings(sys.stdin.read())]
    if args.diff:
        problems += scan_patch(sys.stdin.read())
    for path in args.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                problems += scan_lines(fh.read(), path)
        except (OSError, IsADirectoryError):
            continue
    if args.history:
        problems += scan_history()
    if args.accept_history:
        scan_history(accept=True)
        print(f"history findings accepted into {BASELINE_FILE.name}")

    if problems:
        print("✘ identifiers from a real project found:\n", file=sys.stderr)
        for p in problems:
            print(f"  · {p}", file=sys.stderr)
        print(f"\n{EXPLANATION}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
