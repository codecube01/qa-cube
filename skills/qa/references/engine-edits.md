# Editing the engine from a retro

Read at step 7 of `../SKILL.md` — **only when `engine-clone` is a valid clone**, whole, before the first edit to the engine. Without a
clone the lesson becomes a row of `.claude/qa-cube-feedback.md` and this file does not apply: the row meets the engine at `/qa-setup`'s
reconciliation, not here.

Why it exists: the engine's repository reviews every change before it is committed, and the retro — running in another project's session,
with that project as its working directory — never sees the repository's own rules. So the review kept finding the same slips in retro
edits, all of them visible to whoever made the edit: a version bumped with no CHANGELOG line, one rule written twice with two different
thresholds, a rider filed under a section whose definition excludes it, a second precedent appended mid-sentence, an entry with no index
line. The steps below are that review, moved to the place where the edit is made.

## Before writing: find the entry that already says it

- **Search the whole clone for the lesson, not the catalogue you are about to open** — by the symptom (the error text, the observable),
  by the mechanism, by two or three of the lesson's key nouns: `grep -rn` over `skills/` and `agents/`. An entry that already states the
  rule or its symptom takes the lesson IN — a new shape, a sharper sentence, a better precedent — and nothing is written elsewhere except,
  at most, a pointer to it. Two entries on one symptom drift apart at the first retro that touches only one of them. Precedent: the same
  tab-drift error got a recipe in two entries of one catalogue, one saying «where it keeps recurring», the other «from the first call».
- **The address is decided by the section's definition, not by the neighbour that looks alike.** Read the head of the section or family
  the lesson is headed for and check that the lesson's case falls under what the head defines. Precedent: a rider about a task that
  states a checkable claim was filed under «the task has NO requirements at all», whose head defines that as «nothing but a title».
- **The form is decided by what failed, before a word of the rule is written.** The same lesson holds in one form and backfires in
  another, and prose in a catalogue is only one of the forms:

  | What failed | The form that holds | Where it lives |
  |---|---|---|
  | knew the rule and broke it under pressure — the user waiting, a competing incentive | a flat rule plus the thought that comes just before the break («I'll just check it myself, it's faster») | the entry; a rule of `SKILL.md`'s procedure — its thought becomes a row of that file's «Red flags» |
  | did the work, but the output came out the wrong shape — a bloated brief, a buried verdict | a recipe: what the output IS, its parts in order; never a list of «don't» | the step or the template that produces it |
  | left out one element of something it produces anyway — a field of the brief, a line of the report | a slot in the template it fills in | `templates/`, not prose beside the template |
  | mechanical: countable or matchable, the same every time | a check in a script, with its test | `scripts/check_session.py` for session files, `scripts/session.py` for the folder's housekeeping; the entry shrinks to a pointer |
  | right in one situation, wrong in another | a condition on something the agent can observe | the entry |

  No nuance clauses: «don't X unless it matters» reopens the very negotiation the rule exists to close, so a real exception is written
  as a condition of its own on an observable fact. This is also how a catalogue over its budget makes room: an entry that is really a
  slot or a check leaves the catalogue for the template or the script. Precedent: the output language lived only in the profile, which an
  executor reaches late, and the executors kept narrating in the engine's language until it became a slot — the first line of every prompt, a field of the brief;
  and three report checks (the column count, the cell length, a secret value) went out wrong at least once each while they were rules
  to keep in mind, until they became `check_session.py`.
- **Where a catalogue's «Contents» says its lines are the rules** (`planning.md`, `manual-brief.md`, `report.md`, `automation.md`, `executor.md`), the index line IS the rule and the body is its
  mechanism and precedent — so a lesson there is written twice, and the line comes first: a trigger, an arrow, what the plan does about
  it, in one sentence; the body then carries the «why» and the precedent, and never a second version of the rule. A new shape of a
  family is one more `· trigger → rule` item on the family's line. The validator refuses an index line without an arrow. Precedent: the
  manager read the whole catalogue because its index named the shapes without saying what to do about them, and the reading cost about
  half of the manager's context at the end of planning.
- A family, the third-patch rule and the engine/profile split are in step 7 of `../SKILL.md` and hold here unchanged.

## Writing

- **Re-read the entry whole and rewrite it, do not patch it.** The new clause goes where it belongs in the argument; a sentence inserted
  into the middle of another leaves the entry with two conclusions and the reader with the older one.
- **One point, one precedent.** A second precedent for the same rule replaces the first or merges with it into one story. A rider with a
  mechanism of its own is not a second precedent — it gets a paragraph of its own (`*And where …*`) with its own precedent. Precedent: a
  refused-mutation entry ended up with the new precedent in its middle and the old one at its end, the old one readable against the new
  rule.
- **The index and the counts move with the entry**: the line in the catalogue's «Contents» (or one more `·` item in a family's line;
  in a rules index, a `trigger → rule` line, as in «Before writing»), and any count written in words — «read eight ways», «the eight
  entries below», «all four still pay».
- **Anonymisation covers the description, not only the names.** Step 7's rule, plus: a precedent that stacks the domain's own nouns until
  they describe one kind of product is reworded down to the generic class — the mechanics survive it, the product's portrait does not.

## After writing

1. **A CHANGELOG line** under `## [Unreleased]` in `<engine-clone>/CHANGELOG.md`, in the right subsection (`Added` / `Changed` /
   `Fixed`): two or three lines, what changed for the reader, no precedent and no retold mechanics. A line on the same subject already
   there is extended, not repeated. The patch bump from step 7 is made now, before the checks, and once per retro however many files
   it touched; `claude plugin update` waits until after the review, so the cache gets the reviewed text.
2. **The checks, from the clone:**
   `python3 <engine-clone>/.github/scripts/validate-plugin.py` and
   `git -C <engine-clone> diff -U0 | python3 <engine-clone>/.github/scripts/check_identifiers.py --diff`.
   The validator also ratchets the edit against the last commit: an engine change with no bump, a bump with no CHANGELOG line, a section
   that gained an entry while its index group stayed the same, a count that no longer matches its list. It also holds every catalogue
   and agent instruction to a size budget, because each is read whole — by the manager, or by the reviewer that reads it for them — and every entry is paid for in every session: over it, the same
   edit makes room — entries sharing a mechanism folded into one family, a second precedent merged into the first — and the number in
   `check_engine_edits.py` is not the retro's to raise. Reading the repository (`git diff`,
   `git show`) is not a «git operation» in step 7's sense; adding, committing, stashing or switching branches is. A failure is fixed and
   the checks re-run — the retro does not end on a red validator.
3. **A review with fresh eyes — one subagent (`general-purpose`), launched with no context from the session.** Its brief: the clone's
   path; «review `git -C <engine-clone> diff` against the sections "Before writing" and "Writing" of
   `<engine-clone>/skills/qa/references/engine-edits.md`; search the clone for a twin of every added entry; fix what you find with
   targeted edits only — never rewrite a file whole, another project's retro may be editing the same clone — then re-run both checks from
   "After writing", step 2; return one line per fix, or "nothing found"». The diff may hold earlier retros' uncommitted edits: they are
   reviewed too, nobody has reviewed them either. Why a subagent: the author of a lesson reads its own entry as correct and does not go
   looking for the entry it duplicates; a reader with no stake in the lesson does. Precedent: of the slips listed at the top, the one a
   manual review missed as well (an entry with no index line) was found only by the ratchet — and every other one was found by a reader
   who had not written the lesson.
4. **In the retro summary at step 8**, one line: what the fresh-eyes review fixed, or that it found nothing.
