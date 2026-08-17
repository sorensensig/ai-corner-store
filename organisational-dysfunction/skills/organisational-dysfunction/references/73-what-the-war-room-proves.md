# What the war room proves

*Dysfunction `#73` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-ugcPost-7491964720501923840-FtI0) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- A critical service breaks at 2am. Within ninety minutes a handful of people have diagnosed it, agreed a fix, deployed it, and gone back to bed — no approval sought, no ticket raised, no steering group consulted.
- The same engineer who found the root cause then spends three days getting sign-off to make the permanent fix, in daylight, on the same system.
- Incident mode suspends the rules explicitly: whoever is in the room decides, procurement is waived, the change window is ignored, and nobody later complains that this was reckless.
- People describe the incident afterwards as the organisation at its best — "that's how we should work all the time" — and then never ask why they don't.
- The postmortem examines the outage in detail and the *decision-making mode that resolved it* not at all. Everyone returns to the routine constraints without comment.

## The sociotechnical diagnosis

A war room is a **DP2** structure, stood up temporarily inside a **DP1** organisation. For the duration of the incident, control and coordination sit with the people doing the work: the group is multi-skilled, holds a whole task, sets its own next move, and coordinates peer-to-peer. Then the incident closes and the authority is withdrawn. The organisation has run a controlled experiment comparing its two design principles on the same people, the same systems and the same class of problem — and gets the answer every time.

What makes this the sharpest dysfunction in the library is that the evidence is already in the building. The usual objection to DP2 is that these particular people could not handle it: not senior enough, not accountable enough, would make a mess of it. The war room refutes that in ninety minutes. So the objection quietly changes shape — *incidents are different*, they need speed, exceptions are dangerous as a norm. But look at what the exception actually did: it moved **variance control to the point where the variance arose**. Emery and Trist's argument was never that this is a crisis tactic; it is the general condition for a system to absorb the disturbances it meets. Normal work throws up variances continuously — a wrong assumption, a broken dependency, an upstream change — and DP1 routes each one upward for a decision, adding delay and stripping context on the way. The 2am fix was fast because nothing was routed. The three-day fix was slow for exactly the same reason, inverted.

The framing of crisis-as-exception is what protects the design. Calling the war room *heroic* rather than *ordinary* keeps it an anomaly instead of evidence, and lets the organisation admire the outcome without drawing the inference. Meanwhile people learn something corrosive: the whole task, real authority and immediate feedback — several of the six psychological job requirements at once — are available to them only when something is on fire. Some will then start fires, or wait for one. Urgency becomes the currency you pay to get your job back.

## What to do

**The real fix is structural — treat incident mode as the working design and everyday mode as the deviation that needs justifying, not the reverse.**
- Take the incident's authority envelope and write it down as a standing one: what the team can decide, deploy, spend and change without asking. Start from what actually happened at 2am rather than from what governance would have permitted.
- For each approval gate the incident bypassed, ask what it was protecting and whether the bypass caused that harm. Gates that survive an outage untested were not controlling risk; they were controlling people.
- Give the team the whole task the war room briefly gave it — diagnose, decide, change, verify — instead of the fragment plus an escalation path.
- Add the design principle to the postmortem template as a standing question: which constraints did we suspend, and what would it cost to stop reimposing them?

**If you can't change the structure yet:**
- Instrument the comparison. Log the incident timeline against the equivalent routine change — hours to decision, hands it passed through, people consulted. Two dates and two numbers argue better than a principle does.
- Push for a *durable* exception rather than a general reform: one named class of change the team commits without approval, reviewed after a quarter. Concrete and reversible is easier to grant than reorganisation.
- When the praise arrives, redirect it from the people to the arrangement — the team was not better that night, its authority was. That reframing is the whole argument, and it costs nothing to make.
- Refuse the incident-as-heroism story about yourself, and don't let urgency become the only route to autonomy. It works, and it burns the people who use it.

## Related

- [[the-pilot-trap]] — the same shape in slow motion: a working demonstration the surrounding system will not generalise from.
- [[empowerment]] — authority described as delegated while the approval gate stays exactly where it was, until an outage removes it.
- [[the-bureaucracy-that-became-the-work]] — the approvals the war room suspends, seen on an ordinary Tuesday.
- [[permanent-urgency]] — what happens once crisis is the only mode in which people can actually act.
- [[fear-of-making-decisions]] — the daytime behaviour of the very people who decided in minutes at 2am.
