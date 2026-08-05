# Pareto Principle

*Law `#14` in the Laws of UX collection [1]. Primary source: Pareto [15]; named and
generalised by Juran [16]. Synthesised, not quoted.*

## What it says

Roughly 80% of effects come from 20% of causes. A small share of features drives most of
the value; a small share of defects drives most of the pain.

## Why it holds

Pareto observed the income distribution of 19th-century Italy [15]; Juran generalised it
to quality management as the "vital few and trivial many" [16]. The underlying shape is
a power-law distribution, which recurs across usage data, defect counts, and support
volume often enough to be a useful prior — though it is a heuristic, not a law in the
sense that Fitts's is.

## What it constrains

- **Instrument before you optimise.** The principle tells you a vital few probably
  exist; it does not tell you which. Assuming you know is how teams polish the wrong
  20%.
- **Effort should follow usage, not surface area.** The most-used path deserves
  disproportionate attention, and the rarely-used path deserves to work correctly rather
  than beautifully.
- **Beyond features:** the same shape usually holds for the tools you build for
  yourself. A handful of hooks or checks produce most of the caught errors; a long tail
  produce none. Measuring which is which is the only way to know — and the measurement
  frequently contradicts the intuition of the person who built them.

## Getting it wrong

- **Neglecting the tail entirely.** The 20% carries most of the value, not all of it.
  Accessibility features, error paths, and edge cases live in the tail and are often
  non-negotiable. "Rarely used" and "unimportant" are different claims.
- Treating 80/20 as a measured fact rather than a rough prior. The real ratio varies;
  measure it.
- Using it to justify shipping the vital few and never returning. The tail compounds
  into the impression that a product is unfinished.

## Related

- [[occams-razor]] — both bias toward the smallest set that carries the value.
- [[parkinsons-law]] — effort expands to fill the time regardless of where value sits.
- [[goal-gradient-effect]] — finishing the tail is where motivation is scarcest.
