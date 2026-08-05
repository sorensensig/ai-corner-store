# Postel's Law

*Law `#17` in the Laws of UX collection [1]. Primary source: Postel [19]. Also known as
the Robustness Principle. Synthesised, not quoted.*

## What it says

Be liberal in what you accept, and conservative in what you send. Tolerate variety and
imperfection at the input boundary; emit output that is predictable and strictly
correct.

## Why it holds

Postel stated it for TCP implementations in RFC 761 [19]: an implementation should
handle any input it can reasonably interpret while producing strictly conformant output.
Applied to people, the asymmetry is the point — humans are variable, imprecise and
error-prone at input, and intolerant of ambiguity at output.

## What it constrains

- **Accept every reasonable input format.** Phone numbers with spaces, dates in any
  sane order, pasted values with trailing whitespace. Normalise silently rather than
  rejecting; a validation error over a stray space is the system refusing to do work it
  is far better at than the user.
- **Design for variable ability and context**, not just variable formatting — different
  input devices, assistive technology, one-handed use, poor connectivity.
- **Be strict on the way out.** Predictable, well-formed, consistent output is what
  makes a system composable and trustworthy.
- **Beyond forms:** this is the contract for agent interaction. Accept a vague, messy,
  contradictory request and do the work of interpreting it — that is the value on offer.
  Emit structured, consistent, verifiable output. An agent that demands precisely
  formatted instructions has inverted the law and pushed its job onto the user.

## Getting it wrong

- **Over-accepting into ambiguity.** Postel's principle has a well-documented failure
  mode in protocol design: liberal acceptance lets non-conformant implementations
  proliferate until the tolerance itself becomes the de facto spec, and security holes
  hide in the gap between what is accepted and what is expected. When intent is
  genuinely unclear, ask — do not guess liberally.
- Accepting anything and then failing obscurely three steps later. Tolerance at the
  boundary requires clarity about what was understood.
- Treating "conservative in what you send" as licence for terse, unhelpful output.
  Strict means well-formed, not minimal.

## Related

- [[jakobs-law]] — accepting varied input is how you accommodate models formed elsewhere.
- [[teslers-law]] — this law decides who absorbs the irreducible complexity.
- [[aesthetic-usability-effect]] — clean output earns trust the input handling must merit.
