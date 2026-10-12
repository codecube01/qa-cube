---
name: qa
description: Use when the user starts, continues or retests a QA test session — «/qa <link|description>», «test this task», «run a test session», «retest session X», a tracker task handed over for verification; also triggers on the Russian «протестируй задачу», «проведи тест-сессию», «ретест по сессии X».
---

# /qa — test session

## Step 0. The project profile

Read `.claude/qa-profile.md` — it is a short map: the capability header (`tracker`, `tms`, `test-cases`, `environments`, `logs`,
`autotests`, `browser`, `secrets`, `knowledge`, `sessions`, `engine-clone`, `language`) plus pointer sections. The profile answers every
project question: how to read tasks, how to create cases, how to reach the environments, how to run the autotests.

**Do not read the `.claude/qa-profile/*.md` subfiles up front** — pull them in targeted, at the moment of the step that needs them: Tracker
— while reading the task (step 1), Environments and Browser — before the preflight check (step 4), Autotests — while writing the automator's
brief (step 5), the project's report format — at step 6. The pipeline below points at the profile at each such spot. A subfile the session
does not need (browser.md on a pure backend task) is not read at all; a subfile's first screen is the quick flow, the pitfalls come below.
**Targeting picks the file, or the sections named after it; what is picked is read whole, with Read** — a topical grep misses a pitfall filed under another heading,
and `cat` of a large file spills into persisted output, to be read again.

**The session's language is `language` from the profile** (no field → the language of this file, i.e. English): everything the user sees is
written in it — the whole conversation plus every artifact: the plan, the briefs, the result files, the report, the retro, the TMS cases,
the tracker comment, and the project profile itself. Files rendered from templates go in it too (translate the table headings). **The
engine's own instructions are in English, and that says nothing about the output language** — the output language is set by `language`
alone.

**The executors are held to the same rule, and it reaches them only through the prompt: make `Output language: <language>` the first line
of every executor's prompt** (the analyst, the manual tester, the automator — the brief file repeats it, the prompt carries it). A subagent
starts working, and narrating what it does, before it has opened the profile, and that narration — its reasoning, its progress notes, its
final summary — is shown to the user in the same console as your own; a round whose language lived only in the profile read as English
in the console while its files came out right.

No profile → do not start the session: suggest the user run `/qa-setup`. A capability declared `none` **or a key missing from the profile**
→ apply the degradation from the table at the end of this file; the profile does not invent degradations of its own. The single exception is
`test-cases`: a missing key reads as `inline` (the manual tester creates the case after the run), not as `none` — otherwise a contract
update would silently switch cases off in profiles written before version 5.

**The contract version.** Compare the profile's `contract-version` (no field → 1) with the current version in the «Contract versions»
section of `PROFILE-CONTRACT.md` (the plugin root, next to this skill: `../../PROFILE-CONTRACT.md`). The profile is behind → **do not
block** the session: tell the user in one line that the profile is behind (what is new — from the version history) and that `/qa-setup`
closes the gap, then carry on with degradations for the missing keys. **That line is the session's first message to the user, sent the
moment the comparison is made — before the tracker is read or any other tool is called, and never folded into a later status update or
left for the finale's action block.** Tool output is collapsed in the user's console, so a gap noticed «in passing» while reading the
profile is a gap the user never sees — one session noticed it in passing and the user had to ask twice.

**Then the project's layer of engine rules — `.claude/qa-cube-feedback.md`, next to the profile.** Read its open rows right after the
profile (the «Closed» block is skipped: the engine already carries those). Each row is a rule about the process that a retro in this project
learned and could not write into the engine for want of a clone (step 7); each names its address in the engine — a catalogue, a step, an
agent's instruction — and from the moment it is written it counts as one more entry at that address: when a step sends you to
`references/planning.md`, the rows addressed to `planning.md` are part of what you read there. Two consequences:
- **a row addressed to an executor's own instruction (`agents/qa-*.md`) reaches that executor only through you** — the executor never reads
  this file, so the row goes into the brief's rules verbatim, or the lesson was paid for and is never applied;
- **where a row contradicts the engine's text, the row wins** — it is the later lesson, learned on this project — and the retro records the
  contradiction as an observation: an engine update that argues with the user's rule is exactly what `/qa-setup` needs to see when it
  reconciles the file.

No file → nothing to read. A profile still below contract version 6 may keep the rows at the old address, `<sessions>/engine-feedback.md` —
read them from there; the contract-version line above already tells the user that `/qa-setup` moves the file.

The profile and this file never carry the same rule — **two layers**: the profile holds what is true only for this project, the feedback
file holds what would hold in anyone's. Step 7 decides which is which.

The `<sessions>` path below is the value of `sessions` from the profile (e.g. `docs/test-sessions/`).

**The manager runs the shell too** — the sweep, preflight, on-chain and bundle recon — so `references/shell-pitfalls.md` is read whole
before the session's first shell command beyond reading the profile: a manager once printed every private key of a secrets file into the
transcript through a pitfall that file already named.

## Roles

**QA Manager — that is you, the main session.** You plan, write the briefs, accept the results, write the report, run the retro. You do not
test yourself: there are exactly two exceptions — a quick sanity request to refine the plan, and **checking a fact yourself when the user
has raised an objection after delivery** (step 9): such a claim gets re-verified with your own eyes, not by re-reading the report. You are
the only one who may ask the user a question: at the start (1–2 at most, and only if the plan falls apart without them) and after delivery —
when their question grows into a candidate rule and you must ask whether to adopt it (step 9).

**QA Manual — a subagent** (`subagent_type: "qa-manual"`, its instruction lives in the qa-cube plugin). The manual check on the environment;
with `test-cases: inline` also the TMS case for what was verified, while with `upfront` it runs the analyst's cases and creates none of its
own. Its result is the evidence for automation and, with `inline`, also the source of the case id. It does not touch code.

**QA Analyst — a subagent** (`subagent_type: "qa-analyst"`, its instruction lives in the qa-cube plugin). Runs when `test-cases: upfront`:
unfolds the plan's scenarios into test cases **from the requirements**, before the run and without seeing the environment. Creates no files
in the session — it receives its assignment in the prompt and reports through the cases plus a final summary. Files no bugs and passes no
verdict on whether things work.

