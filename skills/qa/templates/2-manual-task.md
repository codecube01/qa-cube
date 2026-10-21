# Task brief: manual round

## Context

<one paragraph: what the feature is, link to the task, what was fixed>

## Environment

- Output language: <language from the profile — everything you write and narrate goes in it>
- Env: <env>
- Requirements: spec-grade | draft — <one-phrase rationale>
- Cases (with `test-cases: upfront`): <case ids from the analyst; those are what we run>
- Environment state: `<sessions>/environment-state.md` — the snapshot for the sanity check (or «none yet»)
- Documentation: <paths in the project knowledge base relevant to the task>
- QA findings: <paths to findings from past sessions, if the section has any>

## Entry state (as of <HH:MM, date> — a dated hypothesis, not a fact: work from the actual state, with a note in the result)

- Instance / profile id: <the id of the browser profile, instance or device — never its caption, never a tab id; «if the tool moves you
  elsewhere, select this id back»>
- Identity oracle: <the call that answers who is logged in>; a «dead» verdict is believed only from a FRESH tab — new tab → navigate → the call
- Who is logged in: <account · organisation / tenant · role> — your first move is to open your own tab and check WHOSE session this is, not
  whether one is alive: a live session under someone else's role turns its refusals into «the result of a permissions check»
- Role for this round's operations: <the role the operations need — permissions differ between roles that log in identically, and the wrong
  one costs the one-time artifact>
- Carriers: <browser session: who, as of when · scripted session (cookie jar / token file): who, as of when — independent: one's liveness
  proves nothing about the other; where the scripted one dies faster, re-enter it right before a script run; a helper you hand over prints
  the body to stdout and the status code and trace id to stderr — one that prints the body alone sends the executor off to write a wrapper>
- On a refusal: <ONE environment pinned — stop and the pause protocol, no probing elsewhere | sweep the candidates with the identity oracle,
  most-recently-connected first, the interactive handshake last>
- Values the round depends on: <the accounts, the path, the flag — pasted here, not «in the file»; a claim about a file's or a config's
  contents is made after reading it, never from the copy already in context>
- Requirements read as of: <the timestamp of the last comment read — a launch that comes after a wait on the environment re-reads the thread first>

## Retest (round 2+ — delete the section on a first round)

- Build fingerprint: <how it is read — the bundle hash, the deploy ref, the image version; taken FIRST, repeated as the LAST action, and again
  right after any anomaly (data vanishing, sessions dropping, 5xx on a healthy endpoint) and before a UI finding is written down; «development must confirm the fix is in the build» is
  a full answer, silence is not>
- Matching versions prove nothing: <the one behavioural probe of the previous round's sharpest finding — the blocked page, the failing
  operation, the wrong field — before a single measurement is inherited; a server can be redeployed under the same reported version>
- Fix scope, verbatim: <what the team accepted — the retest verdict is passed on THIS; verify both, report them apart: the same outcome by
  another route or layer is a NEW finding with its own id, usually side findings, never «the fix did not work»; inputs the fix's own
  condition leaves out (a type, a role, a state) are the SAME finding, partially fixed>
- Previous round's verdicts, line by line (not the gist — without «was: pass» a regression cannot be told from a long-standing defect):

  | Requirement | Was | Finding | Value as quoted | Now, per recon |
  |---|---|---|---|---|
  | <FR-3> | pass / fail / partial / not covered; for a fail — what ALREADY held in that round (its control), or the executor reports old behaviour as «narrowed» | <id or —> | <`RAW_ENUM` sends / «Caption» shows — say which one you hold> | <fixed / remains / unknown> |

- What remains: <what recon shows still unfixed — named here it comes back as a separate finding, unnamed it comes back as a doubt>
- Already filed on these surfaces: <finding ids from the session reports and the side-findings registry — this task's and the neighbours' —
  on the header, the shared formatter, the pass-through text the round will meet>
- Forbidden for the duration of a check: <operations that re-synchronise the same state through another path (a neighbouring write that
  refreshes the whole record) — the fresh action is the TARGET operation alone>
- After a calendar wait: <first read the OBJECT — its state and its last-modified — never the process's history first; sweep the whole
  waiting interval for whatever else touched it>
- Fresh carrier: <where the defect lives in a value WRITTEN AT THE MOMENT OF AN EVENT (a failure text, a snapshot), the old record confirms
  nothing either way — the route to a fresh instance of the failure on this build, and what the old record still shows is a residue for the
  team, not a verdict>
