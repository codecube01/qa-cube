# Briefing and running the manual round

Read at step 4 of `../SKILL.md`, before writing `2-manual-task.md`; the last two sections are read again when the result comes back. Each
entry is a situation the round can land in and the line in the brief that costs nothing to write and a whole pass to omit; the precedent
that closes an entry is what paid for the rule. **Read the file whole** — an executor is briefed once, and a situation you did not foresee
cannot be added to the brief afterwards.

## Contents

Single entries first, then the **families** — one mechanism with its shapes under it. A shape is only readable through its head
entry, so a family is read whole or not at all.

**Preflight and access**

- an access the project issues from inside the product — the manager issues it themselves
- what preflight must hand over about the state it created: the owner, the time, the identity to check
- the name you gave an environment may never reach the executor's listing — the address is a PROBE, not a name
- entering the environment needs a human — test the access with the session's FIRST call, before reading anything
- preflight opens the round's target screen, not just the session — a self-explained observation is a candidate finding
- the manager's recon verifies the address, never the answer
- access refused on every host of the environment — suspect the browser profile, not the environment
- preflight finds the environment in the WRONG state — is that state itself one of the scenarios?
- the scenarios are about an entity's states — is there an instance of each state on the environment
- access to the environment is unstable — batch the evidence first, interact afterwards
- the waits in the brief exceed an hour — say whether isolated environments may run in parallel
- a hypothesis about flakiness or survivability — a control instance and the budget of expendables
- a round about appearance in the user's own environment — settle the window and the focus at preflight
- the round's external instrument is blocked by your OWN harness policy — one question, before the plan

**What goes into the brief**

- endpoint names and HTTP methods — verified by a probe call, or marked in the brief as unverified
- a scenario parameter that depends on the environment's data — a selection criterion, never a value
- which scenarios the executor can close alone, and which depend on their own limits — order them by that
- `test-cases: upfront` — which parts of a case the manual tester may edit and which are untouchable
- every observation you hand over — dated, with the boundary of the sample it was taken from
- a check able to REFUTE the round's central hypothesis — the brief's first step, never the tail of the reading list
- constants your recon uncovered — hand over the values, not a retelling
- recon constants are two kinds: contract values are fact, the composition of the interface is a hypothesis — and an oracle read off a field NAME is a third
- a contract read out of the CLIENT's own query documents — names without types, marked as such
- a profile rule the executor breaks before it reaches the paragraph that states it
- a scenario whose expectation is a RESPONSE CODE — ask for what actually happened as well
- after negative permission probes — read the journal and check whether the refusals were recorded as events
- the scenario may run into a neighboring contour with a different entry
- the scenario needs reference values — cryptographic constants, test vectors, test addresses
- a negative that needs someone else's entity — name the identifier, and verify it exists
- a step performed «under another role» — identify the session before the target call, not after
- a compound requirement («and») — require a third verdict, partial, with the breakdown
- the scenario needs the user's own click mid-run — the pause protocol
- after recon nothing is left that can be done by hand — do not launch the executor at all

- **What you have not checked yourself is handed over as a question** — a claim about the environment · a doubt about an instrument · a seeding route · a hypothesis about the shape of the fix · a list of expected outcomes

- **A sanctioned mutating probe: what the permission must also say** — may the hostile values be combined · an unanticipated refusal and the control call · capping the overshoot · a reverse already known to be missing

**A retest round**

- **the build's fingerprint** — an item of the brief, taken first, last and after any anomaly; and «nothing has changed» is a claim it cannot establish
- check that the observation path itself is still alive, and rest the verdict on the final artifact
- the finding is about the client's reaction — retest on substituted responses, not on expendables
- the retest verdict is scoped to what the FIX was asked to do, not to the finding's original wording
- a previous finding quoted into the brief — say whether the value is a raw enum or a caption on screen
- write out «what remains», not only «what recon says is fixed»

**While the executor is running**

- any message to a working executor dates the state of the environment, it never asserts it

- **The observation channel** — a degraded one returns plausible falsehoods · an instrument armed with the action · a tool that reports success without acting · a tool that breaks the channel · the health stamp taken in the same call · a shared resource addressed by id
- the tooling fails, not the product — «N attempts at an interval, then escalate»
- the blocker can only be removed by the user acting in their own environment

- **The executor stopped** — an infrastructure error · killed by the user · killed by you, with the environment already touched · waiting on a background run

**Accepting the result**

- the round's result CANCELS an already-published fact — re-verify it yourself before editing any artifact
- the CLASS of a finding (the id prefix that routes it to a layer) is assigned at acceptance
- an aggregate that grows from other people's runs — an observation with a question, not a finding
- «survived / did not reproduce» — only with the boundary of observation stated
- a task written as a list of MISSING things asks for existence — quality of the thing is a neighbouring contour
- a field that exists but is empty everywhere — a defect only where the system, not a person, fills it
- no sign the fix was deployed at all — file the findings, but frame the report by the deploy question
- the result's open questions are checked against the executor's OWN earlier text, not only the brief
- the numbers in the case against the numbers in the measurements
- search the tracker again — by the OPERATION's name and by the REQUIREMENT's subject, and read what the entry found CLAIMS

## Preflight and access

- **access that is issued from inside the product, the manager obtains themselves during preflight.** An API key, a service token, a test
  tenant are often created by a regular operation of the product itself (a «create key» mutation, an admin panel) — and «we have no keys»
  turns out not to be a blocker but an unperformed step. Before declaring a contour unverifiable, ask the user how the key is issued and
  issue it yourself; put what you issued into the profile's `secrets` source, not into the session files. The payoff is twofold: the
  executor gets **a contour that does not depend on a short session** (in one session the REST part of the run would have survived any
  disconnect, and five findings were proven by the single fact that an operation was missing, without a single mutating call);

- **Describe a blank created by preflight together with its owner, not just with its state** — «a payment in the right status» without
  «whose it is» gets taken on faith by the executor, who discovers the substitution only by accident. Precedent: one of the two blanks
  belonged to a different merchant and could not produce the observable effect — caught only because the executor printed the composite key
  in full. A state declared by preflight is, for the executor, **a timestamped hypothesis, not a fact**: write it as «as of HH:MM it was …»,
  and explicitly allow them to work from the actual state, with a note in the result, if it has diverged. A shared environment lives its own
  life: in one retest round the browser profile that the manager declared to be a live session of the required account was holding a stray
  session of another company — the executor caught that with an identity check and recreated the session themselves. Record the state
  created by preflight in `2-manual-task.md` as **the entry fact and the state of the environment** (who is logged in, what confirms the
  session is alive, at what time), and **not as a tab/window id**: the executor has their own isolated tab group and cannot reach someone
  else's identifier — only the browser profile's session is ever shared. Instruct the executor explicitly to open their own tab and check,
  first thing, **not whether the session is alive but whose identity it is**: which account and which organization they landed in. A live
  session under someone else's role looks like a working one and silently turns its refusals into «the result of a permissions check».
  Precedent: a new tab opened in a different browser profile under a stray account, and its «Access denied» nearly went into the report as
  confirmation of the access matrix. If the browser profile has a device/profile id — name it in the brief **as the only address, and say
  explicitly that the display name is not one**: profile labels are user-editable and get reshuffled, so a
  brief (or a project profile) that identifies the allowed environment by its caption eventually points at the
  wrong one. Precedent: the label of a known-good profile migrated onto the profile the environment blocks —
  a brief naming ids caught it, a brief naming captions would have sent the executor straight into the block;

