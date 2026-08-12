#!/usr/bin/env python3
"""guard-ds-code.py — PreToolUse(Write|Edit|MultiEdit) hook.

Denies writes that break a Designsystemet contract, with the reason fed back so
the model fixes it rather than the human catching it in review. The checks are
read from the pattern twin's `assertions` — the same field the A/B scorer reads,
so the guardrail and the test can never disagree about what "correct" means.

Python rather than the house bash, because the checks are derived from JSON
assertions at runtime; doing that in bash would hand-restate the twin.

Scope — it stays silent unless ALL of these hold:
  • the tool writes a .tsx/.jsx/.ts/.js file, and
  • the written content (or the file it edits) is Designsystemet code —
    it imports @digdir/designsystemet-react or uses ds-* classes.

What it denies:
  1. Invented props on Designsystemet components (the variant mechanism is data-color).
  2. `import { Suggestion }` — there is no such export.
  3. Raw hex colours (colours come from --ds-* tokens).
  4. Validation UI with no ErrorSummary — Write only, see below.

Check 4 needs the whole file to judge, so it runs only on Write, where the tool
input IS the whole file. On Edit the hook sees a fragment; judging composition
from a fragment would misfire on every partial edit, so it does not try.

Fails open: any missing twin, unreadable file, or unexpected input exits 0.
"""

import json
import os
import re
import sys
from pathlib import Path

# Sentinel prefixing every denial reason. Deliberately not made of ordinary words:
# the harness scans trial transcripts for it to count denials, and a crawling arm
# reads the design system's own docs, where a plain marker like "Designsystemet:"
# matches page headings and invents denials that never happened.
DENY = "ds-guard/deny: "

CODE_SUFFIXES = (".tsx", ".jsx", ".ts", ".js")
DS_MARKERS = ("@digdir/designsystemet", "ds-alert", "ds-suggestion", "ds-error-summary", "--ds-")
PATTERN_SLUG = "skjema-validering"


def twin_root():
    argv = sys.argv
    if "--twins" in argv:
        p = Path(argv[argv.index("--twins") + 1]).expanduser()
        if (p / "patterns").is_dir():
            return p
    env = os.environ.get("DESIGNSYSTEMET_TWINS")
    if env and (Path(env).expanduser() / "patterns").is_dir():
        return Path(env).expanduser()
    return None


def deny(reason):
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


