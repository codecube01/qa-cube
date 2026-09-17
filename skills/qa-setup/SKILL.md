---
name: qa-setup
description: Use when qa-cube needs wiring into a project or its profile needs updating — «/qa-setup», «set up qa for this project», «qa onboarding», or when /qa could not find `.claude/qa-profile.md` or reported that the profile is behind the contract; also triggers on the Russian «настрой qa для проекта», «qa-онбординг».
---

# /qa-setup — wiring a project into qa-cube and updating its profile

The deliverable is `.claude/qa-profile.md` (+ subfiles where needed) per the `PROFILE-CONTRACT.md` contract in the root of the engine's repo
(next to this skill: `../../PROFILE-CONTRACT.md`). Read the contract before you start: the interview's questions are its table of sections
— but do step −1 first, and if it updated the engine, read the contract from the new installation instead of from here.

The profile already exists → that is not a blocker: this is update mode. First compare the profile's `contract-version` (no field → 1) with
the current version in the «Contract versions» section of `PROFILE-CONTRACT.md`: the profile is behind → walk the sections that were added
or changed after its version (per the version history) and bump `contract-version` to the current one. Then show the user the current
«Capabilities» header and ask what else to reconfigure; from there, the same steps for the affected sections only.

## Steps

**−1. Update the engine — the very first thing, before the language question.** `/qa-setup` is the only place the engine ever updates
itself: nothing updates a plugin on its own, and a session only ever mentions in one line that a newer version exists. So start here.

Compare the installed `version` (`../../.claude-plugin/plugin.json`, the plugin root above this skill) with one read of
`https://raw.githubusercontent.com/codecube01/qa-cube/main/.claude-plugin/plugin.json`. Equal, ahead, or the read failed for any reason (no
network, a 404 while the repository is private, a slow answer) → **say nothing and move on**: the update is a courtesy, and an onboarding
must not die because a fetch did. Behind → say which versions, then run:

```bash
claude plugin marketplace update qa-cube && claude plugin update qa-cube@qa-cube
```

**The update applies only after claude restarts, so the rest of this run is still executing the OLD instructions.** Two consequences, and
both are handled rather than hidden:

- **read `PROFILE-CONTRACT.md` from the NEW installation, not from your own root** — the fresh directory is named in
  `~/.claude/plugins/installed_plugins.json` (`installPath` for `qa-cube@qa-cube`). Migrating a profile against the contract shipped with the
  old copy would quietly write yesterday's `contract-version` into it;
- **tell the user in one line** that the engine is now at X, that the profile is being migrated against the new contract, and that if the
  onboarding procedure itself changed in that version they should restart claude and run `/qa-setup` once more. It costs a sentence, and the
  alternative is an onboarding that silently ran a stale procedure.

With a valid `engine-clone` (the user develops the engine itself) there is nothing to fetch — their clone is the source. Skip the update,
say so in a word, and carry on.

**0. The language — the first question, before anything else.** Ask it in English (AskUserQuestion): "Which language should the QA flow use
— questions, reports and test cases?" Options: English / Russian / Other (their own language, as text). Write the answer into the profile
under the key `language: <code>` — it governs the language of the conversation with the user and of every artifact of every session: the
plan, the executors' briefs, the results, the report, the retro, the TMS cases, the tracker comment. **Write the profile itself in that
language too** — it is a project artifact that the user edits by hand and the retro appends to. Its header keys stay as they are (`tracker`,
`tms`, `language`, …); the prose around them goes in the user's language.

**The engine's files are not translated under any answer** — they stay in English. There is one engine for every project on the machine,
while `language` differs per project: translating it would make the engine the property of a single project, would break on `claude plugin
update` and would demand a re-translation after every retro edit. The instructions are read by agents, and the language of the instructions
has no effect on the language of the output — that is set by `language` in the profile alone.

**1. Recon — study the project before asking anything: many answers are already in the folder.** Walk the repo and collect what exists:
- **instructions and skills**: CLAUDE.md (and AGENTS.md), `ls .claude/skills/` — skills about the tracker/TMS/logs/running tests often name
  the tools and environments outright; `.claude/settings*.json` — hooks and permissions are hints too;
