# Changelog

All notable changes to qa-cube are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the versions are the ones in
`.claude-plugin/plugin.json` — that field, not a git tag, is what `claude plugin update`
reads. A release tag `vX.Y.Z` must always match it.

Patch versions are bumped by the retro step of a session whenever the engine is edited, so
not every version becomes a release: a release is cut when there is something worth reading
about.

## [0.16.0] — 2026-09-17

First public release. Nothing is asked of the projects already running the engine: the
profile contract is untouched, so `.claude/qa-profile.md` stays as it is. This version also
folds in the patches 0.15.3–0.15.7, which were cut by retros without a section of their own.

### Added

- **The fixer's correction to the description of YOUR previous finding is quoted as theirs,
  never adopted as the round's expected state** (`manual-brief.md`). A team that accepts a
  finding often amends how it was described, and the amendment arrives with the authority of
  whoever owns the code — so it slides into the brief and the executor ends up measuring
  against the author's model instead of against the requirement. Quote it verbatim, attribute
  it, name the observation that settles it. Precedent: a fix comment said a signing pause
  «never engaged once»; the retest found it engaging and clearing normally, and the whole
  block had been framed around the author's version.
- **A lever that works can still be unable to produce the state a scenario needs — check
  what it CONSERVES, not only that it moves** (`planning.md`). A transfer conserves the
  total, a reassignment conserves the count, a rename conserves everything but the label, so
  «empty both wallets by converting between them» is not hard but arithmetically impossible.
  Where the lever only redistributes, the state is usually reachable from the other side.
- **A lever handed over BY THE USER is verified at preflight like any other, and a
  credential is only half of one** (`planning.md`). The value's authority exempts it from the
  control experiment it most needs; and it is exercised through a contract of use — which
  header carries it, which bytes it signs, whether a timestamp participates — which has to be
  asked for in the same breath as the value.
- **Provenance of the fixture is established before an autotest is promised, and a fresh
  deploy dates more than the code** (`planning.md`). A manual round needs the lever to exist
  today; a test needs it to exist after every deploy. An object somebody configured by hand
  is a finding about the delivery, not a note about the round — and the deploy that makes the
  build verifiable is commonly the one that wiped the data the brief's fixtures name.
- **Two numbers from different sections of the brief are multiplied while slicing**
  (`planning.md`). A setting flipped inside a window of the process is unrunnable when its
  propagation lag exceeds the gap between the phases; a scenario whose running time
  approaches the lifetime of its access renews that access inside the scenario rather than
  around it. Both figures are normally already written down, in sections that never meet.
- **A checklist item carries the framing its finding will inherit** (`planning.md`). A
  regression checklist grows from requirements and from observations of how the product behaved
  last time; written down they read identically, and a finding then goes out as «violates clause
  N» when clause N never said that. Mark the source of every expectation, treat a mismatch on an
  observation-derived item as a question for the analyst rather than a defect, and re-read the
  cited clause verbatim before assigning a priority. Precedent: an item lifted «and the status»
  from a knowledge-base line and cited an access matrix that was silent on the screen's contents;
  the Major regression had to be requalified to Minor along with every derived artifact.
- **A guard you could not satisfy is not a defect until the LEGITIMATE caller fails it too,
  and retest verdicts are transcribed from the executor's own table** (`report.md`,
  `SKILL.md`). A trail of refused attempts establishes that this caller was refused, which is
  what a working guard does; one execution of the real thing dissolves the candidate into a
  blocker of the round. And on a retest the previous report is the richer document, which is
  exactly why a shifted row gets carried across in its old framing — copy the verdicts
  mechanically, then reconcile the totals against the executor's count.

## [0.15.2] — 2026-09-15

### Added

- **A hypothesis read out of minified code is handed over as the excerpt, not as its meaning** (`manual-brief.md`, «What goes into the
  brief»). Recon on a bundle yields quotable strings plus control flow that has to be reconstructed by eye from renamed identifiers — and
  the brief flattens the two, so the manager writes down what they concluded the code does. That conclusion carries an unverified model and
  is worse than no hypothesis, because the executor spends probes on the invented branch. Precedent: a brief described a label as produced
  through a lookup with a fallback, so a collapse of several statuses into one caption would only appear on a missing key; the code held a
  plain conditional, the collapse was the main branch, and probes went into disproving the fallback theory first.