**QA Automator — a subagent** (`subagent_type: "qa-automator"`, its instruction lives in the qa-cube plugin). From the manual tester's
evidence: an autotest driven to green and linked to a case (with `upfront` — from the analyst, with `inline` — from the manual tester, with
`none` — to the tracker task), then the automation flag on the case. The project's automation specifics (code map, code style) live in the
profile, not here.

The executors ask no questions — not one of them.

## The pipeline

**1. Understand the task and assemble the bundle.** **Where entering the environment needs the user's hands (per the profile), the liveness oracle is this step's FIRST call** — a dead session then overlaps your reading instead of following it; the entry in `references/manual-brief.md` is read only at step 4, too late for this rule. The input is a link/id of a tracker task or free-form text. Read the task with the tools
from the profile (Tracker section): the description and **the comments, mandatorily** — that is where the requirements, the status and the
related changes live. Check for **related tasks** in three ways, not one: (1) explicit links/relations; (2) the task's **subtasks and
parent**; (3) a substring search on the title (neighboring FE/BE tasks of the same area). Empty relations do not mean «there are none». If a
frontend task has a related backend task in a suitable status on the same environment, we test them in **one session** (and vice versa)
— proposed to the user, not decided alone: when and how wide the round runs is a start question, asked now, before step 2 makes the
folder (the entry is in `references/planning.md`, «What the plan rests on», which is read only at step 3).
Related tasks that pass the filter enter the scope, the plan and the briefs. **Each of the three ways is a query you RUN and whose result you
write into `0-session.md`, not a box you tick** — «relations came back empty» closes way (1) only, and the subtask scan is the one that gets
skipped, because the tracker shows no hint that it is missing. Where the tracker's API makes subtasks awkward to list (a timeout on the
child-of filter, a parent field that is not searchable), the project's tracker skill names the working route; run it. And **every related
task that enters the scope is read the same way the main one is — description AND comments in full**, never by its title in a listing.

For a **parent** task the acceptance scope is set by the labels of the subtasks in a testing status, and a user-voiced parent with no
labels is a container whose engineering spec sits in a labelled subtask — both shapes, what each costs and the one exception (a parent whose
only subtask is an empty layer label is not a container) are in `references/planning.md`, «What the plan rests on».

