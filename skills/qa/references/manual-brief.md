# Briefing and running the manual round

Read at step 4 of `../SKILL.md`, before writing `2-manual-task.md`; the «Accepting the result» and «the control does nothing» groups are read again when
the result comes back. Each entry is a situation the round can land in and the line in the brief that costs nothing to write and a whole pass to
omit; the precedent that closes an entry is what paid for the rule. **The «Contents» below is read whole, and it is the rules** — one line
per entry, the trigger and what the brief carries; the brief is written from that list and the template's slots, and an entry's body is
opened for its mechanism and its precedent only when its line fired — that entry alone, by `grep -n` for its first words and a `Read` of
~25 lines from there, never the file without a `limit`. After the brief is written, a reviewer with no context from the session reads the
bodies against it (`../SKILL.md`, step 4): an executor is briefed once, and the situation you did not foresee is the one that reader finds.

## Contents

**Every line below is the rule: a trigger, then what the brief carries or the manager does.** Single entries first, then the
**families** — one mechanism with its shapes under it; a shape is only readable through its head. Where a line names a slot, the slot
is in `templates/2-manual-task.md`.

**Preflight and access**

- access the product issues from inside itself (an API key, a service token, a test tenant) → the manager issues it at preflight, puts it in the profile's `secrets` source, and the brief gets a contour that does not depend on a short session
- a state created by preflight (a blank, a session) → the «Entry state» section: its owner and its time («as of HH:MM it was …»), the profile's id as the only address (never a tab id, never a caption), and the executor's first move is to check WHOSE session they are in, not whether one is alive
- a config edit made in the same session → does not reach the executor's context: the values go into «Values the round depends on», and any claim about a file's contents is made after reading it
- an adjacent system with short-lived access → preflight hands over its entity IDs, not only their state (a «Recon facts» row of kind «ids of a short-lived contour»)
- the name you gave an environment may never reach the executor's listing → the address is an id; where the tooling exposes no id either, the «On a refusal» slot names the identity oracle to sweep the candidates with, most-recently-connected first, the handshake last; where the user can re-enter quickly, pin ONE environment and make a refusal a stop, not a search
- entering the environment needs a human → the liveness oracle is the session's FIRST call, before reading anything; a «dead» verdict is believed only from a fresh tab
- each entry spends a one-time artifact (a login link, a code) → choose the role the operations need and probe the existing session first; a scripted and a browser session are independent carriers, an identity per carrier (the «Role» and «Carriers» slots)
- preflight proves the session → open the round's TARGET screen too, and compare the address you land on with the one you asked for; a redirect you explained to yourself is a question for the executor, not noise
- the manager's recon → verifies the ADDRESS (path, method, headers, the selection criterion) and stops at the first response that proves it; running the scenario is the executor's work; the VALUES the probe returned are handed over as «Recon facts» rows
- access refused on every host of the environment, even without cookies → suspect the browser profile (its egress), not the environment; compare the external IP from the tab and from the shell; which profiles work goes into the project profile and the brief, asked once
- a browser-native auth dialog (basic auth) → invisible to the extension, no navigation passes it: on the first symptom (an unparseable-URL error, a CDP timeout, an error page in frame 0, a new-tab address after navigation) ask the user for the entry; the same wall MID-run gets a new tab and one retry first
- preflight finds the environment in the WRONG state → ask whether that state is itself one of the scenarios, and capture it BEFORE fixing it, saying who produced the artifact, when, and that it is not to be replayed
- the scenarios are about an entity's states → one recon request answers whether an instance of each state exists on the environment; «all in one state» turns half the plan into substituted reads, and that is the manager's call
- the order of the scenarios → the order of what DIES WITH THE ACCESS (the «Session-bound» column): a batch capture into the result file within the first few calls, the interactive part under a periodic access check; the session-bound contour's interactive scenarios outrank the independent contour's snapshots; the reading list is split the same way; a bulk source is dumped ONCE and queried locally
- the waits in the brief exceed an hour → the «Waits over an hour» slot says whether isolated environments may run in parallel
- a hypothesis about flakiness or survivability → the «Control instance» slot (one instance, polled rarely, experiments elsewhere) and the «Expendables» slot (minimum per scenario + 1 control + 1 transient, the unit is what is actually spent, restorations count)
- a round about appearance in the user's own environment → the «Window and focus» slot settled at preflight: resizing yes/no, the focus never taken programmatically, the user does not work in the environment until the round ends
- the launch comes after a WAIT on the environment → re-read the task's thread in the same breath as the launch (the «Requirements read as of» slot)

**What goes into the brief**

- a scenario parameter that depends on the environment's data → the «Fixture» column carries a selection criterion anchored on the OBSERVED object, never a value; the discriminating fixture (the owner whose records differ from the majority) is named by the same query
- a fixture that changes shared behaviour → the «Disarm after» column: disarmed the moment the decision it steers has been taken, not in the final cleanup; re-armed explicitly where a later scenario needs it
- which scenarios the executor can close alone → the «Closable alone» column, and the closable ones go first
- `test-cases: upfront` → the brief carries the case ids and the verdict on the requirements; an expected result sourced from `spec` is untouchable, one from an `assumption` or the `KB` is refined against the facts; steps and preconditions are always refined
- a check able to REFUTE the round's central hypothesis (a contract file, a schema, a route table) → scenario 0 of the table, never the tail of the reading list
- a profile rule the executor breaks before it reaches the paragraph that states it (what to open files with, what to read first) → duplicated as the first line of the reading list
- a scenario whose expectation is a RESPONSE CODE → the «Expected effect» column adds «and what actually happened», with the channel that shows it, even where the requirement is only about the code
- after negative permission probes → the table's last row reads the journal for the run's window: what each refusal was recorded as, each refusal's text whole
- the scenario may run into a neighbouring contour with a different entry → the «Neighbouring contour» slot: ask through the manager for <one phrase>, or record an open question and move on
- the scenario needs reference values (constants, vectors, addresses) → the «Reference values» slot: from public sources per <standard>, source cited
- a negative that needs someone else's entity → a concrete identifier in the «Fixture» column, found and verified by you; or where to look AND to collect it during the other contour's snapshot pass
- a step performed «under another role» → the «Acting identity» column is a role plus the exact account handle, and the step begins with «who am I» to the API under test, printed into the result before the target call
- a compound requirement («and») → the brief requires a third verdict, partial, with the breakdown of which half passed
- the scenario needs the user's own click mid-run, or the round logs in through the browser → the template's «Pause protocol» section, filled in; the manager reads every request before relaying it and returns the answer by a direct message to the same agent; the pauses are grouped into series, forms filled in only while the user is available
- after recon nothing is left that can be done by hand → do not launch the executor: file the recon as `<N>-recon-<source>.md` and say in the report why there was no manual run
- **What you have not checked yourself is handed over as a question** — the «Open hypotheses» table, a question with its stake, never a fact, a verdict or a menu: a claim about the environment → «is there an object in state X? it would close Y» · a doubt about an instrument → «check whether it can do X; if so, that closes Y» · a seeding route you have not run → «as far as I know it yields …; if not, what else produces this state» · a link between two records joined by TIME → «matched by time only, the join by id is the question» · a hypothesis about the shape of the fix → «the marker not found is not a verdict, verify by behaviour» · the fixer's correction to your previous description, or the team's claim about the environment → quoted and attributed, the measurement is the verdict · a hypothesis nothing outside the product can settle → marked so, no calls, replaced by its observable consequence · a list of expected outcomes → illustrations only, «any other outcome is also a result»
- **A sanctioned mutating probe: what the permission must also say** — the «Sanctioned probe» block answers in advance what the executor would otherwise decide mid-probe: is the read channel for the effect alive → asked before the sanction, a dead oracle defers the probe with its carrier · who presses an irreversible step → the user through the pause protocol or the manager, never the executor · may the hostile values be combined → yes if each stays identifiable, unwound on a failure · an unanticipated refusal → a literal cause needs no control, a generic one authorises one control call with a value known to resolve · an overshoot → capped at the smallest amount that proves the guard is gone · a reverse already known to be missing → declared, the stuck value is the expected artifact · the budget's unit → the PROPERTY being demonstrated, not the round · a background process the accepted probe starts → not terminated, its id and state recorded
- **What a recon fact may claim** — a row of the «Recon facts» table: the value, its kind, its source, its date, its boundary: a value, not a retelling → the numbers themselves, and «is the fix deployed» by a grep of the served bundle · an endpoint → path and method verified by one probe, or marked unverified · dated, with the boundary of the sample → state re-checked, counts with their window, a mechanism dated by the build, a negative naming the places looked · contract values are fact, the composition of the interface is a hypothesis → confirm by looking · a field-name oracle → a hypothesis, never the primary · a minified excerpt → the fragment, never its meaning, and a LOWER bound on what the product does · an identifier scheme → a convention; the object's own id field is the address · a client query document → names only, types unknown, never «can be relied on»

**A retest round** — the template's «Retest» section, filled in

- the build's fingerprint → an item of the brief, taken first, last and after any anomaly; a negative («development must confirm the fix is in the build») is a full result, and acceptance requires the version the run exercised; «nothing has changed» is a claim it cannot establish — one behavioural probe of the previous round's sharpest finding does, before any measurement is inherited
- a round resuming after a calendar wait → read the OBJECT and its last-modified first, never the process's history; sweep the whole waiting interval
- a retest → check that the observation path itself is still alive, and rest the verdict on the final artifact, never an intermediate UI state
- the finding is about the client's reaction → retest on substituted responses, the real refusal once as the control, not on expendables
- the retest verdict → scoped to what the FIX was asked to do, quoted verbatim; a defect beyond that scope is a new finding with its own id
- a previous finding quoted into the brief → say whether each value is a raw enum or a caption on screen
- what recon says is fixed → write out «what remains» too; it comes back as a separate finding, not a doubt
- the surfaces the round will look at → the findings already filed against them, this task's and the neighbours', named with their ids
- a discrepancy found passively → dated, or reproduced by a fresh action of the TARGET operation alone (re-syncing operations forbidden for the check), before it is called live; a value stored at the moment of an event confirms no fix either way → secure a fresh carrier

**While the executor is running**

- any message to a working executor → dates the state of the environment («as of HH:MM, verify and work from the actual state»), never asserts it; a scenario taken out of scope keeps the evidence already obtained
- **The observation channel** — no finding rests on an observation taken while the channel was degraded; it is a candidate, re-measured once the channel is healthy: a degraded channel (a background window, a throttled tab, a stale cache) → still produces output, and an automation tab is such a channel for the whole round, so the brief promises no width · an instrument → armed in the SAME call as the action, and exercised on your own object before an empty log means anything · a tool that reports success → read the state back, and «not covered, the tool does not work» instead of variants · a tool that BREAKS the channel → banned outright, not retried · the health stamp → taken in the same call as the numbers it certifies; an expendable attempt under a dying session is packed the same way (only a mutation shape the classifier already passed this round; refused once, split from then on) · a shared resource → addressed by the id the tool handed you, never by a substring · the browser itself refuses the channel (repeated downloads) → the control and the capture at the source
- a dead READ channel plus an irreversible action → the carrier is preserved, not spent: the action is deferred with the object, its state and the recipe recorded
- the tooling fails, not the product → «N attempts at an interval, then escalate» written in the brief, the thresholds from the profile
- the blocker can only be removed by the user acting in their own environment → after two failed detours, one phrase naming what exactly to do and what you will do next
- **Your own harness refuses a call** — the classifier judges the SHAPE of a call, not its purpose, and is not deterministic; a refusal is sorted before anything is asked: an external instrument the round rests on (a request sink, a tunnel) → opened at preflight, the user asked before slicing, the half that passes measured and handed over dated, the instrument configured by its own interface rather than by script · a refused mutation → moving value is a human click every time; a write into foreign data is repeated once by the manager in its own session after the user's permission, paired with a control, never re-fired · a wallet signature → a script records or refuses it, never originates it · a harmless call refused for its wording → reworded (roles, neutral ids, one mutation per call); a refused MUTATION is never reworded; a refusal naming an allow-list is checked against the list re-read from the file, not from memory · the classifier is sticky → switch the tool and pause, budget ~15 calls · a login refused after passing → the «Identity fallback» slot, an irreversible step waits for the switch; the first fallback is the manager's own session («LOGIN NEEDED»), the user only after that · the refusals that remain → planned around: facts never packed with a refused action, an independent channel per browser step, a refusal told from «could not reach a verdict»
- **The executor stopped** — the restart depends on WHY: an infrastructure error → resume it with a message saying what is accepted and what remains · killed by the user → a new launch that reads the existing result and continues · killed by you with the environment touched → the cleanup is yours: global settings restored from the run log, confirmed by reading · waiting on a background run → a checkpoint, not a failure: wait on the log yourself and resume with the verdict

