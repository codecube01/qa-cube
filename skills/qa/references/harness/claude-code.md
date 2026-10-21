# Claude Code

The reference harness: the engine was written in it, and everything below is what it does natively.

## Detect

The tool list has `Agent` (with a `subagent_type` parameter) and `AskUserQuestion`. `0-session.md`:
`Harness: claude-code`.

## Launch a role

`Agent` with `subagent_type: "qa-analyst"` / `"qa-manual"` / `"qa-automator"` — the plugin registers the three
roles from `agents/`, so the instruction is loaded as the subagent's system prompt and the prompt carries only
`Output language: <language>` as its first line, then the session folder and the brief. The subagent runs in
the background and its completion arrives as a notification on its own — wait for it, do nothing on its behalf.

## Continue a running executor

`SendMessage` to the same agent (by the id the launch returned): the executor keeps its context, and the
answer reaches it as its next turn. This is how a «Pause protocol» answer is returned (`manual-brief.md`).

## Ask the user

`AskUserQuestion`: up to four questions per call, two to four options each, the recommended option first with
«(Recommended)» in its label; the user can always type «Other».

## Plugin root

`${CLAUDE_PLUGIN_ROOT}` — set in the shell of every command the session runs, e.g.
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/qa/scripts/session.py" …`. It points at the install cache
(`~/.claude/plugins/cache/qa-cube/qa-cube/<version>/`), never at a clone.

## Transcripts

`~/.claude/projects/<project slug>/*.jsonl`, the executors' under `*/subagents/` — the default `--root` of
`transcripts.py`, so it is called without one.

## Hooks

Yes: `hooks/hooks.json` renames a `/qa <task>` session after the task number (`UserPromptSubmit` and a
`PreToolUse` on `Skill`). Uses `jq`; without it the rename is skipped.

## Updating the engine from a clone

An installed copy lives in the cache, and a path inside `~/.claude/plugins/` is an installation, never a clone.
After an edit in the clone: bump the patch version in `<engine-clone>/.claude-plugin/plugin.json`, then
`claude plugin marketplace update qa-cube && claude plugin update qa-cube@qa-cube`; it applies from the next
`claude` launch. Which version is active: `~/.claude/plugins/installed_plugins.json`, `installPath` of
`qa-cube@qa-cube`.
