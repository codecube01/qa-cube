# Shell pitfalls of the harness

Read by `qa-manual` and `qa-automator` before their first shell command; the brief gives the path. The harness runs on macOS with zsh,
and each line below has cost a round. What belongs to one project's tooling stays in its profile.

- **Open markdown with the Read tool, never `cat` through the shell.** The profile's subfiles and knowledge files are large, a large output
  spills into a persisted-output file, and the file has to be read again anyway. The shell is for commands, not for reading.
- **macOS has no `timeout`** — bound time inside the script itself.
- **A background shell task reports «completed» even when its command never started** — judge it by its artifact (the file exists, is
  non-empty, grows), never by its status. `nohup … &` inside a background task dies with its wrapper: make the script itself the background
  command.
- **A wait is a bounded poll in the FOREGROUND.** A foreground `sleep` is refused, and a background task's completion never reaches a
  subagent — so the wait is one call that checks the condition in a loop and returns when it holds or its limit runs out: a Python script
  (`time.sleep` inside it) or, in a page, the `MessageChannel` loop from `browser-techniques.md`, kept under the tool call's timeout. A wait
  longer than one call is a checkpoint — what your instruction says to do with a long process.
- **zsh is not bash.** An unquoted `$VAR` is not word-split, and `set -- $pair` inside `for` sets no positionals — use arrays or Python. A
  word starting with `=` is expanded (`echo ===X===` fails). An unquoted glob that matches nothing aborts the command — quote `'*.md'`.