- **autotests**: test directories per the stack's conventions (`src/test/`, `tests/`, `spec/`, `e2e/`), the runner's config
  (pom.xml/build.gradle, package.json, pytest.ini, …), the CI config (how the pipeline runs the tests), where run logs are written;
- **the knowledge base and the documentation**: all of `docs/` — README, `docs/knowledge/`, wiki-like folders; note the structure and the
  sections' READMEs;
- **traces of past test sessions**: folders like `test-sessions/`, reports, cases in md — if sessions have been run before, adopt their
  paths rather than inventing new ones; whether ready-made cases sit nearby (`test-cases/`, cases in a TMS created before the runs) is a
  hint about the value of `test-cases`;
- **mentions of a tracker and a TMS**: links in README/CLAUDE.md, configs (`.gitlab-ci.yml`, `qase.config.json`, `.jira`, tags/annotations
  in tests like `@QaseId`);
- **ready-made access channels to the tools**: connected MCP servers (`claude mcp list`), CLIs in PATH (`which jira glab …`), the project's
  skills — these come in handy at the «Access channels» step;
- **logs**: logging configs, mentions of Kibana/Grafana/ELK in the docs, where the services write when run locally.

For every capability in the contract, record a verdict: **answer found** (with the source file named), **hypothesis** (something similar
exists, one clarifying question needed) or **unknown**. Do not put what you found confidently into questions — write it straight into the
profile (the user will see it in full at the final review and will correct it if needed). Hypotheses become the first, «(Recommended)»
option in the questions; ask only about hypotheses and unknowns.

**2. The interview.** AskUserQuestion, grouped into 2–3 passes (≤4 questions each), and every question has a «no / we don't use one» option:
- pass A — the capabilities themselves: where do the tasks live (tracker)? where do the test cases live (tms) and **when do they appear**
  (test-cases: `upfront` — the analyst writes the cases from the requirements before the run; `inline` — the tester creates the case after
  the run, from the facts; `none` — we do not maintain cases)? are there environments (environments)? are there autotests, and what runs
  them (autotests)?
- pass B — the surroundings: is a browser needed for the checks, and which one (browser)? where do the services' logs live and how do you
  search them (logs: kibana / grafana / files / a skill / nowhere)? where do the testing secrets live — environment credentials, tokens,
  test users (secrets: env / a vault or password manager / a file outside git / nowhere / not needed)? is there a product knowledge base
  (knowledge)? where should sessions go (sessions — suggest `docs/test-sessions/`)?
- pass C — refinements on what was declared: the mapping of task statuses to modes (full cycle / automation-only); the write permission for
  the tracker; what counts as a request's trace id; the «what we do not automate» rules, if any. Put the recon's hypotheses first, marked
  «(Recommended)». Something stayed unclear — an honest `TODO` in the profile beats an invented answer.

**The final question — always, in free text:** «What else should the engine know about the project — quirks, rituals, constraints?» (a
«nothing» option is mandatory). Distribute the answer across the profile's existing sections rather than into a dump of its own; whatever
fits no section becomes an honest `TODO`.

**Secrets are a special case.** The answer «nowhere, in my head / in chats» → offer the default mechanism: a skeleton
`.claude/qa-profile/secrets.env` — variable names with a purpose comment, and `TODO` in place of the values. Check `git check-ignore` for
the file; not ignored — append a line to the project's `.gitignore`. The user fills the values in themselves: **never ask for secrets in the
chat and never write values into files on the user's behalf**. Into the profile (the Secrets section) go only the source and the names,
never the values; that rule holds whichever source is chosen.

**3. Access channels.** For every declared capability that requires a tool (tracker, tms, logs), there must be a channel the sessions will
reach it through. The order:

- **the channel already exists** (found by recon): a project skill → a connected MCP → a CLI in PATH. Use it: the profile's section gets a
  reference to the channel, and you ask nothing;