- **«First the batch capture» describes the wrong volume when only PART of the round depends on the fragile access** (`manual-brief.md`,
  «Preflight and access»). Where one contour hangs on a short session and another has its own credentials, the honest partition is «what
  dies with the access» against «what can be done at any time», and it cuts across the capture/interact line: the session-bound contour's
  interactive scenarios outrank the independent contour's snapshots. Precedent: an executor deliberately departed from the briefed order
  for exactly this reason and recorded why.
- **When the manager's own tooling refuses the re-verification of a cancellation, the boundary is published rather than papered over**
  (`manual-brief.md`, «Accepting the result»). The claim «the destructive operation now refuses» can only be re-run destructively, which a
  safety guard may block. Take every independent read that constrains the claim, keep the executor's evidence attributed to them, and write
  the split in the report in one sentence. Precedent: a re-run of a delete mutation was blocked by an irreversible-deletion guard;
  acceptance closed the gap with reads in two contours plus an explicit line about whose evidence the refusal texts were.
- **«The channel does not exist» is asked of every contour — visibility is scoped per identity, not per environment** (`report.md`, «What
  "not covered" is allowed to claim»). An empty listing under the credentials the round happens to hold is a fact about the identity that
  asked; the give-away is that the round holds two ways in and consulted one. Where contours disagree, the disagreement is itself the
  finding. Precedent: «no delivery channel is configured» came from an empty listing under an integrator's key, while the operator's
  contour showed two active subscriptions of the same tenant, one of which had accepted four deliveries from the round's own actions.

## [0.15.1] — 2026-09-15

### Added

- **A round on a task with NO requirements at all** (`planning.md`, «What the plan rests on»). The degenerate case of a `draft` verdict —
  an empty description, no acceptance criteria, no comments, nothing but a title — is a different kind of round, not a weaker one: there is
  no expected result, so every observation fits both «works» and «broken», and an executor left to their own judgment invents the missing
  expectation and files it. The entry fixes the two moves that keep such a round honest — say in the brief that no verdict on the subject
  will be passed, and enumerate in advance the defect classes that survive any answer (internal inconsistency, a divergence between what the
  system records and what it does, outright failure) — plus the two riders: measure the cost of each answer in the same round, and hand the
  case over as a candidate with its expected result open instead of canonising behaviour that may be the defect.
- **An oracle read off a FIELD NAME is a third kind of recon constant** (`manual-brief.md`, folded into «recon constants are two kinds»).
  A pair of fields whose names promise exactly the distinction the round needs comes from the same schema as the real contract values and
  inherits their authority, while being a guess about semantics — and live data will not refute it in advance, because on the records
  available at planning time the two fields are equal. Such an oracle is handed over as a hypothesis with its own failure sentence, and never
  as the primary one.

## [0.15.0] — 2026-09-15

### Changed

- **The lesson catalogues are organised into families.** `planning.md`, `manual-brief.md` and `report.md` had grown to ~35 000 words read
  in full every session, and the cost was not the number of rules but the repetition: twelve entries across three files each explained, from
  scratch, that «not covered» is a claim verified by trying; six explained the order of the server-side checks; six more, the fingerprint of a
  build. Those are now **families** — a head entry stating the mechanism once, with its shapes under it, each carrying only what is particular
  to it plus its own precedent. Thirteen families in all (the reference environment, the order of the server-side checks, searching the tracker
  at step 1, dating the build, the main run and its control, «not covered», the gate before an irreversible step, what you have not checked
  yourself, a sanctioned mutating probe, the observation channel, the executor stopped, the first bold sentence, the table copied out whole).
  No rule and no precedent was dropped — the entries the families replaced were verified one by one. The contents blocks now list single
  entries first and families after, so a family is found and read whole.
- **The retro's addressing rule gained the finer half** (`SKILL.md`, step 7): a new lesson either stands alone or joins a family, and where a
  family already states the mechanism the entry says only what is particular to it. Three entries in one catalogue sharing a mechanism are a
  family, not three entries — which is how the catalogues doubled once already.
