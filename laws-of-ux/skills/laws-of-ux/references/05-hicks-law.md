# Hick's Law

*Law `#5` in the Laws of UX collection [1]. Primary sources: Hick [6] and Hyman [7].
Synthesised, not quoted.*

## What it says

The time to make a decision grows logarithmically with the number and complexity of
choices. More options is not merely slower — past a point it produces *no* choice at
all.

## Why it holds

Hick and Hyman independently established that reaction time scales with the information
content of the choice set, `RT = a + b·log₂(n+1)` [6], [7]. Schwartz later documented
the behavioural consequence: beyond a moderate number of options, people defer, abandon,
or default rather than choose, and report lower satisfaction with whatever they do pick
[25].

**This is the most load-bearing law in this library.** The failure mode it predicts is
*no choice*, not *wrong choice* — and that signature is what distinguishes overload from
ordinary friction when you are diagnosing why something built never gets used.

## What it constrains

- **Categorise rather than enumerate.** Grouping ten options into three categories of
  three or four beats a flat list of ten, because the decision becomes two cheap
  decisions instead of one expensive one.
- **Highlight a recommended option.** A default converts a choice into a confirmation.
- **Stage complexity.** Progressive disclosure defers options until they are relevant,
  which is the same log reduction applied over time.
- **Beyond menus:** the option set an agent offers is a choice set governed by this law.
  Presenting four approaches with balanced trade-offs and no recommendation is a
  well-intentioned way of producing paralysis. So is a config file with forty tunables,
  a CLI with thirty flags, or a library of skills large enough that remembering which
  one applies is itself the bottleneck.

## Getting it wrong

- Using the law to justify hiding necessary functionality. The goal is fewer decisions
  *at once*, not fewer capabilities — see [[teslers-law]] for what happens when you
  simply remove the complexity from view.
- Counting options without weighing their complexity. Five similar options can be harder
  than eight clearly distinct ones; the law's term is information content, not item
  count.
- Offering choices at all where a sensible default would do. The cheapest decision is
  the one nobody has to make.

## Related

- [[millers-law]] — the memory ceiling that makes long option lists unholdable.
- [[teslers-law]] — complexity removed from the interface has to go somewhere.
- [[occams-razor]] — the discipline of not adding the option in the first place.
- [[fitts-law]] — a long menu costs decision time *and* travel time.
