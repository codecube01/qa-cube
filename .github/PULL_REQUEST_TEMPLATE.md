## What this changes

<!-- One paragraph. If it comes from a session, name the session and the precedent. -->

## Where the lesson landed

<!-- Engine / project profile / knowledge base — and why here rather than there.
     Rule of thumb: it would work in any project → the engine; it names a specific
     tool, environment or class → a project profile. -->

## Checklist

- [ ] `python3 .github/scripts/validate-plugin.py` passes locally
- [ ] `version` in `.claude-plugin/plugin.json` is bumped
- [ ] Does this require anything of a project profile (a new header key, a new mandatory
      question, a rename)? If yes — `PROFILE-CONTRACT.md` gets a version bump and a history
      row; if no — the contract version stays put
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]`
