# qa-cube

[![Release](https://img.shields.io/github/v/release/codecube01/qa-cube?label=release)](https://github.com/codecube01/qa-cube/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A QA test session, run end to end by Claude Code.** You hand it a tracker task; it plans the
round, checks the feature on your environment, files the findings, writes the autotest, delivers a
report you can paste into the tracker — and closes with a retro that edits its own instructions.

One flow, many projects: the process lives here and is improved once. Everything project-specific
— the tracker, test management, the environments, the autotests — each project declares in its own
`.claude/qa-profile.md`.

> **Not an English speaker?** The engine's own instructions are in English, but it works in **any
> language** end to end. `/qa-setup` asks for your language first and records it as `language:` in
> the profile; every session then talks to you and writes all of its artifacts — plan, briefs,
> results, report, retro, test cases — in that language, down to what the subagents narrate in the
> console while they work.

## 60 seconds

```bash
claude plugin marketplace add codecube01/qa-cube
claude plugin install qa-cube@qa-cube
```

Then, in your project:

```
/qa-setup                      # an interview: where the tasks are, where the cases go,
                               # what the environments are, what runs the tests
/qa <link to a task>           # the session runs
/qa <the same task>            # a retest: the next round lands in the same session folder
/qa-day                        # what did I test today?  --days 7 for the week
```

`/qa-setup` reconnoitres the repository first, so most of its questions arrive with the answer
already filled in. It is safe to re-run at any time.

## What you get

First, in the chat — the round at a glance, then what to do about it:

```
Round 2 on ACME-412, stage3. Verdict: bugs — one finding stands.

🟢 FR-1 — a coupon reduces the cart total by its face value
🟢 FR-3 — an expired coupon is refused, the message names the expiry date
🟡 FR-4 — the order status changes, but the operator does not see it
🔴 FR-2 — a repeated submit applies the discount twice: 4 200 → 3 400

⚪ Coupon stacking with loyalty — no loyalty accounts on the environment
⚪ Behaviour on a payment rollback — needs a day of waiting for the worker

…the findings, and the ready-made tracker comment…

⚠️ Paste the comment into ACME-412 — the profile's tracker token is read-only
💡 Create a loyalty account on stage3 and I will close coupon stacking next round
💡 Two carts named `eval-*` were left on the environment
```

`⚠️` means «I cannot close this without you» and is rare by rule — zero or one line in a normal
round. `💡` is safe to ignore. Every line is an action, not a problem.

Then, on disk — a folder per session, one report per session, a row in the registry:

```
docs/test-sessions/
├── README.md                              # the registry: one line per session
├── side-findings.md                       # bugs found outside any task's scope
├── 2026-09-14_acme-412-coupon-double/
│   ├── 0-session.md                       # tasks, mode, environment, round log
│   │                                      # + the task's raw text and comments, verbatim
│   ├── 1-plan.md                          # scenarios by priority, each with its business effect
│   ├── 2-manual-task.md                   # the brief the manual tester was given
│   ├── 3-manual-result.md                 # what actually happened: requests, responses, trace ids
│   ├── 4-automator-task.md                # the brief for automation
│   ├── 5-automator-result.md              # the test, the run log, the case link
│   ├── 7-retro.md                         # what went wrong, and where each lesson was written
│   ├── 8-manual-task-2.md                 # round 2 continues the same numbering
│   ├── 9-manual-result-2.md
│   ├── 10-retro-2.md
│   └── 99-report.md                       # one report per session, every round updates it
└── 2026-08/                               # closed months are swept into archives
```

And the report — this is the part that gets pasted into the tracker (an example, with a fictional
project and task):

```markdown
**Source:** ACME-412 · **Current verdict (round 2, 2026-09-14):** bugs — one finding stands
**Method:** API + browser, logs by trace id

## What is confirmed (matches FR/AC)

- **FR-1.** ✓ A coupon reduces the cart total by its face value *(round 2; checked on three carts)*
- **FR-3.** ✓ An expired coupon is refused, and the message names the expiry date

## Findings

| № · Priority | Requirement | Description and risk |
|---|---|---|
| **B-17 · Critical** | FR-2 (spec §4.1) | **A customer who submits the order twice is charged the discount twice — the shop loses the difference.** The spec requires the second application to be refused; the total dropped from 4 200 to 3 400 on the repeated submit. Anyone who double-clicks pays less than the order is worth, and the audit log records one application rather than two. *Tech.: POST /cart/coupon is not idempotent; trace 8f31c2, 2026-09-14* |

Fixed: B-15 · Major — the expiry message showed a UTC date to a local-time user; confirmed on round 2.

## Not covered (with reasons)

| What | Reason | Round |
|---|---|---|
| Coupon stacking with a loyalty discount | no loyalty accounts on the environment | 2 |
```

Findings are written in business language on purpose: the table is read by a developer who has
neither the session, nor the files, nor the history of the runs.

## How it works

Four roles. The manager is your main Claude Code session; the rest are subagents it launches and
waits for.

- **QA Manager** (`/qa`) — reads the task *and its comments*, pulls related tasks into scope, plans
  the round, writes the briefs, accepts the results, writes the report, runs the retro. The only
  role that ever asks you a question.
- **qa-analyst** — turns the plan's scenarios into test cases **from the requirements**, before the
  run and without seeing the environment, so that a mismatch later reads as a product defect rather
  than a sloppy case. Enabled by `test-cases: upfront`.
- **qa-manual** — checks the feature on the environment, verifies business effects rather than
  status codes, and leaves evidence solid enough to write an autotest from without re-checking.
- **qa-automator** — turns that evidence into an autotest, runs it until green, links it to the
  case and marks automation.

Projects differ, and the engine expects that: the profile declares only the capabilities that
exist, and every `none` has a documented degradation. No test management? Cases become markdown
files. No autotests? The automation step is skipped and the report says so. No tracker? The input
is your own description.

## When you don't need this

Worth saying plainly, because the setup costs an interview and every session costs tokens:

- **A project with no tracker and no environment.** The engine will run on a free-form description
  against a local build, but most of what it is good at — reading a task with its comments, finding
  the related backend task, dating a retest against the status history — has nothing to work with.
- **A one-off check.** «Does this button work» does not need a session folder, a report and a
  retro. Just ask Claude.
- **A team that wants a different process.** The engine is opinionated: one report per session,
  findings phrased in business language, a mandatory retro, a file scheme it will not negotiate.
  Much of the detail is adjustable in the profile; the shape of the flow is not.

It pays for itself where the same feature comes back for a second round, where a finding has to
survive being copied into a tracker, and where what one session learned should reach the next one.

## Wiring in a project

`/qa-setup` generates `.claude/qa-profile.md` — a capability header plus a section per capability
that points at the project's own skills instead of retelling them. The contract is
[PROFILE-CONTRACT.md](PROFILE-CONTRACT.md); the file is ordinary markdown and editing it by hand is
expected.

For a team, put the marketplace into the project's `.claude/settings.json` so it connects when
colleagues clone (each of them still installs the plugin itself — external plugins are never
auto-installed):

```json
{
  "extraKnownMarketplaces": {
    "qa-cube": { "source": { "source": "github", "repo": "codecube01/qa-cube" } }
  },
  "enabledPlugins": { "qa-cube@qa-cube": true }
}
```

A local-path marketplace works for trying the engine out (`claude plugin marketplace add <path to a
clone>`) but not for distributing to a team — it only works where that path exists.

## Structure

```
.claude-plugin/         plugin.json, marketplace.json
skills/qa/              the test-session engine: SKILL.md — the pipeline's procedure,
                        references/ — the lesson catalogues for steps 2, 3, 4 and 6,
                        templates/ — the session file skeletons,
                        scripts/check_session.py — secrets and table checks over a session's files
skills/qa-setup/        wiring a project in and updating its profile: interview → profile
skills/qa-day/          the digest of a day's (or a week's) sessions across projects: SKILL.md +
                        scripts/qa_day.py — a stdlib-only walk over the session folders
agents/                 qa-analyst, qa-manual, qa-automator
hooks/                  hooks.json + rename-session.sh — a «/qa <task>» session gets named by task number
                        (uses jq; where jq is absent the rename is simply skipped)
tests/                  unit tests for qa_day.py — run by CI
evals/                  behavioural cases for the engine itself — run by a human before a release
PROFILE-CONTRACT.md     the specification of a project profile
ROADMAP.md              what is deliberately not built yet, and why
docs/                   working design docs (not included in git)
```

## How this gets better

Every session ends with a mandatory retro. Lessons about the **project** are edited straight into
its profile, its skills and its knowledge base — they start working with the very next session.
Lessons about the **process** belong to the engine, and where they go depends on one profile key:

- **`engine-clone: none`** — the normal case for a plugin installed from the marketplace. The engine
  is read-only, so such a lesson is re-addressed to the project wherever it can be, and whatever
  stays universal is logged in `<sessions>/engine-feedback.md`. Nothing is sent anywhere and nothing
  asks you to send it.
- **`engine-clone: <path to a git clone>`** — for anyone working on the engine itself. The retro
  edits the clone, bumps the patch version in `plugin.json` and runs `claude plugin marketplace
  update qa-cube && claude plugin update qa-cube@qa-cube` (installing a plugin **copies** its files
  into the Claude Code cache, so edits do not apply without this); the update is picked up by the
  next launch of claude.

Nothing updates a plugin on its own. A session mentions in one line when the engine is behind
upstream, and `/qa-setup` is what actually updates it — and, having done so, says which of your
logged observations have since arrived in the original. If you ever want to hand the rest over, it
offers the text and a link to the issue tracker; posting it is your call, never the engine's.

Version history is in [CHANGELOG.md](CHANGELOG.md); what is deliberately not built yet — in
[ROADMAP.md](ROADMAP.md); how to propose a change — in [CONTRIBUTING.md](CONTRIBUTING.md). A release is a milestone for humans, not the delivery channel:
the marketplace clones the branch, and `claude plugin update` reads `version` from `plugin.json`,
never a tag.

## License

MIT — see [LICENSE](LICENSE).
