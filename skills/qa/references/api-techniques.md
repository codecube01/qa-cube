# API techniques

Read by `qa-manual` on any round that sends requests to the product's API — from the shell or from the page console — and by
`qa-automator` when it writes an API test; the brief gives the path and names the sections the round needs — and by the manager, who reads
the first screen and the contents before writing the brief, which is how the sections get picked (the «GraphQL» one by the product's stack). A round that also drives the
UI reads `browser-techniques.md` beside this file. The recipes are protocol-level and hold in any project; what belongs to one project —
its endpoints, its wrappers, its own auth flow — stays in the profile. Every recipe below was paid for by a lost round.

## TL;DR — the typical flow

1. **Never guess the contract** — read it before the first real request (the API's own description or schema, a captured request, the served bundle).
2. **Replay a captured request, changing only its parameters**, instead of composing one — the request is valid by construction.
3. **Read the status and the raw text first**, and print an error body whole — the formatter must not become the source of a finding.
4. **«The endpoint exists» is proven against a certainly non-existent path**, never by a `200` alone.
5. **A scripted login is walked hop by hop**, not by an auto-following client.

## Contents

- requests and answers — the replay, the status and raw text, an error body printed whole, a redirect chain hop by hop, a write-then-read helper that checks the read's own status
- does it exist — the SPA catch-all and the responder that answers every key alike
- GraphQL (only where the product's API is GraphQL) — the schema, replaying an operation, the error object and a null `data`, the client's cache, what arrived and what is missing

## Requests and answers

- **Replay beats composing.** Take the captured request as it is and change only its parameters: the request is valid by construction (the GraphQL form — «GraphQL», below). Filters, limits and permissions are checked by comparing responses across parameter values — and with and without a secondary argument, which is how a filter silently ignored in the presence of another argument is found. No captured request yet → read the contract first, compose second.
- **Read the status and the raw text first, never a parsed body** (`r.status` + `r.text()` in a page, `resp.status_code` + `resp.text` or `curl -sS -w '%{http_code}'` from the shell) — an expired session answers `401` with an empty or non-JSON body, and a parser replaces the cause with a parse error. **Print the whole error body**, and in a «write, then read» script log the write's result BEFORE the read — a read that throws must not take the record of the writes with it (the GraphQL shapes of both — «GraphQL», below).
- **A «write, then read back» helper checks the READ's own status before comparing values** — a throttled (`429`), expired or failed read that returns no object must come out as «read failed», never as a field equal to `null`. Otherwise a rate limit reads as «the write erased the field», and the finding is filed against the write path. Precedent: a validation sweep paired every write with a read; one read hit the environment's rate limit, the helper mapped the missing profile to `null`, and «a four-character address wipes the field» stood in the result until the journal showed the write had landed. Pace a sweep below the environment's limit and retry the read on `429`.
- **Trim a response's output only when it succeeded; an error response from `curl`/Python is printed whole** (in a page, the same
  rule as «Read the status and the raw text first» above). A «keep the interesting keys» filter turned a `400` into `{}`, which read as
  «the contract promises an error schema and sends an empty body» — the formatter nearly became the source of a finding.
- **A login or other redirect chain scripted outside the browser is walked hop by hop**, reading `Location` and `Set-Cookie` at each step —
  an auto-following client hides where a cookie is set and where the flow breaks. Send a browser-like `User-Agent` (plus the `Origin` and
  `Referer` the flow expects): public hosts answer a library's default one with `403`.

## Does it exist

- **An SPA catch-all answers `200` with the index document on any path** — `/health`, `/openapi.json`, `/docs` and a certainly non-existent path alike. «The endpoint exists» needs a body that differs from the non-existent path's one, compared byte for byte; and a documented path may carry an API prefix the probe forgot. The same control unmasks any responder that answers every key alike — a fallback handler returning zeros for every method looks like «the method exists, its value is 0» until a certainly non-existent key gets the same answer.

## GraphQL

Named in the brief only where the product's API is GraphQL; a product without it never reads this section.

### The schema

- **The schema is read before the first real query, never guessed.** Start with `{__schema{queryType{fields{name args{name}}}}}` (and `mutationType`), then `__type(name: "X")` for each type you touch. Every guessed field is a lost round, and «obvious» ones are the usual casualties — a list that needs a parent id, a wrapper whose array is not called `items`.
- **Read the `kind` of every field and argument.** An object or list field without a selection fails with «must have selections»; a `NON_NULL` argument needs `!` in the variable declaration. Take the RESPONSE type of a mutation too, not only its arguments — wrappers are inconsistent even between paired operations (one returns `{entity {…}}`, its sibling the entity itself).
- **A nested type's name needs four to five levels of `ofType`** — `NON_NULL(LIST(NON_NULL(OBJECT)))` returns `name: null` after three, and `__type` on a guessed name returns `null`. Unwrap `ofType{kind name ofType{…}}` deep enough, or list `__schema{types{name fields{name}}}`.
- **Introspect in small queries** — the root type's fields first, then the fields or input fields of one type; a full dump is truncated by the output limit.
- **A contract read from the client's embedded query text has names without types** — `manual-brief.md`, «A contract read out of the CLIENT's own query documents».

### Replaying and reading the answer

- **Replay an intercepted operation, never compose one.** `const p = JSON.parse(log.body)` and send `{operationName: p.operationName, query: p.query, variables: <yours>}`: only the variables change, the query is valid by construction. No captured operation yet → introspect the type first, compose second. On a browser round, the spy that captures it filters by the page's `operationName`, never by a substring of the body (`browser-techniques.md`, «Intercepting, replaying and substituting network»).
- **Print the whole error object**: a federated gateway wraps the real cause in `extensions.errors[].message` behind a generic «failed to fetch from subgraph». Read it as `e.extensions || {}` — one response can carry a subgraph error with extensions and a «cannot return null for non-nullable field» without them, and a helper that assumes them dies.
- **The same goes for `data`**: in a «mutate, then read» script, log the mutation's result BEFORE the read and read through `r.data && r.data.x` — a create-then-read race answers the read with an error and a null `data`, and an unguarded access throws away the record of the mutations the call already made.

### The client's cache

- **Apollo's normalised cache is a ready-made oracle for list totals.** `__APOLLO_CLIENT__.cache.extract().ROOT_QUERY` holds the server's answer under every variable set the page sent, so «how many rows under this filter» is compared with the reference without an interceptor. Pick the key by a regex on the field name and its variables, never «the last key»: keys go in order of FIRST appearance and a repeated variable set creates none, so after switching the page size back «the last key» reports the old limit. Cross-check with the rows on screen.
- **Where the global is not exposed** (the devtools hook is off in production builds), walk the React fiber tree down from the root container's node to the first object carrying `cache.extract` and `link` — a handful of nodes deep; its normalised cache (`Type:<id>` entries) answers «what the interface sees», which is not always what the API answers.

### What arrived and what is missing

- **The schema's size is a deploy diff** — counts of types by kind, the number of Query and Mutation fields and the list of new type names answer «what arrived since the last round» when the task carries no developer note. Filter out `__*` first: the introspection types (`__TypeKind`, `__DirectiveLocation`) are ENUMs and read as «dictionaries arrived». A dated schema snapshot in the knowledge base is re-taken after a deploy, never trusted. Behind a gateway that composes several services, the schema dates the gateway's re-composition, which can lag the service's rollout by hours — whether a service already runs the new code is read off an execution the round itself caused (`planning.md`, «Dating the build the round runs against»).
- **Missing fields are proven by one query that names them all** — the server rejects it with one «Cannot query field "X" on type "Y"» per absent name, plus a «did you mean» that points at a renamed one; a whole requirement's field list is checked in one call. Build it inside the response wrapper (`entity(id){entity{…}}` where the API wraps its answers): aimed at the wrapper type, every name fails for the wrong reason and the probe answers falsely.
- **Many reads or mutations go as aliases in one document** (`{a: x(id: …){…} b: …}`) — dozens of calls in one request instead of a loop that runs into the rate limit; mutations in batches of about twenty, with the session checked between batches — and only within the mutation budget the brief sanctioned: an alias batch changes how the calls travel, not how many are allowed.
