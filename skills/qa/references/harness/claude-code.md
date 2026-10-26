# Claude Code

The reference harness: the engine was written in it, and everything below is what it does natively.

## Detect

The tool list has `AskUserQuestion` and a subagent tool with a `subagent_type` parameter — `Agent`, or `Task` in older versions. `0-session.md`:
`Harness: claude-code`.

## Launch a role

`Agent` with `subagent_type: "qa-analyst"` / `"qa-manual"` / `"qa-automator"` (a general subagent: `"general-purpose"`) — the plugin registers the three
roles from `agents/`, so the instruction is loaded as the subagent's system prompt and the prompt carries only
`Output language: <language>` as its first line, then the session folder and the brief. The subagent runs in
the background and its completion arrives as a notification on its own — wait for it, do nothing on its behalf. In print mode
(`claude -p`) background subagents are stopped 10 minutes after the manager's last turn, mid-round: a headless session sets
`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`.

## Continue a running executor

`SendMessage` to the same agent (by the id the launch returned): the executor keeps its context, and the
answer reaches it as its next turn. This is how a «Pause protocol» answer is returned (`manual-brief.md`).

## Ask the user

`AskUserQuestion`: up to four questions per call, two to four options each, the recommended option first with
«(Recommended)» in its label; the user can always type «Other».

## Plugin root

Two directories above the «Base directory for this skill» Claude Code prints when it loads `/qa` (that line names
`<root>/skills/qa`): write that absolute path into each script command. `${CLAUDE_PLUGIN_ROOT}` may be used only after
`echo "${CLAUDE_PLUGIN_ROOT}"` has shown it set in this shell — an empty one turns the command into `python3 "/skills/…"`.
For an installed plugin the root is the install cache (`~/.claude/plugins/cache/qa-cube/qa-cube/<version>/`), never a clone.

## Transcripts

`~/.claude/projects/<project slug>/*.jsonl`, the executors' under `*/subagents/` — the default `--root` of
`transcripts.py`, so it is called without one.

## Hooks

Yes: `hooks/hooks.json` renames a `/qa <task>` session after the task number (`UserPromptSubmit` and a
`PreToolUse` on `Skill`). Uses `jq`; without it the rename is skipped.

## Connecting an MCP server

`claude mcp list` shows what is connected; `claude mcp add <name> …` connects a server (the user runs it — `! <command>`
in the prompt puts its output into the session). New servers' tools appear from the next `claude` launch.

## Updating the installed engine

`claude plugin marketplace update qa-cube && claude plugin update qa-cube@qa-cube`; it applies after `claude` restarts. The new copy
lands in the directory named in `~/.claude/plugins/installed_plugins.json` (`installPath` of `qa-cube@qa-cube`).

## Updating the engine from a clone

An installed copy lives in the cache, and a path inside `~/.claude/plugins/` is an installation, never a clone.
After the edit and its bump (`../../SKILL.md`, step 7):
`claude plugin marketplace update qa-cube && claude plugin update qa-cube@qa-cube`; it applies from the next
`claude` launch. Which version is active: `~/.claude/plugins/installed_plugins.json`, `installPath` of
`qa-cube@qa-cube`.
