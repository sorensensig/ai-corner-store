# Miller's Law

*Law `#12` in the Laws of UX collection [1]. Primary source: Miller [13]; see also Cowan
[14]. Synthesised, not quoted.*

## What it says

The average person can hold about **seven (± two)** objects in working memory. The
number is a ceiling on what someone can keep in mind at once — and it is lower than most
design assumes.

## Why it holds

Miller's 1956 paper reported the limit across several judgement and recall tasks [13].
Cowan's later reanalysis put the figure closer to **four** when rehearsal and chunking
are controlled for [14] — so 7±2 should be read as an optimistic upper bound, not a
target.

**The critical and most-misused detail:** the unit is a *chunk*, not an item. A chunk is
whatever the person has learned to treat as one thing. An expert holds seven chunks that
each contain a novice's seven items. This is why the law says nothing about how many
things you may put on a page, and everything about how many *unfamiliar* things you may
require someone to hold simultaneously.

## What it constrains

- **Chunking is the lever, not deletion.** A 16-digit card number is unholdable; four
  groups of four is trivial. The information did not shrink.
- **The limit binds on what must be held *across* steps**, not on what is visible. A
  list of thirty items on screen costs nothing if the user need not remember them; three
  values carried from step 2 to step 5 may exceed capacity.
- **Beyond the visual:** this is the ceiling on how many constraints a prompt can impose
  before compliance degrades, how many flags an operator can compose from memory, and
  how many concurrent unknowns a reviewer can hold while reading a diff. A pull request
  touching seven unrelated concerns is not seven times harder than one — it is past the
  ceiling, and review quality falls off a cliff rather than a slope.

## Getting it wrong

- **"Never more than seven menu items."** This is the canonical misapplication. Miller's
  limit is about memory, not about how many options may be *visible* — a visible list is
  not held in working memory. For option-set size, the governing law is [[hicks-law]].
- Treating 7 as a target when Cowan's 4 is the safer planning number for anything
  unfamiliar [14].
- Assuming chunk size is fixed. It is a function of the user's expertise, which means
  the same interface has different effective complexity for novices and experts.

## Related

- [[hicks-law]] — the law that actually governs list and option-set size.
- [[serial-position-effect]] — *which* of the held items survive.
- [[teslers-law]] — complexity that exceeds the ceiling has to be absorbed somewhere.
- [[law-of-pragnanz]] — simplification as the mind's response to the limit.