- **The finale repeats the whole result delivery under a «Test results» heading** (`SKILL.md`, step 8). The results are delivered at step
  6.5, before the retro, and the retro that follows is minutes of edits across the engine, the profile and the knowledge base — so whoever
  comes back once the session has finished lands on a screen of housekeeping and has to scroll up for the verdict. The finale's order is now
  fixed: Test results (the status list with its icons, the verdict per task, the findings with priorities, the answer to the session's
  question, what stayed uncovered, the tracker comment, plus what was automated and the path to the session folder), then the retro edits,
  then the action block. It is a verbatim repeat, not a digest — a digest is exactly what sends the reader back up the scroll. The detail
  still lives in `99-report.md`, and the icons still stay out of every file.

## [0.14.1] — 2026-09-15

### Added

- **The round's status list opens the chat delivery.** The manual tester already returns a verdict per requirement out of four values, and
  until now the user met them as prose. They are now rendered as one line per requirement — 🟢 pass · 🟡 partial · 🔴 fail · ⚪ not covered
  with its reason in the same line — so the round is legible before the findings are read. Greens are listed one by one up to five and
  collapse into a single count past that: a screen of green buries the two rows that needed reading. In round 2+ a changed verdict carries
  its transition («🟢 FR-5 — was 🔴, fixed»), which is exactly what a retest is read for. **The icons never enter a file**: the report is
  copied into the tracker whole, where an emoji fares as the HTML in a cell does, and every line must read correctly without its icon — a
  terminal may not render it and a reader may not separate red from green.
- **Every entry point closes with an action block: `⚠️` and `💡`.** `⚠️` means «I cannot close this without you», `💡` means «worth doing,
  safe to ignore», and each line states an action rather than a problem — «Paste the comment into <task>: the tracker token is read-only»,
  never «no write permission». The engine already produced plenty of such requests and scattered them through prose; they are now one block,
  in one place. **`⚠️` is rare by rule** — zero or one line is a normal round — and the instruction names the only three things allowed to be
  red: a deliverable only the user can land, a verdict blocked on someone else's decision, and access that must be fixed before the round
  closes. Everything else is `💡`. If everything is urgent then nothing is, and a red line that proves optional costs the trust of every red
  line after it. The block appears at the end of a `/qa` session (and in a message where it stops and cannot continue at all — the same
  statement), at the end of `/qa-setup`, and after a `/qa-day` digest, where an empty block is simply not printed. Subagents print none:
  they never address the user, which keeps `⚠️` rare by construction rather than by discipline.


### Changed

- **Step 9 became a fifth reference catalogue, and three findings paragraphs moved into `report.md`: `SKILL.md` is back to 54.4k of its 64k
  budget** (from 58.8k). `references/after-delivery.md` is read **by trigger** — the moment the user says something once the report is
  delivered — which most sessions never do, so most sessions stop paying for it; the step keeps only what decides the first two moves (a
  question is answered, an objection is re-checked by your own eyes before anything is edited) and points at the file for the rest. The
  three paragraphs about shaping a finding for the tracker — the title line, the table surviving a copy-paste, what goes to the
  side-findings registry instead of the report — moved into `references/report.md`, which step 6 already reads whole, so the move buys
  headroom and legibility rather than tokens; saying which is which matters, because the budget exists to stop the manager paying for
  lessons that do not apply to the round in front of it.

## [0.13.0] — 2026-09-14

### Added

- **`skills/qa/scripts/check_session.py`: the checks the engine used to ask an agent to perform by eye.** Three rules stated in prose and
  enforced by nothing — no secret value in a session file, every table row carrying the same number of `|` as the separator, no finding's
  cell over ~850 characters — are now a script the pipeline runs: at step 4 and step 5 over an executor's result before the manager reads
  it, and at step 6 over the finished report before it is delivered. Step 6 had literally asked for «the two-line check over the finished
  table»; a stray bar shifts the columns invisibly in a rendered preview, and an oversized cell comes back from the customer. The secrets
  half matters most: the rule is repeated in four instructions because an instruction was the only thing enforcing it, while session
  folders are committed into the customer's repository and backed up off-site. It catches assigned credentials, bearer values, JWTs,
  private-key blocks, cloud and forge tokens, and one-time links (a magic link is a credential too, even one the executor requested
  themselves), while the masked forms the engine mandates — `<TOKEN>`, `***`, `$VAR` — stay quiet.
- **28 tests for it, paired by design.** A checker over somebody else's writing fails two ways, and only one is visible: it can miss a
  token, or it can fire on correct work and be switched off within a week. So every «must be caught» case has a «must stay quiet» twin, and
  one test runs the whole engine corpus — the largest body of correct prose available, full of masked credentials and wide tables — and
  requires silence. It caught a real false positive: the first rule flagged the phrase «a wall the executor cannot pass: signing in a
  wallet» in the lesson catalogue, which is how the value-shape guard (letters **and** digits) got in.
