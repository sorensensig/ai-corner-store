#!/usr/bin/env python3
"""Fill the skill's per-component fact block from the twins.

The skill body must never hand-restate what a twin already says — that is the
drift the twin exists to abolish, and the skill is where H1 gets dogfooded: one
source (the twin) feeds both the MCP and the skill.

    generate-skill-facts.py            # rewrite the block in place
    generate-skill-facts.py --check    # exit 1 if the block is stale

Twin root: --twins <path>, else $DESIGNSYSTEMET_TWINS, else ./twins.
"""

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN_ROOT = HERE.parents[2]  # scripts/ -> designsystemet -> digdir -> domains/work
SKILL = Path(__file__).resolve().parent.parent / "skills" / "designsystemet" / "SKILL.md"

# Deliberately NOT the `<!-- kind:id -->` shape: that belongs to the registry
# marker mechanic, and scripts/check-registry.sh rejects any such marker whose id
# is not a registry entry.
START = "<!-- BEGIN twin-facts (generated) -->"
END = "<!-- END twin-facts -->"


def twin_root(argv):
    if "--twins" in argv:
        return Path(argv[argv.index("--twins") + 1]).expanduser()
    if os.environ.get("DESIGNSYSTEMET_TWINS"):
        return Path(os.environ["DESIGNSYSTEMET_TWINS"]).expanduser()
    return Path.cwd() / "twins"


def value(twin, field):
    return (twin.get(field) or {}).get("value")


def render(root):
    lines = [START, ""]
    lines.append(
        "> Generated from the twins by `scripts/generate-skill-facts.py`. "
        "The tools above serve the full contract; this is the part you should not have to ask for."
    )
    lines.append("")

    # Only components that carry AUTHORED rules go inline. The rest are served on demand by
    # get_component. Two reasons: a component with an empty authored layer contributes a name
    # and nothing else, and the extracted layer it would contribute — props, import name — is
    # what agents already get right unaided from the TypeScript types. The authored layer is
    # the part they miss, and it is the only part worth spending context on.
    # Inline set: the form/validation cluster — the components the guard hook checks and
    # the pattern twins compose. Everything else has authored rules too (45/45 since
    # 2026-08-11) but is served on demand by get_component; inlining all 38 non-empty
    # components produced a 57 KB skill body, which taxes every session for knowledge
    # most tasks never touch. Pass --all to inline everything (for diffing/audit).
    INLINE = {"Alert", "ValidationMessage", "ErrorSummary", "Textfield", "Suggestion",
              "ToggleGroup", "Field", "Fieldset", "Label", "Button"}
    inline_all = "--all" in sys.argv
    skipped = 0
    for path in sorted((root / "components").glob("*.json")):
        twin = json.loads(path.read_text(encoding="utf-8"))
        a11y = value(twin, "a11y") or []
        comp = value(twin, "composition") or []
        rel = value(twin, "relations")
        if not (a11y or comp or rel):
            skipped += 1
            continue
        if not inline_all and twin["name"] not in INLINE:
            skipped += 1
            continue

        lines.append("### %s" % twin["name"])
        lines.append("")

        # importName is a bare string in generated twins and {exportedAs, note} in the older
        # hand-written ones. Accept both rather than crashing on whichever came second.
        imp = value(twin, "importName")
        if isinstance(imp, dict):
            note = (imp.get("note") or "").split(".")[0].strip()
            lines.append("- **Import:** `%s`%s" % (imp.get("exportedAs") or twin["name"],
                                                   " — %s." % note if note else ""))
        else:
            lines.append("- **Import:** `%s` from `%s`"
                         % (imp or twin["name"], twin["package"]["name"]))

        props = value(twin, "props") or []
        if props:
            lines.append("- **Real props:** %s" % ", ".join("`%s`" % p["name"] for p in props))

        # relations: a list of {component, note} in generated twins; a dict with a
        # boundaries.never list in the hand-written ones.
        if isinstance(rel, dict):
            for never in (rel.get("boundaries") or {}).get("never", []):
                lines.append("- **Never:** %s" % never)
        elif isinstance(rel, list):
            for r in rel:
                lines.append("- **Use instead — %s:** %s"
                             % (r.get("component"), r.get("note") or ""))

        for rule in a11y:
            wcag = ", ".join(rule.get("wcag") or [])
            lines.append("- **A11y%s:** %s"
                         % (" (WCAG %s)" % wcag if wcag else "", rule.get("rule")))
        for rule in comp:
            lines.append("- **Composition:** %s" % rule.get("rule"))

        if twin.get("needsReview"):
            lines.append("- *Authored rules drafted from the docs, not yet human-reviewed.*")

        lines.append("- Full contract: `get_component(\"%s\")`" % twin["slug"])
        lines.append("")

    if skipped:
        lines.append("%d further components have no authored rules yet — call "
                     "`list_twins()` to see them and `get_component(slug)` for a contract."
                     % skipped)
        lines.append("")

    for path in sorted((root / "patterns").glob("*.json")):
        twin = json.loads(path.read_text(encoding="utf-8"))
        lines.append("### Pattern · %s" % twin["name"])
        lines.append("")
        lines.append("- %s" % value(twin, "summary"))
        for comp in value(twin, "components") or []:
            lines.append("  - `%s` — %s" % (comp.get("ref") or comp.get("name"),
                                            comp.get("role", "")))
        for rule in value(twin, "composition") or []:
            lines.append("- **Composition:** %s" % (rule.get("rule") if isinstance(rule, dict) else rule))
        for rule in value(twin, "boundaries") or []:
            lines.append("- **Never:** %s" % (rule.get("rule") if isinstance(rule, dict) else rule))
        lines.append("- Full contract incl. timing + a11y: `get_pattern(\"%s\")`" % twin["slug"])
        lines.append("")

    lines.append(END)
    return "\n".join(lines)


def main():
    root = twin_root(sys.argv)
    if not (root / "components").is_dir():
        sys.exit("No twins at %s — pass --twins or set $DESIGNSYSTEMET_TWINS." % root)

    text = SKILL.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit("Markers %s / %s not found in %s" % (START, END, SKILL))

    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    updated = head + render(root) + tail

    if "--check" in sys.argv:
        if updated != text:
            sys.exit("STALE: %s does not match the twins. Run generate-skill-facts.py." % SKILL)
        print("OK: skill fact block matches the twins.")
        return

    SKILL.write_text(updated, encoding="utf-8")
    print("Wrote %s" % SKILL)


if __name__ == "__main__":
    main()
