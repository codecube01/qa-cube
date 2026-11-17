# After delivery: objections and questions

Read at step 9 of `../SKILL.md` — **by trigger, not once per session**: the moment the user says anything after the report has been
delivered. Most sessions end at step 8 and never open this file; the one that does is holding either an uncaught defect in its own work or
a gap in the rules, and both are decided in the first two moves.

Handle what the user said **one at a time, immediately**, without saving it up for «the next retro» — what is saved up gets lost along with
the context. First work out which of the two things you are looking at.

## Contents

- a question — answer it, and propose a rule only if one grows out of the answer; a fact about an artifact → read it fresh, a dead connector → the profile's other route
- an objection about a fact — re-check by direct observation, before anything else
- the objection is confirmed — fix the facts before the rules
- only then a mini-retro, in the same session's retro file
- the objection was not confirmed — say so with proof, and change nothing
- what the mini-retro is actually about: the class of claims published without your own eyes

---

## A question

«Why is it like this?», «what about X?», «does it really work that way?» — answer on the merits, do not run a mini-retro. If a rule grows
out of your answer (the question reveals a recurring blind spot), **propose it in one phrase and ask whether to adopt it** — do not write
into the files yourself: not every question means the process must change.

**A question about an artifact — what a case covers, what a test asserts, what a file says — is answered from a fresh read of it, never
from the session's memory of writing it.** Memory holds what was meant, the artifact holds what was written, and an answer to a question
is published as surely as a report line. A connector that failed to start is not the system out of reach: the profile names another
route (a script, the REST API), and «I could not check» is said only after that route fails too — the rule of `report.md`, «"Not
covered — no access to X" is a claim about a fact», applied to an answer. Precedent: asked which of two tasks a
case covered, the manager answered «only the first» from memory, adding that the case tool had not connected; the user's next question
made it read the case through the REST API — the case covered both tasks, its steps through the second task's path.

## An objection about a fact

«Your report says this, but actually it's that», «and here you can see that…» — the order is strict and exactly this.

### 1. Re-check it yourself, by direct observation

Not by re-reading your own report, and not by reasoning. The objection points at a specific screen, endpoint response, number — go and look
there, in several conditions if need be (another window width, another object, another role).

### 2. The objection is confirmed — fix the facts before the rules

The report first (the findings table, the verdicts on the requirements, the summary, the tracker comment), then everything derived: the
session's meta file, the session registry, the side-findings registry, the knowledge base, the findings numbering in the profile. A
withdrawn finding **burns its ID** (the number is not reused) and gets a paragraph «withdrawn on re-check <date>» with a rationale — it has
no right to vanish silently. A changed priority is also an edit of the verdict, not cosmetics.

### 3. Only now — a mini-retro on this one objection

A row in `<N>-retro.md` of the same session (no new file is created) in the same «observation → rule → landed in» format, the fixes by
address (engine / profile / knowledge base / skill), a bump of the plugin's patch version and the question about `contract-version`. In the
chat — a short summary of the edits, as at step 8.

### 4. The objection was not confirmed — say so, with proof, and change nothing

Agreeing out of politeness and rewriting a correct report is a worse outcome than an argument. The rules stay untouched in that case.

## What the mini-retro is actually about

**An objection about a fact almost always means the verdict was issued on someone else's evidence without your own check** — and that is
the material for the mini-retro, rather than the error in the report itself. In the rule, look not for «re-check this screen» but for
«which class of claims do I publish without looking myself».