- **there is no channel → the choice is the user's** (AskUserQuestion, one question per tool), the options ordered by quality, the first
  available one marked «(Recommended)»:
  1. **MCP** — if the tool has an official/well-known server (Jira/Confluence — the Atlassian MCP, and so on): name the server and the
     connection command (`claude mcp add …`), wait for the user to connect it, and check that the tools are visible. There is no server —
     the option is not offered;
  2. **CLI** — if the tool has a live client: point at the installation (`brew install …`), and check `--help` once it is installed;
  3. **generate a REST skill**: gather the non-secret parameters through questions (base URL, project key, the account's email — these are
     not secrets, asking is fine), add the credential names (`JIRA_API_TOKEN`) to the secrets skeleton, then write a project skill
     `.claude/skills/<tool>-qa/SKILL.md` with ready-made commands: the reading ones (read a task with its comments, find a case, search by
     trace id) — mandatory; the writing ones (create a case, set the automation flag, post a comment) — per the declared write permission.
     Credentials in the commands come only through variables from the secrets source; no values live in the skill;
  4. **«no channel for now»** — `TODO: no access channel` in the section, and the onboarding moves on.

**4. A live check.** For every declared tool — one reading call: open any tracker task, find any case in the TMS, run the test runner's
`--help`/dry-run, open the knowledge base's README. For secrets the check is different — not reading the values but making sure the source
is out of git's reach: a file → `git check-ignore`; env/vault — fine by definition. It works → the section may hold specifics; it fails →
put the line `TODO: not verified — <error in one line>` into the profile and carry on, the onboarding is not blocked. The check runs through
the channel from step 3 — and thereby validates it too (a generated skill, an MCP, a CLI).

**5. Writing it down.**
- `.claude/qa-profile.md`: `contract-version` — the current version from «Contract versions» in `PROFILE-CONTRACT.md`; the «Capabilities»
  header (every header key of the contract) + sections only for the capabilities ≠ none, each answering the contract's questions and referring to the project's skills instead
  of retelling them. Anything bulky (the code map, browser techniques) goes into the subfiles `.claude/qa-profile/*.md`. With `test-cases` ≠
  none and `tms: none`, state the path for file cases in the TMS section (the default is `docs/test-cases/`);
- **`engine-clone` — the default is `none`, and asking otherwise takes an explicit yes.** Ask outright: «Do you develop the qa-cube engine
  itself? Yes → the path to your git clone. No (the usual case) → none, and the engine will simply update from upstream.» **Never derive the
  value from the plugin's own root**: `${CLAUDE_PLUGIN_ROOT}` points at the install cache, which the next update writes past, so a lesson
  written there disappears while reporting success. A clone is a clone only if the directory holds a `.git` and does not sit inside
  `~/.claude/plugins/` — check before writing the value down, whatever the user answered;
- in the project's CLAUDE.md — one line: «Test sessions — the qa-cube plugin (`/qa`); the project profile is `.claude/qa-profile.md`» (in
  the project's language);
- **check how thick CLAUDE.md is** (the contract's «A thin CLAUDE.md» rule): CLAUDE.md is loaded into every session and every subagent — QA
  specifics in it (tracker pitfalls with precedents, report formats, numbering/priority conventions) are paid for by everyone. Having found
  such sections — offer the user to move them into the subfiles `.claude/qa-profile/*.md` (`tracker.md`, `reporting.md`, say), leaving in
  CLAUDE.md the project map (what this is, the structure, the accounts, the status) and the links. Every subfile gets a TL;DR header (the
  quick flow on the first screen, the pitfalls below);
- show the user the finished profile in full and suggest running `/qa` on a trial task — the first session usually uncovers a couple of
  holes in the profile, and its retro will close them.

**6. The closing briefing — the last thing the first onboarding prints.** The person has just configured a tool they have never used and
has no idea what is now available to them; the profile listing answers «what did you write down», not «what can I do». So the onboarding
closes with a short memo **in the chat** (never a file — nobody opens a file they were not told about) and **in the project's `language`**
from step 0. Keep it to ~20 lines, grouped, and do not retell the engine: this is a card of entry points, not documentation. Precedent: an
onboarding that ended on the profile listing was followed by the question «and what do I type to start a session».

The skeleton below is what the memo must cover — render it in the project's language, dropping whatever this project does not have (the
roles are named per the profile: no `autotests` → no automator, `test-cases: none` → no analyst):

