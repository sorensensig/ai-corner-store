---
description: >
  Audit code against the Designsystemet contracts and the accessibility rules the
  library cannot enforce. Checks the layer agents actually get wrong — aria-invalid,
  error-summary placement, export names, invented props, raw hex — by reading each
  component's contract rather than pattern-matching prose. Reports; never rewrites.
argument-hint: "[path | --staged] — defaults to the files changed in the working tree"
---

# /ds-check — audit code against Designsystemet

Everything else in this plugin is implicit: the skill triggers on description match, the
MCP on the model's judgement, the guard hook on tool use. This is the explicit door — run it
when *you* decide, on code that already exists, including code the plugin never saw written.

## Scope

`$ARGUMENTS` is a path or `--staged`. With neither, check the files changed in the working
tree (`git diff --name-only` plus untracked), filtered to `.tsx`/`.jsx`/`.ts`/`.html`.

If nothing matches, say so and stop. Do not widen to the whole repo uninvited — an unbounded
audit on a large codebase burns tokens and buries the findings that matter.

## What to check, and why these

Every check below traces to a measured failure. The extracted layer — prop names, tokens,
imports — is what agents already get right unaided; the **authored layer** is where they fail.
Weight the report accordingly.

1. **Call `list_twins` first**, then `get_component` for each Designsystemet component the
   code uses, and `get_pattern` for any pattern it implements. Check against the contract you
   fetched, not against memory. If a component has no twin, say so for that component rather
   than guessing at its rules.

2. **Accessibility (the authored layer — the highest-value findings):**
   - a field in an error state without `aria-invalid`
   - a validation message not linked to its field via `aria-describedby`
   - an `ErrorSummary` whose items do not link to the fields they describe
   - a group control (`ToggleGroup`, `Fieldset`) with no accessible name
   - required state conveyed only visually, never programmatically
   Cite the WCAG criterion from the twin's `a11y` entries, not from memory.

3. **Pattern conformance:** where a pattern twin exists, check its `assertions` — component
   set, ordering, and boundaries. The classic miss is using an `Alert` as the validation
   mechanism instead of `ValidationMessage` + `ErrorSummary`.

4. **Contract violations:** props that do not exist on the component, the wrong export name
   (`Suggestion` does not exist — it is `EXPERIMENTAL_Suggestion`), raw hex where a
   `--ds-*` token exists.

5. **Version drift:** if rendered markup carries `data-ds-version` older than the installed
   `@digdir/designsystemet-react`, flag it and point at `designsystemet migrate` rather than
   proposing hand edits.

## Reach for the CLI, do not reimplement it

`@digdir/designsystemet` is already installed alongside the packages, and it owns work that
must stay in step with the library version. Never hand-write what it generates:

| Need | Command |
|---|---|
| Create a theme / design tokens | `npx @digdir/designsystemet tokens create` |
| Build tokens after a config change | `npx @digdir/designsystemet tokens build` |
| Config from existing tokens | `npx @digdir/designsystemet generate-config-from-tokens` |
| Upgrade across a breaking version | `npx @digdir/designsystemet migrate` |

Hand-written CSS custom properties in place of `tokens build` is itself a finding — it drifts
the moment the theme changes.

## Report

One table, ordered by severity, then a short prose summary. For each finding: file and line,
what is wrong, the rule it breaks, and the twin or WCAG criterion it comes from. Show the
minimal fix as a diff snippet.

**This command reports. It does not edit.** Fixing accessibility wiring without the author
seeing the reasoning is how a defect becomes invisible rather than fixed — and the author is
the one who knows whether the field is genuinely required. If the user asks for the fixes
after reading, apply them then.

State plainly when a check could not run — no twin for a component, no MCP server, a file
that failed to parse. A silent skip reads identically to a pass.
