# opencode

opencode reads the skills from its skills directory and the roles from its agents directory, so the install
(`.opencode/INSTALL.md`) links `skills/` and `agents/` there. Local models are run the same way — the model
changes nothing below. Trust your actual tool list over this file where they disagree.

## Detect

The tool list has `task` (with a `subagent_type` parameter) and `skill`. `0-session.md`: `Harness: opencode`.

## Launch a role

`task` with `subagent_type: "qa-manual"` (or the other role) when the roles are linked into opencode's agents
directory — the prompt as in Claude Code: `Output language: <language>` first, then the session folder and the
brief. The role is not in the `subagent_type` list → the README's «subagents, but no named roles» fallback with
the general subagent.

## Continue a running executor

Not available: a `task` returns once. The README's fallback — a new executor of the same role with
«Continuation» appended to its brief.

## Ask the user

A `question` tool when one is listed; otherwise a plain-text question (the README's fallback).

## Plugin root

No variable: `<plugin root>` is the clone the install linked from — two directories above the `SKILL.md` you
were given (follow the link: `realpath`).

## Transcripts

Kept in opencode's own storage, in a format `transcripts.py` does not read: it exits 1 and the retro carries
«no transcript numbers in this harness».

## Hooks

None for this engine: the session is not renamed after the task.

## Updating the engine from a clone

The install links the clone itself, so an edit applies from the next session — no reinstall. Bump the patch
version anyway: the version is how the other harnesses' installs notice the change.
