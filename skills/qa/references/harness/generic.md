# Another harness

Any harness with files and a shell that matched no row of the README's table. Every answer here is the
README's fallback, chosen by what your tool list does have — look before assuming it lacks something.

## Detect

Nothing matched. `0-session.md`: `Harness: <the harness's own name if you know it, else «other»>`.

## Launch a role

A subagent tool of any shape → the README's «subagents, but no named roles» fallback. None → «no subagents»:
the manager runs the roles itself, and the report says so.

## Continue a running executor

Only if the subagent tool keeps a child addressable; otherwise the README's «Continuation» fallback.

## Ask the user

A question tool if one is listed; otherwise plain text with numbered options, the recommended one first.

## Plugin root

Two directories above the `SKILL.md` you were given (`realpath` it if it is a link).

## Transcripts

Unknown: `transcripts.py --root <dir>` if the harness keeps Claude-format transcripts somewhere; otherwise it
exits 1 and the retro carries «no transcript numbers in this harness».

## Hooks

None assumed: the session is not renamed after the task.

## Updating the engine from a clone

No known command: commit the edit in the clone and tell the user to reinstall the engine the way they
installed it (`README.md`, «Install»); a harness that reads the clone directly needs nothing.