- **`ROADMAP.md`: what is deliberately not built yet, and why.** `/qa --plan` with a checkpoint on the first session in a project,
  `/qa-doctor`, a budget for the round, `qa_day.py --registry` — each with the gap it closes and the shape it would take, plus a «not
  planned» section (a web-tester role, parallel executors, a schema for the profile) so the same proposals stop being re-litigated.


## [0.12.0] — 2026-09-14

### Added

- **38 unit tests for `qa_day.py`, and CI now runs them.** The digest is the only real code the plugin ships, it is parsing end to end,
  and nothing checked it: CI compiled no Python at all and the shell check covered `.sh` only. Parsing does not fail loudly — a parser that
  quietly stops recognising a file prints a shorter digest, and a shorter digest looks exactly like a quiet day. The cases pin the rules
  the skill file states out loud (the day comes from the folder name and never from an mtime; task ids come from the folder name and the
  passport's title only; both folder levels are walked; a localized passport is parsed by structure, not by caption; the fenced tracker
  comment is not repeated in the tail) plus the shapes live projects actually hold — legacy file names, a numbered report from an older
  scheme, a profile with `sessions: none`, a folder with no passport, a root that is not a directory. `validate.yml` gained two steps:
  `compileall` over every tracked `.py`, and `python3 -m unittest discover -s tests`. Unlike the eval suite these are free and
  deterministic, which is exactly why they belong in CI and the evals do not.
- **An eval suite: five behavioural cases over the decisions the engine most easily loses.** Everything CI checked until now was
  structure — file names, frontmatter, the size budget, the absence of project identifiers — and structure cannot tell you whether a rule
  still fires. `evals/` holds a case per invariant: a session refuses to start without a profile and points at `/qa-setup`; a profile of
  `none`s is honoured (no autotest, no case, no tracker comment promised, and the mode asked about); `language: ru` governs the output even
  though every instruction in front of the agent at that moment is English; a second round lands in the existing session folder and updates
  the one `99-report.md`; an `engine-clone` pointing at the plugin's installation is refused and the lesson is re-addressed. Each case
  builds its own fixture project with a scaffold script, and everything in the fixtures is fictional — the no-identifiers rule covers the
  suite too. It is deliberately **not** wired into CI: every run is a real Claude session on a personal credential, so the suite is a
  pre-release gate a human runs (`claude plugin eval . --scaffold --allow-tools Write Edit`, a measured $3.50 for a one-run
  pass), documented in CONTRIBUTING and in the suite's own README.
- **A fourth reference catalogue, `skills/qa/references/session-folder.md`, and step 2 shrinks around it.** The step had grown to 9.4k
  characters — the monthly sweep with its link-fixing passes, the retest specifics, the migration of folders from older naming schemes —
  and the manager paid for all of it in every session, including a first round in an already-swept month where not one of those situations
  occurs. The situational half moved out with its precedents intact, and **unlike the other catalogues this one is not read once per
  session**: step 2 names three triggers (the sweep actually moved something · a session for this task exists · the folder holds old-scheme
  files) and each owns a section. `skills/qa/SKILL.md` is back to 55.9k of its 64k budget, from 60.0k.
- **The plugin manifests carry what a public listing reads.** `plugin.json` gained `homepage`, `repository` and `license`, and its keywords
  were widened; the marketplace entry gained `$schema`, `category: testing`, `homepage`, `author`, a fuller description and keywords. The
  field names are the ones attested in marketplaces in the wild, not invented.
- **The engine now knows when it is behind, and `/qa-setup` is what updates it.** Nothing updates a plugin on its own, so a
  user who installs qa-cube once stays on that version forever while the engine moves on, and no part of the flow ever said
  so. Step 8 of a session now compares the installed `version` against the upstream `plugin.json` and prints a single
  optional line when it is behind; every failure of that check (no network, a 404, a slow answer) is passed over in silence,
  because a courtesy fetch may not add noise to a session's finale. `/qa-setup` gained a step **−1** that actually performs
  the update, then reads `PROFILE-CONTRACT.md` from the newly installed directory rather than from its own root — the update
  applies only after a restart, so a run that migrated a profile against its own stale copy of the contract would quietly
  write yesterday's `contract-version` into it.
