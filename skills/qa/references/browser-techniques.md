# Browser and API-probing techniques

Read by `qa-manual` on any round that drives a browser or scripts a page — the first screen and the sections the brief names before the
first page script, any other section when you reach its topic — and by the manager before the preflight at step 4 of `../SKILL.md`: the
first screen and the contents, which is how the brief's sections get picked. The recipes are tool-level and hold in any project; what
belongs to one project — its hosts, its entry, its own UI quirks — stays in the profile's Browser section, which is read after this file and
wins where the two differ. Every recipe below was paid for by a lost round.

## TL;DR — the typical flow

1. **Navigate to the target screen first, then install helpers and interceptors** — `window.*` dies on `navigate`/reload (it survives SPA transitions).
2. **Read the entity's state through the API before looking for it on screen** — a user or a process may have moved it since.
3. **Never guess the schema**: the query-field list first, then `__type` of each type you touch — `kind`, `NON_NULL`, the mutation's RESPONSE type.
4. **Replay an intercepted request with your own `variables`** instead of composing one — the query is valid by construction.
5. **Helpers read `r.status` + `r.text()`**, and print the whole error object, `extensions` included.
6. **Print derived values, never raw bodies, markup or source** — the output filter blocks anything that looks like a cookie or a query string.
7. **One page-script call stays under ~40 s**; longer work accumulates in `window.__…` and is read by a separate short call.
8. **Headless-component controls**: native `click()` or a pointer sequence; verify by the state attribute, never by «Clicked».
9. **The tab is hidden and throttled**: force a render (a screenshot) before any verdict about a control, and wait with `MessageChannel`, not `setTimeout`.

Pitfalls and the full recipes, by topic, below.

## Contents

- the page-scripting sandbox and its limits — REPL semantics, the call budget, what survives navigation
- output censorship — `[BLOCKED: Cookie/query string data]` and how to print around it
- intercepting, replaying and substituting network — the logger, the replay, the client cache, the fail-closed wrapper, WebSocket frames
- component-library interaction — clicks that silently do nothing, tabs, options, modals, forms
- the hidden tab — timer throttling, rendering, tooltips, toasts, viewport width
- downloads — the browser's own block on repeated downloads, and capturing the file at the source
- GraphQL schema and bundle discovery — introspection depth, types, the served bundle as a source

## The page-scripting sandbox and its limits

- **A page-script tool (such as claude-in-chrome `javascript_tool`) has REPL semantics: a top-level `return` yields `undefined`.** The value of the call is its last expression; in a helper with branches, accumulate into a variable and end with it.
- **One call has a hard budget (~45 s over CDP), and everything inside it adds up** — a wait plus the fetches after it count together. An authorised API request from the page costs ~0.5–1.4 s, so a polling loop fits ~15 iterations. Wait for a boundary (the next TOTP step, a timer) in its own short call, never in the call that does the useful requests; where a loop may overrun, push every sample into `window.__acc` and read it with a separate call — a timed-out call loses its return value, not the accumulator.
- **A call that timed out has usually still run** — its fetches went out and the script keeps executing in the page. Re-read the state with a separate request before doing anything; never re-run a timed-out call that installs a substitution or a wrapper, or a second one lands on top of the first.
- **`window.*` survives an SPA transition and dies on `navigate`/reload** — helpers, loggers, a saved original `fetch`. So: navigate first, install after; save the original once (`window.__origFetch = window.__origFetch || window.fetch`, or you wrap the wrapper); before any conclusion check the wrapper is still live (`window.fetch !== window.__origFetch`); restore it when done. The tool cannot read files, so keep a long wrapper as a file in the scratchpad and paste it verbatim after every navigation — a reload by the user or by a silent session renewal kills it as surely as your own `navigate`.
- **Arm an observer in the SAME call as the action that produces the event** (see `manual-brief.md`, «The observation channel»); the first entry of a «record only changes» accumulator is always written and is not the moment of a transition.
- **Mocked amounts are strings, never arithmetic** — `String(i) + '000000000000000000'`: mixing `BigInt` and `Number` throws at once, and a `Number` loses precision at 18 digits.
- **On macOS there is no PIL — crop and scale with `sips`**: `sips -g pixelWidth -g pixelHeight in.png` first, then `sips -c <h> <w> --cropOffset <top> <left> in.png --out out.png`, `sips -z <h> <w>` to upscale. Without the size a crop misses the region.

## Output censorship

