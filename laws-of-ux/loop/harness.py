#!/usr/bin/env python3
"""
harness.py — evaluation core for the laws-of-ux skill.

Dependency-free (stdlib only). Drives the local `claude` CLI to measure how well
the skill performs, on two axes:

  ROUTING   — given the router (SKILL.md) and a user scenario, does the model open
              the right reference file(s)?
  TRIGGERING — given only the skill's description and a user scenario, would the
              skill fire at all? (positives should fire, near-miss negatives should not)

And, for qualitative mode, an LLM-judge that scores the actual answer the skill
would produce against a rubric (faithful to OST, structural diagnosis, altitude-aware,
actionable).

This file is a library; run it via run_eval.py / run_loop.py, or directly:
    python3 harness.py eval --mode quant
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# --- paths -------------------------------------------------------------------

HARNESS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = HARNESS_DIR.parent
SKILL_DIR = PLUGIN_ROOT / "skills" / "laws-of-ux"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS_DIR = SKILL_DIR / "references"
SCENARIOS = PLUGIN_ROOT / "evals" / "scenarios.json"

DEFAULT_MODEL = "claude-opus-5"

# --- claude CLI --------------------------------------------------------------


def call_claude(prompt: str, model: str = DEFAULT_MODEL, timeout: int = 180) -> str:
    """Run `claude -p` headlessly, prompt on stdin, return stdout text.

    CLAUDECODE is stripped from the child env so this works when invoked from inside
    another Claude Code session (the nested-session guard otherwise refuses to launch).
    """
    child_env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        proc = subprocess.run(
            ["claude", "-p", "--model", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=child_env,
        )
    except FileNotFoundError:
        sys.exit("ERROR: `claude` CLI not found on PATH. Install it or adjust call_claude().")
    except subprocess.TimeoutExpired:
        return ""
    if proc.returncode != 0:
        sys.stderr.write(f"[claude error] {proc.stderr[:400]}\n")
    return proc.stdout.strip()


def _extract_json(text: str):
    """Pull the first JSON value (array or object) out of a noisy model reply."""
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


# --- skill introspection -----------------------------------------------------


def read_skill_md() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def get_description(skill_md: str = None) -> str:
    skill_md = skill_md or read_skill_md()
    m = re.search(r"^description:\s*(.+?)\s*$", skill_md, re.MULTILINE)
    return m.group(1) if m else ""


def valid_slugs() -> set:
    return {p.stem for p in REFS_DIR.glob("*.md")}


def load_scenarios() -> list:
    return json.loads(SCENARIOS.read_text(encoding="utf-8"))["scenarios"]


# --- the three probes --------------------------------------------------------


def probe_routing(scenario: dict, model: str) -> list:
    """Return the list of reference slugs the model would open for this scenario."""
    prompt = f"""You are deciding which reference file(s) of a skill to open.

Below is the skill's router file (SKILL.md). A user has said:

\"\"\"{scenario['prompt']}\"\"\"

Based ONLY on the router's index, which reference file(s) would you open to answer
well? Reply with a JSON array of the file identifiers (the `NN-slug` part, WITHOUT
the .md extension). If none of the laws genuinely fit, reply with [].
Reply with ONLY the JSON array, nothing else.

--- SKILL.md ---
{read_skill_md()}
"""
    reply = call_claude(prompt, model=model)
    data = _extract_json(reply)
    if not isinstance(data, list):
        return []
    return [str(x).replace(".md", "").strip() for x in data]


def probe_trigger(scenario: dict, model: str) -> bool:
    """Return whether the model thinks the skill should fire, from the description alone."""
    desc = get_description()
    prompt = f"""A Claude assistant has access to a skill with this description:

\"\"\"{desc}\"\"\"

The user says:

\"\"\"{scenario['prompt']}\"\"\"

