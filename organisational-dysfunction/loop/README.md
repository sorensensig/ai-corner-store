# The loop harness

An autoresearch-style evaluation + improvement loop for the `organisational-dysfunction` skill,
inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch): a fixed metric, an
agent that proposes a change, keep-if-better / revert-if-worse, logged each iteration.

It is **dependency-free** (Python 3 stdlib only) and drives the local `claude` CLI.

## Files

| file | role |
|---|---|
| `../evals/scenarios.json` | the scenario set — positives (with the reference they *should* route to) and near-miss negatives |
| `harness.py` | evaluation core: routing / triggering probes + the LLM-judge rubric |
| `run_loop.py` | the keep-best loop (quant) and the judge+suggestions report (qual) |
| `research.md` | the optimiser's brief — what to change, what not to, how to read failures |
| `history/` | per-iteration reports + `history.jsonl` (created on first run) |

## The two metrics

- **Triggering** — should the skill fire? Positives yes; near-misses that merely share vocabulary
  ("reword these OKRs", "summarise my performance review PDF", "optimise these slow queries") no.
- **Routing** — when it fires, does the router lead to the right reference file?

`composite = 0.5·triggering + 0.5·routing`.

## Running it

> Each run calls `claude -p` many times and consumes tokens/billing. Start small.

```bash
cd loop

# One-off score, no changes:
python3 harness.py eval --mode quant

# Quant keep-best loop (auto-tunes description + router; reverts regressions):
python3 run_loop.py --mode quant --iterations 5

# Qualitative judge pass over the actual answers -> writes history/qual-suggestions.md for you:
python3 run_loop.py --mode qual --limit 8

# Pin a model (defaults to claude-opus-5):
python3 run_loop.py --mode quant --iterations 5 --model claude-opus-5
```

## Modes, and why they differ

- **quant** auto-applies changes, but only to the **description** and the **router index** — the
  levers the metric actually measures — so it is safe to leave running. It never touches reference
  prose. Best version is left on disk; every iteration is logged.
- **qual** runs the rubric judge (structural diagnosis, OST fidelity, altitude-awareness,
  actionability, rings-true) on the real answers, finds the weakest references, and writes concrete
  improvement suggestions to `history/qual-suggestions.md`. It deliberately does **not** rewrite
  advice automatically — that stays a human decision.

## Extending the scenario set

Add entries to `evals/scenarios.json`. For a positive, set `should_trigger: true` and list every
acceptable reference slug (filename without `.md`) in `expected_refs`. For a near-miss, set
`should_trigger: false` and `expected_refs: []`. The most valuable additions are tricky negatives
and scenarios that currently route to the wrong place.

## Measuring noise before trusting a delta

`variance_check.py` runs the quant harness N times on the CURRENT skill with no
change applied and reports per-metric spread. Run it before attributing any
composite delta to a change — the keep rule's `NOISE_MARGIN` in `run_loop.py`
(0.02, issue #17) was derived from exactly such a pair (0.9655 vs 0.9828,
same config). Two rules of use:

1. Measure OFF the ceiling. A variance run at composite 1.0 reports
   stdev 0.0 structurally — nothing can score higher — and says nothing
   about the metric (this happened once and looked like proof of stability).
2. If the metric, model, or scenario set changes, re-derive the margin from
   a fresh variance run; the stored `best` must also be re-baselined on the
   new model or the margin will reject every candidate indefinitely (#15).