- **`<sessions>/engine-feedback.md`: engine lessons stop evaporating for anyone without a clone.** A retro used to write
  process lessons «into the local qa-cube clone», which only exists for someone developing the engine. For everyone else
  `engine-clone` pointed at an installation — the marketplace copy (no `.git`) or the version cache (a flat copy the next
  update writes past) — so the edit disappeared without an error while the version bump was reported as if it had landed.
  Step 7 now verifies the address before touching anything (the directory exists, holds a `.git`, and is not inside
  `~/.claude/plugins/`), and without a valid clone the lesson is re-addressed instead of applied: whatever can be phrased
  through the project goes into its profile or skills, where it works from the next session, and the universal remainder
  becomes a row in `<sessions>/engine-feedback.md` with the plugin version it was written under. Rows are never deleted.
- **`/qa-setup` reconciles that log after an update and, rarely, offers to hand it over.** Open rows recorded under an older
  version are checked against the freshly installed engine; whatever arrived moves to a «Closed» block with the version it
  arrived in — the only place a user sees their own observation land in the original. When three or more rows remain open,
  the onboarding offers **once** to pass them upstream: anonymised text plus a link to the issue tracker, with the posting
  left entirely to the user. The offer and any refusal are recorded in the file's header, so the next one waits for three
  new rows — a request repeated at every run stops being an invitation.

### Fixed

- **The session-rename hook no longer breaks every prompt where `jq` is missing.** `UserPromptSubmit` carries no matcher, so the hook
  script runs on every message and decides «is this /qa?» only after parsing the payload — with `jq`. Without it the script died at that
  first parse, before the early exit, so an ordinary message in an unrelated project earned a `jq: command not found` and exit 127, every
  time. A `command -v jq || exit 0` guard turns the absence into a silent no-op: the session is not renamed, nothing else is affected. The
  cost of the hook itself was measured at the same time and is ~9 ms per prompt, so the early exit needed no further optimisation.

### Changed

- **The README shows the product instead of describing the architecture.** It opened on what the engine *is* — a portable engine, one
  flow, many projects — which answers a question nobody has before they have seen the thing work. It now opens on what a session does,
  then shows it: a 60-second quickstart, the session folder as it actually looks after two rounds, and an excerpt of the report with a real
  findings row, rendered from the engine's own template so the picture cannot drift from what it produces. A **«When you don't need this»**
  section was added for the same reason — a project with no tracker and no environment, a one-off check, and a team that wants a different
  process are all honest non-fits, and saying so costs less than a disappointed first session.
- **The identifier check now also scans `.py`, `.yaml` and `.yml`.** It was written when the engine was markdown and shell only; the eval
  suite and the tests added case files and fixtures, and a fixture is precisely where a real project's task id would get pasted in without
  anyone noticing.
- **The «Boundaries» section no longer promises a web-tester role that is never coming.** It claimed browser testing was «outside the
  starting composition», while the `browser` capability, the manager's preflight at step 4 and a whole section of the `qa-manual`
  instruction had been doing UI checks all along — a reader who opened that section first would conclude the engine cannot test a frontend.
  Browser work is stated as belonging to `qa-manual`, and the sequential-executors rule keeps its own rationale instead of resting on the
  arrival of a role that does not exist.
- **`engine-clone` now defaults to `none`**, and `/qa-setup` asks for it outright («do you develop the engine itself?»)
  instead of proposing the plugin's own root — `${CLAUDE_PLUGIN_ROOT}` resolves to the install cache, so that default was
  wrong for every user but the engine's author. The key keeps working exactly as before when it names a real clone; the
  profile contract is unchanged and needs no migration.

### Changed

- **Step 9 became a fifth reference catalogue, and three findings paragraphs moved into `report.md`: `SKILL.md` is back to 54.4k of its 64k
  budget** (from 58.8k). `references/after-delivery.md` is read **by trigger** — the moment the user says something once the report is
  delivered — which most sessions never do, so most sessions stop paying for it; the step keeps only what decides the first two moves (a
  question is answered, an objection is re-checked by your own eyes before anything is edited) and points at the file for the rest. The
  three paragraphs about shaping a finding for the tracker — the title line, the table surviving a copy-paste, what goes to the
  side-findings registry instead of the report — moved into `references/report.md`, which step 6 already reads whole, so the move buys
  headroom and legibility rather than tokens; saying which is which matters, because the budget exists to stop the manager paying for
  lessons that do not apply to the round in front of it.

