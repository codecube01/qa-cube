# The session folder: sweeping, continuing, migrating

Read at step 2 of `../SKILL.md` — but **unlike the other catalogues, not once per session: only when its situation actually
occurs.** Step 2 names the three triggers, and each one owns a section here:

- the sweep found folders from previous months → **Sweeping into the month archives**;
- a session for this task already exists → **Continuing a session: round 2+**;
- the folder holds files under the old naming scheme → **Folders from the old scheme**.

A first round in a swept month touches none of them and reads nothing. Read the section your trigger names whole: every entry is
a way the folder has already been broken once, and the precedent that closes it is what paid for the rule.

## Contents

**Sweeping into the month archives**

- moved it — fix the links in the same pass, `mv` breaks them silently
- an empty grep is not proof: verify that every rewritten path exists

**Continuing a session: round 2+**

- date the round's trigger before anything else
- a round whose trigger is the requirements arriving, not a fix — and which therefore launches nobody
- renaming brings the whole name to the convention, not just the date
- what the executor's brief carries over is the line-by-line verdict, not the gist
- re-launch the analyst only when the input changed
- the previous session is a single file in the root
- stale evidence gets its warning inside the archived file

**Folders from the old scheme**

- old names are read as they are and not renamed — except the report and the meta file
- several reports in one folder are several answers to one question

---

## Sweeping into the month archives

### Moved it — fix the links in the same pass

Run a replacement of the paths with the archived ones across the whole repository and check for leftovers with grep. Navigation
from the project map, the profile, the knowledge base, the cases and the registries all rests on session-folder paths, and `mv`
breaks every one of them silently. Precedent: 8 folders moved in a second, 20+ links across six files took two passes to fix.

### An empty grep is not proof the links work — verify that every rewritten path EXISTS

Loop the list through a directory test. A mechanical prefix fix silently keeps pointing at folders that were also renamed, or at
ones that were never migrated in the first place, and the reader discovers it only when they open the link. Run the same
existence check over the links you did not touch, once per sweep. Precedent: a sweep left ~30 dead paths across the cases, the
registry, the profile and the knowledge base — including the profile's own pointer to the sample report, whose folder had been
renamed as well as moved, and a pointer to a session that had never been migrated at all; the prefix rewrite fixed neither, and
the grep came back clean.

## Continuing a session: round 2+

### Date the round's trigger before anything else

From the tracker: what happened to the task since the previous round (status history / `updated_at` / new comments). «Returned
to Testing on Aug 17» answers whether we are testing a new deploy or the same one, and it sets up the «was → now» table in the
report; the cheap way to pull that history is in the project's tracker skill.

### Renaming brings the whole name to the convention, not just the date

The folder is renamed to the current date (`mv <sessions>/2026-08-10_… <sessions>/2026-08-14_…`; a folder coming out of a month
archive returns to the root of `<sessions>/` in the process). **And if the session has ACQUIRED a source task since it was
created** — it began as an initiative run, or the task was filed later — the task id goes into the folder name in the same
motion. A long-lived session otherwise stays outside the naming convention forever and, worse, stops being findable by the
search that every round's step 2 starts with: a grep for the task id across folder names. Precedent: an initiative RBAC review
acquired a spec task two months in; round 2 renamed the folder by date alone, and the customer caught the missing id.

Read all the previous files before planning the round — plan, results, report, retro — and apply their lessons immediately.

### A round whose trigger is the REQUIREMENTS arriving, not a fix — and which therefore launches nobody

The dating above answers «new deploy or the same one», and the shape most rounds take follows from it. There is a third answer,
and it is the one a session started on a requirement-less task is heading for: **nothing was deployed, and what arrived is the
answer to the report's own questions to the analyst.** A numbered question that asks for a value gets a numbered one-line
answer — a type, a number, an owner — and each of those lines is a requirement the previous round did not have. The round it
triggers does no environment work and starts no executor: there is nothing new to observe, and re-measuring the same build
produces the same evidence at full price. Its whole product is a re-framing, and it is worth the pass because the delivered
report is now wrong in the reader's hands — it presents as open questions things the customer has answered, and it carries
findings whose cell says «needs an analyst's decision» about a decision that has since been made. Those cells lose that
sentence and gain the value, with the measured gap stated against it; the questions section becomes a table of answers and what
each one implies; items closed as «no requirement exists» are re-rated exactly as `report.md` requires of any new source of
requirements — some come back as findings, stronger than the candidates they replace, because a violated clause beats a gap.
Say in the report, in one line, that the round did not go to the environment and why; a reader who sees a fresh round assumes
fresh measurements. Two riders. The same round is the moment to re-check what the answers did to the SCOPE, not only to the
verdicts: an answer of the form «I was wrong, it is the other flow» closes an uncovered item outright and demotes another, and
neither happens if only the pass/fail column is revisited. And this is the entry that pays for writing the questions well in
the first place — numbered, one per item, each asking for a value rather than for a yes/no, and delivered through the channel
the poser actually reads. Precedent: a spike with no requirements at all was accepted by registering behaviour and asking four
numbered questions; the poser answered all four within five hours, one answer set a limit five times higher than the measured
one, another said «I was wrong, it is the other flow» — and the round that turned those four lines into requirements ran
without a single executor.

### What the executor's brief carries over is the line-by-line verdict, not the gist

Not the «gist of the findings» from the previous round but their verdict per AC/FR (`pass` / `fail` / not covered). Without a
«was: pass» the executor cannot tell a regression from a long-standing defect — and regressions are usually the most valuable
findings of a retest.

### Re-launch the analyst only when the input changed

The requirements changed (a new version of the spec, comments with clarifications) or the round's scope widened. Same
requirements — the cases are already written and the round goes straight to the manual tester: another analyst pass over
unchanged requirements yields the same cases at the same cost.

### The previous session is a single file in the root

A run from before the switch to folders: create a folder per the scheme and move the file inside with a dumb `mv`, without
renaming. It becomes the archive of round 1, and a `grep` on the task keeps finding the whole history in one place.

### Stale evidence gets its warning inside the archived file

The previous result was written against a contract that has changed since (fields renamed, an endpoint path moved) — append as
the first line of that file «⚠️ the contract changed on <date>: <was> → <now>, the current one is <file>». The round-2 executor
reads evidence as a ready-made recipe; having the rename recorded only in `0-session.md` means betting that they will read both
files, and in the right order. Precedent: assertions nearly went out against dead field names.

## Folders from the old scheme

### Old names are read as they are and not renamed — except the report and the meta file

Sessions from old runs (`session.md`, `task-manual.md`, `lessons.md`, `*-r2.md`, …) are left alone; the round's new files are
created per the current scheme, continuing the numbering from the highest number in the folder (no numbers at all — the new
round starts at 8).

The exception is the report and the meta file. The report sits under a former name (`6-report.md`, `report.md`,
`*-report-2.md`) → first thing, `mv` the latest (freshest) one to `99-report.md` and update that from then on. Same for the meta
file: `session.md` → `0-session.md`, appending the «Raw source» section to it. Two meta files are two answers to the question
«what session is this».

### Several reports in one folder are several answers to one question

Reports from previous rounds, if there are more than one, are merged into `99-report.md`'s «Round history» and deleted: two
reports in a folder are two answers to the question «what is the verdict on the task».
