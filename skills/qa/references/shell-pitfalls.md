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
  longer than one call is a checkpoint — what your instruction says to do with a long process. **A measurement due at an exact second is
  never `sleep N && curl` across the tool's time limit** — past it the call is backgrounded or killed unpredictably and the point lands in
  the wrong second: one background script owns the whole schedule and writes each timestamped result to a file, judged by that file.
- **zsh is not bash.** An unquoted `$VAR` is not word-split, and `set -- $pair` inside `for` sets no positionals — use arrays or Python. A
  word starting with `=` is expanded (`echo ===X===` fails). An unquoted glob that matches nothing aborts the command — quote `'*.md'`.
- **A minified bundle is searched with `python3` + `re`, not `grep`.** macOS grep (ugrep) aborts with «exceeds complexity limits» on
  wide quantifiers (`.{0,400}`) over one-line JS; `re.finditer` over the same file answers at once.
- **The shape of a secrets file is read with its VALUES replaced, never through a filter that masks the keys it guesses are secret.**
  A mask keyed on field names (`key`, `priv`, `token`) prints every secret stored under a name it did not foresee — a short alias, a
  nested map keyed by address — straight into the transcript, and nothing warns that it did. Print the structure instead: keys and value
  types (or lengths) at every level, with no value at all. Precedent: a keys file masked by «`key` or `priv` in the name» printed every
  private key in full, because they sat under a two-letter field.
- **A script whose source carries non-ASCII text (Cyrillic strings, quoted UI captions) goes into a file via Write, not into a heredoc.**
  A heredoc fed to the system Python has failed with a "Non-UTF8 code" SyntaxError and not run at all — silently enough to be mistaken for an empty result.
  The same goes for a request BODY with nested quotes or non-ASCII text: it is written to a file and passed by path, never through argv —
  keep argv for one-line reads.
