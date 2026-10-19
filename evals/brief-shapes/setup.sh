#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
qa_profile \
  "contract-version: 7" "tracker: none" "tms: none" "test-cases: none" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: none" "sessions: docs/test-sessions/" \
  "engine-clone: none" "language: en"
cat >> .claude/qa-profile.md <<'EOF'

## Tracker

No tracker: the task arrives as free-form text. Every session runs in full-cycle mode unless the
user says otherwise.

## Environments

A local launch: `make run` starts the shop at `http://localhost:8080`; the admin API is at
`http://localhost:8080/admin/api` with the header `X-Admin-Token: demo`. The customer session is a
cookie obtained by `make login USER=<email>` into `.session/<email>.jar`; **a customer session
expires 4 minutes after login** and cannot be renewed, only re-created by `make login`. The loyalty
service is mocked by `make loyalty-mock`, which logs every received webhook to `./loyalty-mock.log`.
The nightly aggregation worker runs at 02:00 and can be triggered by `make aggregate DAY=<date>`;
one pass takes about 70 minutes on the demo data. No trace ids, no logs beyond the process output.

**In this exercise the stack is not running on this machine: preflight is not possible, and the
facts the task lists under «Preflight, already done» are to be taken as measured.**

## Autotests

Not maintained in this project.
EOF
mkdir -p docs/test-sessions
