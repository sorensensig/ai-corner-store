# Law of Similarity

*Law `#10` in the Laws of UX collection [1]. Primary source: Wertheimer [10].
Synthesised, not quoted.*

## What it says

Elements that look alike are perceived as related, even when separated in space. Shared
colour, shape, size, orientation or typography creates a group across distance.

## Why it holds

A Gestalt grouping principle from Wertheimer's original set [10]. Similarity operates
independently of position, which makes it the tool for relating things that layout keeps
apart — and the trap when two unrelated things happen to share a style.

## What it constrains

- **Consistent styling is a semantic claim.** If all primary actions are the same
  colour, an element in that colour is read as a primary action. Style consistency is
  not decoration; it is a taxonomy.
- **The corollary is the important half:** anything styled like a link must behave like
  a link. Non-interactive text in the interactive colour is a broken promise, and users
  learn to distrust the whole system rather than that one element.
- **Similarity beats proximity across distance.** Use it to relate a legend to a chart,
  or a footnote to its marker.
- **Beyond the visual:** naming is similarity in text. Two functions named `getUserData`
  and `getUserInfo` assert a relationship and a distinction the reader must then
  reverse-engineer. Consistent verb prefixes across a CLI group commands as surely as
  colour groups buttons. In config files, key naming conventions do the same work — and
  an inconsistent key reads as a different *kind* of setting.

## Getting it wrong

- Using colour as the only similarity signal. Roughly 1 in 12 men has a colour vision
  deficiency; pair colour with shape, weight, or an icon.
- Over-styling until every element is distinct, which destroys grouping entirely — if
  nothing matches, nothing groups.
- Letting a design system's semantic colours drift into decorative use, which severs the
  learned association everywhere at once.

## Related

- [[law-of-proximity]] — grouping by position rather than appearance.
- [[von-restorff-effect]] — the deliberate violation of similarity, to make one thing
  stand out.
- [[jakobs-law]] — cross-product similarity is where conventions come from.
