---
name: qa-day
description: Use when the user asks what was tested over a day or a week, or how a session on some task ended — «what did I test today», «day digest of test sessions», «QA summary for the week», «how did the session on task X end»; also triggers on the Russian «сводка сессий за день», «что я оттестировал сегодня», «что тестировал за неделю», «чем закончилась сессия по задаче X».
---

# /qa-day — the digest of a day's test sessions

The typical case, one command:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/qa-day/scripts/qa_day.py" <project root> [<another root> …]
```

No root given — the current repository. The variable is expanded by the plugin runtime; a shell that does not have it takes the
path from this very file's own directory (`scripts/qa_day.py` sits next to this SKILL.md).

The script prints facts out of the session folders; **the answer to the user is written by you**, not by the script — see «How to
deliver it». Nothing here needs configuring: the paths come from the project profile that `/qa-setup` already wrote, and the
digest introduces no key of its own.

## The flags

| Flag | What it does |
|---|---|
| *(roots as positional arguments)* | one run covers several projects — a QA touches several repositories in a day, and three separate runs are three separate answers to one question |
| `--date YYYY-MM-DD` | the window's last day; the default is today |
| `--days N` | how many days back the window reaches, `--date` included (default 1) — a week's summary is the same question asked with `--days 7` |
| `--task <ID>` | the secondary mode: the freshest session on a task id, at any date. For «the task has already been moved out of a testing status, what did it end with» |

`--task` searches in two passes: folder names first (`*_<id>-*`, in the root of `<sessions>/` and in the month archives), and
only then a grep of the passports. The second pass is what finds a task that was tested inside a **multi-task** session named
after a different task — without it the answer would be «there was no session», which is worse than a slower search.

## What the script reads, and what it deliberately does not

- **the sessions path per root** — `sessions:` from `<root>/.claude/qa-profile.md`; no profile or no key → the contract's default
  `docs/test-sessions/`. It also picks up `language:` and prints it per project;
- **session folders at two levels** — the root of `<sessions>/` (what is alive) and its subfolders (the month archives the
  engine sweeps closed sessions into). A digest that walks one level loses everything from the previous month;
- **the day of a session is the date in its FOLDER NAME**, never a file's mtime: by the engine's convention the folder is named
  after the last round and a retest renames it. Consequence, stated plainly because it will come up: a session worked on today
  whose folder was not renamed is not in the digest. Precedent: a digest built on mtimes counted a session as today's because a
  typo was fixed in its report, and the day's list stopped matching what the person had actually run;
- **the passport and the report** — `0-session.md` and `99-report.md`, falling back to the names earlier schemes used
  (`session.md`, `report.md`, `*-report*.md`): live projects hold both schemes, and a round that ran under the old one is still
  a round that happened;
- **the passport is localized, so nothing is matched by a field's caption** — the parse rests on the template's structure (the
  `- **field:** value` rows above the first `##`, then the last row of the round log) and prints the values verbatim. The
  interpreting is yours: that is what makes the digest work in any project language;
- **the task ids of a session** come from the folder name and the passport's title only, never from the passport's body: the
  body lists parent tasks, neighbours and past rounds. Precedent: reading ids out of the whole passport reported six tasks for
  one session, of which one was the session's;
- **the registry row** — the line in `<sessions>/README.md` that mentions the folder;
- **out of the report** — the verdict lines, the count of findings by severity (the untranslated `Blocker/Critical/Major/Minor`
  scale is the one anchor a script may match in a localized report) and the tail sections with their own headings, which is
  where «what is left on the environment» and the open questions live. A project format that has no such section simply has
  none — that is not an error;
- **nothing found is never an error**: a missing sessions directory, a folder with no passport, a report with no status each get
  an honest `note:` line and the run carries on. One unconfigured project must not cost the digest of all the others.

## How to deliver it

1. **Group by project, one live line per session:** `<task ids> <name> — <what was done: the round, the verdict, how many
   findings>`. That is the shape of the answer to «what did I test today»; anything longer is the person doing the reading
   themselves. Precedent: raw output for one day across two projects ran past a hundred lines, and the question went unanswered
   until it was retold in five.
2. **Name what is left on the environment separately**, collected across all the projects — not scattered through the
   per-session lines. Leftover test entities and changed settings are what the next round's sanity check starts from, and a
   leftover named in the middle of a session's paragraph is a leftover nobody carries over.
3. **Write in the project's language** (`language`, which the script prints for every root). Roots with different languages —
   keep the whole digest in the language of the first root, the repository the user is sitting in: the digest is addressed to
   the person, and switching language mid-list serves nobody.
4. **Do not dump the raw stdout.** It carries the passport's whole header and the report's tail so that you can pick from it;
   pasting it makes the user the parser.
5. **Do not invent what the files do not say.** A `note:` line means exactly what it says — «no passport, status unknown» is a
   fine thing to report, «probably finished» is not. A session that carries several task ids is reported with all of them.
6. **Say what the window was**, and add the one caveat when it matters: the day comes from folder names, so a session whose
   folder was not renamed to today is absent. Volunteering that once is cheaper than the user rebuilding trust in the digest.
7. **Close with the action block** — `⚠️` for «I cannot answer this without you», `💡` for «worth doing, safe to ignore», each line
   an action rather than a problem. A digest reads files and asks nothing, so `⚠️` here is almost always absent and that is the
   correct outcome; the useful lines are `💡`: clean up the leftovers named above, rename a folder whose round ran on another day
   so tomorrow's digest finds it, open the session whose passport is missing. An empty block is not printed at all.

## Boundaries

- **The digest does not go to the tracker** and does not count the queue of tasks: reconciling with a tracker, and writing the
  result anywhere outside stdout (personal notes, a diary, someone else's files), is project specifics and lives in a project
  skill. The engine hands over the facts from its own folders, and that is the whole contract.
- **It writes nothing** — not into the project, not into the sessions. Reading and printing only.
- **It introduces no profile key** and asks nothing at onboarding: it works from the moment the plugin is installed. A digest
  that first needs a setup pass is a digest that gets set up on the day someone finally needs it.
