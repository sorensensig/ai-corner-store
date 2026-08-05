# Fitts's Law

*Law `#3` in the Laws of UX collection [1]. Primary source: Fitts [4]. Synthesised, not
quoted.*

## What it says

The time to acquire a target is a function of the distance to it and its size. Far and
small is slow; near and large is fast. The relationship is logarithmic, not linear —
doubling the distance costs less than halving the size.

## Why it holds

Fitts modelled aimed movement as an information-transmission problem and found movement
time predicted by `MT = a + b·log₂(2D/W)`, where `D` is distance to target and `W` its
width [4]. The law has held across mice, touch, styluses, and eye-tracking for seventy
years — it describes the motor system, not a particular input device.

## What it constrains

- **Touch targets have a floor.** Below roughly 44×44 pt, error rates climb steeply.
  This is a physical constraint, not a style preference.
- **Screen edges are infinitely large in one dimension.** A target at an edge cannot be
  overshot, which is why menu bars and docks live there.
- **Distance is measured from where the pointer already is**, not from the centre of the
  screen. Contextual menus win because they appear under the cursor.
- **Destructive actions should be far and small; frequent actions near and large.** The
  law is as useful for making things *hard* to hit as easy.
- **Beyond the pointer:** the cost analogue for keyboard and CLI work is keystrokes and
  path depth. A command buried four subcommands deep is a small, distant target. So is a
  config value that requires knowing an undocumented key name. Aliases, sensible
  defaults and shallow verb hierarchies are Fitts's Law applied to text.

## Getting it wrong

- Shrinking a delete button to make it "less prominent" while leaving it adjacent to a
  common action — small *and* near is the worst combination for an irreversible control.
- Designing for the pointer's resting position at page load and ignoring where it
  actually is mid-task.
- Treating dense toolbars as efficient. Many small adjacent targets maximise both
  acquisition time and misclick rate.

## Related

- [[hicks-law]] — acquisition cost and decision cost compound; a big menu is slow twice.
- [[law-of-proximity]] — grouping shortens travel between related controls.
- [[teslers-law]] — complexity you refuse to absorb becomes distance the user travels.