## [0.11.0] — 2026-09-10

### Added

- **A new skill, `qa-day`: the digest of a day's (or a week's) test sessions across projects.** The engine already lays
  the work out into session folders but had no answer to «what did I test today», so every consumer wrote that sweep by
  hand — pure mechanics over the engine's own file scheme, which is where it belongs. `SKILL.md` plus a stdlib-only
  Python 3 script (`skills/qa-day/scripts/qa_day.py`, called through `${CLAUDE_PLUGIN_ROOT}`): several project roots in
  one run, `--date` / `--days N` for the window, and a secondary `--task <ID>` mode for «the task has left the testing
  status, what did its session end with». It reads the sessions path from each project's profile (`sessions:`, falling
  back to `docs/test-sessions/`), walks both levels (the live root and the month archives), takes the passport and the
  report under the current names and the legacy ones, and prints the facts for the agent to retell in the project's
  `language`. Nothing is written anywhere and no profile key is introduced — the skill works the moment the plugin is
  installed, with no onboarding question of its own. Two parsing rules are load-bearing: the day of a session is the
  date in its **folder name**, never a file's mtime (an mtime digest counts a typo fix as a round), and a session's task
  ids come from the folder name and the passport's title only, never from the passport's body (whose text lists parents,
  neighbours and past rounds). A localized passport is parsed by the template's structure rather than by field captions,
  and findings are counted off the untranslated `Blocker/Critical/Major/Minor` scale, so the digest works in any project
  language.
- **`/qa-setup` now closes a first onboarding with a short briefing instead of a profile listing.** The person has just
  configured a tool they have never used, and the listing answers «what did you write down», not «what can I do now»:
  the new final step prints ~20 grouped lines in the project's language — how a session is started and how the next
  round of the same one is run, the day digest (already working, nothing to configure), that `/qa-setup` is safe to
  re-run and also migrates a profile to a newer contract, what happens by itself (the subagent roles the profile
  declares, the session file scheme, the mandatory retro), what to edit by hand (the profile and its subfiles are
  ordinary markdown; `language` sets the output language) and how engine edits reach a project. Precedent: an onboarding
  that ended on the profile listing was followed by the question «and what do I type to start a session». In update mode
  the memo is not repeated — the closing is one line about what changed.

- **A round about APPEARANCE settles the window and the focus with the user at preflight.**
  Where the round observes through an environment the user also works in, «may the executor
  resize it and take the focus» is a load-bearing condition, not a detail: asked late, the
  restriction arrives as a scope correction after the measurements are already spent. The
  request is «do not work in this environment for the duration of the round», not «keep the
  window in front», and the ban on taking the focus programmatically goes into the brief from
  the start, with what to do instead. Precedent: both corrections arrived mid-round, and the
  whole width-threshold scenario was struck out with its measurements already taken.
- **Three new entries on the observation channel while the executor runs.** (1) The tool did
  something, and what it did was break the channel — then the instrument is banned outright
  rather than wrapped in «three attempts, then escalate», and its health is read after every
  application, not only at the start (precedent: a resize tool moved the window off-screen,
  which occluded the tab and froze the measured width). (2) The stamp of the channel's health
  is taken in the same call as the numbers it certifies — otherwise the gap between the check
  and the reading silently voids the measurement. (3) A shared resource is addressed by the id
  the tool handed you, never by a substring of its name or URL: in the user's own environment
  the matcher stops being unique the moment the round moves to a second environment, and the
  next call operates on somebody else's object (precedent: a script navigated a stranger's tab
  and cost the round an unattributable measurement).
- **A RECOMPOSITION fix makes the reference environment mandatory and first.** A relaid-out
  screen, a table turned into a list, a restructured payload: the new state is visible, but
  only the pre-task build says what «everything» was, and after the rollout that list is
  unobtainable. Enumerate the old surface first and make the verdict a mapping «every old
  element → where it lives now»; comparing the served artifacts dates the fix for free.
  Precedent: an optional final control scenario turned out to be the round's most valuable —
  it dated the fix by an unchanged stylesheet hash and yielded the baseline that proved
  nothing was lost.

