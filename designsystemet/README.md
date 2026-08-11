# designsystemet — build with Digdir's Designsystemet correctly on the first attempt

A Claude Code plugin for anyone building Norwegian public-sector services with
[Designsystemet](https://designsystemet.no). It closes the gap A/B trials showed no
model closes alone: agents produce plausible, WCAG-silently-broken markup unless the
system's real contracts travel with the task.

**What's in it, and why each piece earned its place** (all claims trial-backed, see
the evidence note at the bottom):

| Piece | What it does |
|---|---|
| **Skill** | Injects the form/validation cluster's quote-verified rules (the part agents miss most) and points at the rest. |
| **Twins registry (bundled)** | 45 component + 2 pattern contracts: extracted layer regenerated from source, authored layer quote-verified against designsystemet.no and human-reviewed (`reviewedAgainst: 1.18.0`). Served by the `designsystemet-twins` MCP server (`list_twins`, `get_component`, `get_pattern`, `find_equivalent`). |
| **Guard hook** | PreToolUse deny on writes that break a contract — invented props, raw hex for tokens, deprecated imports, validation UI without its accessibility wiring. The reason is fed back so the model fixes it. |
| **/ds-check** | Explicit audit of an existing codebase against the contracts; surfaces the `tokens` and `migrate` CLIs. |

## Install

```bash
/plugin install designsystemet
```

Or per client, shadcn-style — the MCP server alone works anywhere MCP does:

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

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `DESIGNSYSTEMET_TWINS` | bundled `registry/` | Point at a newer or local twins directory (e.g. a checkout of the upstream registry) to override the pinned snapshot. |
| `DESIGNSYSTEMET_PYTHON` | `python3` | Interpreter for the guard hook. |

The bundled registry is **pinned** to the package version it was reviewed against
(`@digdir/designsystemet-react` 1.18.0). When upstream hosts the registry publicly,
point `DESIGNSYSTEMET_TWINS` at it — or update the plugin, which re-pins.

## Provenance model (the part to trust)

Every authored rule in a twin carries a verbatim quote from designsystemet.no, and the
quote is machine-verified to exist on the cited page at merge time. Rules keep the
docs' own modality — "should" stays should. What the docs don't state, the twins
don't claim (`null`, never invented). Extracted fields (props, imports, emitted DOM)
regenerate from the component source and cannot drift.

## Evidence

Built from a pre-registered A/B programme (2026-08, claude-sonnet-5, N=8–9/arm,
complex form task): twins raised first-attempt conformance from ~50% (live docs) to
100% at cost-neutral-or-better per conforming solution; the true-null arm never uses
Designsystemet unprompted; two live-docs trials shipped stale or invented APIs that
reading the docs did not correct. Ledger: sorensensig/claude-stack#74.

## Status

- v0.1.x — interim home in ai-corner-store; moves to kihub when it can take
  contributions. Registry pinned at 1.18.0.
- Roadmap (tracked on the ledger): non-React twin tracks (web components / CSS-only —
  real consumer: Mattilsynet's CSS-layer sub-system), update-checker in `/ds-check`,
  federation kit for agency sub-systems, pattern starter code ("blocks").