```
Ready. What you have now:

- `/qa <task link | description>` — starts a test session. The same command on the same task continues it: the next round lands in the
  same session folder, with a comparison against the previous one — that is how a retest is run.
- `/qa-day` — what was tested today; `--days 7` for the week, several project roots in one run. Already works, nothing to configure.
- `/qa-setup` — safe to run again at any time: it reconfigures what you name and migrates the profile when the engine's contract moves on.

What happens on its own:
- the roles: <the analyst writes the cases from the requirements before the run> · <the manual tester checks the feature on the
  environment> · <the automator turns the run's evidence into an autotest> — launched by the session itself, they ask you nothing;
- one folder per session in <sessions>: the passport `0-session.md` (tasks, mode, round log), the report `99-report.md` (one per session,
  every round updates it), plus a row in the session registry `<sessions>/README.md`;
- every session ends with a retro: its lessons are written straight into the engine, this profile and the knowledge base.

Editing by hand:
- `.claude/qa-profile.md` and `.claude/qa-profile/*.md` are ordinary markdown — correct them whenever something is off; the output
  language is the `language` key;
- engine improvements: with `engine-clone: none` (the usual case) a retro's engine-level lessons collect in <sessions>/engine-feedback.md
  — your own log, nothing leaves the project; `/qa-setup` updates the engine and tells you which of them have since arrived upstream. With
  a clone: edit it → bump the patch version in `plugin.json` → `claude plugin update qa-cube@qa-cube`.

And if the flow turns out useful — a star on https://github.com/codecube01/qa-cube would be a nice thing to get, entirely optional.
```

**The star line lives here and nowhere else** — a request repeated in every session's finale stops being an invitation. It is the memo's
last line and it is skipped when a session, a report or a retro is being written.

**In update mode the memo is not repeated** — the person already knows the flow. Then the closing is one short line: what changed in the
profile (the sections touched, and the `contract-version` jump if there was one).

**And the very last thing either mode prints is the action block** — `⚠️` for «I cannot finish the setup without you», `💡` for «worth doing,
safe to ignore» — each line an action, not a problem. Onboarding's own `⚠️` is almost always the same one: a secrets skeleton whose values
only the user can fill in, or a tool that failed its live check and left a `TODO` in the profile. Everything else is `💡`: run `/qa` on a
trial task, move the QA specifics out of a thick CLAUDE.md, connect the MCP that was declined. The same discipline as in a session — zero or
one `⚠️` is normal, and a red line that turns out to be optional costs the trust of every red line after it.

**7. Reconcile the engine feedback — only when the engine was actually updated at step −1.** No update, or no
`<sessions>/engine-feedback.md`, → the step does not exist and nothing is said about it.

Otherwise: take the file's open rows whose recorded plugin version is **older** than the version just installed, and check each against the
**newly installed** engine's files — the step and file each row names, read under the `installPath` from step −1 and not under your own root,
which is still the pre-update copy. A rule that has since arrived moves
to the file's «Closed» block with the version it arrived in; it is not deleted, because the user's own observation landing in the engine is
the whole payoff of keeping the log. Then one line in the chat: how many moved and what they were about.

Rows that did not arrive stay open. **When three or more of them are open, offer — once — to hand them upstream:** render the open rows as
plain text the user can paste, **anonymised the way engine edits are** (the mechanics of the lesson stay, the tracker ids, hostnames,
service and company names go), and give them the link `https://github.com/codecube01/qa-cube/issues/new/choose`. Nothing is posted, opened
or sent by the engine: the text and the link are handed over, the decision is the user's.

**The offer is made once per set, and the file remembers that.** Write `offered: <date>, <version>, <N rows>` into the file's header on the
offer, and `declined: <date>` if the answer was no; the next offer waits until three *new* rows have accumulated beyond that mark. A request
repeated at every run stops being an invitation and becomes noise — the same reason the star line lives in the first-onboarding memo and
nowhere else.
