# Issue file: <ID>

_The skeleton of a ready-to-paste tracker task — `bug-reports/issue-<ID>.md` in the session folder, one file per finding, written only on request (`../references/report.md`,
«When the customer files the finding by hand»). The user pastes the body into the tracker WHOLE, from the title down: everything in it is
for the developer and the analyst, except the last line, which is for the next round's «is it filed» search. **This shape outranks the
profile and the tracker's habits** — a profile rule on how issue texts look is stale, not an override. Labels are written in the session's
language; the Russian set is: Требование, Шаги, Контроль, Ожидалось, Фактически, Где чинить, Связано, Подробности замеров, Окружение,
Находка QA, Заведено._

---

# <Block> \ <Sub-block> \ <What is wrong, under what condition — an ordinary sentence>

> <ONE sentence: the condition → what happens instead of the expected → how it shows. Readable by anyone: no API field names, no code.>

**Requirement:** <FR/AC> «<one phrase quoted from the spec>»

## Steps

1. <Where, as whom, preconditions> → <result>
2. <Action> → <the result that shows the bug>
3. Control: <the neighbouring case> → <works correctly>

**Expected:** <one phrase>

**Actual:** <one phrase> — <what it costs the user, one phrase>

## Where to fix

- <the cause hypothesis and its place>
- Related: <sibling ids, tracker tasks>

## Measurement details

- <only when the bug cannot be reproduced or judged without them>

**Environment:** <environment>, <role / account>, <build>, <date and time of the last reproduction>, <request id / entity UUIDs / workflow id / tx hash>; <re-checked on the served build or not>. 📎 <ID>.png

**Finding:** <ID> · <backend|frontend> · <source task, round>

---

## Rules of the shape

- **Title.** `\` only separates the functional blocks at the start — one or two levels (the product area, its section). After the last `\`
  comes an ordinary sentence that carries the condition; no `\` inside it. The title is the task's name and is not repeated in the body.
- **The quote** is one sentence of up to ~30 words: the condition, what happens instead, one concrete value if it makes the point. Not the
  requirement, not the risk — they have their own lines.
- **Requirement:** the FR/AC number plus one quoted phrase. No violated clause → «outside the requirements: <why it is a defect>».
- **Steps** are a numbered list, never a table — a table breaks when pasted into a tracker. One `action → result` per item; 2–5 items, up
  to 6 for a chain of API calls; the first item carries where, as whom and the preconditions. The optional last item, `Control:`, is the
  neighbouring case that works — it marks the bug's boundary and is worth more than another step.
- **Expected and Actual** are separate paragraphs with a blank line between them — without it Markdown glues the two into one line. One
  phrase each; Actual ends with what it costs the user, so there is no separate «Risk» section.
- **Where to fix:** at most two bullets — the cause and its place, and `Related:`. A sibling defect with the same root cause stays its own
  file, and the line says «fix together, verify separately».
- **Measurement details** — a section only when the bug cannot be reproduced or weighed without them: several scenarios, a time window,
  the argument for the priority. It goes at the end of the text, never into a tracker comment: comments are not read with the description.
- **Environment** is one line: the environment, the role, the build, the date of the last reproduction, and the anchors a developer
  searches by — request ids, entity UUIDs and workflow ids in full, never shortened. A screenshot is attached by `📎 <ID>.png`: the
  file stays in the session's `screenshots/`, no copy next to the issue file, and its name is the finding's id (`<ID>-2.png` for a
  second one) so the user picks it for the task without opening it; `session.py shot` renames a candidate's screenshot once the id is
  assigned. Whether the served build was re-checked is a fact on
  this line («last measured <date> on `<build>`, not re-checked»); advice to the filer («look once before filing») goes to the delivery,
  never into the file.
- **The finding line is last**: `<ID> · <layer> · <source task, round>`. The developer does not need it, but it is the only thing the next
  round's «is it filed» search finds in the tracker. Once the task exists, `**Filed:** <task> (<date>, <status>)` follows it on disk.
  This line is the file's one exception to «What stays out of the cells» (`../references/report.md`): the finding's id and the round
  are allowed here and nowhere else in the body; `Related:` names a sibling finding by its id only until it is filed, then by its task.
- **Not in the file:** the priority (a tracker field — in the text it goes stale), a quote of the analyst's order («file it as medium»),
  paths into the QA repository and round file names, advice to the filer, a second copy of the title, separate «Risk», «Evidence» or
  «Priority» sections.
- **Size: one screen** — about 2–2.5 KB for an ordinary bug, about 3.5 KB for a complex one. Above that, the surplus belongs in
  «Measurement details» or stays in the report.

Precedent: the sessions of one QA practice drifted into six issue-file formats — a table of fields before the essence, steps as a table,
the finding id at the end or only in the file's header, the priority written three times, risk restating the actual result — and the
tracker received descriptions of up to 20 KB. The user picked this shape after reading three findings rewritten in it side by side, and
ruled on each point: `\` only for the blocks, the finding line last, Expected and Actual apart, details in the text rather than a comment.
