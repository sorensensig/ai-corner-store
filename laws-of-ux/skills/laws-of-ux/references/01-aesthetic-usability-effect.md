# Aesthetic-Usability Effect

*Law `#1` in the Laws of UX collection [1]. Primary source: Kurosu and Kashimura [2].
Synthesised, not quoted.*

## What it says

People perceive attractive things as more usable than they actually are. Visual quality
buys a credit line against functional quality — and the credit is real: it changes what
users report, what they tolerate, and how long they persist before giving up.

## Why it holds

Kurosu and Kashimura tested 26 variations of an ATM interface and found apparent
usability correlated far more strongly with perceived aesthetic quality than with actual
ease of use [2]. Later work replicated the pattern. The mechanism is affective: a
positive first impression lowers perceived effort, and lowered perceived effort makes
people more forgiving of the friction they then hit.

## What it constrains

The effect cuts both ways, and the second way is the one that matters here.

- **It hides usability problems in testing.** Users of a polished prototype under-report
  friction they genuinely experienced. A beautiful thing that tests well may be testing
  its own beauty.
- **It buys tolerance you should spend deliberately.** The credit is finite. Use it to
  survive necessary complexity, not to avoid fixing avoidable complexity.
- **Beyond the visual:** the same halo attaches to *any* surface with evident care.
  A well-formatted CLI output, a config file with coherent naming and real comments, a
  clearly structured prompt — all read as more trustworthy and more correct than they
  are. An agent that formats its output beautifully will have its reasoning questioned
  less. That is a hazard, not a feature: presentation quality is not evidence quality.

## Getting it wrong

- Treating polish as a substitute for fixing the interaction. The credit runs out, and
  when it does the disappointment is sharper for the contrast.
- Reading positive usability-test sentiment on a high-fidelity prototype as validation
  of the *flow* rather than the *skin*. Test the flow at low fidelity if you want an
  honest read.
- Assuming the effect only applies to visual design. Any artefact that looks
  well-made — including generated output — inherits the halo.

## Related

- [[peak-end-rule]] — both concern remembered experience diverging from lived experience.
- [[jakobs-law]] — familiarity produces a similar unearned sense of ease.
- [[occams-razor]] — polish is not simplicity; a beautiful thing can still be overbuilt.
