# Law of Common Region

*Law `#7` in the Laws of UX collection [1]. Primary source: Palmer [9]. Synthesised, not
quoted.*

## What it says

Elements enclosed within a shared boundary are perceived as a group. A border or a
background panel creates a group even when the elements inside are far apart and unlike
each other.

## Why it holds

Palmer showed common region to be a grouping principle strong enough to override
proximity: items further apart but inside one enclosure group more strongly than nearer
items split across two [9]. Enclosure is a very cheap, very loud signal.

## What it constrains

- **A border is a claim about relatedness.** Draw one and you assert everything inside
  belongs together. Draw it carelessly and you assert something false.
- **It beats proximity, so use it to override.** When layout constraints force related
  things apart, an enclosure can still bind them.
- **Backgrounds count.** A subtle fill is an enclosure; a card is an enclosure. You are
  grouping whether or not you meant to.
- **Beyond the visual:** in text, the enclosure analogues are fenced code blocks,
  indented sections, `---` separators, and heading hierarchy. A config file's section
  headers make a common region — putting an unrelated key under `[network]` misfiles it
  in the reader's mind as surely as a stray border would. Same for a heading in a doc
  that scopes more than it should.

## Getting it wrong

- Boxing everything. When every group has a border, borders stop carrying information
  and only add visual noise.
- Enclosing items that merely happen to be adjacent in the data model rather than in the
  user's task.
- Nested enclosures more than two deep — the grouping claim becomes ambiguous and the
  reader stops trusting it.

## Related

- [[law-of-proximity]] — the weaker grouping signal that common region overrides.
- [[law-of-uniform-connectedness]] — the strongest grouping signal of the three.
- [[law-of-similarity]] — grouping by appearance rather than position.