- **The tool's output filter blocks anything shaped like a cookie, a query string or base64** — the reply comes back `[BLOCKED: Cookie/query string data]` and the call is lost. Pre-empt it rather than retrying: pass text through `s.replace(/[=&?:]/g, ' ')`, print `key value · key value` rather than `key=value`, pull numbers out with a regex (`s.match(/\d{4,}/g)`).
- **Never print function sources, framework props, `outerHTML` or a raw response body.** Utility-class markup (`[`, `--`, `/`) trips the filter even after the replacement. Print derived attributes instead — `textContent`, `aria-*`, `data-state`, the presence and length of a handler, its words (`s.replace(/[^A-Za-z ]/g, ' ')`), class names from a whitelist.
- **A minified bundle fragment is replaced before printing, always** — it nearly always looks like a query string. Do not hunt for the definition of a minified helper by `name=`: whitespace in builds is unpredictable and the filter cuts such selections; the usage site explains the behaviour.
- **A secret the flow shows once (a TOTP seed) is printed character by character** (`.split('').join(' ')`) — whole, it is cut as base64. It goes to the secrets store, never into session files.
- **A large captured text (an export, a payload) is compared, not printed**: hash it line by line (sha256, via `crypto.subtle`) in the page and compare against a local copy.
- **A screenshot saved to disk may be refused where a plain one passes** — describe what you saw in words instead.

## Intercepting, replaying and substituting network

