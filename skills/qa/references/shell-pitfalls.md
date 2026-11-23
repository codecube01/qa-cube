# Shell pitfalls of the harness

Read by `qa-manual` and `qa-automator` before their first shell command (the brief gives the path), and by the manager before its own —
preflight and recon run the same shell. The harness runs on macOS with zsh, and each line below has cost a round. What belongs to one
project's tooling stays in its profile.

## Contents

- reading and output — markdown by the Read tool, a quoted separator line, a wide search by `python3` + `re`
- time and processes — no `timeout`, a stop by PID, a background task judged by its artifact, a wait as a bounded foreground poll (an exact second, an absolute moment, the harness's limit), the lid and the power source, a monitor buffered by its last stage
- helpers — a temp file unique to the call, no helper named after a standard-library module, path arguments resolved before `cd`
- zsh — no word-splitting, words starting with `=`, unmatched globs, tied and read-only parameters, a colon after a variable
- secrets and files — a secrets file or a foreign dump read by structure or a whitelist, a non-ASCII source written with a coding line, files written by Write/Edit at absolute paths, no secret on argv, a `\uXXXX` in a tool's JSON

## The pitfalls

- **Open markdown with the Read tool, never `cat` through the shell.** The profile's subfiles and knowledge files are large, a large output
  spills into a persisted-output file, and the file has to be read again anyway. The shell is for commands, not for reading.
- **macOS has no `timeout`** — bound time inside the script itself.
- **A separator line is quoted: `echo '====='`.** zsh expands a word that starts with `=` into a command's path, so an unquoted
  `echo =====` aborts the line with `not found` — and the output it was meant to frame with it. Precedent: three executors who had read
  this file lost a call each to it while the rule sat in the middle of the zsh entry below.
- **A process is stopped by its own PID, never by a pattern — and a hung foreground call is not killed at all.** The shell runs on the
  user's own machine, next to their browser, their editors and the session's own servers, so `pkill -f <word>` or `killall` matches
  far more than the command it was aimed at: every process whose command line carries the word anywhere — an application path, a
  config directory. Stop what you started by the PID you recorded when you started it, or by the harness's own task stop; a
  foreground call that hangs is left to time out and re-run another way (in the background, judged by its file). Precedent: an
  executor cleared a hung call with a pattern kill on a three-letter word and terminated the user's browser — the round's own
  instrument — together with a container runtime, a VPN service and the session's tool servers.
- **A background shell task reports «completed» even when its command never started** — judge it by its artifact (the file exists, is
  non-empty, grows), never by its status. `nohup … &` inside a background task dies with its wrapper: make the script itself the background
  command.
- **A wait is a bounded poll in the FOREGROUND.** A foreground `sleep` is refused, and a background task's completion never reaches a
  subagent — so the wait is one call that checks the condition in a loop and returns when it holds, when its limit runs out, or on the first
  ERROR response: a Python script (`time.sleep` inside it) or, in a page, the `MessageChannel` loop from `browser-techniques.md`, kept under
  the tool call's limit. A wait longer than one call is a chain of such polls on a command started in the background (the rider below);
  when the chain becomes a checkpoint is what your instruction says to do with a long process. The error
  exit is not optional — a poll that tests only its condition spins to the limit on a malformed request, since an unknown field errors on
  every iteration. Precedent: such a poll lost nine minutes of a time-boxed window. **A measurement due at an exact second is
  never `sleep N && curl` across the tool's time limit** — past it the call is backgrounded or killed unpredictably and the point lands in
  the wrong second: one background script owns the whole schedule and writes each timestamped result to a file, judged by that file
  (a Python one run as `python3 -u`, below — buffered, the file stays empty until it exits). A wait until an absolute moment compares
  timezone-aware datetimes (`datetime.now(timezone.utc)` against the parsed moment): a naive `now()` is local time, and the wait ends
  hours off or dies on `can't compare offset-naive and offset-aware datetimes`.
  *And the tool call's limit is the harness's, not the call's `timeout`*: past it — in Claude Code about three minutes — a foreground
  call is moved to the background whatever its `timeout` says, and its output is lost. So a command expected to run longer — a test
  run, a seed — starts in the background, is judged by its artifact, and each wait on it is a foreground poll well under the limit
  (~160 s in Claude Code). Precedent: two executors set a ten-minute timeout on a test run and each lost a call when it was
  backgrounded at ~180 s.
- **A run longer than a few minutes on the user's laptop starts with a read of the lid and the power source** — `ioreg -r -k
  AppleClamshellState -d 4` and `pmset -g batt`. A closed lid on battery puts the machine to sleep every quarter of an hour, and
  `caffeinate` does not hold it; the sleep shows up as a network fault — a handshake dropped mid-request, one call «hanging» for many
  minutes, a poll overrunning its own limit, the clock jumping between two calls — so the first two failures get blamed on the VPN or the
  environment. `pmset -g log` (`Entering Sleep state`) settles it in one read. Closed and on battery → the run is not started: say so and
  wait for the lid or the charger. *And a run that dies from outside — the sleep, the tool's background limit — skips the test's own
  teardown*: every mutation its fixture made stays on the shared environment and is restored by hand at once, as for a killed executor
  (`manual-brief.md`, «The executor stopped»), and named in the result. Precedent: three runs of one test broke in a row and the first
  two were written off as a proxy fault; the third left two accounts flagged as the default handler, ready to intercept other runs'
  operations, until they were restored by hand.
- **A helper that can run in two processes at once writes its temp files under a name unique to the call** — `mktemp`, or the pid plus a
  counter. A fixed `_out.txt` shared by a background batch and the foreground checks lets one call's body land in another call's
  comparison, and it reads as a product answer: a `200` with a body of the wrong shape. Precedent: a background batch of detail reads
  overwrote the listing response a foreground check was comparing, and one false failure cost a re-run of the whole scenario.
- **A helper is never named after a standard-library module (`types.py`, `json.py`, `secrets.py`)** — the script's directory comes first on
  Python's path, so every `import` of that name beside it, a library's own included, loads the helper and fails far from the cause. A
  helper with side effects (a request sent, a file written) keeps them under `if __name__ == '__main__':`, or importing it for one
  function fires them again.
- **A helper that changes directory resolves its path arguments BEFORE the `cd`** — a relative body file read after it is a missing
  file, the request goes out with an empty body and the server answers `400 bad request`, in the shape of a product answer.
  Precedent: a helper handed to an executor did `cd` to the project root first, and twelve reads in a row came back `400`.
- **A monitor pipeline is only as line-buffered as its LAST stage.** `tail -f log | grep --line-buffered X | cut …` stays silent for minutes:
  `cut`, `sed` without `-u`, `head` and `awk` without `fflush()` buffer their output, so the event reaches the watcher long after it
  happened, or never. After a `--line-buffered` stage only `grep --line-buffered` / `awk '{…; fflush()}'` follow, or the whole filter is one
  Python loop that flushes. Precedent: a monitor for a long operation's commits fired nothing for twenty minutes while the log grew.
  *And a Python script that outlives the tool call buffers its whole stdout once it is not on a terminal* — a call moved to the background
  leaves an empty output file until the script exits. Run long scripts as `python3 -u` (or `print(..., flush=True)`). Precedent: a deadline
  wait backgrounded at the tool's limit left nothing to read; the state was rebuilt from the helper's own call log.
- **zsh is not bash.** An unquoted `$VAR` is not word-split, and `set -- $pair` inside `for` sets no positionals — use Python or a
  loop over literal names (zsh's own splitting, `${=VAR}` and `set -A`, stops the round on an approval: the entry on files the round
  produces, below). A word starting with `=` is expanded (the separator entry above). An unquoted glob that matches nothing aborts the command — quote `'*.md'`.
  Some lowercase names are zsh's own special parameters and do not hold a value of yours. `path` is tied to `PATH`, so `path=$3` in a
  helper leaves every later command `command not found` — `local path=$1` included, `local` does not protect it; `fpath`, `cdpath` and
  `manpath` are tied the same way. `status` is read-only (the assignment aborts with `read-only variable`), `argv=…` rewrites the
  positional parameters, `pipestatus` is overwritten by the next pipeline — name variables `url_path`, `code`, `args`. A colon right after
  a variable is a history modifier: `"$id:e…"` eats `:e` and the key comes out wrong — brace it, `"${id}:e…"`; the failure reads as «not
  found» from the API, not as a shell error.
- **A wide-context search is run with `python3` + `re`, not `grep`.** macOS grep (ugrep) aborts with «exceeds complexity limits» on
  wide quantifiers (`.{0,400}`) over a minified bundle, and on a narrower one (`.{0,200}`) over ordinary markdown in a non-Latin script —
  multibyte characters widen the automaton the same way a one-line file does; `re.finditer` over the same file answers at once.
- **The shape of a secrets file — and of any dump whose keys you did not write: a process history, a workflow's input, a relay's
  response — is read with its VALUES replaced, or through a whitelist of named fields (a label, an address); never through a mask of
  what looks secret.** A mask keyed on field names (`key`, `priv`, `token`) prints every secret stored under a name it did not foresee —
  a short alias, a suffixed field, a nested map keyed by account — and a mask on the value's shape prints every value its test gets
  wrong, straight into the transcript, with nothing to warn that it did. Print the structure instead: keys and value types (or lengths)
  at every level, or the fields you named. Precedent: three blacklists, three leaks — a key-name mask let a keys file's two-letter field
  through whole and a two-word mask a suffixed sign-in credential, and an «everything that does not look secret» listing printed nine
  secrets its value-shape test misjudged.
- **A script whose source carries non-ASCII text (Cyrillic strings, quoted UI captions) goes into a file via Write, not into a heredoc,
  and its first line is `# -*- coding: utf-8 -*-`.** The system Python rejects such a source with a "Non-UTF-8 code" SyntaxError and
  runs nothing — silently enough to be mistaken for an empty result — and the file being valid UTF-8 does not save it: a line past ~8 KB of
  non-ASCII text fails the same way from a file written by Write (Python 3.9: 3 000 Cyrillic characters pass, 9 000 fail) until the coding line is added.
  The same goes for a request BODY with nested quotes or non-ASCII text: it is written to a file and passed by path, never through argv —
  keep argv for one-line reads.
- **A file the round produces — a request body, a helper, a line of the result — is written by the Write/Edit tool at an ABSOLUTE
  path, never by a shell redirect; and a shell command carries no `cd $VAR` and no zsh expansion flags (`${(U)x}`, `${=r}`, `set -A`).**
  The harness's permission check reads each command statically: an overwrite (`> file`) whose target it cannot resolve — a relative
  name after `cd` into a directory held in a variable — or an expansion it cannot parse reads as a possibly destructive command, and
  the round stops on a manual approval the user may not be watching. The fix is the shape, not an allow-list, since the check is on the
  form of the command rather than its name: literal absolute paths, one helper call or a loop over literal names per command, labels
  passed verbatim or computed inside the script. Precedent: an executor built eight request bodies per call with `cd $DIR; echo … > x.json`
  and looped over them with `${(U)x}` — five approval prompts in one round, one of which stalled it for 45 minutes.
- **A SECRET never rides argv at all — a header no more than a body.** `curl -H "Key: $KEY"` puts the key in the process list for every
  process on the machine to read, so headers carrying a credential go from a file (`-H @<file>`, mode 600), as the body does
  (`qa-manual.md` holds the same rule for the executor's own calls: credential bodies by file, auth headers built inside the
  script). Precedent: a helper the manager handed over sent an account's API key as `-H`, and the executor rewrote it mid-round.
- **A tool's parameters are JSON, so a `\uXXXX` typed into a file's content reaches the file as the character itself.** A brief
  that lists `"\u00a0"` as a probe value then carries a real non-breaking space, indistinguishable from a plain one when copied. To
  write the escape as text, double the backslash; before handing over a file that names invisible characters, scan it for them
  (`python3 -c` over the file, counting `\u00a0`, `\u3000`, `\u200b`). Precedent: a brief's whitespace probes went out as real
  characters, and only a reviewer reading the file noticed; the retro that wrote this line hit it again on the line itself.