**Accepting the result**

- before reading a single verdict → `check_session.py` lists every scenario of the brief no heading names; a step with no section is evidence that is not in the file, sent back at once while the executor's context is alive
- your own tooling refuses the re-verification of a cancellation → every independent READ that constrains the claim, the executor's evidence kept as theirs, and the split written in the report in one sentence
- the round's result CANCELS an already-published fact → re-verify it by your own observation before editing any artifact, then grep the other artifacts for the same claim
- the CLASS of a finding (the id prefix that routes it to a layer) → assigned at acceptance against the profile's convention; a reassigned number is burned
- an aggregate that grows from other people's runs → a dated observation with the one question that separates a dead consumer from a broken producer, not a finding
- an item the executor left «not covered — the oracle does not reach it» → one deeper read of the same channel (the steps the process performed, the payload) before the row is published, the boundary kept
- «survived / did not reproduce» → accepted only with the boundary of observation stated, set at no less than twice the expected boundary
- a task written as a list of MISSING things → asks for existence; each quality defect goes to the contour that will use the thing, checked finding by finding, not wholesale
- a field that exists but is empty everywhere → a defect only where the SYSTEM fills it; user-entered fields are closed by proving the write path accepts them
- no sign the fix was deployed at all → file the findings, frame the report by the deploy question, mark the block as the state as of <date>; an unchanged journal vocabulary proves nothing by itself
- the result's open questions → checked against the executor's OWN earlier text (`check_session.py` lists the lines that ask; deferrals by eye), not only the brief
- an observation about an environment INCIDENT → dated to the minute and re-checked with one request before the report
- an orchestrator step reported COMPLETED → a fact about the backend, not the product's state: the verdict rests on the product's own read, each store checked separately; a derived store's gap equal to the operations still in flight is compared again once they settle, never filed as a divergence
- the numbers in the case → reconciled against the numbers in the measurements
- before the findings are locked → search the tracker again by the OPERATION's name and the REQUIREMENT's subject, read what the entry found CLAIMS, and search what the round left UNCOVERED the same way

**A finding of the shape «the control does nothing»**

- a control that «does nothing» → the flow is driven to its terminal confirming control, named in the evidence with each click's DOM read; an empty log counts only with proof the last control was reached; an empty LIST needs the view's own request intercepted; «the click never landed» is told from «the handler does nothing» by an oracle (a request interceptor, an audit log), not by repeated clicking; the counter-control is the neighbouring item of the same menu; one click, then wait, then read the DOM

**When the brief caps an amount, state the platform's fee next to the cap**

- a cap on an amount → the «Amount cap» slot carries the fee or the minimum viable amount beside it, checked against each other at planning; where the cost is paid BEFORE the refusal, no figure — «measure the fee across a few amounts, take the smallest that leaves a positive result»

## Preflight and access

**What preflight establishes about the entry — the instance, the identity, the carriers, the values the round depends on — goes into the
brief as the template's «Entry state» section, dated; the entries below keep what each of its lines cost.** Everything else in this section
is what preflight does, and learns, before the brief is written.

- **access that is issued from inside the product, the manager obtains themselves during preflight.** An API key, a service token, a test
  tenant are often created by a regular operation of the product itself (a «create key» mutation, an admin panel) — and «we have no keys»
  turns out not to be a blocker but an unperformed step. Before declaring a contour unverifiable, ask the user how the key is issued and
  issue it yourself; put what you issued into the profile's `secrets` source, not into the session files. The payoff is twofold: the
  executor gets **a contour that does not depend on a short session** (in one session the REST part of the run would have survived any
  disconnect, and five findings were proven by the single fact that an operation was missing, without a single mutating call);

- **A state created by preflight is described with its OWNER and its time, and the executor's first move is to check WHOSE session they
  are in — not whether one is alive.** «A payment in the right status» without «whose» is taken on faith, and a shared environment lives
  its own life: one of two blanks belonged to a different client organisation and could not produce the observable effect — caught only
  because the executor printed the composite key in full; a browser profile declared to hold the required account was holding a stray
  session of another company, caught by the executor's identity check. The entry is written as «as of HH:MM it was …» and the executor
  is allowed to work from the actual state, with a note. A live session under someone else's role looks like a working one and turns its
  refusals into «the result of a permissions check» — a new tab under a stray account nearly put its «Access denied» into the report as
  confirmation of the access matrix. The address is the profile's id, never a tab or window id (the executor's tab group is its own) and
  never a caption: labels are user-editable and get reshuffled, and the label of a known-good profile once migrated onto the profile the
  environment blocks — a brief naming ids caught it, a brief naming captions would have sent the executor straight into the block.

- **An edit you make to a project config file in the same session does not reliably reach the executor's context — the values go
  into the brief («Values the round depends on»).** The executor is handed its own snapshot of the file at launch, and a snapshot from the
  session's cache can predate an edit made minutes earlier: it reads the old copy, concludes the precondition is missing and escalates a
  blocker that no longer exists, with nothing in the result looking wrong. The second line of the slot protects the manager as well: any
  claim about a file's contents is made after reading it, never from the copy already in context. Precedent: three fixture identities were
  added to the project's allow-list before the launch; the executor's copy predated the edit, it reported «none of these accounts are
  permitted», and half a round was spent idle before one `grep` settled it.

- **Where a scenario reaches into an ADJACENT system whose access is short-lived, preflight hands over that system's entity IDs, not
  only their state** — a row of the «Recon facts» table, kind «ids of a short-lived contour». State is what the plan reasons about, an id
  is what the executor acts through, and both are collected in the same breath; once the fragile session dies, listing endpoints are often
  closed on the machine contour, lookups by name silently return nothing, and the evidence becomes unreadable through a channel that is
  otherwise alive. Precedent: three companies snapshotted by name and status in a neighbouring compliance system; the officer session died
  before the executor reached that step, the machine contour answered `405` to the listing and had no name-based lookup, and the executor's
  retro asked for exactly this line.

- **The name you gave an environment may never reach the executor's own listing — the address is an id, and where the tooling exposes
  no id either, a PROBE.** The manager selects the environment interactively, the user names it during that handshake, and the executor's
  listing comes back with generic placeholders; a brief naming the environment then points at nothing, and an executor forbidden to ask is
  left to guess or to wait out a handshake that costs the user minutes. Identity is cheap to measure: the «On a refusal» slot names the
  sweep — the identity oracle over the candidates, most-recently-connected first, the executor's own workspace created in each, so a
  candidate that answers wrong leaves nothing behind — with the interactive handshake as the fallback for «none answered», never the
  first move. Precedent: the executor's listing held three
  indistinguishable placeholders; the probe found the right one on the first attempt, and the executor's retro proposed exactly this
  inversion of the fallback order.

- **The probe sweep has a cost of its own: an executor that sweeps can pin a verdict on the WRONG environment — so when the user can
  re-enter quickly, the «On a refusal» slot pins ONE environment and makes failure a stop, not a search.** A sweep answers «where is the
  live session» only while exactly one candidate holds it; with several environments in different states, an executor that lands in the
  wrong one after a silent tool switch reads that environment's refusal as the truth and writes «dead everywhere». The choice is the
  user's: one id as the brief's first line, «if the tool moves you elsewhere, select this id back», no fallback list, and on any refusal the
  pause protocol. Precedent: a live session was declared dead and a scenario closed as uncovered for exactly that reason; the user set this
  rule for every following round, and no round after it lost a scenario to the environment.

- **Where entering the environment needs a HUMAN, test the access with the session's very first call — before reading the task, the
  spec or the knowledge base.** A login only the user can perform costs their attention and their latency, and everything you would have
  read anyway can be read while they do it: one call at the top of the session — the liveness oracle the profile names — turns a dead
  session from a full stop mid-round into a request the user is already working on while you build the plan. Precedent: a round read the task, the parent spec, the comment thread
  and the knowledge base, wrote the plan, and only then found the session dead — the manual re-login was the round's longest pause, and
  it could have overlapped every one of those reads.

  *And a «dead» answer is believed only from a FRESH navigation in a new tab* (the «Identity oracle» slot says so): a leftover tab
  outlives what made it a valid probe — the extension reconnects, the tab group is rebuilt, the page keeps a state from before a re-login
  — and its identity call answers `401` while the profile's session is alive; a false «dead» costs the user a re-login they did not need.
  Precedent: a round-2 oracle fired from the round-1 tab answered `401` twice in two minutes, the user was asked to log in and replied
  that the session was alive — a new tab in the same profile answered `200` at once.

- **Where each entry spends a one-time artifact (a login link, a code), the identity is chosen and the existing session probed BEFORE
  the artifact is spent** — the «Role» and «Carriers» slots. Permissions differ between roles that log in identically, and entering under
  the wrong one costs the artifact; a scripted session (a cookie jar, a token file) and a browser session are independent carriers, so
  one's liveness proves nothing about the other, and the identity is handed over per carrier. Precedent: a round re-entered a scripted
  session three times while the browser session of the same contour lived for over three hours; another spent a login artifact entering
  under a role the operation refused.

- **Preflight opens the round's TARGET screen, not just the session — and an observation you explained to yourself on the spot is a
  candidate finding, not noise.** Checking that the credentials work («the identity query answers 200 under the right account») proves the
  session, and that is a different claim from «the feature under test can be reached». The gap between them is where a whole class of blockers
  hides: an access guard on that one route, a feature flag off for that role, a page that redirects somewhere harmless. Both halves cost one
  navigation: request the exact address the task is about and **compare the resulting address with the one you asked for** — a silent redirect
  is the whole symptom. The second half of the rule is the expensive one: when the preflight navigation lands somewhere other than where it
  was aimed, that is a measurement, and «probably just a load-time redirect» is a hypothesis you have not tested. Write it into the brief as a
  question for the executor rather than explaining it away. Precedent: the manager navigated to the target page during preflight, got a
  different address back in the same response, read it as a routine redirect and launched the round — the executor found, two hours later,
  that the page is unreachable for the only role available, which was the round's Blocker and had been visible in the manager's very first
  call;

- **The manager's recon verifies the ADDRESS, never the answer.** Confirming an endpoint's path, method, required headers and the selection
  criterion for a fixture is preflight and belongs to the manager — a brief built on a guessed header costs the executor a tour of 4xx. Running
  the scenario end to end — creating the entity, polling it to a terminal state, watching what the product does — is the executor's work, and
  doing it «just to be sure» costs three ways: the round's own evidence now exists only in your context instead of the result file, the executor
  re-runs it anyway (or, worse, quotes yours without observing it), and the environment carries artifacts nobody attributed. The boundary that
  holds: **stop at the first response that proves the address is right.** If the answer to «is this the correct call» is already in hand, the next
  call belongs to the executor. Precedent: a manager's «quick sanity» grew from four probes into a full create-poll-finalize cycle, and the user
  stopped the session to ask why the manager was running the flow at all.

  *And what the address probe already returned is handed over whole — the VALUES of the round's fields on the sampled record, as rows
  of the «Recon facts» table, never only the fact that their keys exist.* Precedent: an address probe on three list endpoints reported the
  filter's field «present in the record of each»; on one of them it was an empty string on every record — the only finding of the round —
  and the executor lost a pass rebuilding its reference data from another endpoint.