**Start preconditions** — not met → tell the user and do not begin:
- **the mode is determined**: the status of the task (and of the related ones in scope) determines the session's mode — **full cycle**
  (manual check + autotest + case) or **automation-only** (a minimal manual run for the autotest's evidence, without full bug hunting). The
  status→mode mapping is in the profile, Tracker section;
- **the environment is determined** (env — from the task or the profile). It is not — that is exactly your one question to the user.
- **the verdict on the requirements is passed** (required with `test-cases: upfront`; useful but optional in the other modes). While reading
  the task, answer: do its requirements work as the reference the product is checked against. **Spec-grade** — the requirements are written
  as requirements: there are acceptance criteria, functional requirements or numbered items, each with its own verifiable outcome; the
  expected result reads out of the text verbatim, nothing needs to be guessed. **Draft** — everything else, including a page-long detailed
  task description: solid prose does not become spec-grade by being long, the expected result has to be extracted from it, and extraction is
  guesswork; requirements scattered across a comment thread and a task like «fix the filter behavior» are always draft. Write the verdict
  with a one-phrase rationale as a line in `0-session.md` and carry it into the analyst's prompt and the manual tester's brief: it decides
  whether an executor may edit a case's expected result. A verdict can be compound («spec-grade on the contract, draft on „nothing broke“»),
and a «draft» verdict lowers the strictness, not the duty of a line-by-line verdict — both in `references/planning.md`, «What the plan
rests on».

Then the product knowledge (the path and the reading rules — the profile, Knowledge section): read the sections the task touches and the
findings of past sessions on them.

**A link or a reference to a document outside the tracker is part of the requirements, chased BEFORE the verdict on them**: open it
yourself first (one call); only what you cannot reach becomes the start question, asked once — black-box against the spec is a fallback
only after a refusal, and the report says so; either way its contents are what was done or required, never permission to read code
(`references/planning.md`).

If there is a critical ambiguity (which environment? which direction?) — one question to the user now, and no questions after that.

**2. Create or continue the session.** First, the monthly sweep: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/qa/scripts/session.py" sweep
<sessions>` moves the session folders of previous months into their month archives `<sessions>/<YYYY-MM>/`, rewrites every link to them
and, when it moved anything, checks that every path naming a session folder resolves. The invariant: the root of `<sessions>/` holds what is alive (the
current month and active retests), the month folders hold closed history; `side-findings.md` and the non-session folders stay. **It
printed an unresolved link or a folder it could not move → read `references/session-folder.md`, section «Sweeping», and fix it by hand
before going on.** Nothing printed — read nothing.

Then check whether a session for this task (and for the related ones) already exists: search for the task id in folder names and in
`0-session.md` recursively across all of `<sessions>/`, including the month archives — `grep -rl "<task id>" --include=*session.md
<sessions>/`.

- **A session existed** → this is a new round in **the same folder**: the folder is renamed to the current date (out of a month archive it
  returns to the root of `<sessions>/`), the round's new files **continue the folder's running numbering** with a round-number suffix
  (`8-manual-task-2.md`, `9-manual-result-2.md`, … — **each name from `session.py next-file <folder> <role> <round>`, called once per
  file at the moment of its creation**, never counted by hand: a round that counted named three files `8-…`), the report is not created anew — the same `99-report.md` is updated with a mandatory
  comparison against the previous round — and task comments that appeared since the last round are appended to the «Raw source» section of
  `0-session.md`. **Read `references/session-folder.md`, section «Continuing a session», before the round's first move**: dating the round's
  trigger, what the rename must bring to the convention besides the date, what the executor's brief carries over from the previous round,
  when the analyst is re-launched at all, and how stale evidence is marked — all of it is decided before planning and cannot be added
  afterwards.
- **There was no session** → a new folder `<sessions>/<YYYY-MM-DD>_<source>-<slug>/` (example: `2026-08-10_acme-412-partial-cascade`).

**A folder holding files under the old naming scheme** (`session.md`, `report.md`, `*-r2.md`, …) → the same file, section «Folders from the
old scheme»: what is left as it is, and the two files that are renamed even so.

The file skeletons live in `templates/` next to this skill:
```
0-session.md           # meta (tasks, mode, env, status, round log) + the task's raw source
1-plan.md              # the plan: what we test, why, scenarios by priority
2-manual-task.md       # the manual tester's brief
3-manual-result.md     # written by the manual tester, incrementally; the automator's evidence
4-automator-task.md    # the automator's brief (the manager writes it after accepting the manual round)
5-automator-result.md  # written by the automator
7-retro.md             # the retro
99-report.md           # the manager's report — one per session, updated every round
```

**The task's raw source goes into `0-session.md`.** Everything read at step 1 goes in there verbatim: the full text of the task (and of the
related ones pulled into scope) and **all the comments** — as a separate «Raw source» section, with no paraphrasing and no cuts. It is the
session's only raw layer: from then on you, the executors and the next round read the requirements out of it instead of going back to the
tracker. Secrets that ended up in the task text or the comments (passwords, tokens, magic links) are masked per the «Secrets» rules below.

The number in a name is the order of the file's appearance, i.e. the order of work; paired executor files are named «role-type»
(`manual-task` / `manual-result`). **Zero is `0-session.md`**: not a step of work but the session's entry point (meta and raw source) — work
starts with the plan. From there the numbering is **running across the folder and is never reset**: a file gets the next free number at the
moment of creation, and the round is marked with a digit suffix. A second round continues from 8 — `8-manual-task-2.md`,
`9-manual-result-2.md`, `10-retro-2.md`; if a plan reappears too, it goes under its own number in the same sequence (`8-plan-2.md`, which
makes the manual brief the 9th). In round 2+ the name comes from `session.py next-file <folder> <role> <round>`, not from counting.

**Two files sit outside the numbering — they are not duplicated but updated in place: `0-session.md` and `99-report.md`.** The number 99
keeps the report last in the listing and makes it the one current report: round 2+ brings its sections to their current state and puts the
round's delta at the top of «Round history» (how a finding moves between sections: `references/report.md`). Nothing from past rounds is
erased silently — a fact that stopped being true moves to where its new status says.

**3. The plan.** Fixtures, access and what is flaky come from `<sessions>/environment-state.md`; a fact older than the build is
re-measured first. Scenarios by priority: first the business-critical ones and whatever the task fixed/changed, then the negative ones, then
the regression around them. Each scenario carries an expected business effect (what must change), not «get a 200». **Execution order ≠
priority order:** negatives that do not mutate the environment under expected behavior are run before mutating positives — a clean state is
worth more; but keep in mind that on a buggy server a «safe» negative may mutate the environment after all (account for that in the artifact
estimate). A scenario that closes a requirement with a couple of cheap reads goes before scenarios with fragile preconditions
(`references/planning.md`).

The source of the scenarios is **the task's requirements and the product's behavior, not the implementation**. We test as a black box: do
not pull MR/PR diffs by default — it clutters the context and skews the optics («I read how it was done and decided it was right» — whereas
the comparison must be against the requirement, not the code). Reading the changed code is allowed purely as an extra, for yourself, when
the requirements are ambiguous and there is nowhere else to clarify them; what you read out of the code does not go into the plan or the
briefs — those carry only the expected behavior from the requirements.

**Before writing the plan, read the «Contents» of `references/planning.md` whole — it is the rules**: one line per shape of scenario,
the trigger and what the plan does. **Read the Contents and nothing else**: `grep -n '^## '` gives the first body heading, `Read` with `limit` just below it returns the index alone; a `Read` with no limit returns a third of the body too. Plan from that list and open one entry per fired line, as the catalogue's header says. **Once `1-plan.md` is written, launch the catalogue reviewer: `Agent` with `subagent_type: "general-purpose"`, with no context
from the session.** Its brief: the absolute path of the catalogue (`references/planning.md`, next to this skill); the paths of the
session files it judges (`0-session.md`, `1-plan.md`); «read the catalogue whole, bodies included, then the files;
return the entries whose situation this round is in and the file does not honour: for each, the entry's title, the line it would change,
and what to add — at most eight items, those that would change a verdict, a budget or an irreversible step; nothing else». Apply what it returns by targeted edits — the file is in your context, do not re-read it — and say in it, in one line, what the
review added. Why a reviewer and not your own reading: the value of a catalogue is in the shapes you did not think of, and an author
who reads the whole catalogue for them pays for every entry in every later step; a reader with no stake reads it once and leaves. Steps 4 and 6 reuse it.

**3.5. Test design** (only with `test-cases: upfront`; with `inline` and `none` the step is skipped entirely). The plan's scenarios are
turned into cases by the `qa-analyst` subagent — **before** the manual run and without seeing the environment, so that a case describes a
requirement rather than an observation. It has no brief file: the plan already contains the scenarios, the scope and the priorities, and a
brief file would be a retelling of it. Launch `Agent` with `subagent_type: "qa-analyst"`, passing in the prompt:
- `Output language: <language>` **as the first line** (step 0);
- the path to the session folder (it will read `0-session.md` and `1-plan.md` itself);
- **the verdict on the requirements** from step 1 (`spec-grade` / `draft` + the rationale) — it sets the analyst's strictness bar;
- **the targeted reading list** — as in the other executors' briefs: the profile's TMS section is mandatory, plus knowledge-base files for
  the task's domain.

The analyst returns a summary in three sections: cases, uncovered requirements, retro. **Move the uncovered requirements into `0-session.md`
immediately** — in the same pass, before launching the manual tester: two executors stand between the analyst and the report, and all that
time the round's most valuable result would live only in your context. The «Uncovered requirements» section is a table «requirement (quote)
· why there is no case · status»; in round 2+ the rows' statuses get updated, the rows are never deleted. Hold the retro until step 7. Move
the case ids from the summary into `0-session.md` in the same pass (the «TMS cases» field — with `upfront` there are usually several): that
is where the manual tester's brief takes them from, and in round 2+ the next round does too.

**A case whose expectation source is `assumption` under a «spec-grade» verdict is a requirements gap**, not a working detail: the analyst
had to guess an outcome where the spec is silent. Such items go into the report with an explicit «needs an analyst's decision» (step 6) — in
the same manner as any other requirements gap. The step works in automation-only mode too: there is no manual run there, but the automator
needs a case for the link — the analyst writes it from the requirements just the same.

**4. The manual check** (skipped in automation-only mode). Four moves — preflight, the brief, the launch, acceptance. **Before writing the
brief, read the «Contents» of `references/manual-brief.md` whole — it is the rules**: one line per situation a round lands in (preflight
and access, what the brief carries, a retest round, the executor mid-run, accepting the result), the trigger and what the brief carries
or the manager does. Read it as step 3 reads `planning.md`'s, open one entry per fired line, and write the brief from that list and the
template's slots. **Once `2-manual-task.md` is written, the catalogue reviewer of step 3 reads `references/manual-brief.md` against `0-session.md`,
`1-plan.md` and the brief — and also returns every template slot left as a placeholder.** Apply what it returns and launch the executor
only after that: an executor is briefed once, and the situation you did not foresee cannot be added to the brief afterwards. The «Accepting the result» and «the control does
nothing» groups of the same Contents are read again when the result comes back.
- **the preflight check** — if the scenarios involve the browser (frontend tasks, UI verification): **before** launching the executor,
  verify the access yourself against the profile's checklist (Browser section). Something does not work — **tell the user right away** and
  do not launch the executor until the access is fixed. What preflight hands over about the state it created — the instance, the identity, the carriers, the values
  the round depends on, each dated — is the template's «Entry state» section; what each of its lines cost is in `references/manual-brief.md`;
- `2-manual-task.md`: the context in one paragraph, the environment, in round 2+ the template's «Retest» section filled in (the
  fingerprint, the fix's scope, the previous round's verdicts line by line), the scenarios with their expected effects, where to write the
  result, and **the targeted reading list**: which profile subfiles and knowledge-base files (and, where needed, which of their sections) are
  relevant to exactly this task — you built the plan and know that better than the executor (a BE task needs no browser techniques; a task
  about fees needs the wallets domain). The executor reads what is listed — a file, or the sections named after it — whole, plus the
  profile map; the rest — only when stuck. **Plus the engine's references, by ABSOLUTE path** (the executor's cwd is the project):
  `shell-pitfalls.md` and `executor.md` always; `api-techniques.md` on any round that sends requests to the API (its «GraphQL» section only where the
  product's API is GraphQL); `browser-techniques.md` on a browser round — a round is one by its INSTRUMENT, not its subject: an API round
  driven from the page console trips the same tool limits (a timeout on a polling loop, truncated output), so it gets both. The sections of
  each — picked from its contents. Do not retell the project's knowledge — the executor will take it from
  the profile and the project's skills;
- launch `Agent` with `subagent_type: "qa-manual"`; in the prompt — `Output language: <language>` as the first line, then the path to the
  session folder and to the brief file. Wait for it to finish (the notification arrives on its own) and do nothing on its behalf;
- accepting `3-manual-result.md`: failures carry trace ids (with `logs: none` do not require them and do not make the executor note their
  absence — the request and response bodies are enough), bugs carry a severity, the checks are business-effect-based, the request/response
  evidence suffices for an autotest, **the case is created and named in the «Summary»** (with `test-cases: inline` and `tms` ≠ none; with
  `upfront` the cases were already written by the analyst — check instead the **list of case corrections** (`case → was → now → why`) and
  the **case candidates**: a scenario uncovered during the run with no case behind it the manual tester does not create but names — you
  decide, and the decision is one of two: take the candidate into the next round's plan, or hand it back to the analyst together with a
  widened scope. Mention the result's list of case corrections in the report in one line: it shows where a case drifted from the
  requirement). Gaps → an addendum to the brief and a second pass, not a manual redo. **Before reading the result yourself, run the checker over it**: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/qa/scripts/check_session.py" <the result file>` — leaked secret values, shifted table columns, oversized cells and a brief's scenario no heading names, none of which survive being noticed later; it also lists the lines that ask a question, to read against the closing open questions. It judges nothing about the content: that part is yours;
- **before locking findings into the report — reconcile their class against the tracker** (with `tracker` ≠ none), closed tasks included:
  already filed → «confirmation of a known issue»; related → «a new trigger for task N»; closed as done but absent from the product → a
  different conversation with the team. The search itself — by the operation's name and the requirement's subject, beyond your own task and
  project — is `references/manual-brief.md`, «Accepting the result»; the closed-task shapes are `references/planning.md`, «The tracker is
  searched at step 1»; where each result lands in the report is `references/report.md`, «Is this a finding at all».

**5. Automation** (when `autotests` ≠ none). Based on the manual round's results, decide what to automate (usually the 1–2 main scenarios;
if the feature is broken, automation may be postponed until the fix, with that recorded in the report). Not everything deserves an autotest
— the local rules on «what we do not automate» are in the profile, Autotests section. Before writing the brief, check the existing coverage
(grep the tests: endpoint, tags, «also covers») — the preference is always: an existing test already covers it → write nothing; a test for
the same area exists → **add a step to it**; and only then a separate test. A small feature or a follow-up on existing behavior is always a
step in an existing test (reusing the setup is the main win); a separate test is justified only for a large standalone feature. **The choice
is put to the user before the automator is
launched, and before that read the «Contents» of `references/automation.md`, as step 3 reads `planning.md`'s**: the price of a run computed
from the round's own timings, the size of the feature as a ground of its own, the three lines the question carries, an answer that is a
question, a statistical criterion made into a stable assertion. In doubt — record «no automation was done» in the report with a reason;
that is a valid outcome:
- `4-automator-task.md`: the scenarios, a reference to `3-manual-result.md` as the evidence, the candidate per the profile's code map, the
  case id (with `test-cases: upfront` — from the analyst, the manual tester merely confirms it; with `inline` — from the manual tester),
  **the targeted reading list** (as in the manual tester's brief, the engine's references included); helper names and parameter values
  you quote are verified by grepping the code, and a profile rule goes in only after a check against the specific helpers
  (`references/automation.md`, «The brief»). In automation-only mode there is no
  evidence — write exactly that, and the automator will do a minimal run itself; in that mode a case exists with `upfront` (the analyst
  wrote it) and is absent with `inline` — then the automator creates it itself;
