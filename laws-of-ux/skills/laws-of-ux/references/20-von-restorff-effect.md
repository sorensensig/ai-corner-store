# Von Restorff Effect

*Law `#20` in the Laws of UX collection [1]. Primary source: von Restorff [23]. Also
known as the Isolation Effect. Synthesised, not quoted.*

## What it says

When several similar objects are present, the one that differs is the one remembered.
Distinctiveness buys attention and recall.

## Why it holds

Von Restorff found that an item isolated from its neighbours by any salient
difference — colour, size, shape, category — was recalled markedly more often than its
uniform peers [23]. The effect depends on contrast against a uniform field: it is a
property of the *set*, not of the item.

## What it constrains

- **Make the primary action visually distinct.** This is the mechanism behind a single
  emphasised button among plain ones.
- **Distinctiveness is a scarce resource.** It works only against uniformity. Two
  emphasised buttons are half as effective; five are none.
- **Beyond the visual:** the same scarcity governs warnings in text. One `⚠` in a long
  document is read; fifteen are wallpaper. A log where every line is `ERROR` conveys
  nothing. A prompt where every instruction is `IMPORTANT` and `NEVER` has no emphasis
  left for the instruction that genuinely is. Emphasis inflation destroys the channel it
  runs on.

## Getting it wrong

- **Relying on colour alone.** Colour-blind users and anyone in a high-glare
  environment loses the signal. Pair contrast with size, weight, position or an icon.
- Using motion as the differentiator without respecting `prefers-reduced-motion`; for
  some users animation is not merely distracting but disabling.
- Emphasising so much that nothing is emphasised. The commonest failure, and it is
  cumulative — each addition devalues every prior one.
- Making something distinctive that is not actually important. Attention is drawn
  regardless of merit, and misdirected attention is worse than none.

## Related

- [[law-of-similarity]] — this effect is the deliberate violation of it.
- [[serial-position-effect]] — the tool for rescuing an item from the forgettable middle.
- [[peak-end-rule]] — distinctive moments are candidates for the remembered peak.