- **The name you gave an environment may never reach the executor's own listing — so the brief's address is a PROBE, not a name.** The rule one entry above says to identify a shared environment (a browser profile, an instance, a device) by its id rather than its caption, because captions are user-editable. There is a harsher case underneath it: the tooling can expose **neither** — the manager selects the environment interactively, the user names it during that handshake, and the executor's listing still comes back with nothing but generic placeholders. A brief that names the environment then points at nothing at all, and an executor forbidden to ask the user is left with two bad options: guess, or stop and wait out an interactive handshake that costs the user minutes of attention. Neither is necessary, because identity is cheap to *measure*: give the brief the liveness/identity oracle the round already uses and say to sweep the candidates with it — most-recently-connected first — creating the executor's own workspace in each and reading who answers. The right one usually answers on the first or second try, and a candidate that answers wrong leaves nothing behind. Keep the interactive handshake as the fallback for «none of them answered», not as the first move. Precedent: a manager selected the environment interactively and wrote its name into the brief as the address; the executor's listing held three indistinguishable placeholders, the probe found the right one on the first attempt, and the executor's retro proposed exactly this inversion of the fallback order.

- **Where entering the environment needs a HUMAN, test the access with the session's very first call — before reading the task, the spec or the knowledge base.** The natural order puts preflight after the reading, because preflight is a step of the pipeline and reading comes first in it. That order is right when access is yours to fix and wrong when it is not: a login only the user can perform costs their attention and their latency, and everything you would have read anyway can be read while they do it. One call at the top of the session — the liveness oracle the profile names — converts a dead session from a full stop in the middle of the round into a request the user is already working on while you build the plan. The cost is one call in the case where access is fine; the cost of the other order is the whole reading pass spent before the wait even starts. Precedent: a round read the task, the parent spec, the comment thread and the knowledge base, wrote the plan, and only then found the environment's session dead — the user's manual re-login was the round's longest pause, and it could have overlapped every one of those reads.

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

- **the user usually has several browser profiles, and they differ not only in sessions but in network egress — when access is refused,
  check first whether it is the right profile, not the environment.** The symptom: the environment answers with the same error (403/timeout)
  on **all** of its hosts, including the login page and the open services, and does so even for a request without cookies; from the shell
  the same URLs answer normally. This is not an expired session, not a block on the environment and not a broken login, but the wrong
  profile — one sitting behind a VPN, say, whose address the environment does not admit. The diagnosis takes one comparison of the external
  IP from the tab against the one from the shell, and the cure is picking another profile. **Which profiles are the working ones and what
  their ids are is a question you ask the user ONCE, after which it goes into the project profile and into the executor's brief**: otherwise
  every subsequent round loses the same half hour. Precedent: half an hour spent diagnosing «the environment has been closed off» — with a
  live environment and the correct account;

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

- **The rule below is about the ORDER of what dies with the access, not about the KIND of work — and those are
  different volumes.** «First the batch capture, then the interactive part» is a good proxy only while the
  unstable access gates the whole round; where one contour depends on the fragile session and another does not
  (an API with its own credentials, a queue read anonymously, a public artifact), the honest partition is «what
  dies with the access» against «what can be done at any time», and it usually cuts across the capture/interact
  line: the session-bound contour's *interactive* scenarios outrank the independent contour's *snapshots*. Say
  the partition in the brief, marking each scenario by which side it falls on, or a conscientious executor
  follows the letter and spends the fragile resource last. Precedent: a brief ordered the batch capture first
  and the independent API's negatives immediately after; the executor deliberately departed from it, ran the
  whole session-bound contour first and recorded why — the credentials-based contour could be caught up at any
  time, the session could not.
- **if access to the environment is unstable** (a short session, entry only by hand from the user, a flapping environment) — prescribe the
  order «**first a batch capture of all the evidence, then the interactive part**» in the brief: the contract/schemas, reference numbers for
  every filter value, samples of live records, anchor ids — into the result file within the first few calls, and only then the UI scenarios
  with a periodic access check. Then a loss of access costs you part of the scenarios rather than the whole round. Precedent: one approach
  burned down entirely on a dead session, and the second survived only thanks to this order;

- **if the waits in the brief exceed an hour** — decide and state explicitly whether observations may be spread across isolated environments
  (browser profiles, contours) and run in parallel: «one session at a time» forbids logging in over a live session but does not forbid two
  isolated environments, and without explicit permission the executor will choose the sequential route. Precedent: ~85 minutes of nearly
  pure waiting where two observations could have run in parallel;

- **a hypothesis about survivability, flakiness or «it breaks sometimes» requires a control instance** — prescribe it in the brief: one
  instance (a session, an application, an account) is set up as the control and only polled rarely, and every experiment is run on a
  **separate** instance. Otherwise the experiment spoils its own baseline and «it broke» cannot be told from the norm. In the same place,
  **name the budget of expendables** («one instance per hypothesis, N will do») — otherwise the executor either economizes at the expense of
  cleanliness or spends blindly. **Sanity-check the unit of the budget:** «no more than 8 activations» is meaningless if an activation is
  precisely what does not produce an expendable operation. Precedent: activation did not create a screening — which turned out to be the
  round's main finding, and the budget had to be recomputed on the fly. Count in what is actually spent, and allow the executor to recompute
  against the facts. Precedent: a non-deterministic session loss could only be described after the executor assembled a long-lived control
  session on the fly — ~15 minutes and three burned instances. **Compute the budget as «the minimum per scenario + 1 for an environment
  transient»**: in one session a budget of «2 + 1 spare» came out at exactly zero, and had the last expendable burned on a browser-extension
  transient, the last scenario would have gone uncovered;

- **On a round about APPEARANCE, «may the executor resize the window and take the focus» is a load-bearing condition of the whole round —
  settle it with the user at preflight, before the scenarios are sliced.** The shape: the user shares the environment the round observes
  through (their own working browser, desktop, terminal), and the scenarios that measure layout are built on changing its geometry. Ask it
  early and the round is sliced correctly; ask it late — or never — and the restriction arrives as a scope correction **after** the action has
  been performed, which is the expensive order: the measurements are already taken, the time is already spent, and the scenario they served
  is struck out. Two riders on the phrasing. The request to the user is not «keep the window in front» but **«do not work in this environment
  for the duration of the round»** — otherwise the executor and the user fight over the focus, and every observation the executor takes while
  losing that fight is void. And the ban on **taking** the focus programmatically belongs in the brief from the start, with what to do
  instead (record the degraded channel, switch to the non-interactive part, re-check later, escalate) — an executor who discovers a working
  way to raise the window will use it, and it is the user's attention that pays. Precedent: both corrections («stop resizing», «do not force
  the focus») arrived mid-round after the corresponding action; the round's whole width-threshold scenario was struck out with its
  measurements already spent, while the parts the executor could have closed instead stayed uncovered.

