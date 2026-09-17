# Task brief: automation

## Context

<one paragraph: what the feature is, link to the task; in automation-only mode — note that there is no evidence from a manual round>

## Evidence

- Manual run: `3-manual-result.md`, scenarios <numbers>   (or: «none — do a minimal run yourself»)
- Output language: <language from the profile — everything you write and narrate goes in it; test code follows the project's code style>
- Env: <env>

## What to read (targeted, not everything)

- <profile subfiles this task needs: usually the Autotests section + the code map>
- The remaining profile subfiles — only when stuck.

## What to automate

| Scenario | Candidate (class/file) | TMS case |
|---|---|---|
| <from the plan, usually the 1–2 main ones> | <per the code map in the profile> | <id> — with `test-cases: upfront` from the analyst, with `inline` from the manual tester; with `none` there are no cases and the link goes to the tracker task |

## Deliverable

- Write to: `5-automator-result.md` (every fix iteration — immediately)
- Mandatory: <test: class/file#method>, case `<TMS case>` (with `test-cases: none` there is no case — what gets checked is the link to the tracker task per the profile's convention), the test-to-case link in the code, <run log>, the «Executor retro» section
