#!/usr/bin/env python3
"""Rebuild the bundled registry snapshot from a designsystemet fork checkout.

The bundle is NOT a plain copy — three transforms, each of which shipped a silent
failure when done by hand (see PR #39):

  1. kebab-case filenames (Alert.json -> alert.json) — the twins server's slug
     discipline; CamelCase files resolve to nothing.
  2. strip EXPERIMENTAL_ prefixes and dots from names.
  3. inject the guard's assertion specs into the pattern twins from the fork's
     rubrics — the public registry is answer-key-stripped (an experiment
     concern), but the assertions ARE the guard's checklist (a product need).

    python3 scripts/sync_registry.py <fork-root>   # e.g. ~/…/designsystemet/fork
"""
import json
import re
import shutil
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
DEST = PLUGIN / "registry"


def kebab(stem):
    name = stem.replace("EXPERIMENTAL_", "").replace(".", "-")
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower().replace("--", "-")


def main():
    fork = Path(sys.argv[1]).expanduser().resolve()
    src = fork / "registry"
    rubrics = fork.parent / "tests" / "rubrics"
    if not (src / "components").is_dir():
        sys.exit("no registry/components under %s" % fork)

    shutil.rmtree(DEST, ignore_errors=True)
    (DEST / "components").mkdir(parents=True)
    (DEST / "patterns").mkdir(parents=True)

    for p in sorted((src / "components").glob("*.json")):
        shutil.copy(p, DEST / "components" / (kebab(p.stem) + ".json"))

    injected = 0
    for p in sorted((src / "patterns").glob("*.json")):
        twin = json.loads(p.read_text())
        rub = rubrics / p.name
        if rub.exists():
            a = json.loads(rub.read_text()).get("assertions")
            if a:
                twin["assertions"] = a
                twin.pop("rubricOnly", None)
                injected += 1
        (DEST / "patterns" / (kebab(p.stem) + ".json")).write_text(
            json.dumps(twin, indent=2) + "\n")

    for extra in ("llms.txt",):
        if (src / extra).exists():
            shutil.copy(src / extra, DEST / extra)

    n = len(list((DEST / "components").glob("*.json")))
    print("synced %d components, %d patterns (%d with assertions) from %s"
          % (n, len(list((DEST / "patterns").glob("*.json"))), injected, src))


if __name__ == "__main__":
    main()
