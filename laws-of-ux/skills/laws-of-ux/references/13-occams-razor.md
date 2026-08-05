# Occam's Razor

*Law `#13` in the Laws of UX collection [1]. Attributed to William of Ockham (14th c.).
Synthesised, not quoted.*

## What it says

Among competing solutions that satisfy the requirements, choose the one with the fewest
assumptions and the fewest parts. Entities should not be multiplied beyond necessity.

## Why it holds

Ockham's principle is epistemological — prefer the explanation requiring fewest
assumptions — and it transfers to design as a bias toward the smallest sufficient
solution. The justification is not aesthetic: every element carries ongoing cost in
attention, maintenance, and surface area for error, and unnecessary elements pay that
cost forever while contributing nothing.

## What it constrains

- **The test is "does removing this break a requirement?"** — not "is this nice to
  have?" Anything that survives that question honestly stays.
- **Analyse before you cut.** The razor selects among solutions that *all meet the
  requirement*. Cutting something load-bearing is not simplification; it is scope
  reduction wearing a principle as a disguise.
- **Beyond the visual:** every configuration option is a permanent maintenance and
  documentation liability plus a decision imposed on every user. Every abstraction layer
  is one more thing to hold. Every element added to a system that a human must operate
  is drawn against [[millers-law]] and [[hicks-law]] simultaneously. The cheapest
  option is the one that does not exist.

## Getting it wrong

- **Confusing "simple" with "minimal".** Hiding necessary complexity produces something
  that looks simple and behaves worse — see [[teslers-law]].
- Using the razor to justify removing accessibility affordances, error handling, or
  edge-case coverage. Those are requirements, so they are outside what the razor
  selects among.
- Applying it to the artefact while ignoring the process: a simple interface backed by
  an incomprehensible mental model has not been simplified, only relocated.

## Related

- [[teslers-law]] — the limit on how far simplification can go before complexity moves.
- [[hicks-law]] — why each additional option has a compounding cost.
- [[law-of-pragnanz]] — the perceptual tendency this design discipline serves.
- [[parkinsons-law]] — both concern resisting expansion that adds no value.