- **When the round's whole block rests on an EXTERNAL instrument — a public request sink, a mail catcher, a tunnel, a third-party sandbox — preflight has to open it, because the thing most likely to block it is your own harness, not the environment.** The lever check in `planning.md` is written against levers that rot on the environment; this one fails differently and earlier: the instrument is alive and perfectly reachable, and the session's own safety classifier refuses to navigate to it or to script writes against it, because a service whose whole purpose is to capture arbitrary requests looks exactly like exfiltration. Discovered by the executor mid-round, that costs the block twice over — they cannot lift the policy, and no amount of retrying changes it. So open the instrument during preflight, and where it is refused, put it to the user **before slicing the plan**, as a choice with prices: allow this host, stand up a receiver they control, or drop the block to a later round. Two riders. The refusal is rarely total — in one round reads and UI clicks passed while scripted `POST`/`PUT` to the same origin stayed blocked — so measure which half works and hand the executor that dated split, along with the instruction to configure the instrument by its own interface rather than by script. And whatever the instrument's free tier caps (retained requests, response options, lifetime) is measured in the same pass, because those numbers size the scenarios that will use it. Precedent: a round whose main block was webhook delivery found the agreed receiver refused by the classifier at preflight; one question to the user restored it, the scripted-writes half stayed blocked, and the brief carried both facts — the executor configured the receiver by clicking and closed sixteen requirements.

## What goes into the brief

- **Endpoint names and HTTP methods are verified before they go into the brief; the product's own documentation counts as a summary, not as
  a source.** A name taken from someone else's summary or description without a request body is confirmed by recon (environment logs, docs)
  or marked in the brief as unverified, and an endpoint found only in the docs gets one probe call before a scenario is built on it — **the
  path and the method together**, because a wrong name costs the executor a tour of 404s. Precedent: an operation that exists only in the
  documentation answered 404 on the environment, while a neighboring endpoint carried the scenario through on an undocumented parameter; in
  another round a documented endpoint was written into the brief as a POST and turned out to be a GET with query parameters;

- **Scenario parameters that depend on the environment's data are given as a selection criterion, not as a value.** The method type, the
  currency, a specific entity — «a method the entity actually has», with the concrete value offered only as an illustration: a fixed value
  copied from the docs may not exist on the instance the executor picks. Precedent: a source value taken from a documentation example turned
  out to be an empty slice for every account on the environment;

- **Mark, for each scenario in the brief, whether the executor can close it alone or whether it depends on their own limits — and put the closable ones first.** An executor's boundaries are not visible from the plan: some calls they refuse by their own rules (financial identifiers, an operation that could succeed in transferring value), and the refusal arrives only when they try. Order the scenarios so that the round's evidence is collected before it can hit a wall, and say per scenario which side of the boundary you expect it to fall on — the executor will correct you from the environment, and that correction is itself useful. Precedent: a brief put the decisive measurement first, it turned out to be exactly the call the executor cannot make, and three calls went into an attempt doomed from the start — while the scenario the brief had labelled «the main open risk» and placed second was the one that carried the whole round.

- **with `test-cases: upfront`, the brief carries the analyst's case ids and the verdict on the requirements**. The right to edit is decided
  by the case's own line, not by the session as a whole: an expected result whose source is `spec` is untouchable — a mismatch with it is a
  defect, and rewriting the case to match the facts would legitimize work done against the requirements; an expectation sourced from an
  `assumption` or the `KB` the manual tester refines against the facts, noting the edit. **Steps and preconditions they always refine, in
  both modes** — those are technique (the UI path, the endpoint name, the way to create an entity), not requirement, and forbidding it would
  simply stall the run on «the case says press a button that isn't here»;

- **Every observation you hand over is dated, and carries the boundary of the sample it was taken from.** Two halves of one rule. *Numbers
  describing the environment's state* — from a previous round or from your own recon — go in with the date they were taken and an explicit
  caveat «re-check that the precondition is still alive»: contract constants (TTLs, limits, operation names) are stable, state is not, and
  on a shared environment a reservation is released by a timeout, applications are wiped by someone else's run, limits are changed by a
  neighboring session. The phrasing: «taken on <date>; if the precondition no longer holds — do not bend it, look for a direct discriminator
  of the source and say so». *Counts of observations* go in with the window, the filter and the page they were counted over: «observations
  4/4/3» without «taken over such-and-such dates» leaves the executor unable to tell a discrepancy from their own mistake when their own
  sample yields different numbers — they will either spend a pass reconciling or, worse, bend their scope to match yours. Precedent: an
  executor handed «the initiator's limit is taken up by an application, so the free remainder is 0» built their proof on it, and the
  reservation had been released a day earlier — the fix was proved another way only because they went and checked the precondition.
  Precedent: recon looked at three days while the brief required the whole retention window, the full window added a run the manager had
  never seen, and the executor lost a pass working out whose numbers were right;

- **A check able to REFUTE the round's central hypothesis goes in as the brief's first step, never at the tail of the reading list.** The
  tell is what it reads: the rest of the round reads *behavior*, while this one reads the *source of truth* — the machine-readable contract,
  the schema, the spec, the declared route table. Such a check is cheap (seconds) and asymmetric: confirming it changes nothing, refuting it
  invalidates every scenario built on the hypothesis, so its position in the brief decides whether the round is rebuilt at the start or
  discovered wrong at the end. Two failure modes, both from the same misplacement: written into the reading list as a minor aside («from
  that file only the fact of X is interesting — grep it, do not read it»), it gets done late or not at all; and once the scenarios are
  already sliced around the hypothesis, an executor who does refute it has to redesign mid-run on their own budget. Precedent: a round's
  whole hypothesis table rested on «this operation does not exist on the environment», measured by trying paths by hand; the contract file
  sat in the brief's reading list as the last line of the «not needed this round» block, the executor grepped it anyway, and it named the
  operation's real prefix in five seconds — every hypothesis of the plan had been formed from paths that were never the contract's.

