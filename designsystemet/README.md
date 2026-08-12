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
| **Registry + MCP server** | A contract ("twin") for every component and pattern, served by four tools: `list_twins`, `get_component`, `get_pattern`, `find_equivalent`. |
| **Guard hook** | Blocks writes that break a contract — invented props, raw hex instead of tokens, error states without `aria-invalid` — and feeds the reason back so the agent fixes it. |
| **/ds-check** | On-demand audit of existing code against the contracts. |

## Install

```bash
/plugin install designsystemet
```

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

The design is evidence-driven: each piece exists because pre-registered A/B
trials on complex form tasks showed agents fail without it — including the
finding that reading the live documentation alone still ships inaccessible
validation. Twins raised first-attempt conformance from roughly half to all
trials at equal-or-lower cost per correct solution.