- **the user usually has several browser profiles, and they differ not only in sessions but in network egress — when access is refused,
  check first whether it is the right profile, not the environment.** The symptom: the environment answers with the same error (403/timeout)
  on **all** of its hosts, including the login page and the open services, and does so even for a request without cookies; from the shell
  the same URLs answer normally. This is not an expired session, not a block on the environment and not a broken login, but the wrong
  profile — one sitting behind a VPN, say, whose address the environment does not admit. The diagnosis takes one comparison of the external
  IP from the tab against the one from the shell, and the cure is picking another profile. **Which profiles are the working ones and what
  their ids are is a question you ask the user ONCE, after which it goes into the project profile and into the executor's brief**: otherwise
  every subsequent round loses the same half hour. Precedent: half an hour spent diagnosing «the environment has been closed off» — with a
  live environment and the correct account;

- **A browser-native auth dialog (HTTP basic auth in front of the environment) is invisible to the browser extension, and no number of
  navigations gets past it — ask the user for the entry at the first symptom.** Each of these is sufficient on its own: a page script fails
  with «cannot interact with browser-internal or unparseable URLs»; a script call times out at the CDP limit (~45 s); a screenshot reports an
  error page in frame 0; the tab list shows a new-tab address right after a navigation to the environment. One shell request with the
  credentials from the `secrets` source tells «the host is alive, the dialog is the only problem» from «the environment is down». The
  browser forgets these credentials whenever its data is cleared, so the dialog returns between sessions. **A wall of the same shape
  appearing MID-run** (`origin` null, no scripts on the page) first gets a new tab and one retry — it often clears by itself within a minute
  — and only then a request to the user;

- **when preflight finds the environment in the WRONG state, ask whether that state is itself one of the round's scenarios — and capture it
  BEFORE fixing it.** Fixing is usually destructive to the observation: logging in as the right account destroys the stray session, seeding
  the missing data destroys the empty case, restoring a setting destroys the degraded one. And the wrong state is very often a case the plan
  lists as hard to arrange — an organization with nothing in it, an account with no permissions, a resource at zero. One capture costs a
  couple of calls and buys a scenario that cannot be recreated later; it also hands the executor a reference artifact for the shape of the
  output. Say in the brief who produced that artifact, when, and that it is not to be replayed. Precedent: the live session at preflight
  belonged to a neighbouring account whose organization was empty — exactly the «nothing to report on» edge case; the export was taken from
  it before asking the user to log in, and it became the structural reference the whole round's parsing was checked against;

- **a scenario about an entity's states (statuses, roles, flags) starts with the question «is there an instance of each state on the
  environment» — one request during recon, before slicing the scenarios.** The answer «all objects are in one state» turns half the plan
  into substituted reads, and that is the manager's call to make, not the executor's on the fly. Precedent: all 23 users on the environment
  were `active`, while the scenarios checked the card of a blocked and a deactivated one — the executor worked that out themselves and
  rebuilt the plan (it worked, but at their expense);

- **The order of the scenarios is the order of what DIES WITH THE ACCESS, not of the kind of work — the «Session-bound» column.**
  Where access is unstable (a short session, entry only by the user's hand, a flapping environment) the round opens with a batch capture
  of all the evidence into the result file — the contract, reference numbers for every filter value, samples of live records, anchor ids —
  within the first few calls, the interactive part after it under a periodic access check, so that a loss of access costs part of the
  scenarios rather than the whole round: one approach burned down entirely on a dead session,
  the second survived only thanks to this order. But «capture first, interact after» is a proxy, right only while the fragile access
  gates the whole round; where one contour depends on the session and another does not (an API with its own credentials, a queue read
  anonymously, a public artifact), the session-bound contour's *interactive* scenarios outrank the independent contour's *snapshots*, and a
  conscientious executor who follows the letter spends the fragile resource last. Precedent: a brief ordered the batch capture first and
  the independent API's negatives immediately after; the executor deliberately departed from it, ran the whole session-bound contour
  first and recorded why. The same partition splits the reading list (the template says so): on a session that dies in minutes, «read
  the whole list first» and «session-bound steps first» cannot both be kept — a retest brief listed a dozen files «read whole before
  anything» next to «the session might die in minutes», and the executor read two, ran the block, read the rest after, and asked for
  exactly this split. The first half is what the block cannot run safely without — the access and browser pitfalls, the contract
  snapshot to compare against, and the shell pitfalls whenever the block may touch the shell at all, because the executor's own
  instruction reads them before its first shell command.

  *And a bulk source is dumped ONCE even when it is stable* (an execution history, a log index): every later question is a local
  computation over the file — going back to the network for the same history costs minutes and shifts the sample's boundaries between
  answers. Where the source answers only inside a page session, «the file» is the page's own memory — `window.__…` or `localStorage`,
  chosen by whether a navigation lies in between (`browser-techniques.md`, «The page-scripting sandbox and its limits») — with only the
  derivatives and full ids written to disk; a brief ordering the raw dump onto disk orders a download the executor will not make. The
  parsing filters are built one condition at a time: an `A and B or C` returned every event through operator precedence.

- **if the waits in the brief exceed an hour** — the «Waits over an hour» slot says whether observations may be spread across isolated
  environments and run in parallel: «one session at a time» forbids logging in over a live session but not two isolated environments, and
  without explicit permission the executor chooses the sequential route. Precedent: ~85 minutes of nearly pure waiting where two
  observations could have run in parallel;

- **a hypothesis about survivability, flakiness or «it breaks sometimes» requires a control instance, and every expendable has a number —
  the «Control instance» and «Expendables» slots.** Without a control polled rarely, the experiment spoils its own baseline and «it broke»
  cannot be told from the norm: a non-deterministic session loss could only be described after the executor assembled a long-lived control
  session on the fly — ~15 minutes and three burned instances. Without a number the executor either economises at the expense of
  cleanliness or spends blindly, and each clause of the slot was paid for once: the unit — «no more than 8 activations» was meaningless
  because activation did not create a screening, which turned out to be the round's main finding; the control term — a challenge budget of
  five was spent exactly as planned, the one outcome nobody had foreseen then needed a control, and the executor took it as a sixth, over
  budget; the transient term — a budget of «2 + 1 spare» came out at exactly zero, and had the last expendable burned on a browser-extension
  transient, the last scenario would have gone uncovered; the restoration — a budget of six risk-level changes closed at exactly six only
  because the last negative probe happened to return the fixture to a sensible value on its way;

- **On a round about APPEARANCE, «may the executor resize the window and take the focus» is a load-bearing condition of the whole round
  — the «Window and focus» slot, settled with the user at preflight, before the scenarios are sliced.** The user shares the environment the
  round observes through, and the scenarios that measure layout are built on changing its geometry; asked late, the restriction arrives as a
  scope correction AFTER the action, with the measurements already taken and the scenario struck out. The request to the user is «do not
  work in this environment for the duration of the round», not «keep the window in front» — otherwise the executor and the user fight over
  the focus and every observation taken while losing that fight is void; and the ban on taking the focus programmatically goes into the
  brief from the start, with what to do instead, because an executor who discovers a working way to raise the window will use it, and the
  user's attention pays. Precedent: both corrections («stop resizing», «do not force the focus») arrived mid-round after the corresponding
  action; the whole width-threshold scenario was struck out with its measurements spent, while the parts the executor could have closed
  instead stayed uncovered.

- **When the launch comes after a WAIT on the environment, the task's comment thread is re-read in the same breath as the launch** —
  the «Requirements read as of» slot carries the timestamp that makes the gap visible. The team fixes the environment and writes about it
  in one motion: the developer who deploys the build also posts the contract it implements, the defaults, the route the plan guessed
  wrong, while the manager, released by the environment's own signal, goes straight to the brief on text read an hour earlier. One read of
  the comments posted since costs a call; missing it costs a brief built on superseded text and a correction competing with the scenarios
  it rewrites. Precedent: the developer posted the implementation contract — the only creation route, the verdict operation, a replaced
  requirement, a new negative — a minute before the deploy job finished; the executor was launched on the old brief, the user had to point
  at the comment, and the correction reached the executor before its first scenario only by luck of timing.

## What goes into the brief

- **The «Fixture» column is a selection criterion, never a value, and the criterion is anchored on the object the scenario OBSERVES —
  not on its owner or container.** A fixed value copied from the docs may not exist on the instance the executor picks: a source value
  taken from a documentation example was an empty slice for every account on the environment. And «a live account», «a recent tenant»
  answers whether the carrier exists, not whether it holds anything to look at — on an environment reseeded by automation the freshest
  carrier is routinely the emptiest, and the executor opens a listing with zero rows. Invert the order: find an instance of the object
  first, take its owner from that record, then check the owner is alive; the same query names the DISCRIMINATING fixture — the owner
  whose records hold a value different from the majority — which keeps a comparison from being degenerate. Precedent: a brief told the
  executor to pick the carrier by recency; the freshest one had zero operations, and the executor's rebuilt selection turned up the one
  owner with a non-default value, without which the round's cross-consumer comparison would have proved nothing.

- **A fixture that changes SHARED behaviour (an active routing rule, a price, a flag other runs read) is disarmed the moment its
  scenario is done — the «Disarm after» column, not the final cleanup step.** The cleanup block is written for the round that finishes;
  rounds also stop in the middle — a lost connection, a user's pause, a killed executor — and a disarm scheduled last does not run then.
  «Done» means the decision the fixture steers has been taken, not that the triggering call has returned: under a propagation lag a
  disarm timed by the trigger reaches that decision first (`planning.md`, the restore rider under «FLIPS A SETTING»). Precedent: an
  executor disarmed its routing fixture as soon as it proved unusable rather than at the scheduled end; minutes later the user paused
  the round for a network outage, and the shared environment's nightly preparation passed untouched.

- **The «Closable alone» column says whether the scenario depends on the executor's own limits, and the closable ones go first.** An
  executor's boundaries are not visible from the plan — some calls they refuse by their own rules (financial identifiers, an operation
  that could succeed in transferring value) — and the refusal arrives only when they try; the executor corrects the column from the
  environment, and the correction is itself useful. Precedent: a brief put the decisive measurement first, it turned out to be exactly
  the call the executor cannot make, and three calls went into a doomed attempt — while the scenario labelled «the main open risk» and
  placed second was the one that carried the whole round.

- **with `test-cases: upfront`, the brief carries the analyst's case ids and the verdict on the requirements**. The right to edit is decided
  by the case's own line, not by the session as a whole: an expected result whose source is `spec` is untouchable — a mismatch with it is a
  defect, and rewriting the case to match the facts would legitimize work done against the requirements; an expectation sourced from an
  `assumption` or the `KB` the manual tester refines against the facts, noting the edit. **Steps and preconditions they always refine, in
  both modes** — those are technique (the UI path, the endpoint name, the way to create an entity), not requirement, and forbidding it would
  simply stall the run on «the case says press a button that isn't here»;

- **A check able to REFUTE the round's central hypothesis is scenario 0 of the table, never the tail of the reading list.** The tell
  is what it reads: the rest of the round reads *behaviour*, this one reads the *source of truth* — the contract, the schema, the
  declared route table. It is cheap and asymmetric: confirming it changes nothing, refuting it invalidates every scenario built on the
  hypothesis, so its position decides whether the round is rebuilt at the start or discovered wrong at the end — written into the reading
  list as an aside («grep it, do not read it»), it is done late or not at all, and an executor who does refute it mid-run redesigns on
  their own budget. Precedent: a round's whole hypothesis table rested on «this operation does not exist on the environment»; the
  contract file sat as the last line of the «not needed this round» block, the executor grepped it anyway, and it named the operation's
  real prefix in five seconds.