- **Constants uncovered by your recon go into the brief as numbers, not as a retelling.** Recon hands the executor not only the conclusion
  («there is a retry limit», «there is no extension») but the values themselves: the storage key, the TTL, the timer period, the retry limit
  and intervals, the operation names. Recon retold in words forces the executor to obtain them all over again — in one session they grepped
  the bundle themselves although the manager had already seen those numbers. Separately, for FE tasks: the question «is the fix deployed?»
  is answered most cheaply by grepping the served bundle for the names from the task description (that is an observable distribution, not
  reading the repository's code) — in one session two curls and a grep took 2 minutes and produced the round's main finding, confirmed
  afterwards by black box;

- **Recon constants are two different kinds, and only one of them may be handed over as fact.** *Contract values* — limits, thresholds, operation signatures, dictionaries, format lists — are what the running system enforces, and they belong in the brief as numbers (the entry above). *The composition of the interface* — which controls a menu has, which columns a table shows, which actions a row offers — reads out of the same artifact just as crisply and is a different kind of claim: a string in the bundle only proves that a string exists, not that any component renders it. Mixed into one table of «what is already known», the second kind inherits the authority of the first, and the executor meets a screen that does not match it. So split the table, or mark the composition rows explicitly as «expected from the artifact, confirm by looking» — and add, in the same line, that a mismatch is a result worth recording rather than a discrepancy to reconcile silently. Precedent: a brief listed a row menu's three items from the localisation map; the live menu had two, and the third operation was implemented in an entirely different control — the executor perimetered it correctly, but only because the brief demanded behaviour over artifacts elsewhere. **A third kind hides inside the first: an oracle built on what a FIELD IS CALLED.** A pair of fields whose names promise the distinction the round needs — requested against actual, planned against effective, original against current — reads as a contract value because it comes from the same schema as the real ones; it is in fact a guess about semantics, and the moment it is wrong the round's primary measurement is gone. It is also the kind of guess live data will not refute in advance: on the records available at planning time the two fields are equal, which is exactly why the pair looks usable. So hand such an oracle over as a hypothesis with the sentence that names its failure — «if these two turn out to hold the same value, the oracle is dead, do not interpret it» — and never make it the primary: put a mechanism-based oracle first (a recomputation, a categorical switch) and let the field pair confirm it. Precedent: a brief offered a field pair as the way to tell two amounts apart, noting only that it was degenerate on the records seen so far; it was degenerate on the target records too — the field named for the original value holds the current one — and the round survived on the arithmetic oracle that had been written in as the fallback. **And a hypothesis read out of MINIFIED code is handed over as the excerpt itself, never as its meaning.** Recon on a bundle yields two different things, and the brief usually flattens them: the strings are quotable, while the control flow around them has to be reconstructed by eye from renamed identifiers — so the manager writes down what they concluded the code does. That conclusion carries a model nobody verified, and it is worse than no hypothesis at all, because the executor spends probes on the branch it invents. Paste the fragment, name the identifiers as they appear, and let the executor read it against the screen; the fragment costs two lines and it is the only part of the observation that is actually evidence. Precedent: a brief said a status label was produced through a lookup with a fallback, so the collapse of several statuses into one caption would only appear where the dictionary key was missing; the code held a plain conditional with no lookup at all — the collapse was the main branch, and the executor burned probes proving the fallback theory wrong before measuring what the screen actually did.

- **A contract read out of the CLIENT's own query documents carries names without types — handing it to the executor as «introspection, you can rely on it» seeds a contract that is wrong in exactly the places nobody will re-check.** The artifact is seductive because it looks like the real thing: a served bundle, a generated client or a captured request embeds the query text verbatim, field for field, so the composition it yields is genuinely accurate. What it cannot carry is the *type* of any field — the query language names fields, the schema types them — and a manager transcribing that list into the brief fills the types in from the shape of the name. Every guess is plausible and several are wrong in the same direction: a plural-sounding field turns out to be a scalar, a singular one a list, a nullable one non-null. The round survives it when the brief's first step is an independent introspection (the executor simply re-takes it); it does not survive when the manager's table is the only source, and it is invisible until something machine-readable is built on it. Two lines close it: mark **the source of every contract row** — «from the client artifact: names only» versus «from introspection: names and types» — and never let the first kind carry the phrase «can be relied on». Precedent: a brief handed over a liveness contract taken from a bundle's embedded query text under the heading «facts of the contract (introspection)»; the executor's own introspection disagreed in four places — two fields were lists rather than a scalar and an object, two more were non-null — and the executor's retro noted that a test written from the manager's table would have been red on the first run.

- **A profile rule that the executor breaks before they get around to finishing the profile must be duplicated straight into the brief — as
  the first line of the reading list.** This concerns rules about reading itself and about the order of work (what to open files with, what
  to read before the first request to the environment, where not to go): the executor takes their first action before reaching the relevant
  paragraph of the profile, and the rule fires into the void. Precedent: «open profile subfiles only with Read, not `cat`» sat in the
  profile's header for three runs and was broken all three times — the executor's first action is a `cat`, and the paragraph forbidding it
  is read after;

- **A scenario whose expectation is written as a RESPONSE CODE gets a second half — «and establish what actually happened» — or it is closed
  on the code alone.** «It must not answer 5xx», «expect a 200», «check it is not rejected» are convenient to write and easy to verify, and
  that is the trap: the code says the call was accepted, never that the operation did anything. An endpoint whose whole job is to trigger a
  side effect can answer perfectly while doing nothing at all, and a status-only expectation licenses the executor to stop before the
  interesting part. Pair every code-shaped expectation with the observable effect and the channel that shows it — the journal, the log line,
  the receiver, the changed record — even when the scenario's requirement is genuinely only about the code. The cost is one extra read; the
  cost of omitting it is that a wide executor closes the gap on their own initiative (and you were lucky) while a narrow one does not (and
  nobody notices). Precedent: a scenario briefed as «the resend endpoint must not answer 5xx» came back `200 OK` — the executor went to the
  logs and the receiver unprompted and found the call to be a silent no-op that an administrator cannot distinguish from a real resend, which
  was the round's most interesting observation and had no place in the brief that produced it;

- **After negative permission probes, require an explicit step: read the journal/audit log for the run's window and check what the
  refusals were recorded as.** A rejected call is supposed to leave either nothing or a refusal event; systems routinely record it as a
  performed action instead, and that defect is invisible from the call's own response — the executor sees a clean `access denied` and moves
  on. The step costs one read, it is the only moment in the round when you know exactly which calls were refused, and it doubles as a check
  that the negatives really changed nothing. Precedent: two Major findings (rejected calls written to the journal as completed operations by
  roles forbidden to perform them, and an actor's role field carrying the SSO group instead of the system role) surfaced only because the
  brief happened to ask for every action in the window to be listed — nobody had planned to look.

- **If a scenario may run into a neighboring contour with a different entry** (another environment, another account, entry by the user's own
  hand, a closed network) — **write in the brief in advance what to do**: request access through the manager (and what exactly to ask for,
  in one phrase) or record an open question and move on. Without that line the executor decides for themselves and usually leaves the
  finding unproven in silence, so as not to spend the user's round. Precedent: a key finding (the admin panel shows a third of the
  organization's funds) ran into one request to a neighboring environment behind basic auth and stayed hedged — while one entry agreed in
  advance would have closed it in the same round;

- **if a scenario needs reference values (cryptographic constants, test vectors, test addresses), explicitly allow taking them from public
  sources with a note on where from** — otherwise the executor spends time on the doubt «doesn't this count as inventing evidence» and may
  give no values at all, devaluing the retest protocol. The phrasing «take them from public sources per <standard> and cite the source» is
  unambiguous; «if you can write them out» is not;

- **a negative that needs an entity belonging to someone else gets a concrete identifier in the brief — found and verified by you, not a
  pointer to «take one from the knowledge base».** Refusals of the kind «this address / account / document already belongs to another party»
  cannot be provoked with a value the executor invents: it has to be a real foreign entity, and it usually lives in a contour the executor is
  not logged into at that moment. A pointer instead of a value costs either a wasted search or an extra role switch, and the switch is what
  hurts — mid-run it can cost a whole login cycle. Check the identifier exists at recon time and paste it into the brief; if you genuinely
  cannot get one, say where to look **and** say to collect it during the snapshot pass in the other contour, before the run leaves it.
  Precedent: the brief said «take an address of another company from the knowledge base», it was not there, and the executor was saved only
  by having happened to take the snapshot under the other role first;

- **A step whose whole point is «the same action under a different role» begins with identifying the session, not with the action.** Switching identity is a side effect of tooling — a cookie jar, a header, a client instance — and tooling substitutes a default silently: the call goes out under the previous, usually more privileged, identity and answers exactly as the scenario hoped it would not. Nothing in the response says whose it was. Require the order explicitly: after switching, call the «who am I» endpoint and print the account and its permissions into the result, and only then make the target call. On a mutating scenario this is also a budget guard — the misfire is spent from the expendables and, where the operation has no rollback, it cannot be taken back. Precedent: the decisive permissions probe went out under the superadmin because a helper received one argument too many; it was caught afterwards, from the author id in the journal, and cost one unbudgeted irreversible mutation plus a re-run;

- **a compound requirement gets a compound verdict.** Half the requirements of a typical spec are «and»: «the status changes **and** the
  officer sees it», «up to five attempts **and** then it is recorded as FAILED». A binary pass/fail on such an item lies in both directions:
  a «pass» hides the half that was not met, a «fail» buries the half that works. Require a third verdict in the brief — **partial, with an
  explicit breakdown of which half passed and which did not** (in one session there turned out to be 14 such items out of 89 — more than the
  clean fails);

- **if a scenario requires actions from the user mid-run** (the profile limits the executor — clicks that move funds, say), include a
  **pause protocol** in the brief: the executor prepares everything up to the point (forms, intercepts), appends to the result and ends its
  turn with a request message («CLICK NEEDED: the environment, the tab, the button, what will happen»); the manager relays that to the user
  and returns the confirmation **by a direct SendMessage to the same agent** (not a fork, not a new agent). **Name the environment the click
  must happen in — the browser profile / instance id, not only the tab**, whenever the user has more than one: the tab identifier means
  nothing outside the executor's own group, and the wrong profile can be one where the environment is unreachable. Where profile labels are
  user-editable, name the id and say the label is not an address. Precedent: the user asked for it in as many words — «always say which
  browser profile». The same request line warns about **autofill**: a login form arriving pre-filled with a neighboring account (with its
  saved password) turns one confirming click into a session under the wrong identity, and every check built on it into a false one — so state
  the exact account to type, and after the pause verify **whose** session came back, not whether one is alive. **If the value the user will see on screen is
  not known in advance (it is computed when the window opens, it depends on live data) — give them not a number but a boundary: «click at
  any value up to X, above that — do not click».** Asking «tell me the number the window shows» can be impossible in principle, while a
  boundary computed in advance removes both the extra approval round trip and the risk of a wrong click. Precedent: instead of an
  unpredictable rate, the user was given a ceiling inside which confirming is safe at any outcome. Group the pauses into series; after a
  pause the executor starts by re-reading the actual state rather than from expectations (the user may have done not all of it, done it long
  ago, or not done it). A pause of a day or more nullifies the page's prepared state — fill forms in only while the user is available. **Two
  fields the request line must always carry, or the user is confirming a button rather than an action: what the step will do TO THE STAND
  (amount, recipient, which entity changes) and what KIND of window it is — a free, reversible signature or an irreversible transaction that
  costs a fee.** The executor will not add them on its own initiative, and the manager ends up dictating both mid-run. **And do not demand
  that a signature and the send be merged into one request — that is physically impossible**: between them the executor must click «Send» on
  the page, and by then its turn is over. The form that does work: warn about the second window in advance and ask the user to stay at the
  keyboard. **Say in the brief what to do when the user clicks the wrong thing** (confirms where cancel was asked): the mistaken click is
  recorded as a fact and the scenario is NOT replayed if the stand was not affected — otherwise the executor burns a turn deciding this on
  its own. **When the result is visible ONLY to a human (a chat message, an email, a screen with no API), require the executor to state a
  verifiable expectation as a number BEFORE the observation** — «I expect one message with six items in the order A→B→C», not «take a look
  at what arrived». Then an ordinary human answer «all as planned» becomes usable for a verdict: what gets confirmed are concrete numbers,
  not a general impression. The flip side — **the limit of confidence is written explicitly**: «confirmed in aggregate, per-item timestamps
  were not taken», otherwise a month later the report reads as re-verified evidence. Precedent: the entire verdict on alert merging rested
  on numbers stated in advance. **Mark, in the same list, which of those points the executor can obtain without the human** — an orchestrator
  history, a job's input payload, a delivery log often hold half of them; then a human answering «all done» in one phrase does not block the
  verdict, and the report says precisely which half rests on the machine and which on the person. Precedent: of five points put to the user,
  three were closed by the invitation workflow's own input (the link's host, path and parameters), and the user's one-line reply cost nothing;

- **if after the recon not a single step remains that can be performed by hand** (everything verifiable reads out of the logs/execution
  history, and the rest needs access that does not exist) — do not launch the executor: a brief with no content burns a round and returns a
  retelling of your own recon. Then put the recon's evidence into the session folder as a separate file (`<N>-recon-<source>.md`) and **name
  in the report, explicitly, the reason there was no manual run** — otherwise the reader will assume the step was forgotten;

### What you have not checked yourself is handed over as a question

**Anything in the brief you did not verify goes in as a question with the reason it matters — never as a fact, a verdict, or a menu of answers.** The executor cannot tell your certainty from your phrasing, and each wrong wording closes the search its own way: a stated fact is not re-checked, a pre-authorised «not covered» is adopted, a listed outcome is chosen from. The cost is invisible in the result file — it comes back as a legitimate-looking row nobody can tell from a real one.

- **A claim about the state of the ENVIRONMENT, least of all one with the verdict attached.** «There is no such object — record it as not covered and move on» looks like sparing the executor a search; it closes the search, and confirming a negative is indistinguishable from never having looked. Shared environments accumulate objects nobody in this session created, so your belief is at best a dated observation. Write the question plus the stake: «is there an object in state X? it would close requirement Y». Precedent: a brief asserted the environment could not hold an entity in the pre-approval state; one aggregate query found nineteen of them, a third of all tenants — the fixture several rounds had declared unreachable had been sitting there the whole time.

- **A doubt about what an INSTRUMENT can do.** You do not know whether the receiver can delay its reply or the console exposes that filter, so «if there is no such setting, record it as not covered» hands the executor your uncertainty as a verdict they may adopt without looking. Phrase the two-step it is: «check whether the instrument can do X; if it can, that closes requirement Y». Precedent: a brief hedged about whether a request sink could delay its response; the setting sat in the same dialog the executor was already using, and half an acceptance criterion two rounds had left uncovered closed in five minutes.

- **A seeding route you have not run yourself** — «run X and it creates A, B and C» reads as verified, so the executor spends their attempts making that route work instead of asking whether it is the right one. Two failure modes seen in one round: the claimed producer created nothing (the provisioning lived in a neighbouring step of the same suite), and the claimed path was forbidden outright by server-side validation. The wording: «as far as I know this route yields …; I have not run it — if it does not, the question is "what else in the system produces this state", and the answer goes into the result».

- **A hypothesis about the SHAPE of the fix, phrased so that refuting it is not a verdict.** «If the argument is gone from the schema, the fix is structurally confirmed» saves a round when you guessed right and misleads when you did not — the fix may have been made by validating the value instead of removing the field. Always add: «the marker not being found is not a verdict, verify by behavior». Precedent, round 3: the contract-address argument stayed in the schema and is still required, while the fix was a server-side comparison of the value — a behavioral experiment gave `pass`.

- **The fixer's correction to YOUR previous round's DESCRIPTION is a claim about observable state — quote it as theirs, never build the scenario around it.** When a team accepts a finding they often amend how it was described: «the order is the reverse of what you wrote», «that mode never actually engaged», «the blast radius is narrower». The correction is welcome and usually partly right, and it arrives with the authority of whoever owns the code — so it slides into the brief as the round's expected state and quietly reshapes the block built on it, leaving the executor measuring against the author's model instead of against the requirement. Quote it verbatim, attribute it, and name the observation that settles it; the executor's measurement is the verdict, the author's account is not. Precedent: a fix comment said a signing pause «never engaged once, the flag has been false since the migration» — the retest found the flag engaging and clearing normally, and the whole block had been framed around the author's version.

- **A list of a probe's expected outcomes BIASES the executor** — «two outcomes are expected, and both are valid» reads as a menu, and the result gets filed under the nearest listed heading instead of described. Give the question, give the outcomes only as illustrations of why the probe is worth running, and close with «any other outcome is also a result, and a third one is more valuable than either of these». Precedent: a probe brief anticipated a refusal or a success; the server did a third thing entirely — rejected the value by its own domain check, before the external system was consulted — and the executor flagged that the wording had nudged them the other way.

### A sanctioned mutating probe: what the permission must also say

**A probe is authorised as one call, and the brief answers in advance everything the executor would otherwise decide alone, mid-probe, with the mutation already half-performed.** Four questions recur; each costs a clause to write and an unbudgeted artifact — or the round's sharpest measurement — to omit.

- **May the hostile values be COMBINED?** Escaping, encoding and injection checks come as a matrix (a separator, a quote, a newline, a leading formula character), and one artifact usually carries all of them at once — four mutations become one and the restore shrinks to a single call. The conditions to state with the permission: the values must not mask one another (each stays individually identifiable in the output), and if one fails the operation, the merge is unwound into separate probes. Precedent: four hostile characters were folded into a single rename by the executor's own initiative, closing the escaping requirement in one mutation and one restore.

- **What if it fails in an UNANTICIPATED way — is a control call in the budget?** Off-script, the executor faces a question the brief never answered: is a second call (the same operation with a value known to work, proving the refusal is about the value under test) covered by the permission? Write the branch: «if the refusal names the cause literally, the mechanism is proven by the response and no control is needed; if it is generic, one control call with <a value known to resolve> is authorised — and here is what it will leave behind». Precedent: the probe was refused with a self-explanatory message and the executor judged a control unnecessary, recording why — the right call made without cover, and on a vaguer message the round would have stalled on an approval round trip.

- **When the probe is «overshoot the available amount», cap the OVERSHOOT, not only the probe.** The reverse operation routes the whole excess back through the fixture, so a carelessly chosen overshoot parks an absurd intermediate state on a shared object for as long as the restore takes and leaves a journal entry of that size forever. One clause: «exceed the available amount by the smallest amount that still proves the guard is gone» — and the evidence gets sharper besides. Precedent: an executor overshooting a balance kept the excess minimal on their own and noted in the retro that the brief had not said to — the restore had to pass a sum two orders of magnitude larger than anything else in the round through the same account.

- **When the reverse is already known not to work, say so and declare the residue expected.** A reversibility protocol reads as a promise the executor must keep, so a known defect that makes the restore impossible costs twice: attempts spent hunting for a way back that does not exist, and the probe skipped rather than break the protocol. You usually know before the round — it sits in a review-remarks entry or a comment on a neighbouring task, read at step 1. One line: «the restore of this field will probably fail, that is the expected artifact and itself the evidence, not a failure of the protocol; record it under environment artifacts». Precedent: a probe aimed at the one field whose clearing was already filed as a deferred remark came back with the value stuck on the environment — the right outcome, obtained without cover, and the executor's retro asked for exactly this line.

## A retest round

- **The build's fingerprint is an item of the brief — taken FIRST, repeated as the last action, and again immediately after any anomaly.** Taken only at the end it is taken after the fact, and a deploy landing mid-round goes unnoticed with half the measurements describing one build and half another; taken at both ends, the pair also answers «did the environment change under us». The third reading is triggered by an event, not by a position in the sequence: an anomaly (data vanishing, sessions dropping, 5xx on a healthy endpoint) is exactly when the answer matters most, because it decides whether the earlier evidence describes the same build as the later. Require an answer even a negative one — build versions are usually opaque hashes and tying them to a commit without repository access is impossible, so «development must confirm the fix is in the build» is a full result, while silence lets the reader take as verified something never checked. Acceptance then requires the version the run actually exercised (the bundle hash, the deploy ref, the image version), or the verdict cannot be tied to a build and the next retest starts with archaeology. Precedent: a round took the fingerprint at both ends as instructed, and the redeploy that had wiped the environment mid-round surfaced only because the executor happened to re-read the deploy jobs after re-seeding; in another session a retest had to reconstruct indirectly that the round before it had run on the previous bundle, meaning part of its conclusions applied to a different build than assumed. How the same reading dates a retest's trigger and decides the environment is in `planning.md`, «Dating the build».

- **«Nothing has changed since the last round» is a claim about a fact, and the fingerprint does not establish it — one behavioural probe does.** Every cheap signal agrees: no status movement, no new comments, the fingerprint matching digit for digit. The conclusion is wrong because the fingerprint answers a narrower question than it appears to — usually «was the client rebuilt», never «did the server change»: a service can be redeployed without touching the version it reports, and behaviour a whole round rested on moves with it. So before proposing that a round is pointless — and before writing «the environment is unchanged» anywhere — spend the one call that probes the previous round's sharpest finding directly: request the blocked page, call the failing operation, read the field that was wrong. Say the general form in the brief, because it governs every verdict the executor is about to write: **matching versions are not grounds for inheriting a single one of the previous round's measurements.** Precedent: a round whose every external signal said «nothing moved» was running on a server redeployed in between, and the previous round's Blocker had been fixed — «do not run the round at all» had already been put to the customer as a legitimate option, and the probe that refuted it was one call.

- **on a retest, first check that the observation path itself is still alive, and rest the verdict on the final artifact rather than on an
  intermediate UI state.** A «symptom of the defect» goes stale together with the build: in one session the symptom was «zero checkboxes
  ticked while storage is non-empty», and on the fixed build the dialog started closing by itself — a DOM snapshot taken during the closing
  animation looked exactly the same. The executor nearly recorded a false reproduction and was saved by a control file. Rule: a retest
  verdict is settled by the result (the file, the record, the callback); an intermediate state is only a hint;

- **Set the retest of a finding on substituted responses rather than on an expendable instance when what is being checked is the client's
  reaction.** If the finding is about how the system responds to a refusal (logout, retry, rollback), the reaction is reproduced by
  intercepting on the client side: no expendable is spent, no one else's state is spoiled, and the run is repeatable. Leave the real refusal
  for a single control run. Precedent: during the retest the expendables ran out and a stray live session turned up in the environment —
  emulation delivered a full verdict on two requirements where the real path was already unavailable.

- **A retest verdict is passed on the scope of the FIX, not on the original wording of the finding — and a defect found beyond that scope
  is a new finding, not a live one.** Findings are usually written broadly («this role can be granted at all»), while what the team accepted
  is narrow («remove it from the form»). Verify both, but report them apart: the narrow task is closed on its own merits, and whatever the
  round found outside it — the same outcome reachable by another route, a neighbouring layer, an API path around the UI — is filed as its own
  finding with its own id and its own place, usually the side-findings registry. Merging the two reads as «the fix did not work», which is
  false and costs the developer a pointless round; splitting them keeps both facts and lets the customer decide the priority of the new one.
  The place to settle this is the brief: state the fix's scope verbatim and require a separate verdict on it. Precedent: a round reported
  «the fix is cosmetic, the defect is alive on the server», and the customer's answer was that the task had been to change the form — done —
  while the server-side route was a separate defect for the side registry.

- **When you quote a previous round's finding into a retest brief, say whether each value is a RAW ENUM or a caption the user sees.** Findings are written from evidence, so they mix the two freely — the technical line names the enum, the business line names the label — and the compression into a retest brief usually keeps whichever was shorter. The executor then meets a screen whose captions do not match your quoted list and has to decide, mid-run, whether the product changed or the brief is loose; on a retest where the round's whole question is «what is different now», that doubt is expensive precisely when it is least affordable. Mark each value at the point of quoting («the filter sends `NEW`/`UNDER_REVIEW`, the dropdown shows «New»/«Under review»»), and where you only have one of the two, say which one it is. Precedent: an executor lost half a minute deciding whether a dictionary had changed under them, and was rescued only by remembering that the bundle hash was unchanged and the captions had nowhere to change from.

- **In a retest brief, write out not only «what recon says is fixed» but also «what remains».** Recon of a distribution usually shows both;
  a remainder named in advance gets checked by the executor in the same motion and comes back as a separate finding rather than as a doubt.
  Precedent: «the refusal branch is inverted, but the retry limit is still there» — both halves were confirmed, and the remainder became a
  Minor finding with no extra pass.

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

- **A degraded channel still produces output** — a window in the background, a minimized viewport, a throttled tab, a stale cache, a session in a reduced state. Structure comes back, sizes come back, elements are found, and yet controls report the wrong state, labels collapse, disabled and hover states are invisible, selections do not take. Everything about it invites a defect report, because the executor is looking at real output. Precedent: two defects were nearly filed from a background window — a control that «silently does nothing» and a field showing a count instead of a name; in the foreground both turned out to be correct behavior.

- **An instrument is armed in the SAME call as the action that produces the event.** Set up after the target screen is reached, an observer records the state *after* the transition, and the timing evidence can only be re-taken on another expendable; and one that wraps a global the application already captured — a constructor, a fetch, a timer held in a closure since bundle init — reports an empty log while the mechanism runs perfectly. So before writing «the product never does X» from an empty log, exercise the instrument on your own object and say in the result whether it caught it. Related trap: the first entry of a «record only changes» accumulator is always written, and it reads exactly like the moment of transition — never date anything by it. Precedent: a frame logger wrapped the constructor after page load and stayed empty through a fully working push channel; the executor's control socket was the only thing that stopped «the application opens no connections» from going into the report.

- **A tool that reports success has not necessarily done anything** — a resize, a click, a navigation, a cache reset: the harness reports what it dispatched, not what the page did. The line: «after a step that changes state through tooling, read back the state itself — the width, the DOM, the URL — and if it did not change, record "not covered, the tool does not work" instead of trying variants». Precedent: four window resizes all answered «successfully resized» while the viewport never moved, and the round lost the measurement it was sent to take.

- **The next round of that lesson: the tool did something, and what it did was BREAK the channel — then it is banned outright, not wrapped in retries.** An instrument that changes the environment's presentation can succeed at its own job and push the observed surface into the degraded state above, so the measurement never updates and a stale number reads as a fresh one. Diagnose it by reading the channel's health **after every application of the instrument** — checking before it is checking the wrong moment — and then say «do not use it at all»: a «three attempts, then escalate» rule instructs the executor to break their own channel three times, while the honest «not covered, the tool destroys the measurement» is reachable on the first. Precedent: a resize tool reported success and left the measured width unchanged — it was moving the window off the screen, which occluded the tab and stopped the renderer from recomputing the viewport.

- **The stamp of the channel's health is taken in the SAME call as the numbers it certifies.** Checking and then measuring are two moments, and the gap is enough for the user to click elsewhere, a window to lose focus, a session to drop a privilege: the measurement then looks clean, is void, and nothing in the result shows it. One line, free to the executor: «return the channel's state together with the values, in one call, so every measurement is self-certifying». Precedent: an executor arrived at the trick alone, near the end of a round in which several measurements had already been discarded.

- **A shared resource is addressed by the identifier the tool handed you, never by a substring of its name, title or URL.** The user's environment holds dozens of near-identical objects, so a matcher that resolves uniquely at the start stops being unique the moment the round moves to a second environment, and the next call silently operates on somebody else's object — the measurement becomes unattributable and the user's own state is disturbed. The line: «resolve the target once, by the id the tool reports, verify it against your own session's object, and never re-resolve by matching text». Precedent: CDP scripts matched by a URL substring; after switching to the control environment one of them navigated a tab belonging to the user — one discarded measurement, and a stranger's tab left pointing at the wrong environment with the original address never known.

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

### The executor stopped

**How you restart it depends on WHY it stopped, and the wrong move costs either the run's context or the environment.**

- **It died on an infrastructure error** (a dropped connection, an API timeout) — **resume it with a message**, saying what has already been accepted and need not be redone and restating the remaining order of work. A new launch loses the run's context and repeats the expendable actions.

- **The user killed it** — then it is not resumed: a new launch, with an explicit instruction to read the existing result in full and continue from it rather than replay what is done. An incremental result makes that possible — precedent: a killed executor's own result file carried enough of the run for the replacement to pick up mid-scenario instead of starting over.

- **You killed it after it had already touched the environment — the cleanup is now yours.** Killing an agent runs no rollback: whatever it set up stays set up, and the executor's own restore step (usually its last) never runs. Look first at **global settings** — the ones a test switches on at the start and restores at the end; they are visible in the code as a «save the original …» step, and their original values are usually printed in the run log. Restore them, **confirm by reading**, then record in the report what was left and what you returned. Precedent: an automator stopped mid-run left a global anti-fraud rule switched on for the whole shared environment — every account was one failed operation away from an automatic ban, and other people's runs would have collected false bans; the original values were recovered from the killed run's own log.

- **It stopped at «waiting for the background run to finish» — that is a checkpoint, not a failure**: no notification from its background process will reach it. Take the waiting on yourself (a background until-loop over the run's log file with success/failure markers and the stop condition «the log stops growing»), then resume the executor with a message carrying the verdict and the path to the log. Precedent: an automator stopped at «waiting» three times, the manager waited for the log and woke it up three times — and not once was work lost.

## Accepting the result

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

- **«survived / did not reproduce» is accepted only with the boundary of observation stated**: «alive ≥600 s» without the note «we did not
  look further» reads as a property of the system while describing only the length of the run. Precedent: a round's conclusion «the control
  session is healthy» rested on a 600 s boundary — in the next round the same session under the same conditions died at second 700, and the
  finding's priority changed to Critical;

- **A task whose whole description is a list of missing things is a requirement of EXISTENCE, and everything about the QUALITY of those things belongs to the contour that will use them.** The shape is common on follow-up tasks: the description reads «absent: A, B, C» and nothing else — no acceptance criteria, no behaviour. Once the fix lands, the round is suddenly rich: the new things exist but are unvalidated, unpopulated, untyped, missing a dictionary, or writable only through half a path — and every one of those looks like a finding of this task, because it was found in exactly the code the task delivered. It is not. The verdict here answers one question per item of the list, «is it there», and each quality defect is filed against whichever task owns the use of the thing — the editing form, the process that populates it, the consumer. Get this wrong and the findings table triples, the customer re-scopes it back by hand, and the genuinely unmet items of the list get lost among defects that were never in question. Two riders that repay the discipline. Re-scoping moves findings, it does not withdraw them: they keep their ids, their priorities and their evidence, and gain an addressee. And **the premise «quality is someone else's task» has to be checked against each finding rather than applied wholesale** — the ones it does not cover are the round's most valuable output, because they have no owner at all: a field nobody types by hand is not covered by «the form will fill it», and a write path that rejects a mandatory field is a precondition of that future task rather than a consequence of it. Precedent: a round filed seven findings against a task whose description was a list of absent fields; the customer's frame («this task only asks for the fields to appear») left three — and the two findings that the frame demonstrably failed to cover turned out to be the ones at risk of falling between tasks entirely.

- **A field that exists but is empty on every record is a defect only where the SYSTEM fills it, not a person.** After a migration lands, the honest first reading of «0 out of N populated» is «nobody has typed anything yet» — especially when the requirement itself says the field is user-entered and the editing surface does not exist. Filing that as a defect reads as an accusation about work that was never in scope, and the customer withdraws it in one sentence. Split the new fields by who is supposed to write them before assigning a single verdict: user-entered ones are closed by proving the write path accepts them (one sanctioned probe does it), while auto-populated ones — timestamps, sources, counters, derived statuses — are exactly where emptiness is the defect, and there the control is a record the system processed today. Say the practical consequence out loud either way, because it is real: on today's data the consumer of those fields sees a screen of dashes, and accepting the frontend on it will show nothing. Precedent: twenty-one new fields were empty across every record; the report filed one finding (on the two the system was supposed to fill, with a same-day processed record as proof) and explained the other nineteen as an absent editing form — the write path having been proven by a single probe.

- **When the round finds NO sign that the fix was ever deployed, the findings about unmet requirements are still filed — but the report is framed by the deploy question, not by them.** The temptation runs both ways and both are wrong: writing «the developer did not implement any of it» when the build may simply never have reached the environment, or withholding the findings until someone confirms the deploy, which leaves the round with no product. What works: lead the report with «no external sign of the delivery was found; development must confirm the fix is in the build», file each unmet requirement as its own finding with its measurements, and mark the block explicitly as «the state of the environment as of <date>; if the delivery turns out to be missing, these are re-checked after the deploy». Then nothing measured is lost, nobody is accused of work they may have done, and the customer's first action is the cheap one — asking about the deploy. Two oracles usually settle it without repository access: the artifact's fingerprint at both ends of the round, and — for an audited feature — the journal's own vocabulary of event types, since a requirement that obliges new kinds of records makes their absence a dated fact.

- **Check the result's «open questions» against the executor's OWN earlier text, not only against the brief.** A good executor raises questions as they go — «how did this get here?», «is that another path?» — and writes them into the running result next to the observation that prompted them. The final section, however, is usually assembled from the brief: every scenario the manager asked for has an answer, so the count comes out zero, and the question the executor invented for themselves is left behind in the middle of the file, unanswered and now invisible. It is worth catching because a self-raised question is, by construction, the thing the round noticed and nobody planned — often the sharpest item available. The check costs one grep of the result for question marks and for the words that mark a deferral («выясним», «проверим ниже», «to be answered in step N»). Precedent: an executor flagged an anomaly in the batch-capture step, deferred it to a later scenario, answered the three questions the brief listed there, and reported zero open questions — the deferred one turned out to need a single call and became a Critical.

- **reconcile the numbers in the case against the numbers in the measurements**: the executor writes the case's preconditions before
  finishing the measurement, and a draft value stays behind in the case. Precedent: «TTL ≈600 s» in the case against the ≈300 s measured in
  the same result.

- **Before the findings are locked, search the tracker twice more: by the OPERATION's name and by the REQUIREMENT's subject.** The step-1 search (`planning.md`, «The tracker is searched at step 1») was run on what the round expected to find; by acceptance you know the endpoint, the mutation and the field the evidence actually names, and those are the words somebody else's entry is titled in — often under the wrong area or a neighbouring contour, which is why a search on your own business wording missed it and the report is about to hand the customer a duplicate. **And when the entry is found, read what it CLAIMS**: a discrepancy between «the check exists, its list is just wider» and your executor's «there is no check at all» is not phrasing but a gap in the round — settle it with one more probe before the report goes out. The subject search pays differently: a requirement phrased as «… according to the spec» delegates its content to a neighbouring task, and that task's comments are where the decision lives. Where it sits in a testing status and its own item was explicitly descoped («we asked to skip this one»), the finding changes shape entirely — not «nobody wrote the requirement» but «two tasks contradict each other, one of them is being accepted right now», which is a different sentence to the customer and a different fix. Name both tasks in the cell. Precedent: a finding presented as new turned out to have been filed five weeks earlier under a title naming the wrong contour, and its text corrected the executor's over-broad claim in the process; in another round a section marked «no target list exists, needs an analyst's decision» turned out to be owned, verbatim, by a task in review whose corresponding item had been dropped by request three weeks earlier — and the same comment thread disproved two of that task's own claims about the contract.

## A finding of the shape «the control does nothing»

An executor clicks a control, nothing happens, and files a defect. Two states produce that
observation and they are not the same: the control is dead, or the flow was never finished —
a menu item that only opens a confirmation modal, a button that arms a second step, a form
whose submit lives in a drawer footer. The negative oracle (an empty audit log, no request in
the network panel) is identical in both cases, because a mutation that was never triggered
leaves the same trace as a handler that never fires.

What the brief must require, and what acceptance must check:

- **drive the flow to its terminal confirming control** and name that control in the evidence
  («menu → item → modal → its button»); a screenshot after **each** click, not only at the end;
- an empty log is admissible only **together** with proof that the last control was reached;
- separate «the click never landed» from «the handler does nothing» with an oracle rather than
  repeated clicking: a `fetch` interceptor that records request bodies, or an audit log that
  records even rejected calls;
- the counter-control is the neighbouring item of the same menu on the same row — it shows
  whether clicks reach that widget at all.

Precedent: a Major was filed for «the reactivate item performs no reactivation» on three
attempts plus an empty audit log; the manager's re-check found a confirmation modal behind the
item, and after confirming, the mutation fired and the record changed state. The finding was
withdrawn, its id burned, and every derived artifact had to be edited.

## When the brief caps an amount, state the platform's fee next to the cap

A cap agreed with the customer («small amounts only, 1–10 of the unit») can be arithmetically
unreachable on the platform the round runs on: if the assigned fee exceeds the cap, every
attempt dies on «fees exceed amount» and the scenario is unrunnable. The executor discovers
this only after measuring, and the instruction handed to the human has to be rewritten with a
different number.

So: name the fee (or the minimum viable amount) beside the cap in the brief, and check the two
against each other while planning. Same for any other precondition expressed as a limit —
balance, quota, remaining allowance.