- **A finding's title line now has a required shape: `Area \ what happens, under what
  condition`.** The report step spells out the mechanics — one line of ~90 characters, the
  observable behaviour rather than the cause, never «X does not work», numbers and selectors
  in the body, one defect per title, and a re-read of the title after the body is written. The
  title is what a tracker search matches, so it is the dedup key for the «reconcile the
  finding's class against the tracker» rule, and where the tracker already has a title
  convention the report follows it. Precedent: a Critical went out with a 144-character title
  chaining three defects while its own tracker had been using `Area \ symptom under condition`
  all along, leaving neither the finding nor its duplicates findable by title.

### Changed

- **The step-6 lesson corpus moved out of `SKILL.md` into a third catalogue, `references/report.md`.** SKILL.md had grown
  past the 64 000-character budget the validator enforces, and the overflow was all in step 6: twelve situational lessons
  about findings — is this a finding at all, how its business sentence is worded, what a stray `|` does to the table — which
  the manager paid for in every session, including the ones with no findings to write. They now live in
  `references/report.md` («Is this a finding at all» · «Wording a finding» · «The table's own mechanics», with a Contents
  list), read whole at step 6 the way `planning.md` is read at step 3 and `manual-brief.md` at step 4; the wording of every
  lesson is unchanged. SKILL.md keeps the procedure — the report's structure, the table's contract, the title line, the
  priority scale, report versus side-findings registry, ID numbering, the cell format and its pre-delivery check — and is
  back under budget with room for the next retros (55 100 characters). The retro step's address list now names the new
  catalogue, so a situational lesson about a finding has somewhere to land instead of growing SKILL.md again.

## [0.10.15] — 2026-09-04

### Added

- **The executors are told their output language in the prompt, not left to find it in the
  profile.** `Output language: <language>` is now the first line of every executor's prompt
  and a line of the brief templates, and the three agent instructions state that the language
  governs everything the executor emits — the result files and cases as before, but also its
  reasoning, its progress notes and its final summary, which the user reads in the same
  console as the manager's. The engine's own instructions stay in English; the profile's
  `language` alone sets the output. Before this, a round in a non-English project produced
  artifacts in the project's language while narrating the whole run in English, because the
  language lived in a profile the subagent only reached after it had started working.
  Test code is the one exception: it follows the project's code style.

### Changed

- **The planning and briefing corpora grew the lessons of a trimmed-scope round.** Planning
  (`skills/qa/references/planning.md`): a task that re-states requirements already tested (an
  MVP cut, a phase two) is planned by first re-rating the previous round's findings against
  the new text; an «always / never» finding is only as wide as the inputs actually tried; a
  retest whose trigger the tracker never dated is dated by the served build; a contract is
  pulled with its types, not only its field names. Briefing
  (`skills/qa/references/manual-brief.md`): listing a probe's expected outcomes biases the
  executor; a sanctioned mutating probe needs its unanticipated-refusal branch written in
  advance; a negative that needs someone else's entity gets a verified identifier; a browser
  profile is addressed by id, never by its user-editable label; a tool that reports success
  has not necessarily done anything.
- **A link sweep after archiving is proven by existence, not by an empty grep** (step 2): a
  mechanical prefix rewrite keeps pointing at folders that were themselves renamed, or never
  migrated, and the grep for the old pattern still comes back clean.
- **A report's business sentence may use no noun that is neither visible in the UI nor
  verbatim in the evidence** (step 6), and its quantifiers are checked against the evidence
  the same way: a term borrowed from the spec brings a model with it that nobody verified.

## [0.10.4] — 2026-09-03

### Added

- **The anonymisation rule is now enforced beyond file contents.** Commit messages, file
  names, PR titles and PR bodies are checked too — the gap that let `Fix per ABC-123` reach
  the published history while the files themselves were clean.
  - `.githooks/pre-commit` inspects added lines and file names; `.githooks/commit-msg`
    inspects the message. Enable in a fresh clone with
    `git config core.hooksPath .githooks`.
  - The CI job reads the commits a push or PR adds, plus the PR's title and body; the
    release workflow checks the tag name, since the release title is built from it.
  - The pre-commit hook also checks the current branch name, which travels into PR
    listings and merge commits.
  - `.github/scripts/check_identifiers.py` is the single definition of «an identifier»,
    shared by the validator, the hooks and CI, so the rule cannot drift between them.

## [0.10.3] — 2026-09-03

### Changed

- **No identifiers from real projects anywhere in the engine.** Every precedent that carried a
  tracker id from the project it was learned in is now anonymised: the mechanics of the lesson
  stay, the address goes. 77 references across the skills, the agent instructions, the hook,
  this changelog and the contributing guide. The engine is published outside the projects it is
  written in, and those numbers are a client's data.
- The retro step (step 7) now states the rule for future edits, and `CONTRIBUTING.md` documents
  it: session files, project profiles and project knowledge bases may name anything, the engine
  may not.

### Added

- CI enforces the above — `validate-plugin.py` fails on a task-shaped identifier
  (`ABC-123`, `service#456`) in the engine's files, naming the file and line. Requirement
  markers (`FR-1`, `AC-2`) and the fictional `ACME-` examples stay allowed.

