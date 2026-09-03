# The enterprise architect

*Dysfunction `#85` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-ugcPost-7500788467862462464-36-w/) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- A target operating model lands: capabilities decomposed, domains bounded, interfaces specified, ownership assigned. It is genuinely good work, and the leadership team recognises their business in it.
- Everyone signs it off, and nobody can say what is missing — only that something is. The model is accurate and somehow inert.
- Within a year the organisation has grown past it. Teams route around the boundaries, real work crosses the interfaces the wrong way, and the diagram is quietly no longer what happens.
- The architecture is never abandoned; it is never revised either. It stays on the wiki as the official shape, and drift from it is treated as non-compliance rather than as information.
- When something breaks, the response is to restore conformance to the model — never to ask whether the model is still the right one.

## The sociotechnical diagnosis

The method is borrowed, and the borrowing is the fault. Systems engineering works on **closed systems**: bounded, specifiable, designed to hold a stable state. You decompose the whole into components, optimise each, define the interfaces between them, and the behaviour of the whole follows from the parts. An organisation is an **open system** — it lives by exchange with an environment it does not control and cannot fully model, and its viability comes from continuously adapting to that environment rather than from holding a designed configuration. A diagram is a closed system by construction. Applying one to an open system produces something that is correct on the day it is drawn and structurally unable to stay correct.

Look at what decomposition does on the way in. Splitting the whole into components and specifying how they connect turns **relationships into interfaces**, which is exactly the move that makes coordination someone else's job: once each part holds a fragment optimised for its own contract, integrating them requires a level above the parts. That is **DP1 by construction** — the operating model does not choose redundancy of parts, it inherits it from the decomposition method. It also guarantees the classic OST failure of **suboptimising the whole**: every component can meet its interface and the system as a whole can still be losing, because the model has no representation of the whole except the sum of the boxes.

The missing thing the leadership team could feel has a name: the people who do the work were the object of the design, not its authors. In OST the design of the work is done *by* those who will live in it — the participative design workshop and the Search Conference exist for precisely this, because the knowledge of how variance actually arises and gets absorbed lives at the point of work and is not recoverable from a modelling exercise. An architecture produced above the work can only encode what was visible from up there. And this is why resilience is the wrong ambition to aim at it: **resilience returns a system to its designed state — it never asks whether that state is still right.** What an open system needs is active adaptation, which means the capacity to change the design, held by people close enough to the environment to notice it has moved.

## What to do

**The real fix is structural — stop treating the organisation as a system to be specified, and build the capacity to redesign it where the work meets the environment.**
- Make the architecture a **hypothesis with an owner and a review**, not an approved end state. If nothing about it can change without a governance cycle, it will be wrong long before it is revised.
- Design **with** the people who do the work, not for them — participative design workshops rather than a modelling exercise validated in a review board. What the diagram cannot see is exactly what makes it inert.
- Locate the boundaries around **whole tasks with a real outcome**, not around functional capabilities. Decomposing by capability optimises for control and buys suboptimisation of the whole; decomposing by outcome keeps the coordination inside the team that owns it.
- Judge the architecture on **adaptation, not conformance**. Drift from the model is data about the environment. An organisation that outgrew its architecture in a year did not fail to comply; it told you the model was closed.

**If you can't change the structure yet:**
- Publish the model's assumptions alongside the model — what environment it assumes, what it optimises for, what would falsify it. An architecture whose assumptions are visible can be argued with; one that is just boxes can only be complied with.
- When drift shows up, describe it as a finding rather than a violation. "Three teams route around this boundary" is a design input; "three teams are non-compliant" ends the conversation.
- Get the people who live the handoffs into the room before the next revision, even informally. One session with the people crossing an interface will tell you more about it than another modelling pass.
- Be careful with "we just need better governance". That adds a level above a problem caused by there being a level above, and it will feel like progress for about two quarters.

## Related

- [[built-for-yesterday]] — the same architecture a few years on, still authoritative and no longer describing anything real.
- [[local-optimisations]] — what decomposition-by-capability reliably produces: every box meeting its contract while the whole loses.
- [[team-topologies-the-wrong-way-round]] — the team-shaped version of the same mistake, copying a diagram without moving authority.
- [[the-market-we-think-we-shape]] — mistaking the internal model of the environment for the environment itself.
- [[rearranging-the-furniture]] — redesign performed *on* the work by people above it, which is why it doesn't take.