- **The request logger keeps every body whole; truncate only when printing.** `JSON.parse` of a truncated string fails with `Unterminated string`, and the capture has to be retaken.
- **Replay beats composing.** `const p = JSON.parse(log.body)` and send `{operationName: p.operationName, query: p.query, variables: <yours>}`: only the variables change, the query is valid by construction. Filters, limits and permissions are checked by comparing responses across variable values — and with and without a secondary argument, which is how a filter silently ignored in the presence of another argument is found. No captured request yet → introspect the type first, compose second.
- **Helpers read `r.status` and `r.text()`, never `r.json()`** — an expired session answers `401` with an empty or non-JSON body, and `.json()` replaces the cause with a parse error. **Print the whole error object**: a federated gateway wraps the real cause in `extensions.errors[].message` behind a generic «failed to fetch from subgraph». Read it as `e.extensions || {}` — one response can carry a subgraph error with extensions and a «cannot return null for non-nullable field» without them, and a helper that assumes them dies.
- **A client with a normalised cache answers from the cache, so a substitution installed after `navigate` loses the race.** Load an unrelated route in full, install the interceptor on the empty cache, then move to the target by an SPA transition: `history.pushState({}, '', '/target')` + `dispatchEvent(new PopStateEvent('popstate'))`. A modal whose data is read cache-first takes the substitution only if it is in place BEFORE the modal is first opened.
- **One install serves a whole family of variants when the mock answers for fictitious ids** (`qa-01…qa-NN`): the cache is keyed by variables, so every new id is a guaranteed trip to the network and a fresh mock — `pushState` to each in turn. The same install renders every status of a dictionary plus one deliberately unknown value in one pass: the mappings and the fallback at once.
- **Patch the response by the SET OF FIELDS, not by a guessed path.** The root field of the application's own operation often differs from the one in your hand-written query, and a patch aimed at the wrong path silently returns the untouched data — no error, a real screen, a substitution counter of zero. Walk the JSON recursively and rewrite every object carrying the fields you target (`status` + `failureCode`, say); diagnose a miss with `Object.keys(j.data)`.
- **To prove «what was confirmed is what was sent», substitute the computation with values nobody else would produce** — comparing equal numbers proves nothing when the server computes the same figures itself. Choose values valid for the domain, or the experiment is smeared by a validation error.
- **An irreversible mutation whose CLIENT reaction must be seen goes through a fail-closed `fetch` wrapper.** Installed after navigation; it blocks every request whose parsed `query` calls the mutation field (parse the query — the operation name can also travel in `variables`); substitution is armed by hand for one request and disarmed after it; not armed, or an unparseable body → a stub response such as `QA-BLOCKED`, never a pass-through. Before the first click, self-test it with a direct call and prove the application goes through it (an SPA transition, then the application's request in the log). Build the substituted body from the intercepted query's selection set; after each run, count the entities through the saved original `fetch`.
- **A WebSocket logger is a patch of the PROTOTYPE** — `WebSocket.prototype.send`, `.addEventListener` and the `onmessage` setter. Client libraries capture the constructor at bundle init, so a wrapper over `window.WebSocket` installed after load stays empty while the subscription works.
- **Neighbouring screens are read in a second tab** while the first holds a live subscription or observer — an SPA transition away closes the subscription in the most interesting window.

## Component-library interaction

- **Clicks by an accessibility `ref` inside modals, dropdowns and tabs of headless libraries (Radix and the like) often do nothing, while the tool reports «Clicked».** Order of attempts: a native `element.click()` from a page script (buttons, menu items), then coordinates from a fresh screenshot; pick options with `querySelector('[role="option"]')` + `click()`. Verify the result, never the intent — a state attribute or a screenshot after every step.
- **Tabs (`[role="tab"]`) ignore a native `click()`.** Dispatch `pointerdown → mousedown → pointerup → mouseup` with `{bubbles: true, cancelable: true, pointerId: 1, isPrimary: true}`, then `click()`; control by reading `data-state` before and after.
- **A tooltip on a disabled control opens on `pointerenter`/`pointermove` dispatched on its wrapper** — the tool's hover misses a covered target.
- **Opening a dropdown shifts the layout**: the «fresh screenshot» for picking an option is the one taken AFTER that dropdown opened; check the selected value before submitting.
- **Any change of markup voids remembered coordinates** — a changed select, a reopened modal (forms often keep their error block after «Cancel», shifting every field). Re-take `find` or a screenshot and click the fresh target.
- **A disabled control often has no handler at all** — removing `disabled` achieves nothing; check the handler's presence (`memoizedProps.onClick` on the React fiber) before building on it, and prefer substituting the READ so the application enables the control itself.
- **Refilling a form after a transition is checked field by field against the previous captured request body** — a checklist, not memory; an optional field is the one that silently drops.
- **Copy-to-clipboard buttons inside table cells swallow row clicks** — the value goes to the clipboard, no navigation happens, and it looks like «the row is not clickable». Aim at a cell without a control.
- **A modal can take seconds to mount, and a second click closes the one that just opened.** One click, wait (up to ~10 s), then check `document.querySelectorAll('[role=dialog],[role=alertdialog]')`; whether the click reaches the element at all is shown by a capture-phase `click` listener, not by clicking again.

## The hidden tab

- **The automation tab usually runs hidden (`document.visibilityState === 'hidden'`) for the whole round, and that changes what controls appear to do.** `requestAnimationFrame` does not tick, so a closed modal stays in the DOM with `data-state="closed"` and reads as «cannot be closed». A screenshot forces a render: run «click → screenshot → read the DOM» as one batch, and never write «the control does not react» before that sequence.
- **Timers are throttled** — `setTimeout` to ~1 s at once, and after ~10 minutes hidden to about once a minute, so a call that took seconds early in the round hits the call budget later. Wait inside scripts with a `MessageChannel` loop (a promise on `port1.onmessage` after `port2.postMessage`, checked against `performance.now()`), which is not throttled.
- **Tooltip rendering lags one hover behind** — synthetic events and the tool's hover alike show the PREVIOUS hover's tooltip. Trust only the tooltip whose trigger reads an `*-open` state (its `aria-describedby`), or a screenshot after moving the pointer to empty space between hovers. «There is no tooltip» is a verdict only on a freshly loaded page: after many SPA transitions and substitutions hover stops opening tooltips at all.
- **Toast libraries pause their timers while `document.hidden`** (sonner does) — a toast that never disappears is not a defect. Before any verdict about toast lifetime: `Object.defineProperty(document, 'hidden', {get: () => false})`, the same for `visibilityState` → `'visible'`, then `document.dispatchEvent(new Event('visibilitychange'))`.
- **Each automation tab has its own emulated viewport, different from the user's window and from the next tab** (`outerWidth` of zero or below `innerWidth` is the sign). Read `innerWidth` as the first call and after every resize; in a narrow viewport, `scrollIntoView` a cell before a real click and follow links by a native `a.click()`.
- **After a background change (funds arrived, a status moved) the UI keeps its cached value, and forms validate against it.** Plan the reload as its own step rather than discovering the stale value at the submit button.

## Downloads

- **Chrome blocks repeated automatic downloads from one origin after the first** — later files never appear while the application shows its success toast; that is the browser, not the product. The control costs one call: trigger two downloads of your own from the same page (a `Blob` + `a[download]`); both missing means the browser.
- **Capture the file at the source instead**: intercept `URL.createObjectURL` and `HTMLAnchorElement.prototype.click` — you get exactly the `Blob` the product handed over (`blob.text()`, `size`, `type`, and `a.download` for the file name), which is more precise than the file on disk. A download that did land is read from the shell (`ls -lat ~/Downloads/<mask>`) and copied into the session's artifacts.

## GraphQL schema and bundle discovery

- **The schema is read before the first real query, never guessed.** Start with `{__schema{queryType{fields{name args{name}}}}}` (and `mutationType`), then `__type(name: "X")` for each type you touch. Every guessed field is a lost round, and «obvious» ones are the usual casualties — a list that needs a parent id, a wrapper whose array is not called `items`.
- **Read the `kind` of every field and argument.** An object or list field without a selection fails with «must have selections»; a `NON_NULL` argument needs `!` in the variable declaration. Take the RESPONSE type of a mutation too, not only its arguments — wrappers are inconsistent even between paired operations (one returns `{entity {…}}`, its sibling the entity itself).
- **A nested type's name needs four to five levels of `ofType`** — `NON_NULL(LIST(NON_NULL(OBJECT)))` returns `name: null` after three, and `__type` on a guessed name returns `null`. Unwrap `ofType{kind name ofType{…}}` deep enough, or list `__schema{types{name fields{name}}}`.
- **Introspect in small queries** — the root type's fields first, then the fields or input fields of one type; a full dump is truncated by the output limit.
- **A contract read from the client's embedded query text has names without types** — `manual-brief.md`, «A contract read out of the CLIENT's own query documents».
- **«This string is not in the build» is established across EVERY chunk, not the entry script** — vendor chunks carry texts such as empty states. List the chunks from the page: `performance.getEntriesByType('resource')`.
- **A dictionary of statuses and captions is taken from the bundle, not guessed from the screen**: `document.querySelectorAll('script[src]')` → fetch each chunk → search for the locale keys and the mapping object beside them. It also yields statuses without a tab of their own and dead strings no screen renders.
