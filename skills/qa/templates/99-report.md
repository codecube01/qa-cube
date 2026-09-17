# Report: <session name>

_A living document: one per session, every round updates it in place. The sections below are the **current state**; the history lives in «Round history»._

**Source:** <the tracker task + related tasks pulled into scope>
**Current verdict (round N, <date>):** <one phrase — done / bugs / blocked>
**Method:** <how it was checked: API, browser, logs>

| Round | Date | Env | Trigger | Verdict |
|---|---|---|---|---|
| 1 | <date> | <tier> | initial check | <one phrase> |
| 2 | <date> | <tier> | <returned to Testing / new deploy> | <one phrase> |

## What is confirmed (matches <FR/AC>)

- **<FR-1>.** ✓ <what exactly was checked and which effect confirmed it> *(round N; caveats about the limits of the check — in italics)*

## Findings

<⚠️ If the project profile defines its own report format — render by that one, not by this template.>

<The table holds ONLY CURRENT findings (open/reproducing) that come from the task's requirements; side findings go to the side-findings registry and are listed with a link BELOW the table. The table gets copied into the tracker as a whole, so its cells carry no file paths, no ids from other runs and no round numbers — only words, dates and identifiers a developer understands (tracker tasks, entities, endpoints).>

| № · Priority | Requirement | Description and risk |
|---|---|---|
| **<ID> · <Blocker\|Critical\|Major\|Minor>** | <FR/AC numbers + source, not prose> | **<A bold phrase in business language: what is broken from the user's point of view>** <evidence with numbers: what the spec requires versus what came out.> <The risk in user terms.> **<Needs an analyst's decision: …>** *Tech.: <root cause, endpoint, trace id, date>* |

<Whatever got fixed during this session goes in a block below the table: «Fixed: <ID · priority> — <what it was, what confirmed the fix>»; details — in «Round history».>

<Whatever is already filed in the tracker goes in a line below the table: «Outside the table (not carried to the tracker): <what reproduces>, <date>, already filed as <task>».>

## Not covered (with reasons)

| What | Reason | Round |
|---|---|---|
| <scenario/requirement> | <why: no access, needs a second artifact, requires a day of waiting> | <N> |

## Automation

- Test: <test: class/file#method> — <green / disabled with a reason / not written, reason>
- Case: <TMS case: id>, placed in <path/suite>

## Round history

<The newest round on top. One block per round: the delta only, no retelling of the sections above.>

### Round 2 — <date>

**Trigger:** <what happened to the task after the previous round, per the tracker>
**Fixed:** <finding IDs + what confirmed it>
**Still broken:** <IDs + what we see now>
**Newly broken:** <regression IDs>

### Round 1 — <date>

**Outcome:** <the round's verdict in one phrase>
**Findings filed:** <IDs, comma-separated>

## Environment leftovers

<what was created and stayed behind: entities, changed settings, live markers and their lifetime; «the environment was restored» is an answer too>

## Open questions

<the goal is: empty>

## Tracker comment

_(the section is dropped with `tracker: none`; keep it to 3–5 lines — what goes to the tracker is the findings table, not a retelling; every round rewrites it for its own verdict)_

```
QA: checked <date> on <env>. <Verdict in one phrase>.
Findings: <N> (<priorities>) — <where they live: report / side-findings registry>.
Not covered: <one line with the reason>.
Case: <id>. Autotest: <test> (the line is dropped if no test was written).
Report: <path to the session folder>
```