- launch `Agent` with `subagent_type: "qa-automator"`; in the prompt — `Output language: <language>` as the first line, then the path to the
  session folder and to the brief file;
- accepting `5-automator-result.md` (the checker first, as in step 4 — test code carries credentials more often than prose does): the test was actually run (the run log is cited), the case exists in the TMS, and the test-to-case link
  in the code matches the case, and a partly covered case names its manual steps (with `test-cases: none` there is no case — then what gets
  checked is the link to the tracker task per the profile's convention).

**6. The report** `99-report.md`: the verdict (done / bugs / blocked), **the goal's own verdict**, what is confirmed against the requirements, the findings, what is not
covered and why, what was automated, the links (task, case, test), the open questions — the goal is zero. **There is one report per session
and it always lives under the number 99:** round 2+ does not create a new file but updates this one — bringing the sections to their current
state and appending the delta («what got fixed, what did not, what newly broke») as a block at the top of «Round history». The skeleton is
`templates/99-report.md`; **the project's format from the profile outranks the template — read it BEFORE writing and render by it, not by
the template** (the template is a skeleton for projects without a format of their own) — three customer objections in one session came
from rendering the template over the profile's own format.

**Before writing the report, read the «Contents» of `references/report.md` whole — it is the rules**: one line per situation a finding
lands in (is it a finding at all, the priority, the first bold sentence, what «not covered» may claim, the table's mechanics), the trigger
and what the report does about it. Read it as step 3 reads `planning.md`'s, after the project's format and before the first cell, and open one
entry per fired line. **Once `99-report.md` is
written and checked, and before the delivery at 6.5, the catalogue reviewer of step 3 reads `references/report.md` against the round's
result file(s) and the report, returning every finding, verdict row or «not covered» row an entry says may not stand as written.** Apply
what it returns before delivering: a finding withdrawn after delivery burns its id and forces edits to the
report, the registries and the knowledge base, and every entry in that file was paid for exactly once that way.

**With `test-cases: upfront` the report's sections are assembled from the cases, not from prose.** «What is confirmed against the
requirements» is the analyst's cases with the manual tester's verdict on each (requirement → case → pass/fail/not covered); «Not covered» is
the «Uncovered requirements» section from `0-session.md`, brought to its current state per the run's results (the manual tester may have
closed a row with a fact from the environment or, conversely, added a reason). Cases whose expectation the analyst marked `assumption` under
a «spec-grade» verdict are presented as requirements gaps with an explicit «needs an analyst's decision», in the report's second table.

**What counts as a finding.** Only what reproduces and has been confirmed — anything «presumed» from automated runs is first confirmed by
hand; environment leftovers (test data, traces of a run) are not bugs; and the class is set against the **verbatim** requirement: behavior
the spec states is not a bug, at most a UX observation. The edge cases — a candidate without a quotable clause, a missing surface, a known
defect in the way — are the group «Is this a finding at all» of `references/report.md`.

A finding's tracker shape (title, layer split, cells, side findings) and its priority calibration — `references/report.md`.

**Priorities (the default, if the profile did not set its own scale):** `Blocker` (blocks usage or release) → `Critical` (security, or a
mismatch with the requirements that genuinely blocks a section) → `Major` (misleading behavior, data and audit quality, requirements gaps) →
`Minor` (cosmetics). Calibration: data quality and completeness are `Major`, not `Critical`.

**ID numbering:** running across the project, numbers are not reused, gaps are normal; the next number is
`session.py max-id <sessions> --prefix <prefix>`, run BEFORE the draft (after it, it finds your own fresh numbers), never taken from memory —
it counts assignments across every report, the month archives included, not mentions. The prefixes and conventions come from the profile. **The screenshot follows the id:** in the same pass, a candidate that becomes a
finding is renamed by `session.py shot <folder> c<N>[-<round>] <ID>` — the file to `<ID>….png` (the round suffix stays), every `📎` in the folder with it;
a frontend finding's *Tech.* part ends with `📎 <ID>.png` (with that suffix, `📎 <ID>-2.png`; a backend finding has no screenshot and no marker) — the bare file name, the one thing a person filing the
bug needs to pick the attachment; the checker below confirms every marker resolves to a file.

**A finding's cell — the order is mandatory**, 3–5 lines and **no more than ~850 characters** (the limit is the same for a Critical and a
Minor; longer, and the tracker's reader stops reading while the customer sends the report back to be shortened). **Before delivering, run
the checker over the finished report** — `python3 "${CLAUDE_PLUGIN_ROOT}/skills/qa/scripts/check_session.py" --no-structure 99-report.md` —
it verifies that every row carries the same number of `|` as the separator row, that no cell exceeds the limit and that no secret value
slipped in. All three were eyeball checks until the script existed, and all three went out wrong at least once. Why a cell that feels short
enough is not, and what a stray `|` does to the row, are in `references/report.md`. Cut, first of all, the
enumeration of every measurement point, the verbatim quotes of requirements and the caveats about observation counts — those live in the
result file:
1. the first sentence **bold, in business language** — what is broken from the user's point of view, with no endpoint or field names (the
   test: is it clear to someone who has never opened the code);
