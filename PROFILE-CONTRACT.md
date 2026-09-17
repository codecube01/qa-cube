# The project profile contract

The profile is the file `.claude/qa-profile.md` in the root of the consuming project. It is
committed to the project's repository: a colleague gets a working `/qa` along with the clone.
Bulky sections may be moved out into the subfiles `.claude/qa-profile/*.md` (with the profile
referring to them explicitly); the profile's scripts live in `.claude/qa-profile/scripts/`.

The profile is created and updated by the `/qa-setup` skill; editing it by hand is fine too —
it is ordinary markdown. Its readers are Claude sessions (the `/qa` manager and the
qa-analyst/qa-manual/qa-automator subagents), so the format is free: what matters is answering
the questions in the tables below. The absence of a rigid schema and a validator is deliberate.

**The profile's language is the project's language** (`language` from the header): its prose is
written for the person who edits it. The header keys and their values stay as they are
(`tracker`, `tms`, `test-cases`, …), and so do the file names the engine refers to. Section
titles may be written in the project's language — the engine names them in English (Tracker, TMS,
Environments, Logs, Autotests, Browser, Secrets, Knowledge), and a reader matches them to the
profile's own headings by meaning.

Three token-economy rules (the readers are agents, and every unnecessary read costs money):

- **Subfiles are read targeted, by every role.** The only thing read up front at the start is
  `qa-profile.md` itself — and that is exactly why it must be a short map (the capability
  header + pointer sections). Subfiles are pulled in at the moment of need: the manager — at
  the pipeline step that needs the section; the executors — per the «What to read» list in
  their brief. A subfile the session does not need is not read at all.
- **A subfile's TL;DR header.** Every subfile `.claude/qa-profile/*.md` starts
  with a short working flow (≤10–15 lines: what to do in the typical case); the pitfalls,
  the precedents and the rare cases come below. The reader reads the header by default and
  goes deeper when stuck.
- **A thin CLAUDE.md.** The project's CLAUDE.md is loaded into every session and every
  subagent automatically — keep only the project map in it (what this is, where things
  are, accounts/environments, status). QA specifics — tracker pitfalls, report
  formats, numbering conventions — move into the profile/subfiles, which are read
  targeted and only by those who need them. `/qa-setup` checks this during onboarding
  and migration.

## The «Capabilities» header

The profile's first section is a declaration:

```markdown
## Capabilities
contract-version: 5    # the contract version the profile matches; set by /qa-setup
tracker: gitlab        # jira | <other> | none — none: the input is free-form text only
tms: qase              # <other> | none — none: cases = md files next to the sessions
test-cases: upfront    # inline | none — upfront: qa-analyst writes the cases before the run; inline: qa-manual writes them from the facts; none: we do not maintain cases
environments: stages   # local | none
logs: kibana           # grafana | <path|skill> | none — none: diagnostics from response bodies only
autotests: junit       # <any runner> | none — none: the automation step is skipped
browser: dedicated     # default | none
secrets: .claude/qa-profile/secrets.env  # env | vault | <path> | none — none: the sessions need no secrets
knowledge: docs/knowledge/     # path | none
sessions: docs/test-sessions/  # path — mandatory, always present
engine-clone: none     # a git clone of the engine (the address for retro edits), or none — the usual case
language: ru           # the sessions' language: the conversation and every artifact (no field → the engine's language, English)
```

The values to the left of `#` are an illustration; the engine cares about two things: `none`
versus non-`none`, and where to look for the details. The degradations for `none` are described
in the engine (`skills/qa/SKILL.md`, the «Capability degradations» table) — **the profile
neither overrides nor invents them**. **A key missing from the profile reads as
`none`** — profiles on older contract versions keep working with a safe
degradation.

`test-cases` is **independent of `tms`**: it answers not «is there a TMS» but «when does a
case appear». With `tms: none` + `test-cases: upfront` the analyst writes the cases as
files in `docs/test-cases/` (the profile may override the path). There is deliberately no key
about the quality of the requirements: it changes from task to task, and the verdict on each
task is passed by the manager at step 1 of the session. The single exception to the rule
«a missing key = `none`» is `test-cases` itself: its absence reads as `inline`, not as
`none`. Profiles written before version 5 keep maintaining cases exactly as before —
otherwise a contract update would silently switch cases off in every existing project.

## The sections

One section per capability ≠ none, answering the engine's questions.
The principle: **the profile is a map, not a dump**. If the project has a skill about a
tool (the tracker, the TMS, the logs, running tests) — the section refers to that skill
instead of retelling it; only what the skills do not have stays in the profile.

