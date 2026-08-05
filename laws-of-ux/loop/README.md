# The laws-of-ux eval harness

Three measurements over `../evals/scenarios.json`. Dependency-free (Python 3 stdlib
only); drives the local `claude` CLI.

| file | role |
|---|---|
| `../evals/scenarios.json` | 34 scenarios — 27 positives with the law(s) they should route to, 7 near-miss negatives |
| `harness.py` | the eval core: triggering, routing, the judge rubric, and the lift control arm |
| `variance_check.py` | run the quant eval N times to measure score stability |
| `history/` | per-run reports (created on first run; gitignored) |

## The three measurements

- **Triggering** — should the skill fire, from its description alone? This description is
  deliberately broad ("anything a human will read, operate, or choose from"), so the
  negatives matter more here than they would for a narrower skill. They share vocabulary
  on purpose: a team of *seven* people, a *400ms* query, support *response time*.
- **Routing** — when it fires, does the index lead to the right law?
- **Lift** — does the skill actually beat an unaided model?

`composite = 0.5·triggering + 0.5·routing`, matching the sibling harness.

## Why lift is the one that matters

Triggering and routing measure whether the machinery works. Neither tells you whether the
corpus is worth loading — a skill can route perfectly to a file whose advice the model
would have given anyway.

So scenarios can carry a `trap`: a documented error models reliably make on that question.
`--mode lift` asks the model cold, checks whether the cold answer commits the error, then
checks the skilled answer.

```
lift     cold WRONG, skilled RIGHT   the skill earned its context
wash     both right                  the corpus added nothing here
no-help  both wrong                  the reference did not land
damage   cold right, skilled WRONG   the corpus made things worse
```

`lift_rate` is computed over *contested* scenarios only — the ones where the cold model
actually failed. Scenarios the base model already gets right cannot demonstrate lift, and
including them would inflate the number.

The clearest trap is `menu-length`. Asked how many nav items is too many, models reliably
cite Miller's 7±2 — the canonical misapplication, since Miller's limit governs what must be
*held in memory*, not what may be *visible*. The right answer is Hick's Law. If the skill
does not win that one, it is not doing anything.

The trap check is **judged, not string-matched**: the trap is a claim, not a phrase, and a
grep for "Miller" would fire on an answer that names Miller precisely to correct the error.

## Running it

> Each run makes several `claude -p` calls per scenario and consumes tokens. `--mode lift`
> is the most expensive — four calls per trap scenario (cold, cold-judge, skilled,
> skilled-judge). Start with `quant`.

```bash
cd loop

python3 harness.py --mode quant     # triggering + routing, ~2 calls/scenario
python3 harness.py --mode lift      # the control arm, ~4 calls/trap scenario
python3 harness.py --mode qual      # judge rubric on real answers

python3 variance_check.py --runs 3  # score stability across repeat runs
```

**Run `variance_check.py` before you believe any single score.** Two runs of an unchanged
skill can differ, and a difference smaller than that spread is noise, not a result. Check
the spread *below* the ceiling — a variance run taken at a perfect score reports zero by
construction and tells you nothing.

## There is deliberately no keep-best loop

The sibling skill has `run_loop.py`, which proposes changes and keeps them if a metric
improves. That is not copied here, for three reasons:

1. **This corpus is fixed.** 21 laws, no watcher, no routine adding entries. A loop's value
   is catching drift as content changes; nothing here changes unless a human changes it.
2. **It would saturate immediately.** 21 laws with distinct scopes leave little room before
   the metric hits its ceiling, after which iterations can only chase noise.
3. **The keep rule it uses has no noise margin** — a bare `trial > best` on a single run.

If routing between the Gestalt laws turns out to be genuinely confusable in practice —
Proximity, Common Region and Uniform Connectedness overlap more than most pairs — that is
the place a tuning loop might earn its keep. Measure first.

## Extending the scenario set

Add entries to `../evals/scenarios.json`. For a positive, set `should_trigger: true` and
list every acceptable law slug (filename without `.md`) in `expected_refs`. For a
near-miss, set `should_trigger: false` and `expected_refs: []`.

The most valuable additions are **traps** — questions where you can name the wrong answer a
model gives unprompted. Those are the only scenarios that measure whether the corpus is
pulling its weight.
