#!/usr/bin/env python3
"""Rebuild the bundled registry snapshot from a designsystemet fork checkout.

Not a plain copy — four transforms:
  1. kebab-case filenames (Alert.json -> alert.json), matching the server's slugs
  2. strip EXPERIMENTAL_ prefixes and dots from filenames
  3. inject the guard's assertion specs into the pattern twins from the fork's
     rubrics — the assertions are the guard hook's checklist
  4. rewrite llms.txt link targets to the kebab-cased filenames

    python3 scripts/sync_registry.py <fork-root>
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

    if (src / "llms.txt").exists():
        text = (src / "llms.txt").read_text()
        text = re.sub(r"\((components|patterns)/([^)]+)\.json\)",
                      lambda m: "(%s/%s.json)" % (m.group(1), kebab(m.group(2))), text)
        (DEST / "llms.txt").write_text(text)

    n = len(list((DEST / "components").glob("*.json")))
    print("synced %d components, %d patterns (%d with assertions) from %s"
          % (n, len(list((DEST / "patterns").glob("*.json"))), injected, src))


if __name__ == "__main__":
    main()
