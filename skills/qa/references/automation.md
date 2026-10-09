# Deciding what to automate

Read at step 5 of `../SKILL.md`, before the automation choice is put to the user and before `4-automator-task.md` is written. Each entry is
a way the automation decision has gone wrong — a test nobody wanted, a price that did not exist, a question read as an order — and the line
that would have settled it before the automator touched the code; the precedent that closes an entry is what paid for the rule.
**The «Contents» below is read whole, and it is the rules** — one line
per entry, the trigger and what the manager does; an entry's body is opened for its mechanism and its precedent only when its line fired —
that entry alone, by `grep -n` for its first words and a `Read` of ~25 lines from there, never the file without a `limit`.

## Contents

**Every line below is the rule: a trigger, then what the manager does about it.**

**The decision**

- the scenario needs dozens of operations or long waits to reach its conclusion → the price of a run is an input to the decision, computed from the manual result's own timings (operations × measured durations + every propagation lag), never from intuition; a noticeable price goes to the user BEFORE the automator is launched
- the test is NEW to its host class → the class's fixed cost (provisioning, per-test hooks, stabilising reads) is read off a recent run log of a neighbouring test and added — no manual timing contains it
- the feature is the size of one query parameter (a filter, a flag) → its size is a ground of its own, beside the price: «is this feature worth a test at all» is asked before the automator edits the code, whatever the run costs
- the automation question is put to the user → it comes before the delivery at 6.5, so three lines go above the options: what the change is and whether it is merged, the round's verdict with its counts, what the test would assert
- the user's answer is itself a question («isn't a test required by our rules?») → it is a question, not the choice: answer it on the merits, then put the choice again; acting on it starts work nobody ordered
- the manual run's acceptance criterion is statistical («each variant ≥ 20 %») → the test asserts the degenerate outcome («each variant occurred at least once»), translated by the manager, not the automator

**The brief**

- a rule of the project's own profile is about to go into the brief as an instruction («these helpers assert 200 internally, add a raw variant») → it is checked against the specific helpers this round touches first; true of the profile's general case, it may be false of these two
- the user asks what the coverage costs → say what measures it: run logs often carry no timestamps on step lines, so a step's duration is measured by a run on reverted code, repeated where the run-to-run spread rivals the delta

## The decision

**The cost of a run is as much an input to the decision as the value of the coverage, and it is computed from the manual result's own
timings.** A scenario that needs dozens of operations to reach its conclusion (a series for a distribution, long waits for workers) costs
minutes in every nightly run: count the operations the steps will wait on — each one through its asynchronous pipeline, create to callback
to final read — multiply by the durations the round measured, and add every propagation lag a step must sit out. A figure put to the user
from intuition under-prices exactly the waits, and the choice is then made at a price that does not exist. Precedent: two tests (30 payments
and 20 payouts with a wait for the cascade) were written and then stopped by the user on the very first run with the words «that run is too
expensive» — the price was visible from the manual result in advance. Precedent: a merge into an existing test was offered at «about 50 s»
and chosen; it cost 131 s — two operations of ~50 s each plus a setting lag, all three durations printed in the manual result.

**A test NEW to its host class pays that class's fixed cost too** — its provisioning, its per-test hooks, its stabilising reads — which no
manual timing contains: read it off a recent run log of a neighbouring test in the same class and add it. Precedent: a new test priced at
~3 min from the manual timings ran 9–10 min, two thirds of it the class's account provisioning, per-test waits and state snapshots.

**The size of the feature is an independent ground, alongside the cost of the run.** A cheap merge into an existing test can still be work
nobody wants: a feature the size of one query parameter may deserve no test at all, whatever the run costs. So the question to the user
before launching the automator is not only «is this run expensive» but also «is this feature worth a test at all» — and it is asked before,
not after the automator has edited the code. Precedent: the manager sliced the automation as steps merged into three existing tests (the
cheapest possible form) and launched the automator; the user's answer was «we only automate bigger features, this is just a filter», and the
edits had to be reverted mid-run.

**That question travels with the round's result.** It comes before the delivery at 6.5, so the user has not yet seen what the manual round
found — put three lines above the options (what the change is and whether it is merged, the round's verdict with its counts, what the test
would assert), or the user dismisses the choice and asks for exactly those lines first. Precedent: a bare automation dialog was dismissed
with «first explain what you did, what automation needs, and what that merge request is».

**An answer to that question that is itself a question is a question, not the choice.** «Isn't a test required by our rules?» is answered on
the merits, and then the choice is put again; acting on it starts work nobody ordered. Precedent: a reply of that shape was read as «write
it», and the user stopped the first tool call of the automator's brief with «that was a question, not a request».

**A statistical criterion is translated into a stable assertion by the manager.** The manual run's acceptance threshold («each variant
≥ 20 %») flakes in a test; what should be asserted is the degenerate outcome («each variant occurred at least once»), and the brief says so
rather than leaving the translation to the automator.

## The brief

**A rule of the project's own profile is checked against the specific helper before it goes into the brief as an instruction.** «These
helpers assert 200 internally, so add a raw variant» is true of the profile's general case and may be false of the two helpers this round
touches; a brief that carries it unchecked orders work that is not needed. The names of any helpers you mention — and the concrete values
of their parameters, if you quote them — are verified by grepping the code rather than from memory: an inexact name or number is an extra
iteration for the automator.

**Asked what the coverage costs, say what measures it.** Run logs often lack timestamps on step lines, so a step's duration is unreadable
from the log — then measure by a run on reverted code, repeated when the run-to-run spread rivals the delta.
