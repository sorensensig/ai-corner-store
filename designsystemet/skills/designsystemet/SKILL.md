---
name: designsystemet
description: >
  Build correct, accessible Designsystemet UI for Norwegian public-sector services. Use
  whenever writing or reviewing code that uses `@digdir/designsystemet-react`, `ds-*`
  classes, or `--ds-*` tokens; when building any form, validation, or error state in such a
  service; when porting or copying markup from another design system (MUI, Bootstrap,
  GOV.UK, Tailwind, shadcn) into a Designsystemet codebase; and on Norwegian framing —
  designsystemet, skjema, skjemavalidering, feilmelding, feiloppsummering, komponent,
  tilgjengelighet, universell utforming. Also use when an agent is about to guess a
  Designsystemet prop, colour, or component name rather than look it up.
---

# Designsystemet

Designsystemet's prop surface is not what a general React prior predicts, and its
accessibility requirements are mostly *consumer* responsibilities the components do not
enforce for you. Both are served by the `designsystemet-twins` MCP. Look them up; do not
recall them.

## First move — before writing any code

| You are about to… | Call | Then |
|---|---|---|
| Build a screen, form, or flow | `get_pattern("<slug>")` | The pattern names the components, their order, the timing rules, and the a11y wiring. Components alone will not give you a correct form. |
| Use a named component | `get_component("<slug>")` | The real export name, the a11y rules the component does not enforce, the token mapping, and the docs links carrying the full prop tables. |
| Port markup from another design system, or resolve a `data-registry` / `ds-*` value off a rendered page | `find_equivalent("<term>")` | Then `get_component` on the match. |
| Not know what exists | `list_twins()` | Inventory with one-line summaries. |

If a component has no twin, the pattern twin still names its role and its rules — read that
rather than guessing a prop surface. A missing twin is a reason to look wider, never a
licence to invent.

## Level 1 — which component for which intent

Cross-component knowledge, true before anything is chosen. Level 2 (the contract for
whatever you choose) lives in the twins.

| Intent | Component | Not the neighbour, because |
|---|---|---|
| Tell the user something about the page or process — info, warning, error, success | `Alert` | It is *not* the mechanism for form validation errors. |
| Report that one field is invalid | `ValidationMessage`, under the field, inside its `Field` | An `Alert` here detaches the error from the control it belongs to. |
| Report that a submitted form has several errors | `ErrorSummary` + a `ValidationMessage` per field | Neither replaces the other; the pattern requires both. |
| Let the user pick from a known list, typing to filter | `Suggestion` | `Select` when the list is short and needs no filtering; `Textfield` when any free text is valid. |
| Group related controls (radios, checkboxes) | `Fieldset` + `Legend` | Loose controls with no group label fail WCAG 1.3.1. |
| Wrap a label + control + its validation message | `Field` | It wires the ids between them; hand-wiring `aria-describedby` is where it breaks. |

## Non-negotiables

These hold across every component, so they are worth carrying rather than fetching.

1. **The variant mechanism is `data-color`.** There is no `variant`, `severity`, or `type`
   prop on the status components. (`Button` genuinely has `variant` — the ban is per
   component, not blanket.)
2. **Colours come from `--ds-*` tokens.** Never a raw hex value, never a foreign system's
   custom property.
3. **A validated form reports errors with `ErrorSummary` + per-field `ValidationMessage`,**
   with `aria-invalid` on every field in an error state. A lone `Alert` is not validation.
4. **Translate, never transplant.** Porting from another design system means mapping each
   element to its Designsystemet equivalent and emitting *that* component's real API — never
   the foreign component name, class name, or colour value.
5. **Errors appear on blur or submit, never while the user is typing.**
6. **Install the packages; never hand-write what the build produces.** Setting a project up
   means `npm install @digdir/designsystemet-react @digdir/designsystemet-css`, importing the
   CSS and then a theme, and adding the Inter font — all of it per
   <https://designsystemet.no/en/fundamentals/code/setup>. Approximating any of it produces
   markup carrying correct `ds-*` class names with none of the design behind it: right
   structure, wrong everything else, and it drifts the moment the theme changes. Reach for the
   CLI rather than reimplementing it — `designsystemet tokens create` / `tokens build` for
   themes, `designsystemet migrate` across a breaking version.

   *Written from a real failure rather than caution: a session that built a demo site by
   hand-copying build output shipped pages with correct class names, no stylesheet, and the
   browser's serif default. Both bugs were invisible in the markup and obvious on screen.*

