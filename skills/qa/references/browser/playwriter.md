# Playwriter

The default browser tool: a Chrome extension plus a CLI (https://playwriter.dev) that runs Playwright code against the user's own
Chrome — their sign-ins, cookies and extensions — from a shell, in any harness. Read beside `../browser-techniques.md`
when the profile's `browser` is `playwriter`; this file holds what is true of this tool only. Measured on version 0.8.0.

## Install

```bash
npm i -g playwriter                              # the CLI; Node 18+
npx -y skills add https://playwriter.dev -g -y   # optional: Playwriter's own skill for the agent
```

plus the Playwriter extension from the Chrome Web Store, which the user installs and connects by clicking its icon once per browser.
`ffmpeg` on `PATH` only for screen recording.

## Preflight

`playwriter browser list` — the connected browsers with their keys (`install:Chrome:<id>` is the extension, `direct:9222` a debugging
port) and, in PROFILE, whether that Chrome profile is signed in. **`playwriter: command not found`** → the «Install» commands to the user;
do not launch the executor until `playwriter --version` answers. The profile's Browser section names which one holds the round's accounts.
**The list is empty, or the extension is not connected** («Waiting for extension to connect» that never ends) → ask the user to open
Chrome and click the Playwriter icon once; launch the executor only once a second `browser list` shows the key (mid-run:
below). Then one probe in a session of your own: open a tab, read its URL and title. The `playwriter --version` you read goes into the brief as part of
the build fingerprint — the CLI can change under a running round («Known failures»). An `is outdated (extension requires X)` notice
goes into the brief once, as a decision — the CLI is upgraded between rounds, with the user's go-ahead; unbriefed, twelve executors of
one session each reported it.

## Connect and pick the tab

A session per actor: `playwriter session new --tab-group qa-<task> [--browser <key>]` prints its id, then tips — take it by
`grep -oE '^(Session )?[0-9]+' | grep -oE '[0-9]+'` (0.11.0: `Session <N> created`), never `tail` (a tip line taken for it once cost a second session); every later call is
`playwriter -s <id> -e '<code>'`. **One group per task, not per actor**: `<task>` is the tracker id in lower case (`qa-acme-412`), or
the session folder's name without its date — one string for every actor and round, given in the brief.
Sessions with one group name share one Chrome group (0.9.0) and keep their own `state`: actors stay apart by session id and the
marker below. Precedent: two actors spelled the task two ways, and the user hunted one task's tabs across two groups. `session list` shows the other sessions on the machine — the user's other work
included — and they are never reset or deleted from a round. There is no default page: `state.page = await context.newPage()` opens a controlled tab in the
session's group with no click, and `context.pages()` lists every session's tabs, so a tab is kept in `state.page` or found by a marker
it carries (below) — an exact URL may match another actor's tab. The tabs a round opened stay open when it ends.

**Another actor's tab is reached through that actor's session, never by URL.** When the manager presses an irreversible step the
executor prepared, two actors' tabs may sit on the same URL, so the press goes through `-s <the executor's session id>` and its
`state.page`, in ONE call with its checks: the marker the executor planted in the page (`window.name`, naming the step — it survives a reload, below), the
identity oracle, and the interceptor's armed flag in `state` — any of them off, the call aborts before the click. The executor's
request therefore carries its session id, tab group, marker and the control's selector — or, for a step prepared as a function in
`state`, the line that calls it and prints its return value (below, «Page scripts and their budget»); for a step behind a dialog that
function opens, fills and checks it inside the call — a modal left open in a background tab can close by itself. Precedent: three
irreversible submits prepared on the URL of the manager's own tab all went through the executor's session and marker with no
clarification.

## Page scripts and their budget

- The code in `-e` is ordinary async Node with Playwright's `page`, `context` and a per-session `state`; its output is what it
  `console.log`s — under a «Console output:» header, **every line prefixed `[log] `**, so a shell parser strips the prefix before
  `json.loads`. Keep the code in single quotes (the shell leaves `$`,
  backticks and `\` alone), or in a file passed as `-e "$(cat f.js)"`.

  *And a function stored in `state` by an earlier call logs into that call, not the one that runs it* — its own `console.log` lines never
  reach a later call's output. A function prepared for another actor's call (the manager pressing a step the executor set up) returns its
  result, and the calling line prints the return value. Precedent: a prepared step's dry run, called without printing, looked like
  nothing had happened.
- **One call has 10 s by default; `--timeout <ms>` raises it** (waits up to 300 s passed in one call with the timeout
  20 s above the wait). Size the timeout per call instead of splitting a wait; a call that timed out has still run
  (`../browser-techniques.md`, «A call that timed out»).

  *And an action waits for an actionable target for the call's whole budget* — a disabled button, an SVG hover in a badge, a role
  name that differs, coordinates from before a layout shift: an action on a control you are not sure of carries `{timeout: 3000}`.
  Precedent: five calls in four rounds timed out on clicks that could never land.

  *And the harness's own shell call has a limit of its own*, which `--timeout` does not lift, so both are set above the wait; past the
  harness's ceiling no shell `timeout` holds the call, and the wait becomes polls (`../shell-pitfalls.md`, «A wait is a bounded poll in
  the FOREGROUND», its last rider). Precedent: a six-minute wait with `--timeout` set went to the background at the shell's two-minute
  default.
- **The code runs with the cwd of the relay process, not of your session** — started by whichever project called
  Playwriter first, so a relative path in `-e` (a helper spawned with `child_process`, a file read with `fs`) resolves
  inside another project. Every path in page-script code is absolute. Precedent: a helper spawned by a relative path resolved in a
  neighbouring project and failed after spending a rate-limited login link.
- **`state` lives on the Node side and survives navigation and reload; `window.*` of the page dies on reload as usual.** So `page.on(...)`
  loggers and CDP sessions persist across navigations, while an in-page `fetch` wrapper is reinstalled after each — by
  `page.addInitScript`, before the page's own code runs.

  *And they outlive the round*: a `page.on('response')` logger writing a file, a `setInterval` poller — removed at the round's end
  by the reference kept when it was attached (`state.onResp = …; page.on('response', state.onResp)` → `page.off('response',
  state.onResp)`, `clearInterval`), named in the result; the tabs stay open. Never `page.removeAllListeners(…)`: it strips
  Playwriter's own listeners on the page too — the CLI's own skill forbids it, whatever a brief says. Precedent: a logger kept writing five hours past the round — 28 MB.
- **A secret captured only in the page reaches a file without being printed**: `fs.writeFileSync(<secrets path>, await
  page.evaluate(...), {mode: 0o600})` from the round's Node code (`fs` from `await import('node:fs')`) moves it into the profile's
  secrets source. Where the harness refuses that write for its shape, it stays in the page's `localStorage` under a named key, and the
  result says which route it took.
- `page.goto` has Playwright's own 10 s timeout, and on some sites `load` — even `domcontentloaded` — never arrives while the page has in
  fact opened. Navigate with `{waitUntil: 'commit'}`, then wait for what the scenario needs (a selector, `readyState !== 'loading'`).

## Screenshots

`await state.page.screenshot({path: '<absolute path>'})` writes a PNG there; `fullPage: true` for the whole page. The path is the session
folder's artifact path from `session.py`, never a guess. `screenshotWithAccessibilityLabels()` overlays labels —
for your own eyes, not for the result.
On high DPR with a wide viewport, `clip` at `scale: 'device'` comes back blank: shoot at `scale: 'css'`, then crop.

## Network

Playwright's own: `page.route(pattern, r => r.fulfill({...}))` substitutes a response to the page's `fetch` (on CLI 0.9.0 it DOES
reach `page.on('response')`, without server headers — mark your own); `page.on('request'|'response')` logs real traffic with bodies
on demand (`await r.text()`);
`getCDPSession({page})` + `Network.enable` gives the debugging protocol's events. Unlike an in-page wrapper these see every request the
page makes, XHR and workers included, and survive navigation — a route goes on a loaded page and comes off (`page.unroute`) right after
the click it guards, before any `goto`/reload, as the fail-closed rule in `../browser-techniques.md` asks. A route comes off by its pattern (`page.unroute(p)`) or by the same
handler object; a predicate pattern and a handler match by reference — a fresh function removes nothing, the stub stays.

- **A route armed across a `goto` or reload can stall the page's own load, and while one is armed the HTTP cache is off**: a module
  request sits paused, the root stays empty with no `pageerror`, each reload re-downloads the bundle. A tab that only reads screens
  carries no route — its guard is an in-page wrapper by `page.addInitScript`. Precedent: executors of six rounds lost about half an hour each to an empty root, masked by a slow channel.
- **A string `pattern` is a glob over the WHOLE URL, query included** — `**/path` misses `…/path?x=1`; match with a function on
  `new URL(u).pathname`. Precedent: a «pass one, abort the rest» route on a GET with a query hit zero times on its dry run.
- **A multipart body is not in the request log**: `request.postData()` comes back empty for a `FormData` that carries a file. Read it with a
  read-only in-page `fetch` wrapper that clones the request (`req.clone().formData()`) and leaves the call itself untouched — **installed with
  `page.addInitScript` and a reload, before the bundle runs**: a wrapper over a global the client captured at init
  logs nothing while the upload goes through (`../manual-brief.md`, «armed in the SAME call»). Where the page cannot be reloaded, «how
  many files went out» is proven by the server's trace of that request, not by an empty wrapper. Precedent: spies on the loaded form
  caught no upload; the count came from the backend's trace.
- **WebSocket frames are logged from Node — `page.on('websocket')` with the socket's `framesent` / `framereceived` / `close`** — not by
  the in-page prototype patch of `../browser-techniques.md`, which dies with every navigation. It survives transitions and reloads and
  shows a subscription's whole life (`subscribe`, `complete`, the socket closing), which tells «this screen never subscribed» from «no
  event came»; it sees only sockets opened after it is attached — attach, then navigate into the screen. Precedent: it proved a «status does
  not refresh» screen held no subscription at all.
- **`route.fetch()` from a route handler crashed the relay in extension mode** and dropped every session on the machine (1/1). Substitute with `route.fulfill` from a body you already hold, or with an in-page
  `fetch` wrapper. `route.continue()` for an hour did not.

## Known failures

- **No output filter**: a query string, a cookie-shaped string and 6000 characters print whole. The rule «Responses carry access»
  in `../browser-techniques.md` is the only guard.

  *And the output IS cut, at about 10 000 characters (0.9.0)*, silently: a population dump is written to a file from the page script
  and only its summary printed, or the tail is lost and the read repeated.
- **`context.cookies()` fails in extension mode (0.9.0)** (`No tab found`) — read per page: `getCDPSession({page})` +
  `Network.getCookies({urls})`, into a file, never printed.
- **`page.setViewportSize` sticks (0.9.0)**: later resizes ignored, frames cropped — a narrow window
  goes over CDP (`Emulation.setDeviceMetricsOverride` / `clearDeviceMetricsOverride`), frames by `Page.captureScreenshot`.
- **`ControlOrMeta+a` does not select a field's text on macOS in extension mode** — the typed value is appended, not replacing.
  Replace a value with `locator.fill(…)` and read the field back before acting on it.
- **Every session shares the one browser, so a tab can be closed from outside** — by another session's code, an extension or a person —
  and only on some pages. The sign is a `close` event you did not cause; prove it with a control URL in the same tab (another page of
  the site stays open). Other sessions are not touched; the page is read from INSIDE: `page.addInitScript` takes the reading at
  `DOMContentLoaded` and hands it to Node by `page.exposeBinding`, the network logger in `state` outliving the tab — named so in the
  result. Precedent: login-page tabs closed 0.4–0.9 s after every load; readings from inside
  closed every requirement.

  *And where the closing page is the one an ENTRY goes through* (a sign-in form the login helper sends from), the auth requests go
  from a same-origin page that does not boot the app (`../browser-techniques.md`, «A session is observed without the application» —
  for an entry any JSON GET serves, the logout endpoint too while there is no session to lose) and the one-time link opens in a fresh
  tab; each attempt through the closing page may have spent a rate-limited link. Precedent: three logins died on the sign-in page; moved to the logout endpoint's JSON page, the helper entered at once.
- **A CLI of another version than the running relay restarts the relay and drops EVERY session on the machine.** The call prints
  `CDP relay server version mismatch (server: X, client: Y), restarting...`, then every session id answers `Session <id> not
  found`; the tabs survive in Chrome. The mismatch is against the RELAY, not the extension: before predicting
  a drop, read the running relay's version off its process (one started through `npx` may be newer) — a CLI brought to that version
  restarts nothing. A restart is dated in the result as the tool's incident, and nobody resets or deletes other sessions to «repair»
  it — they are gone already. The executor opens a new
  session and finds its tabs by a marker planted in the page, never by position or title: `window.name` survives a reload, a
  `window.__<round>` value does not. Precedent: a mid-round upgrade dropped every session; the round went on by such a marker.

  *And the same loss arrives without the version message*: a long call returns `Target page, context or browser has been closed` minutes
  late and every page handle in `state` is dead, while `context.pages()` still lists the tabs. That is the channel failing, not the tabs
  closing — re-bind `state.page` by the `window.name` marker and read the state the page reached; its guards (a route, a `page.on`
  listener) died with the old handle — re-armed, and proven by one blocked probe before the next click; what fell inside the gap is «observed
  after the event», never re-played as if it were live. Precedent: an observation call hung 27 minutes behind a degraded proxy; its
  handles died, all three marked tabs lived on their final pages.

  *And where the extension drops mid-run* (`browser list` empty) past the brief's «N attempts»: the user clicks its icon, then the same
  re-bind by the marker — a handle may show `about:blank`.
- **Files cross the extension badly both ways**: `setInputFiles(<path>)` hangs to the timeout — pass `{name, mimeType, buffer}`,
  clearing a selected file through the form first where it hides the input; `download.saveAs()` fails (`ENOENT`) — take
  the file from the browser's download folder by name and time, and hash it there.
- Controlled tabs show Chrome's automation banner; a scenario about the page's own layout at the top edge accounts for it.
- `snapshot()` returns an accessibility snapshot and, on later calls, diffs against the previous one — a diff that looks empty is «nothing
  changed», not «nothing there».
