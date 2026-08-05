# Law of Prägnanz

*Law `#9` in the Laws of UX collection [1]. Primary sources: Wertheimer [10] and Koffka
[11]. Synthesised, not quoted.*

## What it says

The eye resolves ambiguous or complex forms into the simplest interpretation available.
"Prägnanz" — roughly, *conciseness* or *good figure* — is the Gestalt claim that
perception minimises cognitive effort automatically and without permission.

## Why it holds

Koffka framed it as the organising principle beneath the other Gestalt laws [11]:
proximity, similarity, common region and connectedness are all routes by which the mind
arrives at the least effortful reading. Simplification is not a preference the viewer
applies; it is what perception *is*.

## What it constrains

- **Complexity gets simplified whether you like it or not.** If your structure is
  ambiguous, the viewer will resolve it — possibly into something you did not intend and
  cannot later correct.
- **Simple, symmetrical forms are processed faster and remembered longer.** This is the
  psychological argument for a restrained icon set and a regular grid, independent of
  taste.
- **Beyond the visual:** the same forcing function applies to any structure a person
  parses. An ambiguous API surface gets resolved into whatever mental model is simplest,
  and that model becomes what people believe your system does. Ambiguous documentation
  headings get collapsed into a simpler hierarchy than you wrote. A prompt with unclear
  precedence between instructions gets read — by humans and models alike — as the
  simplest consistent reading, not the one you meant.

## Getting it wrong

- Treating this as licence to strip information until the thing is simple but no longer
  says what it needs to say. Prägnanz describes *perception*, not a target for content
  reduction — see [[occams-razor]] for the discipline that actually governs that.
- Leaving structural ambiguity unresolved and assuming a caption or tooltip will correct
  the reading. The simplification already happened, pre-attentively.
- Assuming your intended reading is the simplest one available. Test with someone who
  has no context; they will find the simplest reading, and it may not be yours.

## Related

- [[law-of-proximity]], [[law-of-similarity]], [[law-of-common-region]],
  [[law-of-uniform-connectedness]] — the specific mechanisms Prägnanz operates through.
- [[occams-razor]] — the design discipline, as distinct from this perceptual tendency.
- [[millers-law]] — simplification is partly a response to a hard capacity limit.