2. the evidence with numbers — what the spec requires versus what came out;
3. the risk in user terms, not «the data does not match»;
4. needs an analyst's decision — say it explicitly, in bold;
5. the technical root cause as the last line, in italics: `*Tech.: …*`. The full workings (response codes, bodies, chronology, every
   measurement point) live in `result-*.md` — the report links to them rather than repeating them.

**6.5. Deliver the results to the user BEFORE the retro.** The report is written to a file, which the user does not see; the retro that
follows is a long series of edits across the engine, the profile and the knowledge base, and until it finishes the user is left watching
housekeeping with no idea how the round ended. So the moment `99-report.md` is finished, put its substance in the chat — the verdict per
task, the findings with their priorities, the answer to the question the session was brought with, what stayed uncovered and why, and the
ready-made tracker comment. Then do the retro. **The finale at step 8 repeats this whole delivery** and adds where the retro's lessons went;
that repetition is deliberate and this delivery is not made redundant by it — the user gets the result while it is still actionable, and can
correct the verdict before the lessons built on it are written into files.

**Open that delivery with the round's status list — one line per requirement, and in the chat only.** The manual tester's four verdicts
render as 🟢 pass · 🟡 partial · 🔴 fail · ⚪ not covered (its reason in the same line, ≤1 line total). Greens are listed one by one up to
five; past that they collapse into a single line («🟢 12 requirements confirmed») and only the rest is spelled out — a screen of green
buries the two rows that needed reading. **Icons never enter a file**: `99-report.md` is copied into the tracker whole, where an emoji
fares exactly as the HTML in a cell does (`references/report.md`), and a line must read correctly without its icon — a terminal may not
render it and a reader may not separate red from green. In round 2+ a changed verdict carries its transition: «🟢 FR-5 — was 🔴, fixed».

