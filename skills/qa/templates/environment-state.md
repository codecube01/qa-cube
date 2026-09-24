# Environment state: <project>

**A snapshot, not a log.** What the environment holds now, for the sanity check before the next run. Every fact carries the date it
was checked; a fact that went stale is **replaced**, never appended next to its old version. The runs' results live in the registry
`README.md`, how the product works — in the knowledge base. A snapshot is not a measurement: balances, objects and access are
re-checked live before a scenario that relies on them, and a discrepancy is fixed here at once.

## TL;DR (as of <date>)

- <the working test objects and what can be done on them today>
- <the preconditions a typical scenario trips over>
- <access: which accounts work, what needs the user>
- <what is flaky right now>
- <the current build fingerprints>

## Access and accounts

- <fact> (<date>)

## Test objects and balances

- <fact> (<date>)

## Left-behind artifacts

<What previous runs created and cannot delete — so the next run neither trips over it nor mistakes it for fresh data.>

- <fact> (<date>, <session>)

## Flaky and degraded

- <fact> (<date>)

## Builds

- <component>: <fingerprint> (<date observed>)
