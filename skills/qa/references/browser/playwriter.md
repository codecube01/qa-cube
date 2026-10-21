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
probe in a session of your own: open a tab, read its URL and title.

## Connect and pick the tab

A session per actor: `playwriter session new --tab-group qa-<task>-<role> [--browser <key>]` prints its id; every later call is
`playwriter -s <id> -e '<code>'`. `session list` shows the other sessions on the machine — the user's other work included — and they are
never reset or deleted from a round. There is no default page: `state.page = await context.newPage()` opens a controlled tab in the
session's group with no click, and `context.pages()` lists every session's tabs, so a tab is found by its exact URL or kept in
`state.page`. The tabs a round opened stay open when it ends.

## Page scripts and their budget

- The code in `-e` is ordinary async Node with Playwright's `page`, `context` and a per-session `state`; its output is what it
  `console.log`s. Keep the code in single quotes (the shell leaves `$`, backticks and `\` alone), or in a file passed as `-e "$(cat f.js)"`.
- **One call has 10 s by default; `--timeout <ms>` raises it** (waits of 30, 120 and 300 s inside one call passed with the timeout set
  20 s above the wait). Size the timeout per call instead of splitting a wait.
- **A call that timed out has still run** — the first navigation of a round opened its page while the call reported a timeout. Read the
  state back before repeating anything (`../browser-techniques.md`, «A call that timed out»).
- **`state` lives on the Node side and survives navigation and reload; `window.*` of the page dies on reload as usual.** So loggers built
  on `page.on(...)` or a CDP session persist across navigations, while an in-page `fetch` wrapper is reinstalled after each — install it
  with `page.addInitScript` to have it before the page's own code runs.
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

## Network

Playwright's own: `page.route(pattern, r => r.fulfill({...}))` substitutes a response to the page's `fetch` (a fulfilled response does
not appear in `page.on('response')`); `page.on('request'|'response')` logs real traffic with bodies on demand (`await r.text()`);
`getCDPSession({page})` + `Network.enable` gives the debugging protocol's events. Unlike an in-page wrapper these see every request the
page makes, XHR and workers included, and survive navigation — remove a route (`page.unroute`) right after the click it guards, as the
fail-closed rule in `../browser-techniques.md` asks.

## Known failures

- **No output filter and no length cut**: a query string, a cookie-shaped string and 6000 characters print whole. Nothing stops access
  from being printed, so the rule «Responses carry access» in `../browser-techniques.md` is the only guard — keep it.
- A `goto` that waits for `load` times out on a page that opened (above) — the timeout is not a navigation failure.
- **Every session shares the one browser, so a tab can be closed from outside** — by another session's code, an extension or a person —
  and only on some pages. The sign is a `close` event you did not cause; prove it with a control URL in the same tab (another page of
  the site stays open). Other sessions are not touched; read the page from INSIDE it instead: `page.addInitScript` takes the reading at
  `DOMContentLoaded` and hands it to Node through `page.exposeBinding`, and the network logger in `state` outlives the tab. Say in the
  result which readings were taken that way. Precedent: a live round's tabs on a login page closed 0.4–0.9 s after every load while the
  site's other pages stayed open; reading from inside the page closed every requirement anyway.
- Controlled tabs show Chrome's automation banner; a scenario about the page's own layout at the top edge accounts for it.
- `snapshot()` returns an accessibility snapshot and, on later calls, diffs against the previous one — a diff that looks empty is «nothing
  changed», not «nothing there».
