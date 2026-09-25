# Contributing to qa-cube

The unusual thing about this repository: **its main source of changes is the retro step of a
real test session, not a backlog.** When `/qa` finishes a session, the manager collects the
executors' retro sections and edits the engine, the project profile, the project's skills or
the knowledge base right there. So the strongest contribution looks like «this happened in a
session, it cost a round, here is the rule that prevents it» — with the precedent kept in the
text. That is why the instructions are full of lines like «precedent: …»: a rule
without its story gets deleted by the next person who finds it inconvenient.

## Where a change belongs

Four addresses, and picking the right one matters more than the wording:

| The change… | goes to |
|---|---|
| would work in any project (roles, acceptance, formats, degradations) | the engine — this repository |
| names a specific tool, environment, class or account | that project's `.claude/qa-profile.md` |
| is a fact about a product (API contract, feature behavior, limits) | that project's knowledge base |
| is a pitfall of a project-local skill | that skill |

In doubt between the first two: if you cannot state the rule without naming your tracker or
your staging host, it is not an engine rule.

## Working on the engine

The engine is plain markdown — skills, agent instructions and templates. There is no build.

```bash
python3 .github/scripts/validate-plugin.py   # structure, frontmatter, templates, contract
```

Installing the plugin **copies** the files into the Claude Code cache, so editing your clone
changes nothing by itself. To try an edit:

```bash
# bump "version" in .claude-plugin/plugin.json first
claude plugin marketplace update qa-cube && claude plugin update qa-cube@qa-cube
```

The new copy is picked up by the next launch of `claude`.

## Two rules that are easy to miss

1. **Every engine edit bumps the patch version** in `.claude-plugin/plugin.json`. Without it
   the update does not reach anyone's cache.
2. **Ask whether the edit requires anything of a project profile** — a new header key, a new
   mandatory question in a section, a rename. If it does, bump the version in
   `PROFILE-CONTRACT.md` and add a row to its history table; if it does not, leave the contract
   version alone. A skipped bump makes profiles drift silently; a needless one gives every
   project a false «your profile is behind» warning.

## The eval suite

`validate-plugin.py` checks structure; it cannot tell you whether a rule still fires. That is what
`evals/` is for — five cases over the decisions the engine most easily loses (starting without a
profile, honouring a profile of `none`s, the output language, continuing an existing session,
refusing an `engine-clone` that points at an installation).

```bash
claude plugin eval . --scaffold --allow-tools Write Edit
```

It is **not** part of CI and is not meant to be: every case is a real Claude session on your own
credential, and a judge's verdict is not deterministic. Run it before cutting a release, and treat
a case that dropped as a regression to explain rather than a number to accept. The suite's own
README covers the flags, the measured cost (~$3.50 for a one-run pass, ~$14 for the full one) and
how to add a case.

## Releases

Two branches. **`dev`** takes every change, retros included, each with its patch bump, and
the entries pile up under `[Unreleased]`. **`main`** is what the marketplace hands out, so a
merge into it is a delivery whether it is called a release or not — and that is why it is one:

1. open a PR `dev → main`;
2. in it, rename `[Unreleased]` in `CHANGELOG.md` to the version in `plugin.json` and put a
   fresh empty `[Unreleased]` above it — CI refuses a PR to `main` that brings a new version
   without its section;
3. merge. The release workflow sees a version with no tag yet, tags the merge commit
   `vX.Y.Z`, builds the archive and publishes the release with the notes from that section.

A merge that does not change the version releases nothing. Versions skip numbers between
releases (0.17.1 → 0.17.9): the patches in between lived on `dev`.

## No identifiers from real projects

The engine travels between projects and gets published, so **nothing in its files may name
the project a lesson came from**: no tracker ids (`ABC-123`, `service#456`), no environment
hostnames, no service, company or account names. Write the precedent by its mechanics —
«precedent: a retest where the defect's symptom went stale together with the build» — and
drop the address. The mechanics are the lesson; the number is a client's data.

Session files, a project profile and a project's knowledge base are the exception: they live
inside their project and may name anything.

This is enforced by CI, not by good intentions. `.github/scripts/check_identifiers.py` is the one
definition of a leak — tracker ids, hosts and URLs outside an allow-list, email and IP addresses,
home directory paths, random-looking entity ids, secret shapes, and the names from a private
denylist — and the git hooks, `validate-plugin.py` and CI all call it, on file contents, file and
branch names, commit messages, PR metadata and the whole published history
(`check_identifiers.py --history`).

Real company, client and service names cannot be guessed by a regex, so they come from a
denylist that never enters git: one term per line in `.identifiers.local` at the repo root
(git-ignored), and in CI the `QA_CUBE_DENYLIST` repository secret. A term also catches its
hyphenated, joined and dotted spellings, and hits are printed masked.

## Style

Match what is already there: an instruction states what to do, then why, and closes with the
precedent that earned it. Keep the identifiers untranslated (profile keys, session file names,
`subagent_type` values, the `Blocker/Critical/Major/Minor` scale). If a patch to an instruction
repeats for the third time, fold it into the main text instead of adding a fourth phrasing.
