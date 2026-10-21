# Playwright MCP

An MCP server that drives a browser of its own through Playwright. Read beside `../browser-techniques.md` when the profile's `browser`
is `playwright-mcp`. Its browser is NOT the user's: no sign-ins, no cookies, no extensions — every round logs in through the profile's
Secrets section, and a flow that needs the user's own session (a wallet extension, an SSO only their browser holds) is out of its reach.
That is why it is never the fallback for a tool the harness lacks (`../../SKILL.md`, «Capability degradations»).

## Install

The harness's MCP route (`../harness/<name>.md`, «Connecting an MCP server») with the server `npx @playwright/mcp@latest`; its browsers come
with `npx playwright install chromium` the first time.

## Preflight

The server's tools are in your tool list, and one probe opens a page and reads its title. Missing → the user connects the server; do not
launch the executor.

## Connect and pick the tab

The server opens and owns its tabs; its tab tools list and select them. A login is done at the start of the round, in that browser, from
the profile's Secrets — never typed from memory.

## Page scripts and their budget

Its evaluate tool runs a function in the page; the budget is the server's call timeout (set in its own flags). Long work accumulates in
`window.__…` as `../browser-techniques.md` describes.

## Screenshots

Its screenshot tool saves to the server's output directory; copy the file into the session's artifacts before citing it.

## Network

Its network tool lists requests; bodies and substitution go through page scripts, as in `../browser-techniques.md`, «Intercepting,
replaying and substituting network».

## Known failures

None recorded yet — a round that meets one writes it here.
