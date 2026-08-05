---
name: laws-of-ux
description: Treat human limits — working memory, attention, tolerance for choice — as hard design constraints rather than preferences. Use when designing or reviewing anything a person will read, operate, or choose from: interfaces and visual layout, but equally CLI output, config files, prompts, docs, API surfaces, error messages, and the set of options an agent offers. Triggers on questions about how many options to show, why something built never gets used, whether a layout groups correctly, how fast a response must feel, what people will remember, and on requests to simplify — especially where "simplify" may really mean "move the work onto the user".
---

# Laws of UX

Approach this as a designer who treats psychology as engineering constraint rather than
inspiration. The people who use what you build have fixed capacity, borrowed
expectations, and attention that leaves at 400 ms. Those are not preferences to be
balanced against business goals — they are the material properties of the medium, in the
same way tensile strength is a property of steel.

Hold these defaults as you work:

- **Cite the specific law, don't restate it.** Name the law and read its reference file
  before advising. "Users can't hold that much" is folk wisdom; [[millers-law]] with its
  actual limit, its chunking caveat, and its common misapplication is a tool.
- **These apply well beyond visual interfaces.** Every reference file has a *beyond the
  visual* section, because a config file, a CLI, a prompt, a set of options offered by an
  agent, and a code review are all things a bounded human must parse and choose from. The
  laws do not care that there is no screen.
- **Most laws push toward less. One law bounds that.** [[teslers-law]] is the check on
  the rest: complexity is conserved, so "simpler" is only real if the *system* absorbed
  it. If it moved to the user, that was a cost transfer wearing a principle as a
  disguise.
- **Name the failure mode, not just the law.** Each file's *getting it wrong* section is
  usually the more useful half — several of these laws are more often misapplied than
  applied.

The 21 reference files each cover one law: what it says, why it holds, what it
constrains, and how it fails. This file holds the shared lens — read it, then route.

## The core lens: capacity, perception, persistence

The laws sort into three questions, and most design problems are one of them wearing a
costume.

- **Capacity — how much can they hold and decide?** There is a hard ceiling on working
  memory and a logarithmic cost to every added option. Exceeding it does not produce a
  worse choice; it produces *no* choice. Governed by [[millers-law]], [[hicks-law]],
  [[occams-razor]], [[pareto-principle]], [[parkinsons-law]] — and bounded by
  [[teslers-law]].
- **Perception — what will they see as related?** Grouping happens pre-attentively and
  cannot be corrected afterwards by a caption. Structure is read before content.
  Governed by [[law-of-pragnanz]] and its four mechanisms, plus
  [[von-restorff-effect]] and [[fitts-law]].
- **Persistence — what survives over time?** What people remember diverges sharply from
  what they experienced, and unfinished things keep costing attention. Governed by
  [[serial-position-effect]], [[peak-end-rule]], [[zeigarnik-effect]],
  [[goal-gradient-effect]], [[doherty-threshold]].

Two laws sit across all three because they are about what users bring *with* them:
[[jakobs-law]] (expectations formed elsewhere) and [[postels-law]] (who absorbs the
messiness at the boundary).

**The diagnostic move:** when something built is not used, or is used wrongly, ask *which
human limit did this exceed?* The commonest answer is capacity, and the commonest
signature is **abandonment rather than error** — people not choosing at all, rather than
choosing badly. That signature points at [[hicks-law]], and it looks like apathy from the
outside, which is why it is usually misdiagnosed as a motivation problem.

## How to use this skill

1. **Identify which limit is under pressure** — capacity, perception, or persistence.
2. **Read the reference file(s)** for the matching law before advising. Several usually
   apply; that is normal, and the interaction between them is often the real finding.
3. **Check the *getting it wrong* section.** If the advice you are about to give appears
   there, give different advice.
4. **Run the Tesler check** on any recommendation that removes something: where did the
   complexity go? If the answer is "to the user", it is not a simplification.
5. **Cite by name** in your answer, so the reasoning is inspectable rather than assertive.

A link written `[[hicks-law]]` refers to `references/05-hicks-law.md` — find its number
in the index below.

## Attribution

The collection and the framing are Jon Yablonski's [1]; each law's primary source is
cited in `attribution.md` and referenced inline by number. These files synthesise the
findings in our own words and extend them to non-visual surfaces. They do not reproduce
Yablonski's text — for his own words, read the book.

## Index

### Capacity & decision — how much can they hold and choose between?
- `#12` **Miller's Law** — ~7±2 chunks, probably 4; the unit is a chunk, not an item. → `references/12-millers-law.md`
- `#5` **Hick's Law** — decision time grows with options; past a point, no decision at all. → `references/05-hicks-law.md`
- `#19` **Tesler's Law** — complexity is conserved; it moves, it does not vanish. → `references/19-teslers-law.md`
- `#13` **Occam's Razor** — fewest parts that still meet the requirement. → `references/13-occams-razor.md`
- `#14` **Pareto Principle** — most of the value sits in a small share of the surface. → `references/14-pareto-principle.md`
- `#15` **Parkinson's Law** — work expands to fill the time; scope needs a binding constraint. → `references/15-parkinsons-law.md`

### Perception & grouping — what will they see as related?
- `#9` **Law of Prägnanz** — the mind resolves ambiguity into the simplest reading, uninvited. → `references/09-law-of-pragnanz.md`
- `#8` **Law of Proximity** — nearness reads as relatedness; whitespace is the primary tool. → `references/08-law-of-proximity.md`
- `#10` **Law of Similarity** — likeness groups across distance; styling is a taxonomy. → `references/10-law-of-similarity.md`
- `#7` **Law of Common Region** — an enclosure groups, and overrides proximity. → `references/07-law-of-common-region.md`
- `#11` **Law of Uniform Connectedness** — explicit connection is the strongest grouping signal. → `references/11-law-of-uniform-connectedness.md`
- `#20` **Von Restorff Effect** — the different one is remembered; emphasis is scarce and inflates. → `references/20-von-restorff-effect.md`
- `#3` **Fitts's Law** — acquisition time from distance and size; also how to make things hard to hit. → `references/03-fitts-law.md`

### Persistence — what survives, and what keeps costing attention?
- `#18` **Serial Position Effect** — first and last survive; the middle is where things are forgotten. → `references/18-serial-position-effect.md`
- `#16` **Peak-End Rule** — experiences are judged by their peak and their ending, not their sum. → `references/16-peak-end-rule.md`
- `#21` **Zeigarnik Effect** — unfinished tasks stay live and keep asking for attention. → `references/21-zeigarnik-effect.md`
- `#4` **Goal-Gradient Effect** — effort rises as a visible finish line approaches. → `references/04-goal-gradient-effect.md`
- `#2` **Doherty Threshold** — under 400 ms keeps attention; above it, the mind leaves. → `references/02-doherty-threshold.md`

### What they bring with them
- `#6` **Jakob's Law** — expectations are formed on other products; convention is a budget. → `references/06-jakobs-law.md`
- `#17` **Postel's Law** — liberal in what you accept, conservative in what you send. → `references/17-postels-law.md`
- `#1` **Aesthetic-Usability Effect** — attractive things are perceived as more usable, and hide their own flaws. → `references/01-aesthetic-usability-effect.md`

If what you are looking at doesn't match any entry, reason from the core lens directly
rather than forcing a fit — and say which limit you think is under pressure.
