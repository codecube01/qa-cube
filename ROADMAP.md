# Roadmap

What is deliberately not built yet, and why. Nothing here is a promise — the engine grows from
sessions that went wrong, so an item stays on this list until a real round makes the case for it.

Ordered by how much of the case is already made.

## `/qa --plan` and a checkpoint on the first session

**The gap.** A session's only point of user control is the one question the manager may ask at the
start. After that it plans, launches executors, writes cases into test management, edits test code
and drafts a tracker comment. For a first run in an unfamiliar project that is a lot of trust to
extend to a plugin installed five minutes ago.

**The shape.** Not a mode threading through the pipeline — a single stop at the end of step 3, which
is where the real boundary runs: everything before it is markdown inside the project's own `docs/`,
everything after it touches outside systems. Two ways in:

- `/qa --plan <task>` — explicit, per-session, no state. The engine already has the convention
  (`/qa-day --days 7`), and the rename hook is unaffected because a flag carries no digits.
- **automatically on the first session in a project** — no session folders and no registry yet →
  stop once, then never again. This is the case the feature exists for, and `/qa-setup` already says
  as much in its closing briefing: «the first session usually uncovers a couple of holes in the
  profile». Self-eliminating, so it cannot become a permanent tax.

What the stop shows is not the plan (that is in the file) but four lines: tasks in scope, mode,
environment, and — the part that earns the checkpoint — **what will be written outside the project**:
which case in which test-management system, which test file, which task gets a comment.

**Rejected:** a profile key (`plan-approval: always|never`). It costs a contract bump and an
onboarding question, and it is the kind of key that gets set once and forgotten, so a year later
nobody remembers why the session stops.

## `/qa-doctor` — the profile and its channels, without running a session

**The gap.** Every declared tool is verified exactly once, during `/qa-setup`. What breaks between
sessions — an expired token, a moved environment, a renamed knowledge base, a secrets file that
stopped being gitignored — is discovered by a session that has already started.

**The shape.** A read-only skill that walks the profile: `contract-version` against the contract,
one reading call per declared tool, `git check-ignore` over the secrets source, existence of
`sessions` / `knowledge` / `engine-clone`. Most of the checks already exist inside `/qa-setup` step
4; this is them, addressable on their own.

## A budget for the round

**The gap.** `qa-manual` stops a scenario that resists for 30+ minutes, `qa-automator` stops after
five iterations. The analyst has no limit at all, and the manager has none for the round as a whole
— so a round can quietly spend an afternoon, which matters most on environments whose session
expires and has to be re-authenticated by hand.

**The shape.** A ceiling the manager tracks (executor launches, or wall time), a checkpoint when it
is crossed — report what the round has cost and ask whether to continue — and the number recorded in
`0-session.md` so the next round can plan against it.

## `qa_day.py --registry`

**The gap.** `<sessions>/README.md` is maintained by hand at step 8, one line per session, and drifts
from the folders it describes — a renamed folder, a verdict that changed on round 2, a session
nobody logged.

**The shape.** The digest already walks exactly these folders and reads exactly these files. A
`--registry` flag prints the table; step 8 pastes it. Cheap, and it removes a class of stale link the
monthly sweep has to fix afterwards.

## Not planned

- **A web-tester role.** Browser work belongs to `qa-manual`: a UI scenario and an API scenario
  belong to the same round, and splitting them would buy a hand-off in the middle of it.
- **Parallel executors, or a shared discoveries file.** The file scheme, the running numbering and
  acceptance all assume one executor at a time. No session has yet been short of parallelism.
- **A schema and a validator for the project profile.** Deliberately absent, and the contract says so:
  the profile's readers are agents, and what matters is that it answers the questions, not that it
  parses.
