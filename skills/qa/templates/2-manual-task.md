# Task brief: manual round

## Context

<one paragraph: what the feature is, link to the task, what was fixed>

## Environment

- Output language: <language from the profile — everything you write and narrate goes in it>
- Env: <env>
- Requirements: spec-grade | draft — <one-phrase rationale>
- Cases (with `test-cases: upfront`): <case ids from the analyst; those are what we run>
- Documentation: <paths in the project knowledge base relevant to the task>
- QA findings: <paths to findings from past sessions, if the section has any>

## What to read (targeted, not everything)

- <profile subfiles this task needs: e.g. `.claude/qa-profile/auth-and-api.md` §1, §3>
- <KB files/sections for the task's domain>
- The remaining profile subfiles — only when stuck.

## Scenarios

<the table from 1-plan.md with expected business effects>

## Deliverable

- Write to: `3-manual-result.md` (incrementally, after each scenario)
- Mandatory: a trace id for every failure (if the project defines one — with `logs: none` there is none), severity for bugs, exact request/response evidence (the autotest is written from it), case `<TMS case>` in the «Summary» (with `test-cases: none` there are no cases — write «cases are not maintained in this project» instead of an id), the «Product findings» and «Executor retro» sections
- With `test-cases: upfront` do not create cases. Do not edit the expected result of a case whose expectation source is `spec` — a mismatch is recorded as a defect; a case sourced from an `assumption` or the `KB` is refined against the facts. Steps and preconditions are always refined.
- As separate lists in the result: **case corrections** (`case → was → now → why`) and **case candidates** (a scenario surfaced with no case behind it — do not create it yourself).
