# Tesler's Law

*Law `#19` in the Laws of UX collection [1]. Primary source: Tesler [22]. Also known as
the Law of Conservation of Complexity. Synthesised, not quoted.*

## What it says

Every system has an irreducible amount of complexity. It cannot be removed — only moved.
The question is never *whether* someone deals with it, but **who**: the user, or the
people building the system.

## Why it holds

Tesler's observation from his work at Xerox PARC and Apple [22]: past a certain point,
simplifying the interface does not eliminate complexity, it relocates it. A field that
can be removed from a form because the system can infer the value has moved work from
the user to the engineer. A field removed because "it's cluttered" has moved work from
the engineer to the user.

**This is the law that stops the others from being abused.** [[occams-razor]] and
[[hicks-law]] both push toward fewer elements; Tesler's Law is the constraint that says
*fewer elements is not automatically simpler* — it names where the complexity went.

## What it constrains

- **The engineering side should absorb it.** Every time. The asymmetry is
  overwhelming: work done once in the system is done for every user forever; work pushed
  to users is repeated by each of them, every time, usually with errors.
- **Ask "where did the complexity go?"** whenever an interface gets simpler. If the
  answer is "into the user's head", the simplification was a cost transfer.
- **Beyond interfaces:** a CLI with sensible defaults absorbs complexity; one that
  requires eleven flags exports it. A tool that requires the operator to remember to run
  it has exported the hardest part — remembering — which is precisely what people are
  worst at while absorbed in work. This is the argument for ambient enforcement over
  invocable helpers: an element that must be remembered at the moment of need has pushed
  its complexity to exactly the wrong side.

## Getting it wrong

- **Hiding complexity and calling it removed.** Burying options in nested menus keeps
  the full cost and adds navigation on top.
- Absorbing complexity through magic that cannot be inspected or overridden. Users
  eventually hit the edge of the inference, and an opaque system offers no way through.
- Assuming the irreducible core is smaller than it is. Some domains are genuinely
  complex, and an interface pretending otherwise fails the expert without helping the
  novice.

## Related

- [[occams-razor]] — pushes toward fewer parts; this law bounds how far that can go.
- [[hicks-law]] — the same tension, for option sets specifically.
- [[postels-law]] — the input-boundary version of "the system absorbs it".
- [[millers-law]] — complexity pushed to the user is drawn against a hard ceiling.
