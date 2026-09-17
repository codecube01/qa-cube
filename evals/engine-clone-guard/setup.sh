#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
# engine-clone points INTO the plugin installation — the trap the guard exists for
qa_profile \
  "contract-version: 5" "tracker: none" "tms: none" "test-cases: inline" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: docs/knowledge/" "sessions: docs/test-sessions/" \
  "engine-clone: ~/.claude/plugins/cache/qa-cube/qa-cube/0.11.16" "language: en"
