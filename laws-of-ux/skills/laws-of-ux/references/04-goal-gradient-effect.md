# Goal-Gradient Effect

*Law `#4` in the Laws of UX collection [1]. Primary source: Hull [5]. Synthesised, not
quoted.*

## What it says

Effort increases as people approach a goal. The closer the finish line looks, the harder
they push — and the more likely they are to finish at all.

## Why it holds

Hull observed rats running a maze faster as they neared the reward [5]. The pattern
replicates in humans and, importantly, responds to *apparent* rather than actual
progress: a loyalty card with ten slots of which two are pre-stamped gets completed more
often than an eight-slot card starting empty, despite requiring identical effort.

## What it constrains

- **Show progress, and show it early.** A progress indicator that starts at zero and
  moves slowly is worse than one that grants visible early advancement.
- **Endowed progress works.** Crediting a step already taken ("account created ✓")
  converts a cold start into a warm one honestly, because the step genuinely happened.
- **Break long tasks into visible stages.** Ten steps with a counter beat one opaque
  form of the same length.
- **Beyond onboarding flows:** this governs any long-running agent task. A run that
  reports "3 of 12 files reviewed" holds an operator who would abandon a silent
  equivalent. It is also why a task list that shows completed items is more than
  bookkeeping — the visible tail of finished work is what sustains the push through the
  remainder.

## Getting it wrong

- **Fake progress.** Endowed progress is honest when the credited step was real. Padding
  a bar to look advanced is a lie the user detects at the first stall, and it costs more
  trust than the effect ever bought.
- Progress bars that jump to 90% and sit there. The gradient works on *believable*
  proximity; an obviously stalled bar near the end reads as a failure, not a near-miss.
- Adding steps to make progress look granular. More steps is more work; the effect
  rewards visible advancement, not ceremony.

## Related

- [[zeigarnik-effect]] — an unfinished task's pull is what the gradient accelerates.
- [[doherty-threshold]] — progress feedback is how you hold attention past 400 ms.
- [[peak-end-rule]] — finishing strong is disproportionately what gets remembered.