- Stale evidence: <the previous result file opens with «⚠️ the contract changed on <date>: <was> → <now>, the current one is <file>» — or
  «none, the contract holds»>
- Verdict artifact: <the file, the record, the callback the verdict rests on — never an intermediate UI state; the observation path itself is
  checked alive first, a symptom goes stale with the build>
- Substituted responses: <where the finding is about the client's REACTION to a refusal (logout, retry, rollback) — the response to substitute
  on the client side, the real refusal once as the control — or «n/a»>

## Recon facts (what the manager measured — one row per fact, the value itself, never a retelling)

| Fact (the value) | Kind | Source | Taken on | Boundary: what was examined, through which channel | Refuted by |
|---|---|---|---|---|---|
| <`POST /v2/orders`, TTL 600 s, the field's value on the sampled record> | contract value | probe call / introspection | <date, build> | <endpoints, records, keys examined> | — |
| <the row menu has three items> | composition — confirm by looking | bundle / localisation map | <date, build> | <chunks searched> | a screen that differs is a result, not a discrepancy to reconcile |

Kinds, each with what its row must add:
- **contract value** (a limit, a path + method, an operation name, a dictionary) — the number, verified by one probe call; an endpoint found only in docs
  and not probed is marked `unverified`;
- **composition of the interface** (controls, columns, row actions) — a string in the bundle proves a string exists, not that a component renders it;
- **field-name oracle** (a pair whose NAMES promise the distinction: requested/actual, original/current) — a hypothesis, never the primary oracle;
  «if the two hold one value, the oracle is dead, do not interpret it»; a mechanism-based oracle (a recomputation, a categorical switch) goes first;
- **identifier scheme** (`<prefix>-<entity id>`, a file named after the account) — a convention read off objects created before <date>; the object's
  own id field is the address, the scheme is the fallback; «not found» means the address is wrong, not the object absent;