## Component and pattern facts

<!-- BEGIN twin-facts (generated) -->

> Generated from the twins by `scripts/generate-skill-facts.py`. The tools above serve the full contract; this is the part you should not have to ask for.

### Alert

- **Import:** `Alert` from `@digdir/designsystemet-react`
- **Use instead — ValidationMessage:** Use for a single form field error instead of Alert
- **Use instead — ErrorSummary:** Use to summarise multiple errors instead of Alert
- **A11y:** Use role='alert' for critical messages that require immediate attention; use role='status' for less critical messages
- **Composition:** Avoid multiple alerts on the same page
- Full contract: `get_component("alert")`

### Button

- **Import:** `Button` from `@digdir/designsystemet-react`
- **Use instead — Link:** Use Link for navigation
- **A11y:** An icon-only button needs an accessible label
- **A11y:** An icon next to text must be hidden from screen readers
- **Composition:** Only one primary button per page
- Full contract: `get_component("button")`

### ErrorSummary

- **Import:** `ErrorSummary` from `@digdir/designsystemet-react`
- **Use instead — Alert:** Use Alert for system-level messages instead
- **A11y:** The summary takes focus when it appears or its content changes
- **A11y:** Every error message must link directly to its field
- **Composition:** The summary should contain every error message present on the page
- **Composition:** Summary messages should be phrased exactly the same as the field-level messages
- **Composition:** Where one error covers several fields, link to the first
- Full contract: `get_component("error-summary")`

### Field

- **Import:** `Field` from `@digdir/designsystemet-react`
- **Use instead — Fieldset:** Use Fieldset to group multiple fields
- **A11y:** Field links label, description, validation message and counter so assistive technology reads them as one unit
- Full contract: `get_component("field")`

### Fieldset

- **Import:** `Fieldset` from `@digdir/designsystemet-react`
- **Use instead — Radio:** Groups radio or checkbox components, even a group of one
- **A11y:** Avoid repeating the same text in both label and legend
- **Composition:** Start with a legend explaining what the fields below relate to
- Full contract: `get_component("fieldset")`

### Label

- **Import:** `Label` from `@digdir/designsystemet-react`
- **A11y:** The label must be clearly connected to its field
- **Composition:** Write in plain language; avoid abbreviations and internal terminology
- Full contract: `get_component("label")`

### EXPERIMENTAL_Suggestion

- **Import:** `EXPERIMENTAL_Suggestion` from `@digdir/designsystemet-react`
- **Use instead — Radio:** Use Radio or Checkbox when there are only a few options
- **Composition:** Keep each option short
- *Authored rules drafted from the docs, not yet human-reviewed.*
- Full contract: `get_component("suggestion")`

### Textfield

- **Import:** `Textfield` from `@digdir/designsystemet-react`
- **Use instead — Input:** Use Input for a simple field without form logic
- **A11y (WCAG 1.3.1):** A textfield must always have a label
- **A11y (WCAG 1.3.1):** Prefixes and suffixes must not be used without a label
- **A11y (WCAG 1.3.1):** Information in a prefix or suffix must also appear in the label
- **A11y (WCAG 1.3.5):** Autocomplete is required where a predefined purpose exists
- **Composition:** Textfield bundles label, help text and validation message
- Full contract: `get_component("textfield")`

### ToggleGroup

- **Import:** `ToggleGroup` from `@digdir/designsystemet-react`
- **Use instead — Radio:** Use Radio when the options are answers in a form
- **Use instead — Switch:** Use Switch for an on/off setting
- **A11y:** Icon-only toggles need a tooltip to convey meaning
- **Composition:** At least two options, few enough to fit on one line
- **Composition:** The group needs a label explaining what the options refer to
- Full contract: `get_component("toggle-group")`

