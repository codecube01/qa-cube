# Installing qa-cube for opencode

opencode reads skills from `~/.config/opencode/skills/` and agents from `~/.config/opencode/agents/`. The install
clones the engine once and links its skills and its three roles there, so `git pull` in the clone is the update.
Any model opencode runs — a hosted one or a local one — works the same way.

```bash
git clone https://github.com/codecube01/qa-cube ~/.config/opencode/qa-cube
mkdir -p ~/.config/opencode/skills ~/.config/opencode/agents
for s in qa qa-setup qa-day; do
  ln -sfn ~/.config/opencode/qa-cube/skills/$s ~/.config/opencode/skills/$s
done
for a in qa-analyst qa-manual qa-automator; do
  ln -sfn ~/.config/opencode/qa-cube/agents/$a.md ~/.config/opencode/agents/$a.md
done
```

Restart opencode, then in your project ask it to load the `qa-setup` skill. The browser checks use
[Playwriter](https://playwriter.dev) by default — see `README.md`, «Browser».

**Update:** `git -C ~/.config/opencode/qa-cube pull`, then restart opencode.

The engine's harness-specific notes for opencode are in `skills/qa/references/harness/opencode.md`.
