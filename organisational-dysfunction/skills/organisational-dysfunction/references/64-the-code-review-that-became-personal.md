# The code review that became personal

*Dysfunction `#64` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-ugcPost-7490287093722718208-Ds57) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- Two people's code reviews have an edge to them that the rest of the team's don't: comments are technically correct and somehow still cutting.
- Each round escalates — one gets defensive, the other doubles down on the critique, and both start saving up evidence for the next exchange.
- They stop engaging in meetings, route around each other's work, and the disagreement resurfaces in unrelated decisions.
- The team's explanation is "personality clash"; the team's fix is scheduling — split their work, assign different reviewers, keep them apart.
- Everyone treats it as a two-person problem, and nobody notices the same friction appearing, milder, elsewhere in the org.

## The sociotechnical diagnosis

A code review is a rare moment when one person's work is publicly judged by another. In a **DP2** structure that is an unremarkable act of peer coordination — the reviewer and the author share accountability for the same outcome, so a critique is information about the work. In a **DP1** structure the same act is loaded with status. Coordination sits above the work, which means visible competence is the currency of advancement, and a review is an occasion where that currency changes hands in front of witnesses. The comment is about the code; the exchange is about standing.

Merrelyn Emery's work is direct about what that environment does to relationships. DP1 produces asymmetric dependence, egocentrism, and the "them and us" syndrome — conditions in which small differences of style are consistently amplified into personal conflict. One person is terse; the other reads condescension. One person over-explains; the other reads a lecture. Neither reading is paranoid: in a structure where people compete for recognition, an unflattering assessment genuinely does cost something. The hothouse is doing exactly what it is designed to do.

The tell is what happens when the structure changes. Emery's finding is that the *same people* who have chronic conflicts under DP1 typically see those conflicts attenuate or disappear entirely under DP2 — not because anyone attended a communication course, but because the competitive stakes were removed and the differences went back to being differences. That is the strongest available evidence that the conflict was never located in the two individuals. Segregating them, meanwhile, removes the friction while preserving the cause, and quietly costs the team the review coverage and shared code ownership it needed.

## What to do

**The real fix is structural — remove the competition from the moment of critique, don't manage the personalities.**
- Make the outcome genuinely joint: the team owns the whole piece of work and is held to it collectively, so a defect found in review is a shared save rather than a mark against an author.
- Strip individual competence signalling out of the surrounding machinery — individual ratings, stack rankings, and per-person quality metrics turn every review into an input to someone's appraisal.
- Give the team authority to set and change its own review norms (what a review is *for*, when pairing replaces it, what "done" means), so the standard belongs to the group rather than to whoever argues hardest.
- Treat a recurring interpersonal conflict as a diagnostic signal about the structure. Where else is the same asymmetry showing up, more quietly?

**If you can't change the structure yet:**
- Move the disagreement out of the asynchronous written channel, which strips tone and rewards score-keeping, and into a short live conversation or a pairing session on the actual code.
- Make the criteria explicit and shared *before* the next review — an agreed standard is something two people can both point at, which is very different from one person's judgement of another's work.
- Resist the segregation fix if you're the one being asked to arrange it; it buys quiet at the price of the team's shared ownership.
- Reframe it for the team, and for yourself: these two are not incompatible people, they are two people being run through a structure that makes ordinary differences expensive.

## Related

- [[them-and-us]] — the same structural asymmetry at the level of whole groups rather than two individuals.
- [[fixing-people]] — the standard misdirected remedy: send them on a communication course instead of changing the conditions.
- [[the-error-factory]] — what happens when defects are counted against individuals; it is the same status logic applied to bugs.
- [[the-performance-review]] — individual appraisal inside work that is actually collective, and a main source of the competitive stakes.
- [[psychological-safety-as-a-patch]] — treating the symptom with safety talk while the structure keeps producing the threat.
