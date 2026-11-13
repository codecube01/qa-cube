# Playwriter

The default browser tool: a Chrome extension plus a CLI (https://playwriter.dev) that runs Playwright code against the user's own
Chrome — their sign-ins, cookies and extensions — from a shell, so it works in any harness. Read beside `../browser-techniques.md`
when the profile's `browser` is `playwriter`; this file holds what is true of this tool only. Measured on version 0.8.0.

## Install

```bash
npm i -g playwriter                              # the CLI; Node 18+
npx -y skills add https://playwriter.dev -g -y   # optional: Playwriter's own skill for the agent
```

plus the Playwriter extension from the Chrome Web Store — the user installs it and clicks its icon once, which connects the extension to
that browser (once per browser, not per tab or per session). `ffmpeg` on `PATH` only for screen recording.

## Preflight

`playwriter browser list` — the connected browsers with their keys (`install:Chrome:<id>` is the extension, `direct:9222` a debugging
port) and, in PROFILE, whether that Chrome profile is signed in. **`playwriter: command not found`** → the «Install» commands to the user;
do not launch the executor until `playwriter --version` answers. The profile's Browser section names which one holds the round's accounts.
**The list is empty, or the extension is not connected** («Waiting for extension to connect» that never ends) → tell the user exactly
that: open Chrome, click the Playwriter icon once; do not launch the executor until a second `browser list` shows the key. Then one
probe in a session of your own: open a tab, read its URL and title. The `playwriter --version` you read goes into the brief as part of
the build fingerprint — the CLI can change under a running round (below, «Known failures»).

## Connect and pick the tab

A session per actor: `playwriter session new --tab-group qa-<task> [--browser <key>]` prints its id; every later call is
`playwriter -s <id> -e '<code>'`. **One group per task, not per actor**: `<task>` is the tracker id in lower case (`qa-acme-412`), or
the session folder's name without its date — one string for every actor and round, no role or round suffix, given in the brief.
Sessions with one group name share one Chrome group (0.9.0) and keep their own `state`: actors stay apart by session id and the
marker below. Precedent: the manager and the executor each named their own group, spelling the task differently, and the user
hunted for one task's tabs across two groups. `session list` shows the other sessions on the machine — the user's other work
included — and they are never reset or deleted from a round. There is no default page: `state.page = await context.newPage()` opens a controlled tab in the
session's group with no click, and `context.pages()` lists every session's tabs, so a tab is kept in `state.page` or found by a marker
it carries (below) — an exact URL may match another actor's tab. The tabs a round opened stay open when it ends.

**Another actor's tab is reached through that actor's session, never by URL.** When the manager presses an irreversible step the
executor prepared, two actors' tabs may sit on the same URL, so the press goes through `-s <the executor's session id>` and its
`state.page`, in ONE call with its checks: the marker the executor planted in the page (`window.name`, naming the step — it survives a reload, below), the
identity oracle, and the interceptor's armed flag in `state` — any of them off, the call aborts before the click. The executor's
request therefore carries its session id, tab group, marker and the control's selector — or, for a step prepared as a function in
`state`, the line that calls it and prints its return value (below, «Page scripts and their budget»). Precedent: the manager's own tab stood on the
very registry URL where the executor had prepared three irreversible submits; all three went through its session and marker without a
single clarification.

## Page scripts and their budget

- The code in `-e` is ordinary async Node with Playwright's `page`, `context` and a per-session `state`; its output is what it
  `console.log`s — under a «Console output:» header, **every line prefixed `[log] `**, so a shell parser strips the prefix before
  `json.loads` (an unstripped one costs a `JSONDecodeError` and a repeat). Keep the code in single quotes (the shell leaves `$`,
  backticks and `\` alone), or in a file passed as `-e "$(cat f.js)"`.

  *And a function stored in `state` by an earlier call logs into that call, not the one that runs it* — its own `console.log` lines never
  reach a later call's output. A function prepared for another actor's call (the manager pressing a step the executor set up) returns its
  result, and the calling line prints the return value. Precedent: a prepared paid step logged its summary inside and was called with
  the return value printed — only the printed line came back; its dry run, called without printing, looked like nothing had happened.
- **One call has 10 s by default; `--timeout <ms>` raises it** (waits of 30, 120 and 300 s inside one call passed with the timeout set
  20 s above the wait). Size the timeout per call instead of splitting a wait.

  *And the harness's own shell call has a limit of its own*, which `--timeout` does not lift, so both limits are set above the wait (past
  the shell's limit the call goes to the background: `../shell-pitfalls.md`, «A wait is a bounded poll in the FOREGROUND»). Precedent: a
  six-minute wait with `--timeout` set went to the background at the shell's two-minute default, and the executor polled the output file
  by hand.
- **The code runs with the cwd of the relay process, not of your session** — the relay is started by whichever project called
  Playwriter first on the machine, so a relative path in `-e` (a helper spawned with `child_process`, a file read with `fs`) resolves
  inside another project. Every path in page-script code is absolute. Precedent: a login helper spawned `scripts/<helper>.py` by a
  relative path, the relay had been started from a neighbouring project, and the call failed after the login email had already been
  requested — one rate-limited link spent for nothing.
- **A call that timed out has still run** — the first navigation of a round opened its page while the call reported a timeout. Read the
  state back before repeating anything (`../browser-techniques.md`, «A call that timed out»).
- **`state` lives on the Node side and survives navigation and reload; `window.*` of the page dies on reload as usual.** So loggers built
  on `page.on(...)` or a CDP session persist across navigations, while an in-page `fetch` wrapper is reinstalled after each — install it
  with `page.addInitScript` to have it before the page's own code runs.

  *And they outlive the round*: a `page.on('response')` logger writing a file, a `setInterval` poller — removed at the round's end
  by the reference kept when it was attached (`state.onResp = …; page.on('response', state.onResp)` → `page.off('response',
  state.onResp)`, `clearInterval`), named in the result; the tabs stay open. Never `page.removeAllListeners(…)`: it strips
  Playwriter's own listeners on the page too, and the CLI's own skill forbids it — a brief that prescribes it is overruled by the
  skill mid-round. Precedent: a round's logger wrote into the session folder five more hours under the page's auto-refresh — 28 MB.
- **A secret captured only in the page reaches a file without being printed**: the round's code runs in Node, so
  `fs.writeFileSync(<secrets path>, await page.evaluate(...), {mode: 0o600})` moves it straight into the profile's secrets source (`fs` comes
  from `await import('node:fs')`). Where the harness refuses that write for its shape, the value stays in the page's `localStorage` under a
  named key, as with Claude in Chrome, and the result says which route it took.
- `page.goto` has Playwright's own 10 s timeout, and on some sites `load` — even `domcontentloaded` — never arrives while the page has in
  fact opened. Navigate with `{waitUntil: 'commit'}`, then wait for what the scenario needs (`waitForFunction(() => document.readyState
  !== 'loading')`, a selector).

## Screenshots

`await state.page.screenshot({path: '<absolute path>'})` writes a PNG there; `fullPage: true` for the whole page. The path is the session
folder's artifact path from `session.py`, never a guess. `screenshotWithAccessibilityLabels()` overlays labels on interactive elements —
for your own eyes, not for the result.
On high DPR with a wide viewport, `clip` at `scale: 'device'` comes back blank: shoot at `scale: 'css'`, then crop.

## Network

Playwright's own: `page.route(pattern, r => r.fulfill({...}))` substitutes a response to the page's `fetch` (on CLI 0.9.0 it DOES
reach `page.on('response')`, without server headers — mark your own); `page.on('request'|'response')` logs real traffic with bodies
on demand (`await r.text()`);
`getCDPSession({page})` + `Network.enable` gives the debugging protocol's events. Unlike an in-page wrapper these see every request the
page makes, XHR and workers included, and survive navigation — remove a route (`page.unroute`) right after the click it guards, as the
fail-closed rule in `../browser-techniques.md` asks. A route comes off by its pattern (`page.unroute(p)`) or by the same handler object
kept in a variable; a fresh function removes nothing, the stub keeps answering.

- **A string `pattern` is a glob over the WHOLE URL, query included** — `**/path` misses `…/path?x=1`; match with a function on
  `new URL(u).pathname`. Precedent: a «pass one, abort the rest» route on a GET with a query hit zero times on its dry run.
- **A multipart body is not in the request log**: `request.postData()` comes back empty for a `FormData` that carries a file. Read it with a
  read-only in-page `fetch` wrapper that clones the request (`req.clone().formData()`) and leaves the call itself untouched — **installed with
  `page.addInitScript` and a reload, before the bundle runs** (the `state` entry above): a wrapper over a global the client captured at init
  logs nothing while the upload goes through (`../manual-brief.md`, «armed in the SAME call»). Where the page cannot be reloaded, «how
  many files went out» is proven by the server's own trace of that request (the log line by its trace id), not by an empty wrapper.
  Precedent: a «one file only» check set its spies on the loaded form, caught no request, and the count came from the backend's
  `attachments_count` in the upload's trace.
- **WebSocket frames are logged from Node — `page.on('websocket')` with the socket's `framesent` / `framereceived` / `close`** — not by
  the in-page prototype patch of `../browser-techniques.md`, which dies with every navigation. The Node-side log survives SPA transitions
  and reloads and shows a subscription's whole life — `subscribe`, `complete`, the socket closing — which is what tells «this screen
  never subscribed» from «no event came». It sees sockets opened after the listener is attached: attach it, then navigate into the
  screen under observation. Precedent: a «the status does not refresh» retest proved the detail screen held no subscription at all —
  the log showed the list screen's subscription completed and its socket closed at the transition, and no socket afterwards.
- **`route.fetch()` from a route handler crashed the relay in extension mode** and dropped every session on the machine; observation
  1/1, held as the rule until a round refutes it. Substitute with `route.fulfill` from a body you already hold, or with an in-page
  `fetch` wrapper. `route.continue()` on every GET for an hour did not crash it.

## Known failures

- **No output filter**: a query string, a cookie-shaped string and 6000 characters print whole. The rule «Responses carry access»
  in `../browser-techniques.md` is the only guard.

  *And the output IS cut, at about 10 000 characters (0.9.0)*, silently: a population dump is written to a file from the page script
  and only its summary printed, or the tail is lost and the read repeated.
- A `goto` that waits for `load` times out on a page that opened (above) — the timeout is not a navigation failure.
- **`ControlOrMeta+a` does not select a field's text on macOS in extension mode** — the typed value is appended, not replacing
  (`3` typed over `2` reads `32`). Replace a value with `locator.fill(…)` and read the field back before acting on it.
- **Every session shares the one browser, so a tab can be closed from outside** — by another session's code, an extension or a person —
  and only on some pages. The sign is a `close` event you did not cause; prove it with a control URL in the same tab (another page of
  the site stays open). Other sessions are not touched; read the page from INSIDE it instead: `page.addInitScript` takes the reading at
  `DOMContentLoaded` and hands it to Node through `page.exposeBinding`, and the network logger in `state` outlives the tab. Say in the
  result which readings were taken that way. Precedent: a live round's tabs on a login page closed 0.4–0.9 s after every load while the
  site's other pages stayed open; reading from inside the page closed every requirement anyway.

  *And where the page that closes is the one an ENTRY goes through* (a sign-in form the login helper opens to send its requests from) —
  the entry does not need that page: the auth requests go from a same-origin page that does not boot the app (`../browser-techniques.md`,
  «A session is observed without the application»; for an entry, any GET that answers JSON serves — the logout endpoint
  too, since there is no session to lose yet, never on a live one), and the one-time link opens
  in a fresh tab. Every attempt through the closing page may still have spent a rate-limited link before it died, so count them against
  the budget. Precedent: three logins in one browser profile died with «execution context destroyed» on the sign-in page, each possibly
  spending a link; the same helper, moved to the logout endpoint's JSON page, entered on the first try.
- **A CLI of another version than the running relay restarts the relay and drops EVERY session on the machine.** The call prints
  `CDP relay server version mismatch (server: X, client: Y), restarting...`, and from then on every session id — the manager's, other
  projects' — answers `Session <id> not found`; the tabs survive in Chrome. A global upgrade of the CLI by anyone mid-round is enough. So
  the version read at preflight is compared on that message, the restart is dated in the result as an incident of the tool, and nobody
  resets or deletes other sessions to «repair» it — they are already gone, and their owners re-create them. The executor opens a new
  session and finds its own tabs by a marker it planted in the page, never by position or title: `window.name`, which survives a reload
  of that tab, while a `window.__<round>` value dies with any reload a failing call made. Precedent: an
  executor's first call after a mid-round upgrade restarted the relay, dropped the manager's session with the rest, and the round went on
  only because its tabs carried such a marker.

  *And the same loss arrives without the version message*: a long call returns `Target page, context or browser has been closed` minutes
  late and every page handle in `state` is dead, while `context.pages()` still lists the tabs. That is the channel failing, not the tabs
  closing — re-bind `state.page` by the `window.name` marker and read the state the page reached; what fell inside the gap is «observed
  after the event», never re-played as if it were live. Precedent: an observation call hung for 27 minutes behind a degraded proxy, the
  handles died, all three marked tabs were alive on their final pages, and the expiry screen it was watching could only be dated afterwards.
- **Files cross the extension badly both ways**: `setInputFiles(<path>)` hangs to the timeout — pass `{name, mimeType, buffer}`,
  clearing a selected file through the form first where it hides the input; `download.saveAs()` fails (`ENOENT`) — take
  the file from the browser's download folder by name and time, and hash it there.
- Controlled tabs show Chrome's automation banner; a scenario about the page's own layout at the top edge accounts for it.
- `snapshot()` returns an accessibility snapshot and, on later calls, diffs against the previous one — a diff that looks empty is «nothing
  changed», not «nothing there».