- **bundle excerpt** — the fragment with its identifiers as they appear, never its reconstructed meaning; a LOWER bound on what the product does
  («one carrier found» is a floor to extend, «none found» is your ignorance, not the product's absence);
- **client artifact: names only** (a query document from a captured request or a generated client) — composition is exact, types are unknown;
  never «can be relied on»; an independent introspection is the executor's first step;
- **mechanism** («this path does not go through the outbox») — from the knowledge base, dated by the BUILD it was measured on; «if the behaviour
  differs, the knowledge base is stale and that is a result»;
- **state / count** («in state X», «free remainder 0», «observations 4/4/3») — dated to the minute, with the window, the filter and the page;
  «re-check that the precondition still holds; if not — do not bend it, look for a direct discriminator and say so»;
- **negative** («nothing of that kind here») — a property of the places looked, in the terms the executor will look in (the screen's columns,
  not the response's keys), plus the channel;
- **ids of a short-lived contour** (an adjacent system's object and its counterpart) — collected while that session lives; a name is not a lookup key there.

A row without a value is not a fact — it goes to «Open hypotheses». A state older than the build is re-measured before anything rests on it.

## Open hypotheses (what the manager did NOT verify — a question with its stake, never a fact, a verdict or a menu of answers)

| Hypothesis | Why it matters (what it closes) | What settles it | From outside? |
|---|---|---|---|
| <is there an object in state X on the environment?> | <closes requirement Y> | <the aggregate query> | yes |
| <the block in this response is produced by the reworked method> | — | nothing the product exposes | no — spend no calls; measure <the observable consequence> instead |

The wording that keeps a row a question:
- a claim about the environment's state — «is there an object in state X? it would close Y», never «there is none, record it as not covered»;
- a doubt about an instrument — «check whether it can do X; if it can, that closes Y», never «if there is no such setting, record it as not covered»;
- a seeding route you have not run — «as far as I know this route yields …; I have not run it — if it does not, the question is what else produces this state»;
- a link between two records made by TIME — «matched by time only — the join by id is the question»;
- the shape of the fix — «the marker not being found is not a verdict; verify by behaviour»;
- the fixer's correction to the previous round's description, or the team's claim about the environment — quoted verbatim, attributed, with the
  observation that settles it; the measurement is the verdict, the author's account is not;
- a hypothesis nothing outside the product can settle — marked so, no attempt expected, replaced by its observable consequence;
- a probe's expected outcomes — illustrations only, closing with «any other outcome is also a result, and a third one is more valuable than either».

## Sanctioned probe (a mutation the user authorised — one block per probe; delete the section otherwise)

- Probe: <the call, the object, the hostile value(s), what the permission said>
- Read channel for the effect: <alive, proven by <a read the manager took at planning> — a probe whose oracle recon already showed dead is not sanctioned; it is deferred with its carrier recorded>
- Who presses: <the executor — a reversible step | the user, through the pause protocol | the manager, in its own session — an IRREVERSIBLE step is never the executor's; the sanction question already said who>
- Combining hostile values: <allowed into one artifact if each stays identifiable in the output; one failing the operation → unwind into separate probes | not allowed>
- Unanticipated refusal: <names the cause literally → the response proves the mechanism, no control; generic → one control call with <a value known to resolve> is authorised, leaving <residue>>
- Overshoot cap: <exceed the available amount by the smallest amount that still proves the guard is gone>
- Reverse: <works | known not to work — the stuck value is the expected artifact and the evidence; record it under environment artifacts, not as a protocol failure>
- Budget unit: <one pair of mutations per PROPERTY to be shown, on the same object, each reversed before the next; restorations count>
- A process the probe starts: <not terminated by you — record its id, state and attempt count at the end of the round; the report hands the decision to the team>

## Budget & limits (delete a line that does not apply)

- Expendables (the instances the round burns — sessions, accounts, one-time artifacts; a sanctioned probe's mutation budget is its
  «Budget unit» line above): <N = the minimum per scenario + 1 for the control of an outcome the plan did not foresee + 1 for an environment transient;
  the unit is what is actually spent (not «activations» if an activation spends nothing); a restoration spends the same budget; recompute
  against the facts and say so in the result>
- Control instance: <the one session / application / account set up as the control and only polled rarely — every experiment runs on a
  separate instance>
- Waits over an hour: <observations may run in parallel on isolated environments (profiles, contours): yes / no — «one session at a time»
  forbids a login over a live session, not two isolated environments>
- Amount cap: <the cap, with the platform's fee or the minimum viable amount beside it; where the cost is paid BEFORE the refusal (a
  signature, gas, a one-time token) — no figure: «measure the fee across a few amounts, take the smallest that leaves a positive result,
  record it»>
- Neighbouring contour (another environment, account, closed network): <ask through the manager for <one phrase> | record an open question
  and move on>
- Reference values (cryptographic constants, test vectors, test addresses): <take them from public sources per <standard>, cite the source>
- Window and focus (an appearance round, the user's own environment): <resizing allowed: yes / no; the focus is never taken
  programmatically — record the degraded channel, switch to the non-interactive part, re-check later, escalate; the user does not work in this
  environment until the round ends>

## What to read (targeted, not everything)

- <profile subfiles this task needs: e.g. `.claude/qa-profile/auth-and-api.md` §1, §3>
- <KB files/sections for the task's domain>
- The engine's shell pitfalls: `<absolute path>/skills/qa/references/shell-pitfalls.md`
- The engine's executor catalogue: `<absolute path>/skills/qa/references/executor.md` — the Contents whole, one entry per fired line
- <a browser round: the engine's techniques, `<absolute path>/skills/qa/references/browser-techniques.md` — the first screen + §<the sections this task needs>>
- <a round with API requests: `<absolute path>/skills/qa/references/api-techniques.md` — the first screen + §<the sections, «GraphQL» only for a GraphQL API>>
- The remaining profile subfiles — only when stuck.
- <a session that may die in minutes: split this list into «Before the session-bound steps» (only what those steps cannot be run safely
  without) and «After them» — `manual-brief.md`, «The order of the scenarios is the order of what DIES WITH THE ACCESS»>

## Pause protocol (a step needs the user's own hands, or the round logs in through the browser — delete the section otherwise)

The executor prepares everything up to the step (forms, interceptors, **a recorder of the state the pause is about, armed BEFORE the
request goes out**, every entry written to storage that survives a navigation), appends to the result, and ends its turn with a request
message opening with `CLICK NEEDED:` (the marker the manager greps the result for, with `LOGIN NEEDED:` from the last line below); the manager relays it and returns the user's answer by a direct message to the same agent. The request line carries, every time:

- Environment: <browser profile / instance id — the id, never its label — then the tab and the button; a tab id alone means nothing outside the executor's own group>
- Account to type: <the exact handle — a pre-filled login form may hold a neighbour's>
- What the step does TO THE STAND: <amount, recipient, which entity changes>
- Kind of window: <a free, reversible signature | an irreversible transaction, with its fee>
- Network allowed: <the one network on which confirming is allowed; a window on any other — reject, whatever it would prove>
- Boundary instead of a value: <«click at any value up to X, above that — do not click», when the on-screen value is computed live>
- Window in time (a click timed against a running multi-step operation): <an absolute clock window, anchored at the observed start of the
  step before it — plus the SHORTEST observed step duration for «during step k», the LONGEST for «after step k has finished»; never the
  mean, whose spread puts the click a step early or late; the sizing rule — `planning.md`, «When the fixture the round needs IS a stuck
  state», its rider on several observations in one window>
- Do not reload the page; do not work in this environment until the round ends
- Expected answer: one word («done» / «clicked») — the executor re-reads the state itself; ask for at most 1–2 concrete VALUES
- Wrong click (confirmed where cancel was asked): <recorded as a fact; the scenario is replayed only if the stand was affected>
- A second window (signature → send) cannot be merged into one request: announce it in advance, the user stays at the keyboard
- Identity fallback (a round that logs in through the browser): <first the manager — the executor ends its turn with «LOGIN NEEDED: <account>», the manager logs in from its own session and confirms the identity; only if that is refused too — «the user logs in as <account> in <environment>»; ready for every switch however many passed before; an irreversible step observed under that identity waits until it is in place>

After the pause the executor re-reads the actual state and the tab list (ids die), checks WHOSE session came back, compares the page's
load time with the recorder's last entry and re-arms it; the state wins over the answer, with a note in the result. The environment may be
gone on return (browser closed, logged out, a pause of a day) — re-create the preparation, replay nothing already accepted; only the
session died while the page still holds an unsaved artifact — re-enter in a separate tab of the same profile, never navigate or reload the
prepared page.

A result visible ONLY to a human (a chat message, an email, a screen with no API): state the expectation as numbers BEFORE the observation
(«one message, six items, order A→B→C»), mark which points the executor can obtain without the human (an orchestrator history, a job's
payload, a delivery log), and write the limit of confidence («confirmed in aggregate, per-item timestamps not taken»).

## Scenarios

Order ≠ priority: the plan's scenarios (`1-plan.md`) in execution order — steps 0–1 first, then the non-mutating reads, then the
mutations, on the round's own fixture only. Where the access is unstable, the «Session-bound» column overrides that: the whole
session-bound block, its mutations included, as a batch while the session lives, the independent contour after it, the identity oracle
before each block; and where the session may die in minutes, the reading list above is split the same way — before the session-bound
block only what it cannot run safely without, the rest right after it.

| # | Scenario | Expected effect + channel | Fixture | Acting identity | Session-bound | Closable alone | Disarm after |
|---|---|---|---|---|---|---|---|
| 0 | The refuting check: <the source of truth that would invalidate the round's central hypothesis — the contract file, the schema, the declared route table — read for <the fact>> | <confirmed → go on; refuted → stop, the plan is rebuilt> | — | <who, or — for a file read locally> | <yes / no> | yes | — |
| 1 | The batch snapshot into the result file: <the contract, the population, reference numbers per filter value, samples, anchor ids; a bulk source is dumped ONCE and queried locally> | <the file holds …> | — | <who> | yes | yes | — |
| N | <scenario> | <never a code alone: what changes and where it is seen — the record, the journal, the receiver, the log line> | <a selection criterion on the OBSERVED object, a value only as an illustration; a foreign entity: <id, verified <date>, or where to collect it in the other contour's snapshot pass>> | <role + exact account handle; «who am I» against the API under test before the target call> | yes / no | yes / depends on <the executor's own limit> | <the shared fixture — a rule, a price, a flag — disarmed the moment the decision it steers has been taken; re-armed explicitly where a later scenario needs it> |
| N+1 | After the negatives: the journal / audit log for the run's window — <what each refusal was recorded as; each refusal's text, whole> | <nothing recorded as performed; the texts quoted> | — | <who> | <yes/no> | yes | — |

## Deliverable

- Write to: `3-manual-result.md` (incrementally, after each scenario)
- Mandatory: a trace id for every failure (if the project defines one — with `logs: none` there is none), severity for bugs, one screenshot in `screenshots/` per frontend candidate and none for anything else (`📎` on its line), exact request/response evidence (the autotest is written from it), case `<TMS case>` in the «Summary» (with `test-cases: none` there are no cases — write «cases are not maintained in this project» instead of an id), the «Product findings» and «Executor retro» sections
- With `test-cases: upfront` do not create cases. Do not edit the expected result of a case whose expectation source is `spec` — a mismatch is recorded as a defect; a case sourced from an `assumption` or the `KB` is refined against the facts. Steps and preconditions are always refined.
- As separate lists in the result: **case corrections** (`case → was → now → why`) and **case candidates** (a scenario surfaced with no case behind it — do not create it yourself).
