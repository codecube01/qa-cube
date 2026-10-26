# Harness adapters

The engine runs in any agent harness that gives the agent files and a shell. Its body names an action by
its role — «launch the role `qa-manual`», «ask the user», `<plugin root>` — and the adapter of the harness
the session runs in says how that action is done there. Read this file and then your harness's adapter at
step 0 of `/qa` and at the start of `/qa-setup`, before the first action an adapter answers.

The harness is never asked about and never written into the profile: the profile is the team's file in
git, and colleagues run different harnesses on the same project. Only `0-session.md` records it, as the
line `Harness: <name>`, so the retro and `qa-day` know what a round ran in.

## Telling the harness

Match your own tool list, first hit wins:

| You have | Harness | Adapter |
|---|---|---|
| `Agent` or `Task` with a `subagent_type` parameter, `AskUserQuestion` | Claude Code | `claude-code.md` |
| `spawn_agent`, `wait_agent` — or, with multi-agent off, `apply_patch` and `update_plan` | Codex | `codex.md` |
| `task` with a `subagent_type` parameter, `skill`, and no `AskUserQuestion` | opencode | `opencode.md` |
| anything else with files and a shell | another harness | `generic.md` |

The tool list is the evidence, not the harness's name in a system prompt or the user's word: a harness
that wraps another one exposes the inner one's tools, and those are what the engine will call.

## When the harness lacks a capability

Every adapter answers every question below, even if only with «not available here». Where it is not, the
fallback is the same in every harness:

- **no subagents** → the manager runs the roles itself, one after another: it reads `agents/qa-<role>.md`
  as the brief's preface, does that role's work under that role's rules (the manual tester still asks
  nothing, the analyst still never touches the environment), writes the role's result file, and only then
  resumes as the manager. The report and the retro say «no context isolation: the roles ran in the
  manager's own context» — the acceptance step then reads the result file as critically as an executor's,
  because the same context wrote both. The session is not blocked;
- **subagents, but no named roles** → a general subagent whose prompt opens with «Your instruction is
  `<plugin root>/agents/qa-<role>.md` — read it whole before anything else», then the usual prompt
  (`Output language: …`, the session folder, the brief);
- **no way to continue a running executor** → a new executor of the same role, with the previous one's
  result file and the answer appended to its brief as «Continuation»;
- **no question tool with options** → a plain-text question with numbered options, the recommended one
  first and marked;
- **no plugin-root variable** → `<plugin root>` is two directories above the `SKILL.md` you are reading
  (`skills/qa/SKILL.md` → the root); you know that path, the harness gave it to you;
- **no hooks** → the session is not renamed after the task; nothing else depends on hooks;
- **transcripts elsewhere or in another format** → `transcripts.py --root <dir>`; exit code 1 (none found,
  or a format it cannot read) → the retro carries the line «no transcript numbers in this harness» and goes
  on without them;
- **no command to update an installed engine from a clone** → the retro's engine edit is committed in the
  clone and the user is told to reinstall the plugin the way they installed it (`README.md`, «Install»).