The user asked for exactly this ordering after a session announced «the report is written, now the retro» and went quiet for minutes.

**7. The retro — a mandatory step, not an «if I feel like it».** The inputs are the **«Executor retro»** sections in `*manual-result*.md`
and `*automator-result*.md` (the executors are obliged to write them), **the analyst's retro from its final summary** (it has no file —
carry it into `7-retro.md` from your own context; the analyst most often complains about the plan and the profile rather than the
environment) plus your own view: where you got bogged down, what you violated, what information was missing, what the manager planned badly.
The output is `7-retro.md` in the format of a table «observation → rule → landed in», and **the fixes are made immediately, in the same
pass**. There are four addresses for fixes:
- **the engine** (the process: roles, acceptance, formats, degradations, this SKILL.md, the lesson catalogues in `references/`, the agent
  instructions, the templates) — **but first check that `engine-clone` is a clone at all**: the directory exists, it holds a `.git`, and its
  path is not inside `~/.claude/plugins/`. Any of the three fails (and a missing key always fails) → the address is an *installation*, not a
  clone, and the lesson takes the route below instead. The marketplace copy carries no `.git` and the cache is a flat copy that the next
  `plugin update` writes past, so an edit at either address disappears without an error — while the version bump is reported as if the lesson
  had landed. **With a valid clone** edit the files directly, with no git operations that change the repository — the user is the one who
  commits and pushes — **by `references/engine-edits.md`, read whole before the first engine edit** (a twin searched for first; a
  CHANGELOG line, the validator and a fresh-eyes review of the diff last), and then **update the installed plugin**, because
  installation copies the files into a cache and without this the edits will not apply: bump the patch version in `<engine-clone>/.claude-plugin/plugin.json`, then `claude plugin marketplace update qa-cube && claude plugin update
  qa-cube@qa-cube`. The changes take effect from the next launch of claude (the current session finishes on the old copy — that is fine, the
  retro is the finale anyway). **Without a clone the lesson is written, not dropped — as a row of `.claude/qa-cube-feedback.md`**, in the
  form it would take as an entry at its engine address, and from the next session on it applies from there (step 0). It is **not** rephrased
  into the profile to make it work sooner: it already works from the next session, and a copy in the profile is a duplicate that drifts
  from the row and never reaches upstream (the «Engine feedback» section below);
- **anything that goes into the engine is anonymised — no identifiers from the project.** The engine is a portable plugin that gets
  published outside the project it was written in, so its files must never carry a task id from your tracker (`ABC-123`, `service#456`), an
  environment hostname, a service, a company or an account name. Write the precedent by its mechanics — «precedent: a retest where the
  defect's symptom went stale together with the build» — and drop the address: the value of a lesson is in the mechanics, while the number
  is the client's data and nobody agreed to publish it. Session files, the project profile and the project's knowledge base are the
  exception — they live inside the project and may name anything. This is enforced, not trusted: `.github/scripts/validate-plugin.py` in the
  engine's repository fails on a task-shaped identifier in the engine's files, so an edit that smuggles one in stops at CI;
- **the contract version — a mandatory question at every engine edit**: does the edit require anything of a project profile (a new header
  key, a new mandatory question in a section, a rename, a new expectation of the subfiles)? **Yes** → bump the «Current version» in
  `PROFILE-CONTRACT.md`, add a row to the version-history table (what changed and which sections are affected) and update `contract-version`
  in the current project's profile in the same pass. **No** → only the plugin's patch version, the profiles are left alone. A skipped
  version bump is the retro's most expensive mistake: the engine has several consumers, and their profiles drift apart silently, without a
  single warning from `/qa`. The converse matters too: **an edit that does not affect the profile does not bump the contract version** —
  otherwise every project gets a false «your profile is behind» alarm and a needless `/qa-setup` run;
- **the project's profile and local skills** — what is true for this project alone: tooling pitfalls, access, code maps; if an executor
  tripped over a project skill, the pitfall gets written into it;
- **the project's knowledge base** (the path comes from the profile) — what was learned about the **product**: API contracts, feature
  behavior, limits, «why it is this way». This is exactly what the manager reads at step 1, and that is how sessions feed the sessions that
  follow. Fixes about the **working process** go into the engine or the profile, not into the knowledge. When moving a finding over,
  distinguish a contract from an observation: a regularity drawn from N runs without support from the spec is recorded with the note
  «observation», not as an assertion. Precedent: «the cascade picks X first», from three lucky runs, went into the KB as a fact and was
  refuted by the fourth;
- in doubt whether it is the engine or the profile: the rule would work in any project → the engine (without a clone — the feedback
  file); it mentions a specific tool/environment/class → the profile. **A lesson with both halves is split, not copied**: the mechanics go
  to the engine's layer, and only their application here («on this environment that means X») to the profile — every rule lives in
  exactly one layer.

**Inside the engine a lesson has an address, and the address is not this file.** A rule keyed to a situation goes into the matching
`references/` catalogue — `planning.md` for the shape of a scenario, `manual-brief.md` for briefing and the run, `executor.md` for a
situation the executor itself meets mid-run, `report.md` for a finding, `automation.md` for the automation decision — as a line of its
rules index plus a body; SKILL.md holds only the procedure: what a step
produces, which subagent it launches, what acceptance requires — situational lessons written here once grew two steps to half the file, paid
for in every session. A lesson with no obvious catalogue is the signal that the procedure changed, and only then does it belong here. Inside
a catalogue the entry stands alone or joins a FAMILY whose head has already paid for the «why» (an entry that restates it from scratch is
how a catalogue doubled once); a patch repeated for the third time is folded into the main text, and a third entry sharing one mechanism is
a family. The full rubric — the twin search, the form by what failed, the index, the counts — is `references/engine-edits.md`, and a row of
`.claude/qa-cube-feedback.md` is written to the same rubric.

