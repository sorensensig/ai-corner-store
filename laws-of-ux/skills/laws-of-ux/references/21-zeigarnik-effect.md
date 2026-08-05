# Zeigarnik Effect

*Law `#21` in the Laws of UX collection [1]. Primary source: Zeigarnik [24].
Synthesised, not quoted.*

## What it says

People remember uncompleted or interrupted tasks better than completed ones. An
unfinished task stays active in memory and keeps asking for attention until it resolves.

## Why it holds

Zeigarnik observed that waiters recalled unpaid orders in detail and forgot them almost
immediately once settled [24]. The interpretation is that an incomplete task maintains a
state of tension that keeps it accessible; completion discharges the tension and
releases the memory.

## What it constrains

- **Visible incompleteness pulls people back.** Progress indicators, partially filled
  profiles, and "3 of 7 steps done" all exploit this — the open loop is what returns
  users to the task.
- **Show the first step already taken.** A started task has far more pull than an
  unstarted one, which is why [[goal-gradient-effect]] and this effect compound.
- **Closure matters as much as the pull.** Unresolved loops accumulate as background
  load. An interface that opens many and closes few is exhausting rather than engaging.
- **Beyond onboarding:** this is why an interrupted work session is expensive — the open
  loop persists and costs attention even away from the desk. For long-running agent
  work, it is the argument for explicit completion signals: an operator who cannot tell
  whether a task finished carries it indefinitely. "Done, and here is what changed" is a
  memory release, not a formality.

## Getting it wrong

- **Manufacturing open loops to drive engagement.** Artificial incompleteness — endless
  badges, permanently incomplete profiles, deliberately withheld closure — is a dark
  pattern. It works, which is precisely the problem: it converts the user's attention
  into a resource extracted without consent.
- Opening loops the user cannot close. A notification about something not actionable
  costs the tension without offering the discharge.
- Forgetting to close loops you opened. A task marked started and never resolved lingers
  as low-grade load long after it stopped mattering.

## Related

- [[goal-gradient-effect]] — the acceleration that the open loop feeds.
- [[peak-end-rule]] — an experience without an ending never resolves.
- [[parkinsons-law]] — an unfinished task keeps drawing effort until something bounds it.
- [[doherty-threshold]] — a slow response is an involuntary interruption.
