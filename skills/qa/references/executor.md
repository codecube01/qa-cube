# Running the check: the executor's catalogue

Read by the manual tester (`qa-manual`) before the first request to the environment, and by the automator (`qa-automator`) before the
first assertion — both from the brief's reading list. Each entry is a situation a run lands in and the move that keeps it from costing a
false finding, a burned expendable or a lost measurement; the precedent that closes an entry is what paid for the rule. **The «Contents»
below is read whole, and it is the rules** — one line per entry, the trigger and what you do; an entry's body is opened for its mechanism
and its precedent only when its line fired — that entry alone, by `grep -n` for its first words and a `Read` of ~25 lines from there,
never the file without a `limit`.

## Contents

**Every line below is the rule: a trigger, then what you do about it.**

**Probing and measuring**

- a VALID mutation refused unexpectedly → a per-field matrix in one pass (one paced probe per input field, on the round's own entity, within the brief's budget, after the snapshot), not hypotheses one at a time
- an operation the server refused, and the theory is «maybe it was stale / cached» → before repeating it, find out where the validating side reads its data; a source that does not change between attempts cannot answer differently, and the retry only spends the expendable
- single-use artifacts (an invite link, a one-time token, the only application in the queue) → consumed by any touch, a trial one included: work out the semantics on an expendable instance, measure on a clean one, one touch per control point; a channel that returns «the latest per key» → compare its timestamp with the clock, save each artifact under its instance's name, prove a batch distinct (`sort -u`) before measuring
- an unknown time boundary (a TTL, a window, a deadline) → bisection from below (1 → 2 → 5 → 10 min), never long probes; many points of one TTL → a batch of untouched instances touched by a background scheduler keyed to absolute epoch times
- a reference value you compute yourself (a hash, a signature, an aggregate) → self-check the primitives on a known vector, print the field-by-field decomposition of the input, and only then compare
- text the user sees → quoted as RENDERED (`textContent`, the screenshot), never with the template's markup; emphasis in your own notation; markup that reaches the screen is said in words, it is itself a defect

**When an outcome looks like a defect**

- an unexpected transition or refusal → not a finding until a control experiment on a deliberately clean object has been run; the same result means normal behaviour
- «the system rejects a valid input» → diff your input against a recent SUCCESSFUL call of the same type, element by element, before writing it: a refused home-made request is usually not the one the product sends
- a conclusion drawn from one passive observation («the interface does not flag X», «the component is locked») → driven to an action before it is written down: press the control, call the method that would refute it

**The round's limits**

- the scenario's result is visible only to the user (a chat message, an email, a screen) → side experiments that produce the same kind of observable event are deferred to the end of the observation loop, not cancelled, not squeezed in; a dropped control is named in the result as what stays an observation
- your own precondition cannot be built (another defect blocks the path) and the requirement is a guard («the action is unavailable while …») → check it on someone else's entity already in the required state: the expected outcome is a refusal, `updated_at` before and after proves the environment untouched

## Probing and measuring

**A VALID mutation refused unexpectedly → a per-field matrix in one pass, not hypotheses one at a time.** One probe per input field (paced)
sorts the fields into «written» / «silent no-op» / «always refused» in a single round; guessing (the format? a field pair? an enum?) burns a
call per guess. Every probe is a write that may land, so the matrix goes only on the round's own entity, within the brief's mutation
budget, and after the snapshot of every scalar field that precedes the first write.

**Before REPEATING an operation the server refused on the theory «maybe it was stale / cached», find out where the validating side reads
its data.** If that source does not change between attempts, the retry cannot give a different answer and only spends the expendable it
consumes — often a user's signature or click. One read of the contract (does the API even expose the list the check runs against?) is
cheaper than the second attempt. Precedent: a removal refused with «X is not a member» was retried and burned a second user signature;
introspection would have shown the member list lives only on the backend's side.

**Single-use artifacts (an invite link, a one-time token, the only application in the queue) are consumed by any touch, including a trial
one.** Work out the semantics on a deliberately expendable instance and take your measurement on a clean one: one touch per control point.
«Let me first check whether the object is still alive» is already a consumption. A channel that hands artifacts back as «the latest one per
key» (a mailbox relay, a message sink) can return a stale or a neighbour's artifact silently: compare its own timestamp with the clock before
using it, save each one under its instance's name the moment it is fetched, and prove all of a batch distinct in one command (`sort -u` over
the ids) before measuring on them — mixed-up instances void a whole series.

