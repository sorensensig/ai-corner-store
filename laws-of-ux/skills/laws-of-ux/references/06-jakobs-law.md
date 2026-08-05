# Jakob's Law

*Law `#6` in the Laws of UX collection [1]. Primary source: Nielsen [8]. Synthesised,
not quoted.*

## What it says

Users spend most of their time on other products. They arrive expecting yours to work
the way those do, and every departure from that expectation is a cost you must justify.

## Why it holds

Nielsen's observation is about where mental models come from: they are built from
aggregate experience elsewhere, not from your product [8]. A convention is a
pre-installed model you get for free. Breaking it means paying to install a replacement,
in attention the user would rather spend on their actual task.

## What it constrains

- **Convention is a budget.** You can afford to break a few, in the places where your
  product's value genuinely differs. Spend it deliberately; novelty everywhere is
  bankruptcy.
- **Transitions are where the law bites hardest.** Redesigns that are objectively better
  still generate backlash, because existing users' models were the asset you just wrote
  off. Offering the old mode temporarily is a real mitigation, not a cop-out.
- **Beyond the visual:** conventions in developer tooling are just as load-bearing —
  `--help`, `-v`, exit code 0, `~/.config`, `Ctrl-C`. A CLI that repurposes a standard
  flag is not being expressive, it is being expensive. For agents, this extends to
  output shape: an agent that invents its own diff format makes every reader translate.

## Getting it wrong

- Invoking the law to justify never differentiating. The law says match expectations
  where they exist and departures are unjustified — not that novelty is forbidden.
- Copying a competitor's *interface* while missing that the convention lives in the
  broader category, not in that one product.
- Confusing familiarity with usability. A widely-copied bad pattern is still bad; it is
  merely cheap to learn. Weigh the switching cost against the ongoing cost.

## Related

- [[aesthetic-usability-effect]] — familiarity, like beauty, produces unearned confidence.
- [[law-of-pragnanz]] — both concern the mind's preference for the least effortful
  interpretation.
- [[postels-law]] — accepting varied input is how you tolerate models that differ from
  yours.
