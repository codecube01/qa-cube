#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
qa_profile \
  "contract-version: 6" "tracker: none" "tms: none" "test-cases: inline" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: docs/knowledge/" "sessions: docs/test-sessions/" \
  "engine-clone: none" "language: en"
# the project's layer of engine rules: one open row, one closed row
cat > .claude/qa-cube-feedback.md <<'MD'
# qa-cube feedback — this project's layer of engine rules

Columns: observation · rule · address in the engine · plugin version. Open rows are read by every
session as additions to the engine; closed rows have arrived in the engine and are not read.

| Observation | Rule | Address in the engine | Plugin version |
|---|---|---|---|
| a retest passed because the executor reused the cart the fix was made on | a retest of a state bug starts from a freshly created object, never from the one the fix was tried on | references/manual-brief.md | 0.17.0 |

## Closed

| Observation | Rule | Address in the engine | Plugin version | Arrived in |
|---|---|---|---|---|
| a finding was filed against a task that only covered its area | «filed» only when the finding's own id appears in a task | references/report.md | 0.16.30 | 0.16.34 |
MD