**Measure an unknown time boundary (TTL, window, deadline) by bisection from below, not with «long» probes**: 1 min → 2 → 5 → 10 → onward.
The estimate in the brief can be off by an order of magnitude; a series of long probes returns the same refusal every time and burns
expendable instances for nothing. Many points of one TTL are measured by a batch of untouched instances: issue N in a row (taking each one
right after it is issued), leave them untouched, and touch them from a background scheduler keyed to absolute epoch times, not offsets from
its own start — one timer then covers every point to the second, and the rest of the round runs under it in parallel.

**A reference value you compute yourself — a hash, a signature, a checksum, an aggregate: first self-check the primitives, then show the
decomposition of the input, and only then compare.** Primitives are verified with a known vector (the reference hash of an empty string, an
address encoder against an address from the same data) — two minutes remove a whole class of «my parser lies». The field-by-field
decomposition of the input is printed BEFORE the comparison: a «does not match» verdict passed before the structure was taken apart is
useless and more often points at your parsing than at the product. Precedent: a «MISMATCH» on a transaction hash turned out to be a wrongly
posed question — the field held a 12-field form while the hash covers nine — and cost twenty minutes.

**Text the user sees is quoted as RENDERED, never with the template's markup.** A caption read from the bundle arrives as
`<b>{email}</b> …`, and pasting the rendered string back in that form makes the one question a text finding exists to answer — «is the
markup visible on screen?» — unanswerable from your file. Quote `textContent` (or the screenshot), and mark emphasis in your own notation
(`**…**`); where the raw markup does reach the screen, say so in words, because that is itself a defect. Precedent: a result quoted a dialog
title as «…<b>address</b>?», and the manager had to reopen the dialog to learn the tags were rendered as bold.

## When an outcome looks like a defect

**An unexpected transition or refusal is not a finding until a control experiment on a deliberately clean object has been run.** You saw
something odd on an object that went through the feature under test — repeat the same action on an object that never went through it: the
same result means the behaviour is normal and unrelated to the feature, a different one means it is now a finding. Costs a minute, saves
you from a false bug in the report. Precedent: a status moved to a failed terminal state on its own and looked like a regression from a
«stale value», yet it reproduced with an empty field too.

**Before writing «the system rejects a valid input», diff your input against a recent SUCCESSFUL call of the same type** — decode what the
product itself sent and compare element by element: a refusal of a home-made request more often means the request is not the one the
product sends. Precedent: a «valid» set of signatures was refused as short by one; the last successful operation of that type carried an
extra service signature first, which the hand-built set lacked.

**A conclusion drawn from one passive observation is driven to an action before it is written down** — «the interface does not flag X»,
«the component is locked»: press the control, call the method that would refute it. Precedent: twice in one round a conclusion already in
the file was refuted by one click (the gate was there) and by one read-only call (the component answered at once).

## The round's limits

**Side experiments that produce observable noise are deferred to the end of the observation loop — not cancelled, not squeezed in
halfway.** When the scenario's result is visible only to the user (a chat message, an email, a screen), any extra call of yours that spawns
the same kind of observable event spoils their main check: keep such experiments in a list and run them once the observation loop is
closed. An experiment did have to be dropped — write in the result which control experiment was not run and what therefore stays an
observation rather than a contract. Precedent: re-checking a neighbouring field would have generated a seventh alert and blurred the
observation of the merge.

**A guard requirement («the action is unavailable while …») may be checked on someone else's entity on the environment — the expected
outcome is a refusal, and a refusal changes nothing.** When another defect blocks you from building your own precondition (the path loops
back on itself), take an existing entity in the required state and perform the forbidden action: record `updated_at` (or its analogue)
before and after — unchanged means the environment was untouched. The technique closes a requirement that would otherwise land in «not
covered» — by the refusal only: a borrowed entity that is NOT refused proves nothing about the guard's absence, since it differs from your
fixture in more than the one attribute (`planning.md`, «Borrowing an object that already HAS the precondition»). Precedent: two guard requirements were unreachable because of a defect in the onboarding that creates the precondition.