- **A profile rule that the executor breaks before they get around to finishing the profile must be duplicated straight into the brief — as
  the first line of the reading list.** This concerns rules about reading itself and about the order of work (what to open files with, what
  to read before the first request to the environment, where not to go): the executor takes their first action before reaching the relevant
  paragraph of the profile, and the rule fires into the void. Precedent: «open profile subfiles only with Read, not `cat`» sat in the
  profile's header for three runs and was broken all three times — the executor's first action is a `cat`, and the paragraph forbidding it
  is read after;

- **The «Expected effect» column is never a response code alone — «and establish what actually happened», with the channel that
  shows it.** The code says the call was accepted, never that the operation did anything: an endpoint whose whole job is a side effect
  answers perfectly while doing nothing, and a status-only expectation licenses the executor to stop before the interesting part — even
  where the requirement itself is genuinely only about the code. A wide
  executor closes the gap on their own initiative (and you were lucky), a narrow one does not (and nobody notices). Precedent: «the
  resend endpoint must not answer 5xx» came back `200 OK`; the executor went to the logs and the receiver unprompted and found a silent
  no-op an administrator cannot distinguish from a real resend — the round's most interesting observation, with no place in the brief
  that produced it.

- **After the negative permission probes, the table's last row reads the journal for the run's window — what the refusals were
  recorded as, each refusal's text whole.** A rejected call is supposed to leave nothing or a refusal event; systems routinely record it
  as a performed action, invisible from the call's own clean `access denied`. It is the one moment in the round when you know exactly
  which calls were refused, and it doubles as the check that the negatives changed nothing. Precedent: two Major findings — rejected
  calls journaled as completed operations by roles forbidden to perform them, and an actor's role field carrying the SSO group instead
  of the system role — surfaced only because the brief happened to ask for every action in the window to be listed. The text matters
  because servers enumerate the roles they would have accepted: one refusal proved that the holder of an unrecognised role had fewer
  rights than a guest, which the schema could not have shown.

- **If a scenario may run into a neighbouring contour with a different entry** (another environment, another account, entry by the user's
  own hand, a closed network) — the «Neighbouring contour» slot says in advance what to do: ask through the manager, and what exactly, in
  one phrase, or record an open question and move on. Without it the executor decides alone and usually leaves the finding unproven in
  silence, so as not to spend the user's round. Precedent: a key finding (the admin panel shows a third of the organisation's funds) ran
  into one request to a neighbouring environment behind basic auth and stayed hedged — one entry agreed in advance would have closed it
  in the same round;

- **if a scenario needs reference values (cryptographic constants, test vectors, test addresses)** — the «Reference values» slot allows
  taking them from public sources with the source cited; otherwise the executor spends time on the doubt «doesn't this count as inventing
  evidence» and may give no values at all, devaluing the retest protocol. «Take them from public sources per <standard> and cite the
  source» is unambiguous; «if you can write them out» is not;

- **A negative that needs an entity belonging to someone else carries a concrete identifier in the «Fixture» column — found and
  verified by you, not «take one from the knowledge base».** Refusals of the kind «this address / account / document already belongs to
  another party» cannot be provoked with an invented value, and the real one usually lives in a contour the executor is not logged into
  at that moment; a pointer costs a wasted search or a role switch, and mid-run a switch can cost a whole login cycle. Where you cannot
  get one, say where to look AND say to collect it during the snapshot pass in the other contour, before the run leaves it. Precedent:
  «take an address of another company from the knowledge base» — it was not there, and the executor was saved only by having taken the
  snapshot under the other role first.

- **The «Acting identity» column is a ROLE plus the exact account handle, and a step under another role begins with «who am I» to
  the API under test, not with the action.** Switching identity is a side effect of tooling — a cookie jar, a header, a client instance
  — and tooling substitutes a default silently: the call goes out under the previous, more privileged identity and answers exactly as
  the scenario hoped it would not, with nothing in the response saying whose it was — so the account and its permissions are printed
  into the result before the target call; on a mutating scenario the misfire is spent from the expendables and cannot be taken back. Precedent: the decisive permissions probe went out under the superadmin because a helper
  received one argument too many — caught afterwards from the author id in the journal, at the price of one unbudgeted irreversible
  mutation plus a re-run. «Who am I» is asked of the API under test: a session of the neighbouring contour lives on in the same tab and
  its API keeps answering — a request from the admin contour's tab to the other contour's API came back under the operator. And «under
  the company's account» is ambiguous wherever one organisation holds several accounts with different roles: «do it under the client's
  account» pointed at the administrator, who is refused that operation, and the round survived only because the profile repeated the
  warning.

- **a compound requirement gets a compound verdict.** Half the requirements of a typical spec are «and»: «the status changes **and** the
  officer sees it», «up to five attempts **and** then it is recorded as FAILED». A binary pass/fail on such an item lies in both directions:
  a «pass» hides the half that was not met, a «fail» buries the half that works. Require a third verdict in the brief — **partial, with an
  explicit breakdown of which half passed and which did not** (in one session there turned out to be 14 such items out of 89 — more than the
  clean fails);

- **if a scenario requires actions from the user mid-run** (the profile limits the executor — clicks that move funds, say), **or the round
  logs in through the browser** (its «Identity fallback» line — «Your own harness refuses a call»), the brief carries the template's «Pause
  protocol» section, filled in. The section exists because an executor adds none of its lines on its own
  initiative, and every one of them was once dictated by the manager mid-run, after the damage: the environment id — the user asked for it
  in as many words («always say which browser profile»); the exact account to type — a form pre-filled with a neighbouring account turned
  one confirming click into a session under the wrong identity; the network on which confirming is allowed — an executor's request said
  a production-network window might be confirmed since a failed transaction would also be a result, the manager rewrote it to «reject»,
  and the window came up on the test network after all; the boundary instead of a value — an on-screen rate nobody could predict was
  replaced by a ceiling inside which confirming is safe at any outcome; the recorder armed BEFORE the request — armed afterwards it sees only the end
  state, armed before it separated to the millisecond the events a remote wallet sent from the ones the page produced, and that split
  carried the round's two findings; «do not reload» — a user's reflexive refresh a minute before a signing click left the round holding the
  transaction but neither the click nor the wallet's answer; the one-word answer — a request asking the user to narrate what they saw came
  back «all done», and the round spent calls establishing which half of a two-step pause had happened; the numbered expectation for a
  human-only result — the entire verdict on alert merging rested on numbers stated in advance, and of five points put to the user, three
  were closed from the invitation workflow's own payload. **The manager's half:** read the request before relaying it — the sentence that
  licenses a click on the wrong network is yours to catch — and return the user's answer **by a direct SendMessage to the same agent**, not
  a fork, not a new agent. Group the pauses into series, and fill forms in only while the user is available: a pause of a day or more
  nullifies the page's prepared state. Precedent for the re-entry rule: a signature pause of about fifty minutes outlived a session that
  does not renew; the executor logged in from a second tab, and the signed ownership proof was still in the form when the next signer's
  step came;

- **if after the recon not a single step remains that can be performed by hand** (everything verifiable reads out of the logs/execution
  history, and the rest needs access that does not exist) — do not launch the executor: a brief with no content burns a round and returns a
  retelling of your own recon. Then put the recon's evidence into the session folder as a separate file (`<N>-recon-<source>.md`) and **name
  in the report, explicitly, the reason there was no manual run** — otherwise the reader will assume the step was forgotten;

### What you have not checked yourself is handed over as a question

**Anything in the brief you did not verify goes into the template's «Open hypotheses» table — a question with the reason it matters, never
a fact, a verdict, or a menu of answers.** The executor cannot tell your certainty from your phrasing, and each wrong wording closes the
search its own way: a stated fact is not re-checked, a pre-authorised «not covered» is adopted, a listed outcome is chosen from. The cost
is invisible in the result file — it comes back as a legitimate-looking row nobody can tell from a real one. The table's legend carries the
wording per shape; this section keeps what each shape cost.

- **A claim about the state of the ENVIRONMENT, least of all one with the verdict attached.** Confirming a negative is indistinguishable from
  never having looked, and shared environments accumulate objects nobody in this session created. Precedent: a brief asserted the
  environment could not hold an entity in the pre-approval state; one aggregate query found nineteen of them, a third of all tenants.

- **A doubt about what an INSTRUMENT can do** hands the executor your uncertainty as a verdict they may adopt without looking. Precedent: a
  brief hedged about whether a request sink could delay its response; the setting sat in the dialog the executor was already using, and
  half an acceptance criterion two rounds had left uncovered closed in five minutes.

- **A seeding route you have not run yourself** reads as verified, so the executor spends their attempts making it work instead of asking
  whether it is the right one. Two failures in one round: the claimed producer created nothing (the provisioning lived in a neighbouring
  step of the same suite), and the claimed path was forbidden outright by server-side validation.

- **A LINK between two records that recon made by their TIME.** A batch process stamps dozens of objects within one second, and a
  background worker acts at the hours a person would. Join through the identifiers the records carry; where neither is in hand, hand the
  link over as unjoined. Precedent: a date on one object was read as the START of a nightly process because a process instance started at
  that very second — it belonged to another object; in the same brief, late-night closures were labelled an operator's by their hour, and
  the orchestrator named a vendor-alert workflow instead.

- **A hypothesis about the SHAPE of the fix** saves a round when you guessed right and misleads when you did not — the fix may validate the
  value instead of removing the field. Precedent, round 3: the argument stayed in the schema and is still required, while the fix was a
  server-side comparison of the value — a behavioural experiment gave `pass`.

- **The fixer's correction to YOUR previous round's description** arrives with the authority of whoever owns the code and quietly reshapes
  the block built on it. Precedent: a fix comment said a signing pause «never engaged once, the flag has been false since the migration» —
  the retest found the flag engaging and clearing normally. *The same holds for the team's claim about the ENVIRONMENT* — «the fix is
  deployed», «our requests went through end to end»: check the state flag and the author and creation time of the records it cites before
  the plan rests on it. Precedent: every request the team cited as proof of a working path had been created by the QA account, before the
  fix — nobody had exercised the fixed path, and a control run had to be added.

- **A hypothesis that nothing OUTSIDE the product can settle is marked unresolvable, not handed over as a question.** The product exposes
  the outer operation and never the call inside it; an executor who takes the question at face value spends calls looking for an angle
  and writes «remained a hypothesis». Replace it with the observable consequence you actually care about — a control that discriminates
  the mechanism's *effect*. Precedent: «the block in this response comes from the method the task reworked» cost two calls before the
  executor concluded it was undecidable by construction, and their retro asked for exactly this marking.

- **A list of a probe's expected outcomes BIASES the executor** — it reads as a menu, and the result gets filed under the nearest listed
  heading instead of described. Precedent: a probe brief anticipated a refusal or a success; the server rejected the value by its own
  domain check before the external system was consulted, and the executor flagged that the wording had nudged them the other way.

### A sanctioned mutating probe: what the permission must also say

**A probe is authorised as one call, and the template's «Sanctioned probe» block answers in advance everything the executor would
otherwise decide alone, mid-probe, with the mutation already half-performed.** Eight questions recur; each costs a line to fill in and an
unbudgeted artifact — or the round's sharpest measurement — to omit. The block states the rule per question; this section keeps what
each one cost.

- **Is the READ channel for the effect alive — before the sanction is asked for?** The rule itself lives under «The observation
  channel» (a dead READ channel plus an irreversible action — preserve the carrier); the block's slot is where it is decided, because a
  sanction is requested at planning, and an irreversible expendable asked for under a scenario whose oracle recon has already shown dead
  is spent on nothing. Precedent: a round asked the user for two irreversible records, one of them for a positive «added → visible in the
  card» whose read channel the recon and a developer's comment had already shown to be missing; the probe was cancelled mid-pause, after
  the user had been asked.

