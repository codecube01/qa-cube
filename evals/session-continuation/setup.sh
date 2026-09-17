#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../fixture.sh"
project_skeleton
qa_profile \
  "contract-version: 5" "tracker: none" "tms: none" "test-cases: inline" \
  "environments: local" "logs: none" "autotests: none" "browser: none" \
  "secrets: none" "knowledge: none" "sessions: docs/test-sessions/" \
  "engine-clone: none" "language: en"
cat >> .claude/qa-profile.md <<'MD'

## Environments — local only: `./run.sh` starts the store on http://localhost:8080; no credentials are needed
MD
printf '#!/usr/bin/env bash\necho "acme-shop on :8080"\n' > run.sh && chmod +x run.sh

# A session for the same task from an earlier round THIS month — the monthly sweep is a
# different rule with its own case, and a fixture that triggers it would make this case
# measure two things at once (and run out of turns doing it).
d="docs/test-sessions/$(date +%Y-%m)-01_acme-412-coupon-double"
mkdir -p "$d"
cat > "$d/0-session.md" <<'MD'
# Session: ACME-412 coupon applied twice

- **Tasks:** ACME-412
- **Mode:** full cycle
- **Environment:** local
- **Status:** bugs

## Round log

| Round | Date | Trigger | Outcome |
|---|---|---|---|
| 1 | (round 1) | initial check | the discount is applied twice on repeated submit |
MD
cat > "$d/99-report.md" <<'MD'
# Report: ACME-412 coupon applied twice

**Current verdict (round 1):** bugs — the coupon is applied twice on a repeated submit.
MD