Should Claude consult this skill to answer? Consider that skills should fire when they
genuinely add value and NOT for adjacent requests that merely share vocabulary.
Reply with ONLY one word: YES or NO."""
    reply = call_claude(prompt, model=model).upper()
    return reply.startswith("Y") or "YES" in reply[:10]


JUDGE_RUBRIC = [
    ("cites_a_named_law", "Names the specific law(s) that apply rather than offering unattributed folk wisdom. 'Users can't hold that much' scores 0; 'Miller's Law, and the unit is a chunk not an item' scores 1."),
    ("correct_law", "The law cited actually governs the situation. Reaching for Miller's Law on a question about option-set size is the canonical error — that is Hick's."),
    ("states_the_real_constraint", "Gives the actual limit or mechanism (400ms, ~4 chunks, logarithmic decision cost, contrast is a property of the set) rather than gesturing at the law's name."),
    ("tesler_check", "When recommending removal or simplification, says where the complexity went. Removing what the system can absorb is simplification; removing what the user must then supply is a cost transfer."),
    ("actionable", "Gives concrete, usable next steps rather than vague platitudes."),
]


def probe_answer(scenario: dict, model: str, refs: list) -> str:
    """Produce the answer the skill would give: router + the routed reference files + the prompt."""
    ref_texts = []
    for slug in refs:
        f = REFS_DIR / f"{slug}.md"
        if f.exists():
            ref_texts.append(f.read_text(encoding="utf-8"))
    bundle = "\n\n---\n\n".join(ref_texts) if ref_texts else "(no specific reference matched; reason from the core lens)"
    prompt = f"""You are answering a user using the 'laws-of-ux' skill.
Use the router guidance and the reference material below. Be sharp and concrete.

User:
\"\"\"{scenario['prompt']}\"\"\"

--- SKILL.md (router + lens) ---
{read_skill_md()}

--- Routed reference material ---
{bundle}
"""
    return call_claude(prompt, model=model)


def probe_judge(scenario: dict, answer: str, model: str) -> dict:
    rubric_lines = "\n".join(f"- {k}: {desc}" for k, desc in JUDGE_RUBRIC)
    prompt = f"""Score an answer that a design assistant gave to a user.

User asked:
\"\"\"{scenario['prompt']}\"\"\"

Answer to score:
\"\"\"{answer}\"\"\"

Score each criterion from 0.0 to 1.0:
{rubric_lines}

