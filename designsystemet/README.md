# designsystemet

> **Experimental.** Interfaces and registry content may change without notice.

A Claude Code plugin for building Norwegian public-sector services with
[Designsystemet](https://designsystemet.no).

## Why

Agents writing Designsystemet code make confident, hard-to-spot mistakes: props
that don't exist, imports that break at build time, and — worst — forms that look
right but fail WCAG because the accessibility wiring the components leave to the
consumer never gets written. This plugin puts the system's real contracts in the
agent's hands and blocks the mistakes that can be blocked.

## What's in it

| Piece | What it does |
|---|---|
| **Skill** | Teaches the form/validation rules agents miss most; points at the lookup tools for everything else. |
| **Registry + MCP server** | A contract ("twin") for every component and pattern — all human-reviewed against 1.18.0 — served by four tools: `list_twins`, `get_component`, `get_pattern`, `find_equivalent`. |
| **Guard hook** | Blocks writes that break a contract — invented props, raw hex instead of tokens, error states without `aria-invalid` — and feeds the reason back so the agent fixes it. |
| **/ds-check** | On-demand audit of existing code against the contracts. |

## Install

Add the store as a marketplace once, then install the plugin — pick
**project** scope to enable it for one repository, or **user** scope for
everywhere:

```bash
/plugin marketplace add sorensensig/ai-corner-store
/plugin install designsystemet
```

**Then restart Claude Code** (exit and start `claude` again in the project).
The guard hook, the twins MCP server, and `/ds-check` are all loaded at
session start — in the session where you ran the install, none of them are
active yet. The same applies when the plugin is enabled through
`enabledPlugins` in a project's `.claude/settings.json`: the first session
only installs it; the plugin works from the next session on.

Verify the install in the new session:

1. Ask for the design system twins — the `list_twins` tool should return the
   full registry.
2. Run `/ds-check` — the command should exist (a clean report on an empty
   project is the expected answer).
3. Ask for a form error rendered as `<Alert>` — the guard hook should refuse
   the write and explain why.

The MCP server alone works in any MCP client:

```json
{
  "mcpServers": {
    "designsystemet-twins": {
      "command": "python3",
      "args": ["<plugin-root>/mcp/twins_server.py", "--twins", "<plugin-root>/registry"]
    }
  }
}
```

## Core concepts

**Twins.** A twin is the machine-readable counterpart of one component or
pattern: a JSON contract carrying its real export name, design tokens,
accessibility rules, and composition rules. Components alone don't make a
correct form, so patterns (e.g. `skjema-validering`) are twins too.

**Provenance.** Every field in a twin says where it came from. `extracted`
fields are regenerated from the component source and cannot drift. `authored`
fields carry rules that exist only as prose in the documentation; each one is
backed by a verbatim quote, machine-verified to appear on the cited docs page,
and human-reviewed (`reviewedAgainst` records the package version of the
sign-off). What the docs don't state, the twins don't claim.

**llms.txt.** The registry's index file, following the
[llms.txt](https://llmstxt.org) convention: one file from which an agent
discovers every contract instead of scraping rendered documentation.

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `DESIGNSYSTEMET_TWINS` | bundled `registry/` | Point at a newer or local twin directory to override the pinned snapshot. |
| `DESIGNSYSTEMET_PYTHON` | `python3` | Interpreter for the guard hook. |

The bundled registry is pinned to `@digdir/designsystemet-react` **1.18.0**, the
version its rules were reviewed against.

## Research

The design comes out of a pre-registered A/B programme (2026-08). The task in
every trial: build a complex Norwegian public-sector form — text field,
filtering suggestion field, validation, error states — where **conforming**
means every rubric check passes *and* the code compiles. 8–9 trials per arm,
`claude-sonnet-5`.

| Arm | Conforming | What it showed |
|---|---|---|
| No cue at all | 0/8 | Unprompted, agents never reach for Designsystemet. Discovery has to be engineered; "the model already knows it" is false. |
| Live documentation | 3/8 | Agents that read designsystemet.no still shipped inaccessible validation, stale APIs, and invented props. |
| Twins registry (this plugin) | 9/9 | Correct on the first attempt (Fisher p = 0.009), at equal or lower cost per conforming solution. |

### The three situations an agent can be in

The same contracts serve all three — this plugin is one part of a broader
effort to make Designsystemet AI-ready:

- **Working in your repository** *(what this plugin is for)*: the agent writes
  Designsystemet code with the contracts one tool call away and the guard hook
  enforcing the rules that can be enforced.
- **Crawling the documentation**: an agent with no plugin discovers the hosted
  registry through `llms.txt` and fetches the same twins over HTTP. In trials
  this matched well-signposted docs on correctness at roughly half the
  retrieval tokens.
- **Landing on a built site**: an agent asked to copy or extend a page built
  with Designsystemet identifies the system from its rendered `ds-*` markup
  and can trace its way back to the contracts.
