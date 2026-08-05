# laws-of-ux

Treat human limits — working memory, attention, tolerance for choice — as **hard design
constraints** rather than preferences.

21 psychological laws, each with what it says, why it holds, what it constrains, and how
it is commonly got wrong. The skill routes from a symptom to the specific law, so advice
cites a named constraint with a real limit attached instead of restating folk wisdom.

## What makes this different from a UX reading list

**It applies past the screen.** Every reference file has a *beyond the visual* section,
because a config file, a CLI, a prompt, an API surface, a code review and the set of
options a tool offers are all things a bounded human has to parse and choose from. The
laws do not care that there is no interface.

**It names the failure modes.** Several of these laws are misapplied more often than
applied — Miller's 7±2 as a cap on menu length is the canonical example, and it is
wrong. Each file's *getting it wrong* section is usually the more useful half.

**One law bounds the rest.** Most of these push toward less. Tesler's Law — complexity is
conserved, it only moves — is the check that stops "simpler" from meaning "we moved the
work onto the user".

## Install

```
/plugin marketplace add sorensensig/ai-corner-store
/plugin install laws-of-ux
```

## Structure

```
skills/laws-of-ux/
  SKILL.md          the shared lens + index, grouped by which limit is under pressure
  attribution.md    IEEE reference list; inline citations key to it by number
  references/       one file per law, 01–21
```

## Attribution

The collection and the framing as *laws of UX* are Jon Yablonski's. Each law's primary
source — Miller, Fitts, Hick, Kahneman, Zeigarnik, von Restorff, Tesler, Postel and the
Gestalt psychologists — is cited in `attribution.md` and referenced inline by number.

These files synthesise the findings in our own words and extend them to non-visual
surfaces. They do not reproduce Yablonski's text. For his own words, read the book:

> J. Yablonski, *Laws of UX: Using Psychology to Design Better Products & Services*,
> 2nd ed. O'Reilly Media, 2024.
