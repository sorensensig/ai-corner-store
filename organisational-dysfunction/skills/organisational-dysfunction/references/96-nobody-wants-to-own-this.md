# Nobody wants to own this

*Dysfunction `#96` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-ugcPost-7502054882032476160-yxBh/) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- A service half the organisation depends on was built years ago by a team that has since been reorganised away. Its commit history lists a dozen people, none of whom still think of it as theirs.
- When it breaks, every dependent team notices at once. When it needs an upgrade, every dependent team waits for someone else to do it.
- The same question shows up in chat every few months: who owns this? The replies say "we only consume it" or "I think that was the old platform team".
- Someone patches the immediate failure on the night, usually whoever is most blocked. Nobody fixes the underlying problem, because the next person to hit it would get the benefit, not them.
- It is on no roadmap and in no OKR, and working on it counts for nothing in anyone's review. So the people who do quietly keep it alive are spending time they will have to account for somewhere else.

## The sociotechnical diagnosis

Neglect like this gets read as apathy or as a prioritisation lapse, but it is neither. People care, and they would prioritise it if they could. The structure simply has nowhere to put it. **DP1** organises work by cutting it into owned pieces: services to teams, components to individuals, functions to departments. Each piece has a box, a manager above the box and a goal for the box. That logic works for anything that fits inside one box. It fails for anything *shared*, such as a platform everyone builds on, a legacy system too costly to replace, or a cross-cutting concern that belongs to the whole rather than any part. Those things sit in the gaps between the boxes, and in DP1 the gaps have no one assigned to them. The measurement regime makes that official: nothing that appears in no one's goals gets investment, because investing in it is invisible.

In **DP2**, a team owns a whole task end to end, and the **boundary location principle** requires the team's boundary to be drawn so that it contains what it needs to do that task. The team controls what it depends on. Seen that way, a widely shared dependency with no owner is not a gap in allocation to fix with a RACI chart. It is a **signal that the boundaries themselves are in the wrong place**: the work was sliced in a way that left something essential outside every team that relies on it. Variance in that service cannot be controlled at the point where it matters, because no unit contains both the service and the consequence of its failing.

So this is a design failure, not a prioritisation failure. Assigning the orphan to whichever team complains loudest does not change where the lines are drawn. That team gets a burden outside its own task, which it will neglect for the same structural reason.

## What to do

**The real fix is structural — redraw the boundaries so every essential dependency sits inside a unit that owns a whole task including it.**
- Map each ownerless dependency to the whole tasks that rely on it, then ask where a boundary would have to run for one team to control it *and* feel the consequences of it failing. Sometimes that means folding it into the team with the heaviest reliance. Sometimes it means a genuine platform team whose whole task, with real users, is the service.
- If it becomes a platform team, give that team the service as its primary task, with its own direction and a direct line to the teams using it. Otherwise it becomes a ticket desk that stands in for ownership without providing it.
- Let the affected teams do the redrawing together, in a participative redesign, rather than having boundaries handed down. The teams living with the gap know exactly where the lines went wrong.
- Remove the measurement reason for neglect: work that keeps a shared whole healthy has to count wherever the whole is judged.

**If you can't change the structure yet:**
- Keep a visible list of ownerless dependencies and when each one last hurt. That turns a string of one-off incidents into evidence of a design fault that someone with authority over boundaries has to look at.
- Among the dependent teams, agree an explicit interim stewardship, rotated and time-boxed, with the time spent on it written into each team's plan. Name it as a stopgap, so nobody mistakes it for the fix.
- Change the question. When someone asks "who owns this?", ask "which team's task is this part of, and why isn't it inside that team?" That moves the conversation from finding a volunteer to fixing a boundary.
- Protect the people who have been quietly carrying it. They are covering a structural gap on personal goodwill, and that is not a gap in their performance.

## Related

- [[passing-the-buck]] — accountability bouncing between fragments; here the fragment is a whole service with no box to land in.
- [[the-gates-they-removed]] — decisions that belong to no one after a restructure; this is the same gap, left behind by how the work was sliced.
- [[somebody-has-to-chase-it]] — cross-team work that moves only on one person's persistence, the informal patch this gap relies on too.
- [[team-topologies-the-wrong-way-round]] — naming a "platform team" without giving it the service as its whole task.
- [[local-optimisations]] — every box tends its own goals while the shared thing that serves all of them decays.
