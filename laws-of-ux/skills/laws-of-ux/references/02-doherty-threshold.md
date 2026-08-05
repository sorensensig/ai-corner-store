# Doherty Threshold

*Law `#2` in the Laws of UX collection [1]. Primary source: Doherty and Thadani [3].
Synthesised, not quoted.*

## What it says

Productivity rises sharply when a system responds to a person faster than **400 ms** —
fast enough that neither side waits for the other. Above that threshold, attention
detaches, and the cost is not merely the lost time but the lost train of thought.

## Why it holds

Doherty and Thadani's IBM work found that reducing system response time below roughly
400 ms produced a disproportionate jump in user productivity — a non-linear return, not
a smooth one [3]. Below the threshold, the interaction stays inside a single unit of
attention. Above it, the user's mind leaves, and re-entry costs far more than the delay
itself.

## What it constrains

- **400 ms is the budget, not 1 s.** The common "under a second feels instant"
  rule-of-thumb is already past the point where the productivity gain collapses.
- **Perceived duration is the variable you can always move.** Skeleton screens,
  optimistic UI, progressive rendering and accurate progress indicators all buy back
  attention even when the underlying work cannot be made faster. A progress bar that
  reports honestly beats a spinner that reports nothing.
- **Beyond the visual:** this is the law that governs agent and CLI interaction most
  directly. A tool that thinks silently for 30 s has lost the operator's attention long
  before it answers, and the operator returns to a wall of text with no memory of what
  they asked. Streaming output, an early "here is what I am about to do", and
  incremental results are not cosmetic — they are the difference between a collaborator
  and a batch job.

## Getting it wrong

- Optimising true latency while leaving perceived latency untouched — or the reverse,
  faking progress so persuasively that a genuinely stuck process looks healthy.
- Treating the threshold as a target for the median. Tail latency is where attention
  actually breaks; a p50 of 200 ms with a p99 of 8 s still feels unreliable.
- Adding artificial delay to make work "feel substantial". This trades a real cost
  (attention) for an imagined benefit (perceived value), and users adapt to the slower
  baseline anyway.

## Related

- [[goal-gradient-effect]] — visible progress is what keeps someone in the loop while
  they wait.
- [[zeigarnik-effect]] — an interrupted task stays live in memory; a slow response is an
  involuntary interruption.
- [[peak-end-rule]] — one very slow interaction can define the remembered experience.
