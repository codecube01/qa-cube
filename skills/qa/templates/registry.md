# Session registry: <project>

<Two or three lines: this is the entry point for «what has already been tested» — one row per session, newest first; the full
report is `<folder>/99-report.md`; side findings — `side-findings.md`; what the environment holds NOW — `environment-state.md`
(the «Left on the environment» column is the session's trace as of its round, not the current state).>

| Task | Last round | Verdict in one phrase | Left on the environment | Folder |
|---|---|---|---|---|
| <key> | <date> (R<n>) | <one phrase, ≤ ~200 characters: the outcome + the finding ids> | <objects/ids the session left, or «none»> | `<folder>/` |

<!--
The registry is this table and nothing else — no sections below it, no «archive», no per-session prose.
- The verdict cell is ONE phrase: the outcome and the ids of the findings. Everything else — the mechanics, the numbers, the
  round-by-round story, what changed since — lives in the session's `99-report.md`, one click away in the «Folder» column.
  A cell that has grown into a paragraph is unloaded into the report in the same finale.
- A new round of the same session rewrites its row (date, verdict); it does not add a second row or append to the cell.
- Stand state does not go here: a fact about what the environment holds now goes into `environment-state.md`.
- Precedent: a registry whose verdict cells grew to 500–1000 characters and which carried a raw «summaries archive» below the table
  reached 80 KB — half of it unreadable, and the whole of it read at every sanity check.
-->
