# Codex

Codex loads the plugin through `.codex-plugin/plugin.json` (skills only — it does not register the plugin's
`agents/` as roles), and its multi-agent tools need `[features] multi_agent = true` in `~/.codex/config.toml`.
Trust your actual tool list over this file where they disagree.

## Detect

The tool list has `spawn_agent` and `wait_agent` (multi-agent on), or neither (off — see «Launch a role»).
`0-session.md`: `Harness: codex`.

## Launch a role

`spawn_agent` with `fork_turns: "none"` — a clean context, never your transcript — and no `agent_type`: the
roles are not registered, so the prompt opens with «Your instruction is `<plugin root>/agents/qa-<role>.md` —
read it whole before anything else», then `Output language: <language>`, the session folder and the brief.
Wait with `wait_agent` in bounded stretches of 5–10 minutes; a finished child's answer also arrives with your
next turn. No multi-agent tools → the README's «no subagents» fallback.

## Continue a running executor

`followup_task` to the same child: it delivers the message and triggers a turn, reloading a child the harness
evicted. Never spawn a fresh executor on the theory that a spawned one cannot be messaged again.

## Ask the user

`request_user_input` when it is listed for this turn; otherwise a plain-text question (the README's fallback).
An empty answer from it is not permission — ask again in plain text when the step cannot go on without it.

## Plugin root

No variable in the shell: `<plugin root>` is two directories above the `SKILL.md` you were given. Hook
commands get `${PLUGIN_ROOT}`, but the engine ships no Codex hooks.

## Transcripts

`~/.codex/sessions/<yyyy>/<mm>/<dd>/rollout-*.jsonl` — a format `transcripts.py` does not read: it exits 1 and
the retro carries «no transcript numbers in this harness».

## Hooks

None: `.codex-plugin/plugin.json` declares no hooks, so the session is not renamed after the task.

## Updating the engine from a clone

`codex plugin marketplace add <path to the clone>` once, then `codex plugin add qa-cube@<that marketplace>`
after each edit; it applies from the next session. Without that wiring — the README's fallback: commit in the
clone and tell the user to reinstall.