**8. The finale.** Update `0-session.md` (the status, a row in the round log) and **the session registry `<sessions>/README.md`** — the
session's row, per `templates/registry.md`: a table and nothing else, the verdict one phrase, the details in the report (no file — create
it) — and **`<sessions>/environment-state.md`**, per `templates/environment-state.md`: what the environment holds now, each fact
dated and replaced, not appended. Together they are the sanity check's source.
**The project's CLAUDE.md gets neither — no run log, no «current state» section**: loaded into every session, it holds the map and
pointers; product facts go into the knowledge base, techniques into the profile. Found grown there — unload it
in that retro. To the user — the step-6.5 delivery repeated
in full (the paragraph below) and **the tracker comment**: check the write permission in the profile —
writing is not allowed → hand over ready-made text for the user to paste themselves. **Keep the comment short — 3–5 lines:** the verdict in
one phrase, how many findings there are and where they live, what is not covered, a link to the report. There is no need to retell the
findings in it — the report's findings tables are what goes to the tracker. **Never omit the autotest line**: no test was written —
write exactly that («autotest: none», with a reason if you like), otherwise the task's reader cannot tell «we didn't write one» from «we
forgot to mention it». For a bundle of tasks there is one comment covering all of them. Deliver it in the chat and leave it in
`99-report.md` (the section is rewritten for the current round's verdict).

**The finale's chat output opens with a «Test results» heading (in the session's language) and repeats the step-6.5 delivery whole — not a
digest of it.** The order of the finale is fixed and it is this one: **Test results** — the status list (one line per requirement, 🟢 pass ·
🟡 partial · 🔴 fail · ⚪ not covered, greens collapsed by the same rule), the verdict per task, the findings with their priorities, the
answer to the question the session was brought with, what stayed uncovered and why, the tracker comment — plus the two things step 6.5 could
not yet say: what was automated and the path to the session folder. Then the retro edits, then the action block. **Repeat the text, do not
compress it**: between 6.5 and here lies the whole retro, and whoever steps away comes back to a screen of housekeeping — the last screen
is the one that gets read, and a digest sends them back up the scroll for the line it dropped. The detail stays in `99-report.md`; icons
here too are chat-only.

**As the last block in the chat — a summary of the retro's edits: one line per address, saying what exactly changed.** The addresses are the
same four: **the knowledge base**, **the engine** (mandatorily with the plugin's version jump, `0.6.1 → 0.6.2`), **the profile** (which
subfile), **a skill** (which one exactly). The line format is `**<address>** — <what changed, one phrase>`; an address with no edits is
simply not mentioned, and «no edits» is a valid one-line answer too. From this summary the user sees where the session's lessons went
without opening `7-retro.md`. Example:

```
Retro edits:
- knowledge base — a new domain 12-auth-service.md (challenges, TTL, sessions)
- engine — 0.6.1 → 0.6.2: the findings rules into step 6, the priority scale into qa-manual
- profile — reporting.md: the project specifics stayed; auth-and-api.md: the rate limit and the 307/401 oracle
- skill orders-qa — three new job prefixes
``` Commit only if asked.

**The last thing the session prints is the action block: `⚠️` for «I cannot close this without you», `💡` for «worth doing, safe to
ignore».** Every line states **an action, not a problem** — «Ask the analyst whether <rule> applies to <finding>: the spec is silent», never
«the spec is silent». **`⚠️` is rare by rule — zero or one line is a normal round, two is already many** — and it is allowed
for two things only: a verdict blocked on somebody else's decision (an analyst's call where the spec is silent), and access that must be
fixed before the round can be closed. **Routine the user performs after every round gets no line at all** — pasting the tracker comment
where writing is not permitted, committing the engine clone: the user knows it, and a line repeated every round trains them to skip the block.
Everything else is `💡`: the engine being behind upstream, a profile behind the contract, environment leftovers, a case candidate for the
next round, a fixture worth creating on the environment. If everything is urgent then nothing is, and a `⚠️` that turns out to have been
optional costs the reader's trust in every red line after it. The block appears **here and nowhere else** — with one exception that is the
same statement: a message where the session stops and cannot continue at all (no profile, the environment is unreachable, the mode cannot be
determined). It goes into no file; the report's «Open questions» is its file-side twin and the two must not contradict each other.

**In the same block — one line about the engine's own version, and only when it is behind.** Compare the installed `version`
(`../../.claude-plugin/plugin.json`, the plugin root above this skill) against one read of
`https://raw.githubusercontent.com/codecube01/qa-cube/main/.claude-plugin/plugin.json`. Behind → «qa-cube is ahead upstream: yours 0.11.11,
upstream 0.12.0 — `/qa-setup` will update it, entirely optional». Otherwise, and **on any failure of the check — no network, a 404, a slow
answer — say nothing at all**: the line is a convenience, not a result, and an unrelated fetch may not add noise to a session's finale.
Nothing updates a plugin on its own, so this line is the only place the user learns the engine has moved. The rest of the engine's
housekeeping — fetching the update, reconciling `.claude/qa-cube-feedback.md`, offering it upstream — is `/qa-setup`'s and never a
session's.

**9. After delivery the session is still open.** Almost anything the user says once the report has been delivered is either an uncaught
defect in your work or a gap in the rules, and each is handled **one at a time, immediately** — what is saved up for «the next retro» gets
lost along with the context. Two branches, and they are not interchangeable: **a question** is answered on the merits (a rule may be
*proposed* in one phrase, never written into the files unasked), while **an objection about a fact is re-checked by your own direct
observation first** — not by re-reading your own report — and only then are the facts fixed, the rules after them. **Read
`references/after-delivery.md` the moment it happens**: what a confirmed objection obliges you to edit and in which order, what a withdrawn
finding does to its ID, where the mini-retro goes, and what to do when the objection does not hold up — all of it is decided in the first
two moves and cannot be repaired afterwards.

