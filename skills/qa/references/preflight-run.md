# A preflight run: `/qa --preflight <task>`

Read at step 0 of `../SKILL.md` — **whole, and only when the input carries `--preflight`** — before step 1 begins: it changes where
every question of the steps below goes, and step 1 asks its first one before the plan exists.

Why it exists: a session can be started with nobody at the keyboard — a watcher outside the engine notices a task entering testing and
opens a session for it. The preparation (reading the task, the plan, the preflight, the brief) is worth doing at once, while the build is
fresh; whether the round runs is the user's call, made later and per session. So the run does everything up to the first executor that
touches the environment, stops, and leaves a card the user can decide on from its first line.

## Where it stops

- **Full cycle**: steps 1, 2, 3 and 3.5, then step 4's preflight, the brief and its catalogue review. Stop before `qa-manual` is launched.
- **Automation-only**: steps 1, 2, 3 and 3.5, then the same preflight against the access the automator's minimal run will use, the
  automator's brief, and stop before `qa-automator` is launched. Step 5's choice of what to automate is not put to anybody: it goes into
  the card as a question, with the lines `references/automation.md`, «The decision», says that question carries.
- **`qa-analyst` does run** at step 3.5 with `test-cases: upfront`: it never touches the environment, and the brief is built on its cases.
  The cases it writes stay in the TMS whatever the user decides — the card says so in its «Plan» line.
- **Not done at all**: the report (`99-report.md`), the delivery of step 6.5, the retro, and any write to the tracker — no comment, no
  status, no assignee. The team must not see a round that the user has not yet decided to run.

## Nobody answers

Every place where a normal session asks the user and waits becomes a question in the card, and the run goes on as far as it can without
the answer. **No question dialog (the adapter's «Ask the user») and no question that ends a turn waiting** — an unanswered dialog
holds the run until somebody happens to look, which is exactly what the run exists to avoid.

- **A choice that shapes the plan** — the environment, the width of a bundle of related tasks, step 1's start question → the plan is built
  on an assumption stated in it, and the card puts that assumption as a question together with what changes if the answer differs.
- **What needs the user's hands** — a sign-in the profile says only the user can make, a wallet, a one-time code, the «Window and focus»
  slot → not attempted; the scenarios resting on it are marked blocked in the plan, and the card names what is needed.
- **A mutation a normal round sanctions with the user** → not performed; the brief carries it as the sanction question, answered at the
  continuation.
- **What a normal preflight does without asking** — issuing access from inside the product, signing in identities that need no hands,
  opening the round's target screen, dating the build → done as usual, and dated in the brief's «Entry state».

## The finale: the card

Files first. `0-session.md`: the status `preflight-done` and a round-log row «preflight» with the time. The registry `<sessions>/README.md`:
the session's row, its verdict cell «preflight: ready / ready with caveats / blocked — <reason>». `<sessions>/environment-state.md`: the
facts the preflight measured, dated. **Several preflights can run on one machine at once**, so each of these shared files is re-read right
before its edit and changed in one edit, never written from a copy read at the start.

Then the card — the run's last message, in the session's language; it replaces step 8's finale and its action block:

```
<READY | READY WITH CAVEATS | BLOCKED: <reason>> — <task id> (<kind> «<title>»)
Mode: <full cycle | automation-only> · environment: <env> · requirements: <spec-grade | draft>
Plan: <n> scenarios — <what they cover>; not covered from the start: <… or «nothing»>; <with upfront: cases written — ids>
Entry state (as of HH:MM UTC): <identity, the screen it is on, the access issued>
Questions: <one per line, each with what its answer changes>
Session folder: <path>
Next: «continue» launches <qa-manual | qa-automator>; «stop» closes the session as dropped
```

**READY** — the round can be launched as briefed. **READY WITH CAVEATS** — it can, but some scenarios are blocked or rest on an
assumption the questions name. **BLOCKED** — it cannot start without the user: the environment is unreachable, the entry needs hands, the
build under test is not on the environment. The first line is the decision, because the user reads several cards in a row; a line with
nothing in it (no questions) is left out.

## The continuation

- **In the same session** — the user's answer arrives. Apply the answers first: one that changes the scenarios edits the plan and the
  brief, and the step-4 catalogue reviewer reads the brief again. Then **re-establish the entry, never trust it**: the card's state is
  hours old by now, so the liveness oracle runs again (a new tab, as step 1 says) and the brief's «Entry state» gets the new time. Then
  the launch, and the session goes on as normal from step 4 — acceptance, step 5, the report, the retro. The retro covers the preflight
  too: its decisions are in the plan and the brief.
- **In a new session** — `/qa <task>` without the flag. Step 2 finds the folder with `preflight-done`: this is **not a new round** — no
  rename, no round suffix, the numbering goes on. Read `0-session.md`, the plan and the brief; append the task comments that appeared since
  the preflight to «Raw source» (one that changes the requirements reopens the plan); redo the preflight check, not the plan; then launch.
- **«stop»** — the status `dropped`, the registry's verdict cell «preflight: dropped by the user», and `environment-state.md` gets what the
  preflight left behind (issued keys, open sessions). No retro, no tracker comment.

`--preflight` on a session that already exists (a retest) stops at the same point of the new round: the round's plan, the preflight, the
brief, the card. On a session still `preflight-done` (the watcher fired twice) it is no new round either: the new comments go into «Raw
source», the preflight is redone, «Entry state» and the card are rewritten, and no file is added.
