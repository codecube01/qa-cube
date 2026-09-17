#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
qa_profile \
  "contract-version: 5" "tracker: none" "tms: none" "test-cases: inline" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: none" "sessions: docs/test-sessions/" \
  "engine-clone: none" "language: ru"