| Section | Must answer |
|---|---|
| **Tracker** | how to read a task (tool/skill); the mapping of task statuses → session modes (full cycle / automation-only); how to find related tasks; whether there is write permission (comments/statuses) — there is not → the manager hands the comment to the user as text |
| **TMS** | how to search for a case (do not breed duplicates); how to create one (placement, mandatory fields); how to set the automation flag; what the case ↔ test link looks like in the code; the format of a case id; where the cases live if there is no TMS (`tms: none` with `test-cases` ≠ none) — the default is `docs/test-cases/` |
| **Environments** | access and restrictions (protocols, proxies); the credentials of test entities — as a reference to the Secrets section; what counts as a request's **trace id** (how to search by it — the Logs section); the sanity check before the scenarios (what other people's runs overwrite); the techniques for reconnoitring «is the feature deployed» |
| **Logs** | where the services' logs live and the access channel (tool/skill); how to search by trace id; which service writes where; the retention depth. Autotest run logs do not belong here — they are in the Autotests section |
| **Autotests** | how to run a single test (tool/skill); where to put new ones (the code map) and the code style — usually a subfile; where the run logs are; known false failures of the environment; the local «what we do not automate» rules |
| **Browser** | which browser instance/profile and how to bring it up (the preflight checklist for the manager); how to authenticate (the safety rules: what must never be typed into forms); the accumulated UI-checking techniques — usually a subfile |
| **Secrets** | where the values live (the source: env, a vault, a file outside git); which variable/record names are there and what each is for; how to read from the source. The hard rule: **the profile holds only the source and the names, never the values** |
| **Knowledge** | what to read before a session (the structure, the README); where to write the retro's product findings. The recommended organization: **one domain = one file** (the business logic + that domain's API contract + its known defects) — then the rule «read the profile doc for the feature» hands the agent the API contract too, without reading a general reference; cross-domain API conventions go into a separate small file |

`sessions` and `engine-clone` are just paths and require no sections. `engine-clone` is `none` for
everyone who does not develop the engine itself — that is the normal case, and the retro then keeps
its engine-level lessons in `<sessions>/engine-feedback.md` instead of applying them.

## Example: a profile skeleton (the fictional project acme-shop)

```markdown
# QA profile of the acme-shop project

## Capabilities
contract-version: 5
tracker: jira
tms: testrail
test-cases: upfront
environments: stages
logs: kibana
autotests: playwright
browser: default
secrets: .claude/qa-profile/secrets.env
knowledge: docs/knowledge/
sessions: docs/test-sessions/
engine-clone: none
language: en

## Tracker       — the jira-task skill; status Ready for QA → full cycle, To Automate → automation-only; a read-only token
## TMS           — the testrail skill; case ↔ the @C<id> tag in the test
## Environments  — staging behind a VPN; trace id = x-request-id (searching → the Logs section); credentials → the Secrets section
## Logs          — Kibana, access → the search-logs skill (generated by /qa-setup); the per-service indices and the retention depth are in the skill
## Browser       — the default Chrome; UI-checking techniques → .claude/qa-profile/browser.md
## Secrets       — .claude/qa-profile/secrets.env (in .gitignore); the variable names and their purpose are comments in the file itself
## Autotests     — the run-single-test skill; the spec map and the code style → .claude/qa-profile/autotests.md
## Knowledge     — docs/knowledge/: product/ (a mirror of the documentation) + QA findings in the root
```

## Contract versions

The current version is **5**. A profile with no `contract-version` field counts as version 1.
Every change to the contract (a new key, a new mandatory question in a section, a
rename) bumps the version and gets a row in the history — `/qa-setup` reads it to know
which sections to walk during a migration, and `/qa` to know what to warn about.

| Version | What changed (the sections affected) |
|---|---|
| 1 | the base set: tracker, tms, environments, autotests, browser, knowledge, sessions, engine-clone, language |
| 2 | the **Secrets** key and section (`secrets`) were added; `contract-version` was added |
| 3 | the **Logs** key and section (`logs`) were added, and searching by trace id moved from Environments to Logs; /qa-setup gained the «Access channels» step (MCP → CLI → generating a REST skill, the user chooses) and the interview's final open question |
| 4 | token economy (the migration = moving content around, every section): (a) **a thin CLAUDE.md** — move the QA specifics (tracker pitfalls, report formats, numbering conventions) out of the project's CLAUDE.md into the subfiles `.claude/qa-profile/*.md`, leaving the project map in CLAUDE.md; (b) **TL;DR headers** — give every profile subfile a first screen with the short working flow, the pitfalls below; (c) **knowledge by domain** — split the API contracts out of the general reference into per-domain knowledge-base files (one domain = business + API + defects), with cross-domain conventions in a separate small file; (d) in /qa the manager now lists in the task files exactly what the executor should read (an engine edit, the profile is untouched) |
| 5 | the **`test-cases`** key was added (`upfront｜inline｜none`, absence = `inline` — behavior unchanged) along with the `qa-analyst` role: with `upfront` the cases are written from the requirements before the run and `qa-manual` does not create them. Sections affected: **TMS** (where file cases live with `tms: none` — the default `docs/test-cases/`). Profiles with the old behavior need no migration: the key may be left out |
