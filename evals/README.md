# The eval suite

Behavioural tests for the engine. The rest of CI checks *structure* — file names, frontmatter,
the size budget, the absence of project identifiers — and structure says nothing about whether a
rule still fires. These cases check the rules an agent actually has to follow, and they are the
only regression net a corpus of instructions can have.

## Running it

```bash
claude plugin eval . --scaffold --allow-tools Write Edit
```

`--scaffold` is required: every case builds its fixture project with an author-supplied bash
script (`setup.sh`), and the CLI refuses to run those unless you ask for it. `--allow-tools`
grants the gated tools a case declares — without them a grader that checks a file was *not*
created passes vacuously, because the run could not have created it either way.

Useful flags while iterating:

| Flag | Why |
|---|---|
| `--case <name>` | one case instead of all five |
| `--ablation none` | skip the no-plugin baseline arm — halves the cost, loses the «did the plugin cause this» signal |
| `--runs 1` | one run per case instead of the declared two |
| `--keep-temp` | keep each run's sandbox (`home/cwd` is the fixture project) for debugging |
| `--max-cost-usd 2` | a hard ceiling; the run aborts and reports partial results |

### What a pass actually costs

Measured, not estimated — the first calibration pass of this suite, one run per case with no
baseline arm, cost **$3.50 and took eight minutes**. Per case it ranged from $0.30
(`profile-missing`, which stops after a few turns) to $1.26 (`degradations-declared`, which reads
the profile and most of the pipeline before answering). A run is a real session, so its cost
follows how far the engine gets, not some flat per-call price.

That makes the declared `runs: 2` with the baseline arm about **$14 a pass**. So in practice:

- **routine check** — `--runs 1 --ablation none`, about $3.50;
- **before a release that matters** — the full pass, for the repeat runs (a judge is not
  deterministic) and the «did the plugin cause this» delta.

Set `--max-cost-usd` if you want a ceiling, but know what it does: it is checked *before* each run
launches and does not stop runs already in flight, so a low ceiling will still spend whatever the
current run costs.

## Why this is not in CI

Every run is a real Claude session on your own credential. GitHub Actions has no credential of
ours, and giving it one would mean every push spending money on a judge whose verdicts are not
deterministic anyway. So the suite is a **pre-release gate run by a human**: before cutting a
release, run it, and treat a case that dropped as a regression to explain rather than a number to
accept. `validate-plugin.py` stays the thing that runs on every push.

## What each case pins down

| Case | The rule it defends |
|---|---|
| `profile-missing` | step 0 does not start a session without `.claude/qa-profile.md`, and points at `/qa-setup` instead of improvising one |
| `degradations-declared` | a profile of `none`s is honoured: no autotest, no case, no tracker comment promised, and the mode is asked about |
| `language-ru` | `language: ru` governs the output even though every instruction in front of the agent at that moment is in English |
| `session-continuation` | a second round lands in the existing session folder and updates the one `99-report.md` |

Three of the five are **behavioural** — the engine is handed a session and the graders read what it
did (`profile-missing`, `degradations-declared`, `language-ru`). Two are **knowledge** cases: they
ask the engine to state a rule rather than act it out (`session-continuation`, `engine-clone-guard`).
That is a deliberate trade and worth knowing when you read a green board. Both of those rules live at
the start or the end of a long procedure, and a run that has to reach them costs three times as much
and dies on the wall clock as often as it succeeds — `session-continuation` was behavioural twice and
failed on turns and then on the 300s timeout, both times in the middle of doing exactly the right
thing. A knowledge case proves the rule is legible and reachable; it does not prove it is obeyed
under pressure. When a rule matters enough to justify $1.50 a run, write the behavioural version and
give it `timeout_seconds` and `Bash` (step 2 renames folders with `mv` — without Bash the engine
cannot do what the case is grading).
| `engine-clone-guard` | an `engine-clone` that points at the plugin's installation is refused, and the lesson goes to the project or to `engine-feedback.md` |

## Writing another case

A case is a directory with `case.yaml` and, where it needs a fixture, `setup.sh` that sources
`../fixture.sh`. The scaffold runs **in the run's own workspace**, which is also the agent's
working directory.

Four things are easy to get wrong — each one cost a paid run to find:

- **`scaffold_script` belongs in the `context:` block**, not in `execution:`. Put it in the wrong
  one and it is silently ignored: no error, no fixture, and a case that looks like it ran.
- **A slash-command prompt does not call the `Skill` tool.** `/qa …` is injected into the context
  directly, so a `tool_used: Skill` grader fails on a perfectly good run. Use the `--ablation`
  delta to answer «did the plugin cause this», not a tool grader.


- **`file_exists` checks what the RUN created, not what is on disk.** A file the scaffold wrote is
  invisible to it. Use it for «the session folder was created» and, with `exists: false`, for «and
  nothing was created here» — never to assert that the fixture exists.
- **A `regex` grader over the last message is a blunt instrument.** `not_contains: autotest` fails
  the correct answer «autotests: none, so no autotest will be written». Keep regexes for things
  that can only appear on the right path (`/qa-setup`, `engine-feedback`, Cyrillic text) and leave
  judgement to an `llm` grader.
- **Keep an `llm` criterion to one question, and say what NOT to judge.** The judge is a cheap
  model. The first version of `answers-in-russian` explained why the language rule exists and what
  the engine's instructions are written in — and the judge voted FAIL three times on an answer
  written in flawless Russian, while the regex on the same text passed. Ask one thing, forbid the
  rest explicitly.
- **A fixture that triggers a second rule measures two things at once.** `session-continuation`
  originally dated its existing session in the previous month, which set off the monthly sweep;
  the run spent every turn archiving folders and fixing links and never reached the sentence the
  grader needed. Build the fixture so only the rule under test applies.

Grader types: `llm` (criteria), `regex` (pattern · `match: contains｜not_contains｜count:N` ·
`target` · `flags`), `tool_used` (tool · `input_match` · `min` · `max`), `tool_order`
(before · after), `file_exists` (path · `exists`), `baseline` (baseline_file · criteria).
`arm: with-only` marks a grader as a plugin-fired indicator rather than part of the score.

Everything in a fixture is fictional, the engine's no-identifiers rule included: the project is
`acme-shop`, the task is `ACME-412`.