- **WHO PRESSES an irreversible step?** A step the user sanctioned in chat that cannot be undone — a permanent record, a non-deletable
  artifact — is decided at slicing as the user's click or the manager's own call, never left to the executor. The sanction exists only as
  the manager's words in the brief, and an executor weighing an irreversible act against a permission it cannot see the user give stops at
  the button and hands it back through the pause protocol — on its own judgment, with no classifier refusing anything — so each such step
  costs a relay round trip the plan never priced. Say who presses in the sanction question itself («you will press it, N times» — or «I
  will make the call») and prepare the pause from the start. Precedent: a round sanctioned two permanent records by the user's answer in
  chat; the executor filled the form, stopped at the button and asked for the user's click, and the second record was dropped mid-pause
  once it proved to add nothing to the verdict.

- **May the hostile values be COMBINED?** Escaping, encoding and injection checks come as a matrix, and one artifact usually carries all of
  them — four mutations become one and the restore shrinks to a single call. Precedent: four hostile characters were folded into a single
  rename by the executor's own initiative, closing the escaping requirement in one mutation and one restore.

- **What if it fails in an UNANTICIPATED way — is a control call in the budget?** Precedent: the probe was refused with a self-explanatory
  message and the executor judged a control unnecessary, recording why — the right call made without cover, and on a vaguer message the
  round would have stalled on an approval round trip.

- **When the probe is «overshoot the available amount», cap the OVERSHOOT, not only the probe.** The reverse routes the whole excess back
  through the fixture and leaves a journal entry of that size forever. Precedent: an executor kept the excess minimal on their own and noted
  that the brief had not said to — the restore had to pass a sum two orders of magnitude larger than anything else in the round.

- **When the reverse is already known not to work, say so and declare the residue expected.** A reversibility protocol reads as a promise,
  so a known defect that makes the restore impossible costs attempts hunting for a way back, or the probe skipped. You usually know before
  the round — it sits in a review remark or a comment on a neighbouring task, read at step 1. Precedent: a probe aimed at the one field
  whose clearing was already filed as a deferred remark came back with the value stuck — the right outcome, obtained without cover.

- **The budget's unit is the PROPERTY being demonstrated, not the round.** A scenario about rendering, formatting or derivation has two or
  three independent properties, each needing its own crafted value; a per-round cap silently picks one and the verdict borrows the rest
  from an adjacent component. Precedent: a round proved the rounding on a value it crafted and had to leave the grouping unproven, purely
  because the brief capped mutations per round rather than per property.

- **What if the probe is ACCEPTED and starts something that runs on?** A negative that unexpectedly succeeds often leaves something alive
  instead of a record to cancel, and the executor then decides alone whether to stop shared infrastructure. The process is also the
  finding's best evidence. Precedent: a replayed registration was accepted with no request behind it and started a process retrying its
  quorum check forever; the executor left it running and recorded the id.

### What a recon fact may claim

**Everything recon measured goes into the brief as a row of the template's «Recon facts» table — the value, its kind, its source, its
date and the boundary it was taken within.** Each column exists because a fact without it has misled an executor: a retelling made them
re-measure what the manager already held, an undated state was taken on faith after it expired, a kind-less row inherited the authority
of the contract values beside it. The shapes below are the kinds; the table's legend states each rule, this section keeps what it cost.

- **A value, not a retelling.** Recon retold in words («there is a retry limit», «there is no extension») forces the executor to obtain the
  numbers again — in one session they grepped the bundle themselves although the manager had already seen every one of them. For FE
  tasks, «is the fix deployed?» is answered most cheaply by grepping the served bundle for the names from the task description — an
  observable distribution, not the repository — and in one session two curls and a grep took two minutes and produced the round's main
  finding, confirmed afterwards by black box.

- **An endpoint's path and method, verified together by one probe — or marked unverified.** The product's documentation is a summary,
  not a source: an operation that exists only in the docs answered 404 on the environment while a neighbouring endpoint carried the
  scenario on an undocumented parameter; in another round a documented POST turned out to be a GET with query parameters, and the
  executor paid for both with a tour of 4xx.

- **Dated, and with the boundary of the sample.** Contract constants are stable, state is not: an executor built their proof on «the
  initiator's limit is taken up, the free remainder is 0» and the reservation had been released a day earlier — the fix was proved another
  way only because they went and checked the precondition. Counts carry their window: recon looked at three days while the brief required
  the whole retention window, the full window added a run the manager had never seen, and the executor lost a pass working out whose
  numbers were right. A *mechanism* claim is dated by the build, because it arrives with a consequence for the method («therefore assert on
  the synchronous response»): a brief carried «this path does not go through the event outbox», on the round's build the record arrived
  two to five seconds later through it, and an assertion written from the brief would have flaked. A *negative* names the places looked,
  in the executor's terms: a brief stated that no money field visible to the customer carried a long fractional tail, having checked three
  keys of one array; a fourth column on the same screen carried one on every record, and the executor lost minutes working out that it
  belonged to a different formatter.

- **Contract values are fact; the composition of the interface is a hypothesis to confirm by looking.** Mixed into one table, the second
  kind inherits the authority of the first, and the executor meets a screen that does not match it. Precedent: a brief listed a row menu's
  three items from the localisation map; the live menu had two, and the third operation lived in a different control — perimetered
  correctly only because the brief demanded behaviour over artifacts elsewhere.

- **An oracle built on what a FIELD IS CALLED is a hypothesis, never the primary.** It comes from the same schema as the real constants and
  live data will not refute it in advance — on the records seen at planning time the two fields are equal, which is exactly why the pair
  looks usable. Precedent: a brief offered a field pair as the way to tell two amounts apart; the field named for the original value held
  the current one on the target records too, and the round survived on the arithmetic oracle written in as the fallback.

- **A reading of MINIFIED code is handed over as the excerpt, and as a LOWER bound.** The strings are quotable, the control flow around
  them is reconstructed by eye, and a reconstructed model is worse than no hypothesis: a brief said a status label came from a lookup with
  a fallback, the code held a plain conditional, and the executor burned probes proving the fallback theory wrong. The excerpts name
  carriers that exist, not all that do: recon read a value's display as one hover-only carrier, the product had three, and the primary
  one — a labelled row on the card — appeared nowhere in the excerpts. A code hypothesis is settled by behaviour and by the COMPOSITION of
  the output, not its count: a slice to the first element read as «two values selected, one applied» and was a single-select dropdown;
  two filter states returning 486 and 6+486 rows gave the same page count, and only the rows told them apart. «Not in the build» holds
  only across every chunk (`browser-techniques.md`, «Bundle and route discovery»).

- **An identifier SCHEME is a convention, and a rebuild is free to change it.** Read off every existing record it reads as a constant;
  the objects sampled are old, the object the executor creates is new, and «not found» then reads as the thing being absent. Precedent:
  the build deployed that morning had switched the scheme, the executor's lookup answered «not found», and for half a minute that looked
  like confirmation of the round's central hypothesis — while the object's own field held the real address all along.

- **A contract read out of the CLIENT's own query documents carries names without types.** The composition is exact — the artifact embeds
  the query text verbatim — and every type the manager fills in from the shape of a name is plausible and several are wrong the same way:
  a plural-sounding scalar, a singular list, a nullable non-null. Precedent: a liveness contract taken from a bundle's embedded query went
  into a brief under «facts of the contract (introspection)»; the executor's own introspection disagreed in four places, and their retro
  noted that a test written from the manager's table would have been red on the first run.

## A retest round

**A retest brief carries the template's «Retest» section, filled in — the fingerprint, the fix's scope, the previous round's verdicts
line by line, what remains, what is already filed, what is forbidden for the duration of a check.** Each line is a way a retest has
been wrong about the one question it exists to answer, «what is different now»: the entries below keep what each one cost, the
section states the rule.

- **The build's fingerprint is an item of the brief — taken FIRST, repeated as the last action, and again after any anomaly.** Taken
  only at the end it is taken after the fact; at both ends the pair answers «did the environment change under us», and the third
  reading is triggered by the event that makes the answer matter. A negative is a full result — build versions are opaque hashes, and
  «development must confirm the fix is in the build» beats silence, which lets the reader take as verified something never checked.
  Acceptance then requires the version the run actually exercised, or the verdict cannot be tied to a build and the next retest starts
  with archaeology. Precedent: a round took the fingerprint at both ends as instructed, and the redeploy that had wiped the environment mid-round surfaced
  only because the executor happened to re-read the deploy jobs after re-seeding; another retest had to reconstruct that the round
  before it had run on the previous bundle. How the same reading dates a retest's trigger is in `planning.md`, «Dating the build».

- **«Nothing has changed since the last round» is a claim about a fact, and the fingerprint does not establish it — one behavioural
  probe does.** The fingerprint answers «was the client rebuilt», never «did the server change»: a service is redeployed without
  touching the version it reports, and behaviour a whole round rested on moves with it. Before proposing that a round is pointless,
  and before writing «the environment is unchanged» anywhere, spend the one call that probes the previous round's sharpest finding;
  the brief says the general form, because it governs every verdict the executor writes: **matching versions are not grounds for
  inheriting a single measurement.** Precedent: a round whose every external signal said «nothing moved» was running on a server
  redeployed in between, and the previous round's Blocker had been fixed — «do not run the round at all» had already been put to the
  customer as a legitimate option, and the probe that refuted it was one call.

- **A round that resumes after a CALENDAR WAIT starts by reading the OBJECT and when it was last touched — never the process that was
  supposed to act on it.** The brief writes itself around the mechanism under test, so the executor opens its execution history, finds
  exactly the event the previous round predicted, and starts writing verdicts — while the object may have been destroyed days earlier
  by another actor, a restarted worker, a neighbouring run. Both facts coexist: the mechanism fired correctly AND the row it acted on
  was already overwritten. A last-modified that predates the expected event is the whole detector, and the sweep of the entire waiting
  interval is what explains the discrepancy. Precedent: a three-day expiry experiment came back with a textbook timer event and a clean
  terminal result, while the request itself had been failed two days earlier by a restarted watcher replaying old blocks — found half an
  hour of verdicts later, and the executor's retro asked for exactly this inversion.

- **On a retest, first check that the observation path itself is still alive, and rest the verdict on the final artifact rather than on
  an intermediate UI state.** A «symptom of the defect» goes stale together with the build: the symptom was «zero checkboxes ticked
  while storage is non-empty», and on the fixed build the dialog started closing by itself — a DOM snapshot taken during the closing
  animation looked exactly the same. The executor nearly recorded a false reproduction and was saved by a control file.

- **Set the retest of a finding on substituted responses rather than on an expendable instance when what is being checked is the
  client's reaction.** A reaction to a refusal (logout, retry, rollback) is reproduced by intercepting on the client side: no expendable
  is spent, no one else's state is spoiled, the run is repeatable; the real refusal is left for a single control run (substituting under
  a client cache has its own order — `browser-techniques.md`, «Intercepting, replaying and substituting network»). Precedent: the
  expendables ran out and a stray live session turned up in the environment — emulation delivered a full verdict on two requirements
  where the real path was already unavailable.

- **A retest verdict is passed on the scope of the FIX, not on the original wording of the finding — and a defect found beyond that
  scope is a new finding, not a live one.** Findings are written broadly («this role can be granted at all»), what the team accepted is
  narrow («remove it from the form»); merging the two reads as «the fix did not work», which is false and costs the developer a
  pointless round, while splitting them lets the customer set the priority of the new one. Precedent: a round reported «the fix is
  cosmetic, the defect is alive on the server», and the customer's answer was that the task had been to change the form — done — while
  the server-side route was a separate defect for the side registry.