def assertions(root):
    """Merged assertion specs from every bundled pattern twin; the primary pattern
    (skjema-validering) wins on id collision."""
    merged = {}
    for slug in ("required-and-optional-fields", PATTERN_SLUG):
        try:
            twin = json.loads((root / "patterns" / (slug + ".json")).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for a in (twin.get("assertions") or {}).get("value", []):
            merged[a["id"]] = a
    return merged


def tags_of(body, component):
    """Attribute text of every <Component ...> / <Component.Sub ...> occurrence."""
    pat = re.compile(r"<" + re.escape(component) + r"(?:\.\w+)?\b([^>]*?)/?>", re.DOTALL)
    return " ".join(m.group(1) for m in pat.finditer(body))


IMPORT_STMT = re.compile(r"^\s*import[\s\S]*?from\s*['\"][^'\"]+['\"];?", re.MULTILINE)


def check_invented_props(content, spec):
    hits = []
    for comp, props in (spec.get("forbidOn") or {}).items():
        attrs = tags_of(content, comp)
        for prop in props:
            if re.search(r"(?<![\w-])" + re.escape(prop) + r"\s*=", attrs):
                hits.append("`%s=` on <%s>" % (prop, comp))
    enum = spec.get("dataColorEnum") or []
    for val in re.findall(r"data-color\s*=\s*[\"'{]+\s*[\"']?([\w-]+)", content):
        if enum and val not in enum:
            hits.append("data-color=\"%s\" (not a Designsystemet colour)" % val)
    if not hits:
        return None
    return (
        DENY + "invented props — %s.\n"
        "The variant mechanism on these components is `data-color` (%s). "
        "Note `Button` genuinely has `variant`; the ban is per component.\n"
        "Call get_component() on the component for its real prop surface."
        % ("; ".join(hits), ", ".join(enum[:4]))
    )


def check_suggestion_import(content, spec):
    if spec.get("ifPresent", "Suggestion") not in content:
        return None
    imports = "\n".join(m.group(0) for m in IMPORT_STMT.finditer(content))
    if not imports or "designsystemet" not in imports:
        return None
    if spec.get("importMustMatch", "EXPERIMENTAL_Suggestion") in imports:
        return None
    if not re.search(r"import[\s\S]*?\bSuggestion\b[\s\S]*?from", imports):
        return None
    return (
        DENY + "there is no export named `Suggestion` — this breaks at build time.\n"
        "Use: import { EXPERIMENTAL_Suggestion as Suggestion } from '@digdir/designsystemet-react';\n"
        "Call get_component(\"suggestion\") for the subcomponent exports."
    )


def check_hex(content, spec):
    pattern = spec.get("forbidPattern", r"#[0-9a-fA-F]{3,8}")
    found = sorted(set(re.findall(pattern, content)))
    if not found:
        return None
    return (
        DENY + "raw hex colour(s) %s.\n"
        "Colours come from --ds-* tokens, never literal hex. "
        "Call get_component() for the component's --dsc-* to --ds-* token mapping."
        % ", ".join(found[:5])
    )


VALIDATION_MARKERS = ("ValidationMessage", "aria-invalid", "validation-message")

# --- v2 checks (2026-08-12) ---------------------------------------------------
# v1's validation checks only fired when the correct markers were ALREADY in the
# file, so only near-correct code was ever inspected: 24 trials shipped forms
# whose errors rendered as plain <Paragraph> text and the guard never fired
# (the guard-does-nothing class, claude-stack#176). These trigger on the
# ERROR-STATE EVIDENCE instead, however the error is rendered.

FIELD_COMPONENT = re.compile(
    r"<(Textfield|Textarea|Input|Select|Checkbox|Radio|Suggestion|EXPERIMENTAL_Suggestion|Field)\b")
ERROR_TEXT = re.compile(
    r"feilmelding|ugyldig|m\u00e5 fylles|kan ikke v\u00e6re tom|fyll ut|is required|"
    r"required field|invalid|error", re.IGNORECASE)
SUBMIT_HINT = re.compile(r"onSubmit|handleSubmit|preventDefault|setErrors?\b|validate", re.IGNORECASE)
REQUIRED_VOCAB = re.compile(r"obligatorisk|valgfri|\boptional\b|\brequired\b|m\u00e5 fylles ut", re.IGNORECASE)
REQUIRED_ATTR = re.compile(r"\brequired\b(?![\w-])|aria-required")


def check_error_state_wiring(content, spec):
    """A form with error-state evidence must carry aria-invalid — however the
    error text is rendered. Fires on evidence, not on markers."""
    if not FIELD_COMPONENT.search(content):
        return None
    if not SUBMIT_HINT.search(content):
        return None
    if not ERROR_TEXT.search(content):
        return None
    if "aria-invalid" in content:
        return None
    return (
        DENY + "this form renders validation errors, but no field carries aria-invalid.\n"
        "However the error text is displayed (ValidationMessage, Paragraph, anything), the "
        "invalid FIELD must be marked programmatically: aria-invalid={true} when invalid, "
        "and the error text linked with aria-describedby (Textfield's `error` prop does "
        "both for you). Screen readers announce the state from the attribute, not from "
        "nearby text. WCAG 3.3.1.\n"
        "Call get_pattern(\"skjema-validering\") for the full wiring."
    )


def check_required_programmatic(content, spec):
    """Required/optional MARKING vocabulary without programmatic required state."""
    if not FIELD_COMPONENT.search(content):
        return None
    if not REQUIRED_VOCAB.search(content):
        return None
    if REQUIRED_ATTR.search(content):
        return None
    return (
        DENY + "fields are marked required/optional in text, but no field carries the "
        "required attribute (or aria-required).\n"
        "The marking must be programmatic as well as visible: assistive technology reads "
        "the attribute, not the label suffix. Add required to the required fields; keep "
        "the visible word (the pattern forbids bare asterisks).\n"
        "Call get_pattern(\"required-and-optional-fields\") for the composition rules."
    )
# ------------------------------------------------------------------------------


def check_error_summary(content):
    if not any(m in content for m in VALIDATION_MARKERS):
        return None
    if "ErrorSummary" in content or "error-summary" in content:
        return None
    return (
        DENY + "this file reports field validation errors but has no ErrorSummary.\n"
        "The skjema-validering pattern requires BOTH: a per-field ValidationMessage and an "
        "ErrorSummary listing every error, placed near the submit control, each item linking "
        "to its field so activating it moves focus there. A lone Alert or lone "
        "ValidationMessage is not the pattern.\n"
        "Call get_pattern(\"skjema-validering\") for the full composition, timing, and a11y rules."
    )


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return

    tool = payload.get("tool_name")
    if tool not in ("Write", "Edit", "MultiEdit"):
        return
    ti = payload.get("tool_input") or {}
    path = ti.get("file_path") or ""
    if not path.endswith(CODE_SUFFIXES):
        return

    if tool == "Write":
        content = ti.get("content") or ""
    elif tool == "Edit":
        content = ti.get("new_string") or ""
    else:
        content = "\n".join((e.get("new_string") or "") for e in (ti.get("edits") or []))
    if not content.strip():
        return

    # Designsystemet code, or a fragment being edited into a Designsystemet file?
    context = content
    if tool != "Write":
        try:
            context = content + "\n" + Path(path).read_text(encoding="utf-8")
        except OSError:
            pass
    if not any(m in context for m in DS_MARKERS):
        return

    root = twin_root()
    if root is None:
        return
    try:
        asserts = assertions(root)
    except (OSError, ValueError, KeyError):
        return

    checks = [
        ("no-invented-props", check_invented_props),
        ("correct-suggestion-import", check_suggestion_import),
        ("tokens-not-hex", check_hex),
    ]
    for aid, fn in checks:
        a = asserts.get(aid)
        if not a:
            continue
        reason = fn(content, a.get("spec") or {})
        if reason:
            deny(reason)

    if tool == "Write":
        for aid, fn in (("aria-invalid-present", check_error_state_wiring),
                        ("required-programmatic", check_required_programmatic)):
            a = asserts.get(aid)
            if a:
                reason = fn(content, a.get("spec") or {})
                if reason:
                    deny(reason)
        reason = check_error_summary(content)
        if reason:
            deny(reason)


if __name__ == "__main__":
    main()