### ValidationMessage

- **Import:** `ValidationMessage` from `@digdir/designsystemet-react`
- **A11y (WCAG 3.3.1):** Messages should be placed close to the field they relate to
- Full contract: `get_component("validation-message")`

28 further components carry authored rules served on demand — call `list_twins()` for the inventory and `get_component(slug)` for a contract.

6 components have no authored rules yet.

### Pattern · Field guidance — placeholders, descriptions and input purpose

- How a form field tells the user what to enter: guidance before the field, never placeholder-only; descriptions (help text) for difficult content such as expected formats; autocomplete attributes where the field's purpose is predefined.
  - `Textfield` — carries label, description and error in one composition
  - `Field` — links label, description, validation message and counter for assistive technology
- **Composition:** Use a description (help text) to explain difficult content — legal terms, specialist language, expected formats
- **Composition:** Only use descriptions where needed, to reduce cognitive load
- Full contract incl. timing + a11y: `get_pattern("field-guidance")`

### Pattern · Required and optional form fields

- Tell users which fields are required and which are optional. Where all fields are required, say so once above the form; where the form mixes both, mark each field individually. Never use an asterisk as the marker.
  - `Textfield` — single-line input; carries its own `label` prop
  - `ToggleGroup` — choice between a small set of options; items are ToggleGroup.Item (exported also as ToggleGroupItem)
  - `Tag` — renders the visible 'Required'/'Optional' marker
  - `Fieldset` — groups related controls and gives the group an accessible name via FieldsetLegend
  - `Label` — programmatic label where a component does not carry one
- **Composition:** All fields required: state it once above the form; do not mark each field.
- **Composition:** Mixed required and optional: mark every field individually so the marking is unambiguous.
- **Composition:** The marker is a word — 'Required' / 'Optional' — rendered as a Tag beside the label.
- **Composition:** ToggleGroup is a group control: wrap it in a Fieldset with a legend, or give it an accessible name directly.
- **Never:** This pattern governs MARKING, not validation. Error handling belongs to the errors pattern.
- **Never:** ToggleGroup is for switching between views or a small set of choices; for a form answer the docs direct you to Radio instead. It is used here because the brief asks for it.
- **Never:** Do not invent props on ToggleGroup: the documented surface is variant, value, defaultValue, onChange, name (+ ToggleGroup.Item: value, icon).
- Full contract incl. timing + a11y: `get_pattern("required-and-optional-fields")`

### Pattern · Skjemavalidering (form validation and errors)

- How a validated form reports errors: a per-field ValidationMessage under every invalid field, plus an ErrorSummary listing all errors with links that move focus to the offending field. An Alert is NOT the error mechanism for form validation.
  - `error-summary` — Lists every current error; each item links to its field and moves focus there. Required once more than one error can occur.
  - `validation-message` — The error text for a single field, rendered directly under that field.
  - `field` — Wraps label + control + validation message and wires their ids.
  - `fieldset` — Groups related controls under a Legend (e.g. radio/checkbox groups).
  - `suggestion` — A filtering combobox control; validates like any other field.
  - `alert` — NOT the validation mechanism. Only for page-level info/success messaging around the form.
- **Composition:** Place the ErrorSummary near the Next/Submit button. Page-top placement is the alternative, and only when: the page reloads on submit, users return to the form, or the errors do not prevent progression.
- **Composition:** Every invalid field gets its own ValidationMessage rendered under the field, inside the same Field wrapper.
- **Composition:** Each ErrorSummary.Link href targets the id of the invalid control so activating it moves focus to that control.
- **Composition:** The summary must include all applicable errors and entries must disappear as the user fixes them.
- **Never:** Never disable the submit button to enforce validation.
- **Never:** Never use a lone Alert as the error mechanism for form validation — that is ErrorSummary + ValidationMessage.
- **Never:** Never validate keystroke-by-keystroke while the field has focus.
- Full contract incl. timing + a11y: `get_pattern("skjema-validering")`

<!-- END twin-facts -->
