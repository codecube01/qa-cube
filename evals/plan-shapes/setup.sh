#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
qa_profile \
  "contract-version: 7" "tracker: none" "tms: none" "test-cases: none" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: none" "sessions: docs/test-sessions/" \
  "engine-clone: none" "language: en"
# The sections the session reads at steps 1–4: enough that nothing stops to ask, nothing more.
cat >> .claude/qa-profile.md <<'EOF'

## Tracker

No tracker: the task arrives as free-form text. Every session runs in full-cycle mode unless the
user says otherwise.

## Environments

A local launch only: `make run` starts the shop at `http://localhost:8080` with the demo database
(`make seed` reloads it). The admin API is at `http://localhost:8080/admin/api` with the header
`X-Admin-Token: demo`. The loyalty service is mocked by `make loyalty-mock`, which logs every
received webhook to `./loyalty-mock.log`. The previous build is available as `make run-previous`
on port 8081. No trace ids, no logs beyond the process output.

## Autotests

Not maintained in this project.
EOF
mkdir -p docs/test-sessions