Reply with ONLY a JSON object: {{"<criterion>": <score>, ...}} using the exact keys above."""
    reply = call_claude(prompt, model=model)
    data = _extract_json(reply)
    keys = [k for k, _ in JUDGE_RUBRIC]
    if not isinstance(data, dict):
        return {k: 0.0 for k in keys}
    return {k: float(data.get(k, 0.0)) for k in keys}


def probe_unaided(scenario: dict, model: str) -> str:
    """The answer a model gives with NO skill loaded. The control arm for lift."""
    return call_claude(scenario["prompt"], model=model)


def probe_hit_trap(scenario: dict, answer: str, model: str) -> bool:
    """Did this answer fall into the scenario's known trap?

    Judged rather than string-matched, because the trap is a claim ('cites Miller's
    Law as a cap on menu length'), not a phrase. A grep for 'Miller' would fire on
    an answer that names Miller only to correct the misapplication — the opposite
    of what we are measuring.
    """
    prompt = f"""A user asked:

\"\"\"{scenario['prompt']}\"\"\"

An assistant replied:

\"\"\"{answer}\"\"\"

Here is a specific known error that assistants commonly make on this question:

\"\"\"{scenario['trap']}\"\"\"

Did the reply commit that error? Answer NO if the reply avoids it, or if it
mentions the material only to explicitly correct or reject the error.
Reply with ONLY one word: YES or NO."""
    reply = call_claude(prompt, model=model).upper()
    return reply.startswith("Y") or "YES" in reply[:10]


# --- scoring -----------------------------------------------------------------


def run_quant(model: str, verbose: bool = True) -> dict:
    """Routing + triggering accuracy across the scenario set."""
    scenarios = load_scenarios()
    rows = []
    for s in scenarios:
        positive = s["should_trigger"]
        triggered = probe_trigger(s, model)
        trigger_ok = (triggered == positive)

        routing_ok = None
        predicted = []
        if positive:
            predicted = probe_routing(s, model)
            expected = set(s["expected_refs"])
            routing_ok = bool(expected & set(predicted))  # lenient: any acceptable ref hit
        else:
            # negatives: routing should be empty / not over-eager
            predicted = probe_routing(s, model)
            routing_ok = (len(predicted) == 0)

        row = {
            "id": s["id"], "positive": positive,
            "triggered": triggered, "trigger_ok": trigger_ok,
            "expected_refs": s.get("expected_refs", []),
            "predicted_refs": predicted, "routing_ok": routing_ok,
        }
        rows.append(row)
        if verbose:
            mark = "✓" if (trigger_ok and routing_ok) else "✗"
            print(f"  {mark} {s['id']:<32} trig={'Y' if triggered else 'N'}({'ok' if trigger_ok else 'X'}) route={predicted or '[]'}")

    n = len(rows)
    trig_acc = sum(r["trigger_ok"] for r in rows) / n
    route_acc = sum(r["routing_ok"] for r in rows) / n
    composite = 0.5 * trig_acc + 0.5 * route_acc
    return {
        "mode": "quant", "model": model, "n": n,
        "trigger_accuracy": round(trig_acc, 4),
        "routing_accuracy": round(route_acc, 4),
        "composite": round(composite, 4),
        "rows": rows,
    }


def run_qual(model: str, verbose: bool = True, limit: int = None) -> dict:
    """LLM-judge rubric scores on the actual answers for positive scenarios."""
    scenarios = [s for s in load_scenarios() if s["should_trigger"]]
    if limit:
        scenarios = scenarios[:limit]
    rows = []
    for s in scenarios:
        refs = s["expected_refs"] or probe_routing(s, model)
        answer = probe_answer(s, model, refs)
        scores = probe_judge(s, answer, model)
        avg = sum(scores.values()) / len(scores) if scores else 0.0
        rows.append({"id": s["id"], "refs_used": refs, "scores": scores,
                     "avg": round(avg, 3), "answer": answer})
        if verbose:
            print(f"  {s['id']:<32} avg={avg:.2f}  " +
                  " ".join(f"{k[:6]}={v:.1f}" for k, v in scores.items()))
    overall = sum(r["avg"] for r in rows) / len(rows) if rows else 0.0
    return {"mode": "qual", "model": model, "n": len(rows),
            "overall": round(overall, 4), "rows": rows}


def run_lift(model: str, verbose: bool = True) -> dict:
    """Does the skill BEAT an unaided model, or only fire?

    Triggering and routing measure whether the machinery works. Neither measures
    whether the corpus is worth loading — a skill can route perfectly to a file
    whose advice the model would have produced unprompted.

    This runs the control arm. For each scenario carrying a `trap` (a documented
    error models reliably make on that question), it asks the model cold, checks
    whether the cold answer commits the error, then checks the skilled answer.

      lift   = cold WRONG and skilled RIGHT   <- the skill earned its context
      wash   = both right                     <- the corpus added nothing here
      damage = cold right and skilled WRONG   <- the corpus made things worse
    """
    scenarios = [s for s in load_scenarios() if s.get("trap")]
    rows = []
    for s in scenarios:
        cold = probe_unaided(s, model)
        cold_trapped = probe_hit_trap(s, cold, model)

        refs = s["expected_refs"] or probe_routing(s, model)
        skilled = probe_answer(s, model, refs)
        skilled_trapped = probe_hit_trap(s, skilled, model)

        if cold_trapped and not skilled_trapped:
            verdict = "lift"
        elif not cold_trapped and not skilled_trapped:
            verdict = "wash"
        elif cold_trapped and skilled_trapped:
            verdict = "no-help"
        else:
            verdict = "damage"

        rows.append({"id": s["id"], "cold_trapped": cold_trapped,
                     "skilled_trapped": skilled_trapped, "verdict": verdict,
                     "cold_answer": cold, "skilled_answer": skilled})
        if verbose:
            print(f"  {s['id']:<28} cold={'TRAP' if cold_trapped else 'ok  '} "
                  f"skilled={'TRAP' if skilled_trapped else 'ok  '}  -> {verdict}")

    n = len(rows)
    counts = {v: sum(r["verdict"] == v for r in rows) for v in ("lift", "wash", "no-help", "damage")}
    # Only scenarios where the cold model actually failed can demonstrate lift.
    contested = counts["lift"] + counts["no-help"]
    lift_rate = round(counts["lift"] / contested, 4) if contested else None
    return {"mode": "lift", "model": model, "n": n, "counts": counts,
            "contested": contested, "lift_rate": lift_rate, "rows": rows}


if __name__ == "__main__":
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "quant"
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else DEFAULT_MODEL
    runner = {"quant": run_quant, "qual": run_qual, "lift": run_lift}.get(mode, run_quant)
    result = runner(model)
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
