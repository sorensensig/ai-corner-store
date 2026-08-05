# Law of Proximity

*Law `#8` in the Laws of UX collection [1]. Primary source: Wertheimer [10].
Synthesised, not quoted.*

## What it says

Elements near each other are perceived as related. Distance is read as meaning, whether
or not any was intended.

## Why it holds

One of Wertheimer's original Gestalt grouping principles [10]. Proximity operates
pre-attentively — the grouping is done before the viewer consciously reads anything, so
it frames interpretation rather than following it.

## What it constrains

- **Whitespace is the primary grouping tool**, and it is cheaper and quieter than
  borders. Reach for it first.
- **Space *between* groups must exceed space *within* them.** This single rule fixes
  most muddled layouts. Equal spacing everywhere communicates nothing.
- **A label belongs to whatever it is nearest.** The classic form bug — a label sitting
  midway between two fields — is a proximity failure, and users will attach it to the
  wrong field consistently.
- **Beyond the visual:** blank lines are proximity in text. Log output with no blank
  lines between unrelated events reads as one event. A comment placed directly above a
  line claims that line; placed after a blank line, it claims the block. In prompts,
  instructions clumped together are read as one instruction — including by models.

## Getting it wrong

- Using uniform padding everywhere in the name of consistency, destroying the
  differential that carries the meaning.
- Letting a responsive breakpoint reflow content so that previously-separated groups
  become adjacent, silently changing what the layout asserts.
- Relying on proximity alone across a scroll boundary or column break, where it stops
  being perceivable.

## Related

- [[law-of-common-region]] — a stronger signal that can override proximity.
- [[law-of-similarity]] — grouping by likeness when position cannot be controlled.
- [[law-of-pragnanz]] — proximity is one of the routes to the simplest reading.
