# Law of Uniform Connectedness

*Law `#11` in the Laws of UX collection [1]. Primary source: Palmer and Rock [12].
Synthesised, not quoted.*

## What it says

Elements that are visually connected — by a line, an arrow, a shared continuous
background — are perceived as more related than elements grouped by proximity or
similarity alone. It is the strongest of the grouping principles.

## Why it holds

Palmer and Rock argued uniform connectedness is prior to the classical Gestalt
principles: the visual system first segments the field into connected regions, and only
then applies proximity and similarity within them [12]. Connection wins because it
happens first.

## What it constrains

- **Use it for the relationships that must not be misread.** A line from a label to the
  thing it labels is unambiguous in a way that adjacency never is.
- **It overrides the others, so it can rescue a constrained layout** — but it also means
  an accidental connector asserts a relationship you cannot undo with spacing.
- **Beyond the visual:** connection in text is explicit reference. A cross-link, an `id`
  that appears in two places, a foreign key, a `see also` — these are connectors, and
  they bind harder than co-location does. The double-bracket cross-links in this
  library's *Related* sections are the same mechanism, which is why they are worth
  following. In diagrams and generated output, an arrow is a commitment: it says *this
  causes that*, and readers will believe it over any caption to the contrary.

## Getting it wrong

- Drawing connectors for visual interest. Every line is an assertion; decorative lines
  assert nonsense.
- Building elaborate connector diagrams where a table would serve. Connection is strong
  but expensive to follow at volume — past a handful of edges, a reader loses the thread.
- Relying on a connector that disappears at a breakpoint or in a screen reader, leaving
  the relationship unstated for some users.

## Related

- [[law-of-common-region]] — the next-strongest grouping signal.
- [[law-of-proximity]] — the weakest, and the one connection most often overrides.
- [[law-of-pragnanz]] — connection is a route to the simplest reading.