## [0.10.2] — 2026-09-03

Lessons from live sessions, written straight into the engine by their retro step (this
includes what was bumped as 0.10.1, which was never released separately).

### Added

- **The reversibility gate covers permissions, not the recording of the result.** A dry call
  of the reverse operation proves the form opens and the rights suffice — nothing about whether
  the platform will register the forward step. The destructive step now counts as finished only
  once the request reaches a terminal status, and «executed in the external system, the platform
  says failed» is a signal to stop rather than to continue. The brief must also say what to do
  when the rollback proves impossible through the product's own fault: record it, report it, do
  not repair it by bypassing the product.
- **Two fields every «click needed» request to the user must carry**: what the step does to the
  environment (amount, recipient, which entity changes) and what kind of window it is — a free
  reversible signature or an irreversible transaction that costs a fee. Plus: a signature and the
  send cannot be merged into one request (the executor's turn ends between them), and the brief
  states what happens if the user clicks the wrong thing.
- **Acceptance requires the version of the artifact the run actually exercised** — the served
  bundle's hash, the deploy ref, the image version. Without it a verdict cannot be tied to a
  build and the next retest starts with archaeology.
- **On a retest, check that the observation path is still alive and rest the verdict on the final
  artifact**, not on an intermediate UI state: a defect's symptom goes stale together with the
  build.

### Fixed

- The trailing newline in `.claude-plugin/plugin.json`, dropped again by a version bump — now a
  failing check in CI rather than an invisible detail.

## [0.10.0] — 2026-09-03

### Changed

- **The whole engine is now written in English.** The skills (`/qa`, `/qa-setup`), the three
  subagent instructions, all seven session templates, the profile contract and this
  repository's own docs were translated. Every lesson, precedent and number was carried over —
  the translation is a rewrite, not a summary.
- **The output language is unchanged and still belongs to the project.** `language` in
  `.claude/qa-profile.md` governs the conversation and every artifact — plan, briefs, results,
  report, retro, TMS cases, the tracker comment and the profile itself. The rule is now stated
  explicitly in three places (the manager's step 0, each agent, `/qa-setup`), together with the
  reason: the language of the instructions says nothing about the language of the output.
- The default when a profile has no `language` field is therefore English rather than Russian.
  Existing profiles are unaffected — they all declare the field.
- `README.md` now opens with an installation note for non-English speakers.

### Added

- The engine's own repository grew GitHub scaffolding: structural validation on every push,
  releases built from a tag, this changelog, an MIT license and issue templates.

## [0.9.2] and earlier

The history before 0.10.0 was squashed into a single root commit, so the per-version detail
is gone. The shape of it:

- **0.9.x** — the `qa-analyst` role and the `test-cases` key (`upfront｜inline｜none`):
  test cases can now be written from the requirements *before* the manual run, which is what
  makes a mismatch read as a product defect rather than as a sloppy case. Profile contract v5.
- **0.7.x–0.8.x** — token economy (contract v4): a thin `CLAUDE.md`, TL;DR headers on profile
  subfiles, knowledge organised per domain, and targeted reading lists in the executors' briefs.
  One report per session under `99-report.md`, updated by every round.
- **0.3.x–0.6.x** — the `secrets` and `logs` capabilities, the access-channel step in
  `/qa-setup` (MCP → CLI → a generated REST skill), contract versions 2 and 3.
- **0.1.x–0.2.x** — extraction of the flow from a single project into a portable plugin: the
  manager plus the manual and automator subagents, the session file scheme, retros.