- **A previous finding quoted into the brief says whether each value is a RAW ENUM or a caption the user sees.** Findings mix the two
  freely, and the compression into a brief keeps whichever was shorter; the executor then meets a screen whose captions do not match the
  quoted list and must decide, mid-run, whether the product changed or the brief is loose — on a retest, the one doubt that is least
  affordable. Precedent: an executor lost half a minute deciding whether a dictionary had changed under them, rescued only by remembering
  that the bundle hash was unchanged and the captions had nowhere to change from.

- **A discrepancy found PASSIVELY on a retest proves that it exists, not that the defect reproduces on the current build.** Before the
  verdict «still broken», either date it — did it arise after the fix (for on-chain data, the explorer's own timestamps) — or reproduce
  it by a controlled fresh action with a baseline before and the value after: «the discrepancy exists» → «when it arose» → «reproduces /
  fixed». Precedent: a mismatch inherited from before the fix was nearly reported as the defect living on. The fresh action is the TARGET
  operation alone; operations that re-synchronise the same state through another path mask the trigger under test, and the brief names
  them as forbidden for the duration of the check.

  *And where the defect lives in a value WRITTEN AT THE MOMENT OF AN EVENT — a failure message, a snapshot, a rendered text stored
  with the record — the old record can neither confirm the fix nor show the defect alive, so the retest starts by securing a fresh
  carrier.* A fix changes only the records produced after it; re-reading the old one after the deploy yields the same evidence as
  before, which reads as «not fixed» and is only «not re-written». One read of the old record at planning shows which case you are in,
  and the plan budgets the event itself — by whatever route the environment still allows, since the previous round's lever may be gone.
  The old record stays in the report as a residue for the team (a migration or nothing), not as a regression. Precedent: a retest of a
  leaked internal error in a stored failure text found the original row unchanged after the deploy; the fix held on the first failure
  produced after it, and the row stayed visible, raw, in the one console that prints the stored text as it is.

- **The brief writes out not only «what recon says is fixed» but also «what remains».** A remainder named in advance gets checked in
  the same motion and comes back as a separate finding rather than as a doubt. Precedent: «the refusal branch is inverted, but the retry
  limit is still there» — both halves were confirmed, and the remainder became a Minor finding with no extra pass.

- **The findings ALREADY FILED against the surfaces the round will look at — this task's and the neighbours' — are named with their
  ids.** The screen under test is shared: a header, a common formatter, a text passed through from another contour all carry defects
  filed by other sessions, and an executor who meets them either spends calls establishing novelty or files a duplicate that acceptance
  has to unpick. One grep of the session reports and the side-findings registry for the screen's name produces the list. Precedent: an
  executor reached the end of a round before discovering that two of its observations (an untranslated back button and a raw driver
  error in a failure message) had been filed by neighbouring sessions — its retro asked for exactly this line.

## While the executor is running

- **any message to a working executor — a scope correction, an answer to a pause, a resume — does not assert the state of the environment
  but dates it: «as far as I know, as of HH:MM …; verify the actual state and work from that».** You see the world through the result
  recorded up to the last file save, while the executor has moved on: the claim «you have not mutated the environment yet» turns into a
  false premise on which they will either start from a clean state that does not exist or spend a pass on diagnostics. And **when you take a
  scenario out of scope, add «if it has already been performed — keep the result and the evidence, and mark its status as completed before
  removal»**: otherwise the executor has to choose between your instruction and proof already obtained. Precedent: by the time a scope
  correction arrived, the scenario it removed had already been run along with three other expendable steps — the executor kept the evidence
  and wrote the amendment themselves, but the loss was one message away.

### The observation channel

**Every measurement arrives through a channel, and a broken channel does not go silent — it returns plausible falsehoods that read as findings.** The brief's standing line: **no finding may rest on an observation taken while the channel was degraded — such an observation is a candidate, re-measured by a control reading once the channel is healthy**, and «is the channel healthy» is checked before describing what a control does, not after. Stated in advance it costs one line; discovered in the retro it has already cost the round its credibility.

- **A degraded channel still produces output** — a window in the background, a minimized viewport, a throttled tab, a stale cache, a session in a reduced state. Structure comes back, sizes come back, elements are found, and yet controls report the wrong state, labels collapse, disabled and hover states are invisible, selections do not take. Everything about it invites a defect report, because the executor is looking at real output. Precedent: two defects were nearly filed from a background window — a control that «silently does nothing» and a field showing a count instead of a name; in the foreground both turned out to be correct behavior. **An automation tab is such a channel for the whole round**, and its viewport is neither the user's nor the next tab's — so the brief promises no width, and the executor works by `browser-techniques.md`, «The hidden tab».

- **An instrument is armed in the SAME call as the action that produces the event.** Set up after the target screen is reached, an observer records the state *after* the transition, and the timing evidence can only be re-taken on another expendable; and one that wraps a global the application already captured — a constructor, a fetch, a timer held in a closure since bundle init — reports an empty log while the mechanism runs perfectly. So before writing «the product never does X» from an empty log, exercise the instrument on your own object and say in the result whether it caught it. Related trap: the first entry of a «record only changes» accumulator is always written, and it reads exactly like the moment of transition — never date anything by it. Precedent: a frame logger wrapped the constructor after page load and stayed empty through a fully working push channel; the executor's control socket was the only thing that stopped «the application opens no connections» from going into the report.

- **A tool that reports success has not necessarily done anything** — a resize, a click, a navigation, a cache reset: the harness reports what it dispatched, not what the page did. The line: «after a step that changes state through tooling, read back the state itself — the width, the DOM, the URL — and if it did not change, record "not covered, the tool does not work" instead of trying variants». Precedent: four window resizes all answered «successfully resized» while the viewport never moved, and the round lost the measurement it was sent to take.

- **The next round of that lesson: the tool did something, and what it did was BREAK the channel — then it is banned outright, not wrapped in retries.** An instrument that changes the environment's presentation can succeed at its own job and push the observed surface into the degraded state above, so the measurement never updates and a stale number reads as a fresh one. Diagnose it by reading the channel's health **after every application of the instrument** — checking before it is checking the wrong moment — and then say «do not use it at all»: a «three attempts, then escalate» rule instructs the executor to break their own channel three times, while the honest «not covered, the tool destroys the measurement» is reachable on the first. Precedent: a resize tool reported success and left the measured width unchanged — it was moving the window off the screen, which occluded the tab and stopped the renderer from recomputing the viewport.

- **The stamp of the channel's health is taken in the SAME call as the numbers it certifies.** Checking and then measuring are two moments, and the gap is enough for the user to click elsewhere, a window to lose focus, a session to drop a privilege: the measurement then looks clean, is void, and nothing in the result shows it. One line, free to the executor: «return the channel's state together with the values, in one call, so every measurement is self-certifying». Precedent: an executor arrived at the trick alone, near the end of a round in which several measurements had already been discarded. **An expendable attempt under a session that can die at any moment is packed the same way** — the identity check, the baseline read, the mutation and the read-back in one call: sent as a separate call, a mutation that comes back `401` with an empty body leaves no way to tell whether the attempt was spent, while a packed one is either wholly meaningful or wholly absent. Packing puts the mutation next to fact collection, which the harness-refusal family forbids, so it is done only with a mutation whose shape the classifier has already passed in this round; a shape not yet seen passing goes alone, right after an identity check in the preceding call, and a packed call that is refused is split from then on. Precedent: a consumable attempt fired in its own call after the identity check died on the session in between, and the round could not say whether it had been used.

- **A shared resource is addressed by the identifier the tool handed you, never by a substring of its name, title or URL.** The user's environment holds dozens of near-identical objects, so a matcher that resolves uniquely at the start stops being unique the moment the round moves to a second environment, and the next call silently operates on somebody else's object — the measurement becomes unattributable and the user's own state is disturbed. The line: «resolve the target once, by the id the tool reports, verify it against your own session's object, and never re-resolve by matching text». Precedent: CDP scripts matched by a URL substring; after switching to the control environment one of them navigated a tab belonging to the user — one discarded measurement, and a stranger's tab left pointing at the wrong environment with the original address never known.

- **The browser itself can refuse the channel — and then the product's success message is true and the file is still missing.** The shape: the second export shows its success toast and never lands, because the browser blocks repeated automatic downloads. It reads as a product defect and is not; the brief names the control and the capture at the source (`browser-techniques.md`, «Downloads»). Precedent: a round spent five calls on «the second export produces no file» before the control showed the browser was refusing every download.

- **When the channel that would READ the result is dead and the action that produces it is irreversible, the carrier is preserved, not spent.** The two halves of an experiment fail independently, and a brief that names only the action invites the executor to perform it anyway — the call goes through, the response is a success code, and the measurement is gone along with the only object that could have carried it. The shape is common wherever writing and reading live in different contours: an event can be posted to an unauthenticated receiver while the state it changes is readable only under a session; a job can be triggered by a queue while its outcome shows up only in an admin view. Say it in the brief as a standing rule — **an action whose oracle is unavailable is not performed, it is deferred with its carrier recorded** — and require the executor to write down which object is being held, in what state, and the exact recipe that finishes the measurement once the channel is back. The instinct to «at least do the part I can» is what destroys the experiment, and it feels like diligence. Precedent: the round's key measurement needed a webhook posted and a flag read back; the session that owns the flag was dead in every browser, the webhook would have moved the only free carrier into a terminal state, and creating another one cost money — the executor posted nothing, kept the carrier, and left a three-minute recipe that made the measurement survivable.
- **Close off a tooling failure (not the product's) with the rule «N attempts at an interval, then escalate» right in the brief.** «It
  doesn't work — record it and report» does not answer «how long to wait», and the executor picks intervals at random. Precedent, round 3:
  the browser extension dropped out entirely (the list of connected browsers came back empty), came back on its own in ~9 minutes, and the
  executor guessed at the pauses — ~10 minutes of the round went into the sand. The concrete thresholds go into the profile, next to the
  tool in question.

- **a blocker that only an action by the user in their own environment can remove** (bring a window to the front, unlock the screen, insert
  a key, confirm access at the OS level) — ask for it right away and in one phrase, instead of working through detours. Automating a local
  environment runs into system permissions and hangs silently: in one session an attempt to unminimize the browser window via System Events
  hung the command on an Accessibility access prompt, while two other detours (AppleScript `activate`, activating the tab through CDP)
  reported «success» while changing nothing. The rule: two detours failed — formulate the request to the user, naming **what exactly** to do
  and **what you will do next** («click on the window — I'll finish the remainder, ~10 minutes»);

### Your own harness refuses a call

**The session's own safety classifier judges the SHAPE of a call, not its purpose, and it is not deterministic — the identical call passes, then is refused twenty minutes later.** So a refusal is sorted before anything is asked, a pass is no promise about the next attempt, and the round is planned so that a refusal costs one call rather than the block. Several moments, one mechanism.

- **An external instrument the round rests on — a public request sink, a mail catcher, a tunnel, a third-party sandbox — is opened at preflight, because the thing most likely to block it is your own harness, not the environment.** The instrument is alive and reachable, and the classifier refuses to navigate to it or to script writes against it, because a service whose whole purpose is to capture arbitrary requests looks exactly like exfiltration. Discovered by the executor mid-round, that costs the block twice over — they cannot lift the policy, and retrying changes nothing. Where preflight is refused, put it to the user **before slicing the plan**, as a choice with prices: allow this host, stand up a receiver they control, or drop the block to a later round. The refusal is rarely total — in one round reads and UI clicks passed while scripted `POST`/`PUT` to the same origin stayed blocked — so measure which half works and hand the executor that dated split, with the instruction to configure the instrument by its own interface rather than by script; the instrument's free-tier caps (retained requests, response options, lifetime) are measured in the same pass, since they size the scenarios. Precedent: a round whose main block was webhook delivery found the agreed receiver refused at preflight; one question to the user restored it, the scripted-writes half stayed blocked, and the brief carried both facts — the executor configured the receiver by clicking and closed sixteen requirements.

- **A refused mutation is sorted before anything is asked: moving value, or writing into data that is not yours.** Classifiers pass configuration writes on the round's own objects and refuse the same operation carrying a valid value against a foreign one, because it could damage someone else's data. Moving value (creating, signing or broadcasting a transfer) is a human click every time and no permission lifts it — plan it as one. A write into foreign or possibly damaged data IS lifted by the user's explicit permission: the executor records the refused call verbatim, the manager asks with the outcome and the residue described, and the identical call is repeated once — **by the manager, in the manager's own session**, where the user's words sit in context: a permission relayed to the executor in a message does not reach the executor's classifier, and the repeat is refused exactly like the first attempt. Pair it with the control the executor would have run (the same operation on the round's own object), so the refusal is attributable to the guard under test. The permission buys that one repeat, not a loop — refused again, it is recorded and reported, never re-fired, because the classifier's own noise can pass or refuse it either way. Precedent: a cross-tenant write probe was refused as a write into another tenant's object, in the executor's session both before and after the user's permission was forwarded; the manager ran the same call once in its own session — the server answered `access denied` — and a same-minute control on the fixture's own tenant succeeded, which proved the tenant isolation directly.

  *And the same holds for any request that asks a wallet to sign, a free typed-data signature included.* A page script may record the wallet's traffic or refuse a call, never originate one, so a brief that queues signature requests from a script plans a step that will be refused — let the human press the product's own control instead. Precedent: a brief queued two ownership-proof signatures from the page to save a pause; the call was refused before dispatch, and the round moved those cycles onto a locally held key.

- **The classifier reads the TEXT of a script, so a HARMLESS call can be refused for its wording — and only a harmless call is reworded.** A READ-ONLY script that names actions in its selectors or search strings («Confirm order») is refused as a write: find elements by role, class or index and compare the text in the answer. Placeholder UUIDs of zeros read as an attack on a real id: use neutral ones (`aaaaaaaa-bbbb-…`). Several DIFFERENT mutations packed into one call read as a batch attack and get the whole call refused, so different operations go one per call; a series of the SAME non-destructive mutation with varying payloads — a burst, an alias batch — passes. **A refused MUTATION is never reworded to get it through** — not assembled from variables, not split, not disguised — it is sorted by the entry above: moving value is a human click, a write into foreign data waits for the user's permission. Rewording a mutation until the classifier stops recognising it removes the one check that stands between the round and somebody else's data. A refusal that names an allow-list is checked against the allow-list re-read from the file, not from memory. Precedent: an executor escalated «the account is not on the allow-list» for half a round; the blocker did not exist — the same call, reworded, went through, so the refusal had been about the wording, not the account.
- **The classifier is sticky: after a refusal it refuses harmless reads in the same context for several calls.** Switch the tool (the page-text tool instead of a page script) and pause, rather than retrying the same read; budget for it — one round spent about fifteen calls this way.
- **An identity switch that passed several times is not cleared for the next one — so the brief names the fallback for every switch, and an irreversible step waits until the switch it depends on has succeeded.** A login that goes through a local redirect, a callback page or a one-time link can be refused on any attempt, and the one refused is the one in front of the decisive step. The template's «Pause protocol» carries both as its «Identity fallback» slot, and an irreversible step that has to be observed under that identity is not performed until the identity is in place, so a refused login does not spend the fixture. Precedent: the sixth browser login of a round, through the same local redirect as the first five, was refused; the executor held back the irreversible role revocation it was about to observe, and the scenario ran after the login was made by other hands, without another grant of the role.
  *And the first fallback is the MANAGER's own session, not the user's hands.* The refusal is the executor's classifier judging the executor's call, and the manager holds the same login tooling against the same browser profile, so the switch is requested by a marker («LOGIN NEEDED: <account>», the executor ending its turn), performed by the manager, and confirmed by the identity oracle before the executor resumes; the session's cookies are the profile's, so the executor's own tab picks the identity up. The user is asked only when the manager's attempt is refused too — a login relayed to the user costs their attention for a step the session can do itself, and the user notices. Precedent: an executor's first login was refused, the manager forwarded a «please log in as X» request to the user, and the user answered «but you can log in yourself»; the manager's one attempt passed, and the remaining four switches of the round went through the marker without the user.
- **Around the refusals that remain, the brief plans rather than retries.** Never combine a potentially refused action (installing a substitution, a click that looks like a payment) with collecting facts in one call, or the refusal takes both — the one exception is the packed expendable attempt («The observation channel»), under its own condition. **A message that the tool could not reach a verdict** («Could not verify this site's safety category») is not a refusal: nothing went out, and the call is repeated (`browser-techniques.md`); a message naming a blocked category IS one, and is sorted here. Give every browser-dependent step a plan on an independent channel (the shell to the orchestrator's history, a public explorer, a plain request). A refused `navigate` may pass as a `location.reload()` from a page script, or the other way round — try the other once. When the browser layer is refused entirely, the user can remove your interceptors by reloading the page, the state of live operations is read from the orchestrator, and the report is written from what is collected rather than waited for. Precedent: in one round the browser refused eleven calls and the result still stood, because the key measurements had been taken outside it.

### The executor stopped

**How you restart it depends on WHY it stopped, and the wrong move costs either the run's context or the environment.**

- **It died on an infrastructure error** (a dropped connection, an API timeout) — **resume it with a message**, saying what has already been accepted and need not be redone and restating the remaining order of work. A new launch loses the run's context and repeats the expendable actions.

- **The user killed it** — then it is not resumed: a new launch, with an explicit instruction to read the existing result in full and continue from it rather than replay what is done. An incremental result makes that possible — precedent: a killed executor's own result file carried enough of the run for the replacement to pick up mid-scenario instead of starting over.

- **You killed it after it had already touched the environment — the cleanup is now yours.** Killing an agent runs no rollback: whatever it set up stays set up, and the executor's own restore step (usually its last) never runs. Look first at **global settings** — the ones a test switches on at the start and restores at the end; they are visible in the code as a «save the original …» step, and their original values are usually printed in the run log. Restore them, **confirm by reading**, then record in the report what was left and what you returned. Precedent: an automator stopped mid-run left a global anti-fraud rule switched on for the whole shared environment — every account was one failed operation away from an automatic ban, and other people's runs would have collected false bans; the original values were recovered from the killed run's own log.

- **It stopped at «waiting for the background run to finish» — that is a checkpoint, not a failure**: no notification from its background process will reach it. Take the waiting on yourself (a background until-loop over the run's log file with success/failure markers and the stop condition «the log stops growing»), then resume the executor with a message carrying the verdict and the path to the log. Precedent: an automator stopped at «waiting» three times, the manager waited for the log and woke it up three times — and not once was work lost.

## Accepting the result

- **Before reading a single verdict, list the result's headings against the brief's steps — a step with no section is evidence that is not
  in the file, whatever the summary says.** The executor's final message and the result's closing tables are written last and from the
  executor's context, so they cite every step faithfully even when the file no longer holds the sections they cite, and what remains is
  well-formed. `check_session.py` matches the brief's scenario ids against the result's headings and names each one no heading carries
  — a missing section, or a scenario run inside another whose heading forgot its id; the repair is cheap only while the executor's context and scratch logs are still alive: send it back at once to restore the
  missing sections from them, with no new mutations. Precedent: a result opened at its fifth step — a scripted mid-file insertion had cut
  everything after the first table — while its verdict tables referred to «step 1» and «step 4» throughout; the executor rebuilt the five
  sections from its scratch logs and the page's storage within the same session.

- **When your own tooling refuses the re-verification of a cancellation, the boundary is published, not papered over.** The rule below
  obliges the manager to go and look themselves; sometimes the looking is precisely what the manager's own safety rules forbid — the
  claim is «the destructive operation now refuses», and re-running it is a destructive call. Three moves, in order: take every
  independent READ that constrains the claim (the entities are still there, in every contour that can see them — which also proves the
  executor's run destroyed nothing), keep the executor's evidence as theirs rather than restating it as your own, and write the split in
  the report in one sentence — what acceptance verified and what rests on the round's own measurements. The temptation is to skip the
  sentence, since the conclusion is the same either way; it is the sentence that lets the next round know which half was never
  re-measured. Precedent: a round reported that a hard delete had been replaced by a refusal, cancelling an accepted blocker; the
  manager's re-run of the mutation was blocked by an irreversible-deletion guard, and acceptance closed the gap with reads in two
  contours plus an explicit line that the refusal texts came from the executor.
- **When the round's result CANCELS an already-published fact, the manager re-verifies it by their own observation before editing a single
  artifact.** The shape: an executor's measurement refutes a finding filed in an earlier round, a line of the project profile, or an entry in
  the knowledge base. Ordinary acceptance takes the executor's evidence at face value — correctly, because the report is the round's own
  product. But a cancellation is not a new fact, it is a rewrite of facts other people have already acted on: the finding may have been
  copied into a tracker task, the profile line is read at the start of every session, the knowledge entry is quoted by the next round. So
  treat it the way you treat an objection after delivery — go and look yourself, in the channel the claim names, and only then edit the
  report, the registries, the profile and the knowledge base. The re-check is usually a handful of reads and it also dates the cancellation,
  which the edited artifacts need. Precedent: a round refuted both the task's own premise and a finding filed two days earlier; the manager
  re-measured the four endpoints personally plus one control, and the correction went out with its own date instead of resting on someone
  else's run.
  **Whichever of those artifacts you edit, grep the others for the same claim** — a profile line and a knowledge-base entry that
  contradict each other cost more than a missing entry, because the reader believes whichever they read first. Precedent: a profile line
  «the service has no health endpoints» stood next to a knowledge-base section describing them, both on the reading list of one round.

- **The CLASS of a finding — the id prefix that routes it to a layer — is assigned at acceptance, not by the executor.** An executor names
  the defect where they found it, and a project whose ids encode the layer (backend / frontend, service A / service B) then gets a finding
  filed under the wrong prefix: a title-tag typo lands among the API defects, an unhandled server error among the UI ones. Check every
  finding's nature against the profile's prefix convention before publishing, and where the prefix changes say so plainly — the reassigned
  number is burned, never reused, because the executor's result file already carries it. Precedent: a cosmetic typo in the served page came
  back tagged as a backend finding; acceptance reissued it under the frontend prefix and recorded both ids, one live and one burned.

- **An aggregate that grows from OTHER people's runs on a shared environment is an observation with a question, not a finding.** Counters of
  the «failed», «exhausted», «stuck» kind read as damning and are the easiest thing to file at the wrong priority: the number is real, it is
  the product's own self-assessment, and it is usually growing. What is missing is the discrimination — on a shared environment the same
  number is produced by a legitimately dead consumer (a receiver registered by a session months ago, a queue nobody drains) and by a broken
  producer, and the round almost never separated the two. So publish it as a dated observation plus the one question that separates them
  («is there a live consumer on this environment at all?»), and say why no priority was assigned: an answer of «no» closes it, an answer of
  «yes» turns it into a defect with evidence. Precedent: a counter that had roughly doubled in nine days was filed as a Major; acceptance
  withdrew it — the environment's registered receivers were leftovers of earlier rounds, and the round had measured nothing that told the
  two causes apart.

- **An item the executor closed as «not covered — the channel cannot show it» is worth one deeper read of that same channel before the row is published.** The executor's boundary is usually honest and usually drawn at the level they were working at: they read the *outcome* a process reported (a status, a result payload, a summary field) and correctly concluded it says nothing about the question. One level down — the steps that process actually performed, the payload of the individual activity, the sub-records behind the aggregate — the answer is frequently sitting in plain text, because a system that calls an external party generally records *what it asked for*, even when it cannot record what that cost. The read is cheap at acceptance (the identifiers are already in the result file) and it changes the row's class: «our oracles do not reach this» becomes «the protocol of the call contains exactly two steps and neither is the one in question», with the boundary kept in the sentence after it. Do not let the upgrade erase the boundary — the deeper read licenses a stronger claim about what the system *did*, never about what happened on the other side. Precedent: a round closed «does this operation start a paid vendor subscription» as unverifiable after checking the flag on the entity and the workflow's own result; the activity's decoded payload named the two steps the vendor was asked to perform, neither of which was a subscription, and the answer went out as evidence with the billing boundary intact.

- **«survived / did not reproduce» is accepted only with the boundary of observation stated**: «alive ≥600 s» without the note «we did not
  look further» reads as a property of the system while describing only the length of the run. Precedent: a round's conclusion «the control
  session is healthy» rested on a 600 s boundary — in the next round the same session under the same conditions died at second 700, and the
  finding's priority changed to Critical. So the brief sets the observation at **no less than twice the expected boundary**, and the
  result names the last second actually watched;

- **A task whose whole description is a list of missing things is a requirement of EXISTENCE, and everything about the QUALITY of those things belongs to the contour that will use them.** The shape is common on follow-up tasks: the description reads «absent: A, B, C» and nothing else — no acceptance criteria, no behaviour. Once the fix lands, the round is suddenly rich: the new things exist but are unvalidated, unpopulated, untyped, missing a dictionary, or writable only through half a path — and every one of those looks like a finding of this task, because it was found in exactly the code the task delivered. It is not. The verdict here answers one question per item of the list, «is it there», and each quality defect is filed against whichever task owns the use of the thing — the editing form, the process that populates it, the consumer. Get this wrong and the findings table triples, the customer re-scopes it back by hand, and the genuinely unmet items of the list get lost among defects that were never in question. Two riders that repay the discipline. Re-scoping moves findings, it does not withdraw them: they keep their ids, their priorities and their evidence, and gain an addressee. And **the premise «quality is someone else's task» has to be checked against each finding rather than applied wholesale** — the ones it does not cover are the round's most valuable output, because they have no owner at all: a field nobody types by hand is not covered by «the form will fill it», and a write path that rejects a mandatory field is a precondition of that future task rather than a consequence of it. Precedent: a round filed seven findings against a task whose description was a list of absent fields; the customer's frame («this task only asks for the fields to appear») left three — and the two findings that the frame demonstrably failed to cover turned out to be the ones at risk of falling between tasks entirely.

- **A field that exists but is empty on every record is a defect only where the SYSTEM fills it, not a person.** After a migration lands, the honest first reading of «0 out of N populated» is «nobody has typed anything yet» — especially when the requirement itself says the field is user-entered and the editing surface does not exist. Filing that as a defect reads as an accusation about work that was never in scope, and the customer withdraws it in one sentence. Split the new fields by who is supposed to write them before assigning a single verdict: user-entered ones are closed by proving the write path accepts them (one sanctioned probe does it), while auto-populated ones — timestamps, sources, counters, derived statuses — are exactly where emptiness is the defect, and there the control is a record the system processed today. Say the practical consequence out loud either way, because it is real: on today's data the consumer of those fields sees a screen of dashes, and accepting the frontend on it will show nothing. Precedent: twenty-one new fields were empty across every record; the report filed one finding (on the two the system was supposed to fill, with a same-day processed record as proof) and explained the other nineteen as an absent editing form — the write path having been proven by a single probe.

- **When the round finds NO sign that the fix was ever deployed, the findings about unmet requirements are still filed — but the report is framed by the deploy question, not by them.** The temptation runs both ways and both are wrong: writing «the developer did not implement any of it» when the build may simply never have reached the environment, or withholding the findings until someone confirms the deploy, which leaves the round with no product. What works: lead the report with «no external sign of the delivery was found; development must confirm the fix is in the build», file each unmet requirement as its own finding with its measurements, and mark the block explicitly as «the state of the environment as of <date>; if the delivery turns out to be missing, these are re-checked after the deploy». Then nothing measured is lost, nobody is accused of work they may have done, and the customer's first action is the cheap one — asking about the deploy. Two oracles usually settle it without repository access: the artifact's fingerprint at both ends of the round, and — for an audited feature — the journal's own vocabulary of event types, since a requirement that obliges new kinds of records makes their absence a dated fact. **That fact is about THOSE requirements only:** a fix can change which branches reach the journal without adding a single new type, so an unchanged vocabulary never proves that nothing was delivered — only behaviour does. Precedent: the round after one that had dated a non-delivery by the vocabulary found a finding fixed and a previously silent branch now logged, under the identical set of types.

- **Check the result's «open questions» against the executor's OWN earlier text, not only against the brief.** A good executor raises questions as they go — «how did this get here?», «is that another path?» — and writes them into the running result next to the observation that prompted them. The final section, however, is usually assembled from the brief: every scenario the manager asked for has an answer, so the count comes out zero, and the question the executor invented for themselves is left behind in the middle of the file, unanswered and now invisible. It is worth catching because a self-raised question is, by construction, the thing the round noticed and nobody planned — often the sharpest item available. `check_session.py` lists the result's lines that ask a question; the words that mark a deferral («выясним», «проверим ниже», «to be answered in step N») are the project's language and stay a grep of your own. Precedent: an executor flagged an anomaly in the batch-capture step, deferred it to a later scenario, answered the three questions the brief listed there, and reported zero open questions — the deferred one turned out to need a single call and became a Critical.

- **An observation about an environment INCIDENT is dated to the minute and re-checked with one request before the report is finalised.**
  The team fixes shared environments while rounds run, so a conclusion written at 15:43 may be false at 16:03. While development is working
  on it, write «as of HH:MM UTC», never «does not work». Precedent: a «missed deposit proven live» section had to be rewritten after a
  watcher restart picked the deposit up twenty minutes later.

- **An orchestrator step reported COMPLETED is a fact about what the backend did, not about the state the product ended in.** An execution
  history proves the mechanism and the cause; a verdict on an entity's status rests only on the product's own read (its API or UI). Where
  the state is carried by several stores — the database, a push notification, an external chain — each is checked separately, because a
  notification can announce a status the database never took — and a derived store legitimately differs from its source by the
  operations still in flight, so a gap equal to the pending ones is compared again once they settle, never filed as a divergence. Precedent: an activity that «marked the transaction failed» completed
  successfully while the status stayed unchanged; the finding went out as a Critical and one product read refuted it.

- **reconcile the numbers in the case against the numbers in the measurements**: the executor writes the case's preconditions before
  finishing the measurement, and a draft value stays behind in the case. Precedent: «TTL ≈600 s» in the case against the ≈300 s measured in
  the same result.

- **Before the findings are locked, search the tracker twice more: by the OPERATION's name and by the REQUIREMENT's subject.** The step-1 search (`planning.md`, «The tracker is searched at step 1») was run on what the round expected to find; by acceptance you know the endpoint, the mutation and the field the evidence actually names, and those are the words somebody else's entry is titled in — often under the wrong area or a neighbouring contour, which is why a search on your own business wording missed it and the report is about to hand the customer a duplicate. **And when the entry is found, read what it CLAIMS**: a discrepancy between «the check exists, its list is just wider» and your executor's «there is no check at all» is not phrasing but a gap in the round — settle it with one more probe before the report goes out. The subject search pays differently: a requirement phrased as «… according to the spec» delegates its content to a neighbouring task, and that task's comments are where the decision lives. Where it sits in a testing status and its own item was explicitly descoped («we asked to skip this one»), the finding changes shape entirely — not «nobody wrote the requirement» but «two tasks contradict each other, one of them is being accepted right now», which is a different sentence to the customer and a different fix. Name both tasks in the cell. **The same two searches also pay on what the round could NOT close** — an item heading for «not covered» is searched by the operation that was supposed to answer it, because a neighbouring task's requirements routinely state the rule the round was trying to measure. That does not make the row disappear: the measurement is still missing. It changes what the row says, from «our oracles do not reach this» to «the requirement says X happens at moment Y, we observed that moment and X did not happen there» — which is an answer the customer can act on, assembled from a document that was one query away. Precedent: an analyst's fork («does this operation switch on the vendor's paid subscription — if so it is a blocker») was written up as unverifiable for want of the vendor's billing; a neighbouring task's user story, found by searching the operation's subject, legislated that the subscription switches on when the client is CREATED at the vendor — and the round had already measured that this operation does not create one, which turned the fork's answer from silence into evidence. Precedent: a finding presented as new turned out to have been filed five weeks earlier under a title naming the wrong contour, and its text corrected the executor's over-broad claim in the process; in another round a section marked «no target list exists, needs an analyst's decision» turned out to be owned, verbatim, by a task in review whose corresponding item had been dropped by request three weeks earlier — and the same comment thread disproved two of that task's own claims about the contract.

## A finding of the shape «the control does nothing»

An executor clicks a control, nothing happens, and files a defect. Two states produce that
observation and they are not the same: the control is dead, or the flow was never finished —
a menu item that only opens a confirmation modal, a button that arms a second step, a form
whose submit lives in a drawer footer. The negative oracle (an empty audit log, no request in
the network panel) is identical in both cases, because a mutation that was never triggered
leaves the same trace as a handler that never fires.

What the brief must require, and what acceptance must check:

- **drive the flow to its terminal confirming control** and name that control in the evidence
  («menu → item → modal → its button»), each click recorded in the result by what it opened (the DOM read, not a saved screenshot);
- an empty log is admissible only **together** with proof that the last control was reached;
- **the same rule governs an empty LIST**, which is where it is hardest to remember: a tab, a filter or a search that renders no rows
  invites controls on the *data* — the API returns the records, a neighbouring tab renders its own, a search finds the row — and every one
  of them can pass while the view's own request was never sent. Those controls prove the data exists, not that the view asked for it, so
  acceptance requires the request itself (an interceptor logging the query and its variables), and a server-side filter visible in that
  request also settles whether the filtering is client-side at all. Precedent: a Major went out as «this tab shows nothing», backed by
  three data controls and framed as a closed task's defect living on; a re-check on a byte-identical build showed the tab firing a
  server-side filtered query and rendering both rows — the finding was withdrawn, its id burned, and the report, both registries and the
  tracker comment had to be corrected;
- separate «the click never landed» from «the handler does nothing» with an oracle rather than
  repeated clicking: a `fetch` interceptor that records request bodies, or an audit log that
  records even rejected calls;
- the counter-control is the neighbouring item of the same menu on the same row — it shows
  whether clicks reach that widget at all;
- **one click, then wait, then read the DOM** — a slow modal is closed by the «try again»
  click; the wait and the check are in `browser-techniques.md`, «Component-library interaction».

Precedent: a Major was filed for «the reactivate item performs no reactivation» on three
attempts plus an empty audit log; the manager's re-check found a confirmation modal behind the
item, and after confirming, the mutation fired and the record changed state. The finding was
withdrawn, its id burned, and every derived artifact had to be edited.

## When the brief caps an amount, state the platform's fee next to the cap

The «Amount cap» slot carries the fee, or the minimum viable amount, beside the cap — the two checked against each other while planning —
because a cap agreed with the customer («small amounts only, 1–10 of the unit») can be arithmetically unreachable on the platform the round runs on: if the fee exceeds the cap, every
attempt dies on «fees exceed amount», the executor discovers it only after measuring, and the instruction handed to the human has to be
rewritten with a different number. The same holds for any precondition expressed as a limit — a balance, a quota, a remaining allowance.

And where the operation costs something irreversible **before** the platform refuses it — a signature, gas, a consumed one-time token —
the refusal arrives after the cost is paid, so an unreachable cap is a wasted irreversible act, not merely an unrunnable scenario. There
the slot names no figure and prescribes the measurement: «measure the fee across a few amounts, take the smallest one that leaves a
positive result, and record it». Precedent: a brief named the minimum unit as the amount to sign; at that amount the fee exceeded the sum,
so the signature and the gas would have been spent and only then refused — the executor measured five points, found the real minimum
and signed once, correctly.