## Side findings

`<sessions>/side-findings.md` — a shared file of remarks and bugs **outside the scope of a particular task**: sessions' side findings and
anything the user asks to «put/move into side findings». The format is a table (date, finding, where from, severity, status) — described in
the file's header. Do not confuse the addresses: knowledge about the product goes into the knowledge base, the course of the checks into the
session folder, and orphan bugs plus «somebody should look into this» come here. When a finding is closed, update the status; rows are never
deleted.

## Engine feedback

`.claude/qa-cube-feedback.md` — next to the profile, and its counterpart: **the project's layer of engine rules**. The two layers never
overlap: the profile holds what is true only for this project, this file holds what would hold in anyone's — the retro's engine lessons when
there is no clone to write them into (step 7). It is committed with the profile for the same reason the profile is: a colleague's session
gets the whole rule set with the clone. It is not a log waiting for upstream: every session reads its open rows at step 0 and applies them
at their addresses.

The columns are the retro's plus the version the row was written under — «observation · rule · address in the engine · plugin version» —
and the file's header says so, so it reads cold. The rule is written as the entry it would become in the engine, by its mechanics; the
observation may name the project, since the file lives inside it, and `/qa-setup` anonymises the rows before offering them upstream. A
session sends nothing from it and asks nothing of the user. Rows are never deleted: a lesson that has since arrived in the engine moves to a
«Closed» block at the bottom with the version it arrived in — the only place the user sees their observation land — and is no longer read,
because the engine now carries it. Reconciling the file, and offering the open rows upstream, is `/qa-setup`'s work.

Under the earlier rule universal lessons were rephrased into the profile and never reached the reconciliation; the same lesson, arriving
later from upstream, then stood next to its own paraphrase.

## Capability degradations

| Capability = none | What changes |
|---|---|
| tracker | the input is only a free-form description from the user; ask them for the session's mode too (full cycle by default); the report's «tracker comment» is dropped |
| tms | cases are md files in `docs/test-cases/` (the default; the profile may override the path) (structure: preconditions, steps, expected result — as in a TMS); «mark automation» = a line in the case file |
| test-cases | `upfront` — step 3.5 runs, the analyst writes the cases, the manual tester does not create them; `inline` (and **a missing key**) — today's behavior: the manual tester creates the case after the run; `none` — cases are not maintained at all: `qa-analyst` is not launched, the manual tester creates no case, and the automator links the test to the task rather than to a case. With `tms: none` + `upfront` the cases are written as files in `docs/test-cases/` (or at the path from the profile) |
| environments | the check runs against a local launch per the profile's Environments section; the preflight check reduces to «the local environment is up» |
| logs | diagnostics only from response bodies; blockers are recorded without deep trace-id diagnostics — that is not the executor's fault |
| autotests | step 5 is skipped entirely; the report records «autotests are not maintained in this project»; qa-automator is not launched |
| browser | do not include UI scenarios in the plan; if the task is purely frontend, the session is blocked with an explicit message to the user |
| secrets | the sessions need no secrets; a scenario requiring credentials came up — the executor records a blocker in the result (credentials are neither requested nor invented) and the manager raises it with the user |
| knowledge | the step «read the product knowledge» is skipped; product findings from the retro are placed in `<sessions>/../knowledge/` (create it at the first finding) |
| engine-clone (also: no `.git` there, or the path sits inside `~/.claude/plugins/`) | the retro does not edit the engine — the normal state for a plugin installed from the marketplace. An engine lesson becomes a row of `.claude/qa-cube-feedback.md` and applies from the next session (step 0); only what holds for this project alone goes into the profile or a project skill, and no rule goes into both. No version bump, no `plugin update` — the engine arrives from upstream via `/qa-setup` |

## Boundaries

- **Browser work belongs to `qa-manual`, not to a role of its own.** A UI check is run through the real interface while watching the network
  (the rule is in the agent's instruction, the techniques in `references/browser-techniques.md` and the profile), and the manager's preflight at step 4
  verifies the access before the executor is launched. There is no separate web-tester and none is planned: a UI scenario and an API scenario
  belong to the same round, and splitting them would cost a hand-off in the middle of it.
- The manual tester and the automator work **sequentially** (the manual tester's result is the automator's input). Do not introduce parallel
  executors or a discoveries.md: the file scheme, the numbering and acceptance all assume one executor at a time, and a parallel round has
  never been the thing a session was short of.
- Secret values go nowhere: not into the session files (the folders may be backed up off-site), not into TMS cases, not into the report or
  the tracker comment. In request evidence the values are masked (`Authorization: <TOKEN>`). All the roles take credentials from the
  profile's `secrets` source — and reference it, not the values.

## Red flags

Each row is a rule sessions have broken while knowing it, and the thought that came just before the break: the rule read at step 0
does not survive the user waiting or a shortcut in reach, the thought caught at the moment of the decision does. Caught one — stop and
do what the right-hand cell says.

| The thought | What it actually is |
|---|---|
| «I'll just check this one myself, it's faster» | the manager does not test: the two exceptions are in «Roles», everything else is an addendum to the brief (step 4) |
| «The MR diff will show me what to test» | a plan read off the implementation agrees with it; the scenarios come from the requirements (step 3) |
| «The report is written — the retro first, the user after» | the result goes to the chat before the retro (step 6.5); a session that went quiet for minutes is why |
| «The profile is behind — I'll mention it with the summary» | that line is the session's first message, before any other call (step 0) |
| «The classifier refused the mutation — I'll phrase it differently» | a refused MUTATION is never reworded: the user's permission, then one repeat in your own session, paired with a control (`references/manual-brief.md`, «Your own harness refuses a call») |
| «The template will do for the report» | the project's format from the profile outranks it, read before the first line (step 6) |
| «The user is wrong — my report says otherwise» | an objection about a fact is re-checked by your own direct observation, never by re-reading the report (step 9) |
| «The round went cleanly, there is nothing for a retro» | the retro is mandatory; «no edits» is an outcome written after it, not a reason to skip it (step 7) |
