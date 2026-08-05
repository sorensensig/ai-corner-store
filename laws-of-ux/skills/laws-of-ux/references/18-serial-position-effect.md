# Serial Position Effect

*Law `#18` in the Laws of UX collection [1]. Primary sources: Ebbinghaus [20] and
Murdock [21]. Synthesised, not quoted.*

## What it says

In a sequence, people best remember the first items (primacy) and the last items
(recency). The middle is where things go to be forgotten.

## Why it holds

Ebbinghaus first documented the position-dependent recall curve [20]; Murdock
characterised its shape in free recall [21]. The two ends are served by different
mechanisms — early items get rehearsed into long-term memory, late items are still in
working memory at recall time — which is why the curve has two humps rather than one.

## What it constrains

- **Put the most important items first and last.** This is why primary navigation lives
  at the edges of a bar and why the critical point of a summary belongs in the opening
  and closing sentence.
- **The middle needs help.** Items that must be remembered from the middle of a list
  need a different mechanism — visual distinction ([[von-restorff-effect]]), grouping,
  or simply a shorter list.
- **Beyond navigation:** this governs long prompts and long documents. Instructions in
  the middle of a large context are the ones most likely to be missed — by human readers
  and by models, which show an analogous position-dependent attention profile. It is
  also why a status summary should lead with the conclusion and end with the action, not
  bury either in the middle.

## Getting it wrong

- Ordering by internal convenience — alphabetical, or schema order — when the sequence
  carries meaning to the reader.
- Assuming a long list can be made memorable by styling alone. Past a certain length the
  middle is unrecoverable; shorten or chunk it.
- Putting the most important call to action in the visual centre because it looks
  balanced.

## Related

- [[millers-law]] — the capacity limit; this law says *which* of the held items survive.
- [[peak-end-rule]] — the same recency weighting applied to experience rather than lists.
- [[von-restorff-effect]] — the tool for rescuing an item from the middle.
