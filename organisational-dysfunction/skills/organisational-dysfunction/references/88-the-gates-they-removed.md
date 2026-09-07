# The gates they removed

*Dysfunction `#88` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-ugcPost-7500079164025204736-vfcn/) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- The move to a product model comes with a clearing-out: the CAB is disbanded, architecture review is "advisory now", the security gate and the privacy review are dropped from the pipeline. Lead time improves immediately, and everyone says so.
- The specialists whose sign-off was removed keep behaving as though they still have it. Architecture asks to see designs before build. Security wants to be consulted "early". Nobody granted them that, and nobody withdrew it either.
- Teams ship decisions they were never equipped to make — a data-retention choice, a boundary between two services, an authentication pattern — not recklessly, but because someone had to and no one said who.
- Six months in, the first real incident produces a question nobody can answer: who was supposed to catch this? The team says it wasn't told it owned that. The specialist says it wasn't asked.
- The correction is a new gate under a new name — a "product governance forum", an "architecture guild sign-off" — and delivery slows back to where it started, now with the ceremony of autonomy on top.

## The sociotechnical diagnosis

The gates were not the disease. They were a **compensating mechanism** for coordination sitting in the wrong place: authority over security, architecture, privacy and compliance was held by specialist functions organised apart from the work, so a checkpoint had to be inserted to bring the decision and the work back into contact. Slow, batched, and late — but real. It did something. Remove it and the something does not become unnecessary; it becomes **unassigned**.

That is the precise failure. Responsibility for coordination and control was not relocated to the teams, it was simply left unstated — which is not DP2 but **laissez-faire**, the absence of a design principle rather than the presence of a better one. DP2 is a positive design: a group with a whole task, the multiskilling to make the decisions that task contains, and the authority to make them stick. Deleting a checkpoint supplies none of those. It leaves specialists with responsibility and no authority, and teams with authority they were never told they had and no capability to exercise it. Both halves are now accountable for an outcome neither can control, which is the reliable recipe for the accountability gap that surfaces at the first incident.

Read it as **variance control**: every gate was a place where deviation got noticed and absorbed. Take the place away without building absorption into the team — the skills, the information, the mandate, the standard to work to — and the variance does not stop arriving. It travels downstream, gets absorbed by whoever happens to notice, or is not absorbed at all until it is an incident. And because the organisation never designed a replacement, the only remedy it can reach for is the one mechanism it knows how to build, so the gate returns. The question was never *whether* architecture, security and privacy decisions get controlled — they always do. It is only ever **where** that control sits, and removal is not an answer to that question.

## What to do

**The real fix is structural — you don't delete a gate, you relocate what it was doing.**
- For each removed checkpoint, name the decision it actually made, then say explicitly where that decision now lives. An unstated answer is the dysfunction; "the team owns it" only counts if the team knows and can.
- Move the capability, not just the accountability. Embed the specialists, rotate them, pair them into the teams — whatever puts the security, architecture and privacy skill inside the group that has to decide. DP2 requires multiskilling; a team cannot own a decision it cannot make.
- Replace sign-off with **standards and boundaries the team can work to on its own** — threat models it runs itself, architectural constraints stated as rules rather than opinions, privacy defaults built into the platform. Control at the point of work, applied continuously, instead of a batch check applied late.
- Redesign the specialist function's job at the same time. Its work becomes setting the constraints, building the tooling, and raising the teams' capability — not reviewing output. Left undefined, it will keep reaching for review, because that is the only role it has ever been given.
- When a gate does come back, treat it as evidence of a missing capability rather than a discipline problem, and ask which one. That question leads somewhere; "people aren't following the new model" does not.

**If you can't change the structure yet:**
- Write down what your team now decides without asking, and get it confirmed once, in writing, by whoever used to hold the gate. Most of the paralysis is uncertainty about mandate, not absence of it — and the written answer also exposes the genuinely unassigned items.
- Keep one lightweight list of the decisions you are making that used to be reviewed. It is the cheapest possible evidence when the accountability question arrives, and it makes the gap visible before an incident does rather than after.
- Invite the specialist in as a collaborator on the work rather than a reviewer of it. Same person, same expertise, at the point where it can still change the design — which is what they usually wanted anyway.
- Resist the reflex to reinstate a checkpoint the moment something goes wrong. Ask instead what the team would have needed to catch it itself, and argue for that. It is a slower answer and a much more durable one.

## Related

- [[removing-management]] — the identical subtraction one layer up: delete the holder, leave the function unowned, watch it reappear informally.
- [[the-bureaucracy-that-became-the-work]] — what the gates had grown into before they were removed, and why removal felt like the obvious fix.
- [[empowerment]] — the mirror case: authority announced but never transferred, where here it is transferred but never announced.
- [[the-project-in-product-clothing]] — the product model adopted as vocabulary and structure without the decision rights that make it work.
- [[the-blind-decision]] — the failure mode the gates institutionalised, and the reason removing them looked like progress.
