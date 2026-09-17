#!/usr/bin/env bash
# Shared fixture helper for the eval cases: sourced by a case's setup.sh, which runs
# (as you, with --scaffold) inside that run's workspace — the agent's cwd.
# Everything here is fictional on purpose: the engine's own no-identifiers rule applies
# to this suite too, so the project is `acme-shop` and the task is `ACME-412`.
set -euo pipefail

# qa_profile <key: value> ... — writes .claude/qa-profile.md with the given header
qa_profile() {
  mkdir -p .claude
  { echo "# QA profile of the acme-shop project"; echo; echo "## Capabilities"
    for kv in "$@"; do echo "$kv"; done
  } > .claude/qa-profile.md
}

# a minimal repository around the profile, so the project does not look empty
project_skeleton() {
  mkdir -p src docs
  echo "# acme-shop" > README.md
  echo "Checkout, coupons and password reset for a demo store." >> README.md
}
