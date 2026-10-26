# Installing qa-cube in any agent harness

You are an AI agent and your user asked you to install qa-cube. Follow these steps in order; ask the user only
where a step says so. Claude Code, Codex and opencode have their own shorter routes in `README.md`, «Install» —
use them when you are one of those.

qa-cube is a corpus of instructions: three skills (`skills/qa`, `skills/qa-setup`, `skills/qa-day`), three role
instructions (`agents/qa-*.md`) and small Python scripts (stdlib only). It needs files, a shell and `python3`.

1. **Clone it to a stable place** — the skills refer to their own directory, so it must not move:
   `git clone https://github.com/codecube01/qa-cube ~/.qa-cube`.
2. **Make the skills reachable the way your harness loads skills.** Find out from your own tools and docs:
   - your harness loads `SKILL.md` skills from a directory → link each of the three skill directories there
     (`ln -sfn ~/.qa-cube/skills/<name> <skills dir>/<name>`);
   - it loads named subagents from a directory → link `agents/qa-analyst.md`, `qa-manual.md`, `qa-automator.md`
     there too; without that the engine passes the role's instruction in the prompt of a general subagent;
   - it has no skills at all → add to the user's global agent instructions (`AGENTS.md` or its equivalent) one
     line: «For a QA test session (/qa, «test this task»), read and follow `~/.qa-cube/skills/qa/SKILL.md`; for
     onboarding (/qa-setup) — `~/.qa-cube/skills/qa-setup/SKILL.md`; for a day digest (/qa-day) —
     `~/.qa-cube/skills/qa-day/SKILL.md`». Ask the user before editing that file.
3. **The browser.** UI checks use Playwriter by default: `npm i -g playwriter`, the Playwriter extension from the
   Chrome Web Store (the user installs it and clicks its icon once), and optionally
   `npx -y skills add https://playwriter.dev -g -y`. A project that checks no UI can skip this.
4. **Check:** `python3 ~/.qa-cube/.github/scripts/validate-plugin.py` prints `✔`.
5. **Tell the user** what you linked or wrote and where, and that the next step is `qa-setup` in their project.

**Update:** `git -C ~/.qa-cube pull`. The harness-specific notes the engine reads at run time are in
`skills/qa/references/harness/` — this harness falls under `generic.md` unless one of the others matches.
