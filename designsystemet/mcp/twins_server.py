#!/usr/bin/env python3
"""twins_server.py — MCP server over the Designsystemet structured twins.

Serves the `.json` contract twins (the level-2 relational contract) to an agent
that has the plugin installed. Situation 1 in the control gradient; the same
twins are what a cold-crawling agent fetches over HTTP in situation 2.

    MCP client (Claude Code)
        <── JSON-RPC 2.0 / newline-delimited stdio ──>
    THIS SCRIPT
        <── filesystem reads ──>
    twins/  (components/*.json, patterns/*.json, llms.txt)

Tools: list_twins, get_component, get_pattern, find_equivalent.

Dependency-free on purpose: stdlib only, Python 3.9+. The A/B harness treats a
failed server start as a void trial, so the server must not depend on a pip
install being present in whatever environment a sub-agent runs in.

Twin root resolution, first hit wins:
  1. --twins <path>
  2. $DESIGNSYSTEMET_TWINS
  3. ./twins or ./fork/twins relative to the working directory
"""

import json
import os
import re
import sys
from pathlib import Path

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "designsystemet-twins"
SERVER_VERSION = "0.1.0"

TRANSLATION_RULE = (
    "Map each element to its Designsystemet equivalent and emit that component's real "
    "API. Never reproduce another design system's component names, class names, or "
    "colour values — no foreign classes, no raw hex, no invented props."
)

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Twin loading


def resolve_twin_root(argv):
    candidates = []
    if "--twins" in argv:
        candidates.append(Path(argv[argv.index("--twins") + 1]))
    if os.environ.get("DESIGNSYSTEMET_TWINS"):
        candidates.append(Path(os.environ["DESIGNSYSTEMET_TWINS"]))
    cwd = Path.cwd()
    candidates += [cwd / "twins", cwd / "fork" / "twins"]
    for c in candidates:
        c = c.expanduser()
        if (c / "components").is_dir() or (c / "patterns").is_dir():
            return c
    return None


TWIN_ROOT = resolve_twin_root(sys.argv)


def twin_path(kind, slug):
    """kind is 'components' or 'patterns'. Slug is sanitised — no traversal."""
    if TWIN_ROOT is None:
        return None
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug or ""):
        return None
    p = TWIN_ROOT / kind / (slug + ".json")
    return p if p.is_file() else None


def load_twin(kind, slug):
    p = twin_path(kind, slug)
    if p is None:
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def all_twins():
    """[(kind, slug, twin_dict)] for every twin on disk."""
    out = []
    if TWIN_ROOT is None:
        return out
    for kind in ("components", "patterns"):
        for p in sorted((TWIN_ROOT / kind).glob("*.json")) if (TWIN_ROOT / kind).is_dir() else []:
            try:
                out.append((kind, p.stem, json.loads(p.read_text(encoding="utf-8"))))
            except (OSError, ValueError):
                continue
    return out


def load_equivalents():
    p = HERE / "equivalents.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"aliases": {}, "known_without_twin": {}}


# ---------------------------------------------------------------------------
# Tool implementations


def missing_root_error():
    return {
        "error": "No twin root found.",
        "looked_for": "--twins <path>, $DESIGNSYSTEMET_TWINS, ./twins, ./fork/twins",
        "fix": "Point DESIGNSYSTEMET_TWINS at the directory holding components/ and patterns/.",
    }


def tool_list_twins(_args):
    if TWIN_ROOT is None:
        return missing_root_error()
    entries = []
    for kind, slug, twin in all_twins():
        entries.append(
            {
                "kind": twin.get("kind", kind.rstrip("s")),
                "slug": slug,
                "name": twin.get("name"),
                "summary": (twin.get("summary") or {}).get("value"),
                "fetch_with": ("get_pattern" if kind == "patterns" else "get_component"),
            }
        )
    return {
        "twin_root": str(TWIN_ROOT),
        "count": len(entries),
        "twins": entries,
        "how_to_use": [
            "Building a screen? Read the pattern twin first — it names the components, "
            "their order, the timing rules, and the a11y requirements code does not enforce.",
            "Then read each component twin for the real props, the real import name, and the tokens.",
            "`extracted` fields are derived from Designsystemet source and cannot drift; "
            "`authored` fields carry the package version they were last reviewed against.",
        ],
    }


def tool_get_component(args):
    if TWIN_ROOT is None:
        return missing_root_error()
    slug = (args.get("slug") or "").strip().lower()
    twin = load_twin("components", slug)
    if twin is None:
        known = [s for k, s, _ in all_twins() if k == "components"]
        pattern_refs = load_equivalents().get("known_without_twin", {})
        hint = pattern_refs.get(slug)
        return {
            "error": "No component twin for slug %r." % slug,
            "known_component_slugs": known,
            "note": hint or "Call list_twins for the full inventory, or find_equivalent to map a name.",
        }
    return twin


def tool_get_pattern(args):
    if TWIN_ROOT is None:
        return missing_root_error()
    slug = (args.get("slug") or "").strip().lower()
    twin = load_twin("patterns", slug)
    if twin is None:
        return {
            "error": "No pattern twin for slug %r." % slug,
            "known_pattern_slugs": [s for k, s, _ in all_twins() if k == "patterns"],
        }
    return twin


REGISTRY_REF = re.compile(
    r"(?:^|[/:])(?:ds[-:])?(?P<slug>[a-z][a-z0-9-]*?)(?:\.json|\.md)?$"
)


def normalise(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def registry_slug(term):
    """Resolve a data-registry value, a ds-* class, or a twin URL to a slug."""
    t = (term or "").strip()
    if not t:
        return None
    if t.startswith("ds:") or t.startswith("ds-"):
        return t[3:]
    if "/" in t or t.endswith(".json") or t.endswith(".md"):
        m = REGISTRY_REF.search(t)
        if m:
            return m.group("slug")
    return None


def tool_find_equivalent(args):
    if TWIN_ROOT is None:
        return missing_root_error()
    term = (args.get("term") or "").strip()
    if not term:
        return {"error": "Pass the foreign component name, class, or data-registry value as `term`."}

    equiv = load_equivalents()
    norm = normalise(term)
    matches = []
    seen = set()

    def add(slug, kind, why, confidence):
        if slug in seen:
            return
        seen.add(slug)
        twin = load_twin("components", slug) or load_twin("patterns", slug)
        entry = {
            "slug": slug,
            "confidence": confidence,
            "why": why,
            "has_twin": twin is not None,
        }
        if twin is not None:
            entry["kind"] = twin.get("kind")
            entry["name"] = twin.get("name")
            entry["summary"] = (twin.get("summary") or {}).get("value")
            entry["fetch_with"] = "get_pattern" if twin.get("kind") == "pattern" else "get_component"
        else:
            entry["kind"] = kind
            entry["note"] = equiv.get("known_without_twin", {}).get(
                slug, "Named by a pattern twin; no dedicated twin in the published registry."
            )
        matches.append(entry)

    # 1 · a data-registry value / ds-* class / twin URL resolves directly.
    slug = registry_slug(term)
    if slug and (load_twin("components", slug) or load_twin("patterns", slug)):
        add(slug, None, "Resolved %r as a Designsystemet registry reference." % term, "exact")

    # 2 · authored alias table (foreign design systems, generic UI vocabulary, Norwegian).
    for target, aliases in equiv.get("aliases", {}).items():
        for alias in aliases:
            a = normalise(alias)
            if a and (a == norm or a in norm or norm in a):
                add(target, "component", "%r is the Designsystemet equivalent of %r." % (target, alias), "alias")
                break

    # 3 · fall back to searching twin content, so unknown terms degrade to a hint
    #     instead of a dead end.
    if not matches:
        words = [w for w in norm.split() if len(w) > 2]
        for kind, tslug, twin in all_twins():
            hay = normalise(
                " ".join(
                    [
                        twin.get("name") or "",
                        (twin.get("summary") or {}).get("value") or "",
                        json.dumps((twin.get("relations") or {}).get("value") or {}),
                    ]
                )
            )
            # All content words must appear as whole words — any-substring matched
            # "thing" inside "something" across half the corpus once it grew past
            # the pilot three (found 2026-08-11 by test 10).
            if words and all(re.search(r"\b%s\b" % re.escape(w), hay) for w in words):
                add(tslug, twin.get("kind"), "Matched %r in the twin's own text." % term, "weak")

    return {
        "query": term,
        "matches": matches,
        "translation_rule": TRANSLATION_RULE,
        "next": (
            "Call get_component/get_pattern on the match before writing code — the twin "
            "carries the real prop names and the accessibility requirements the component "
            "does not enforce for you."
            if matches
            else "No mapping found. Call list_twins to see the published twins; do not guess a "
            "Designsystemet component name."
        ),
    }


TOOLS = [
    {
        "name": "list_twins",
        "description": (
            "List every Designsystemet component and pattern that has a structured twin, "
            "with a one-line summary each. Call this first when you do not know what exists."
        ),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "handler": tool_list_twins,
    },
    {
        "name": "get_component",
        "description": (
            "Get the full contract twin for one Designsystemet component: real prop names and "
            "types, the real import/export name, the --dsc-* to --ds-* token mapping, the "
            "accessibility requirements the component does NOT enforce for you, and its "
            "relations to other components. Read this before writing any code that uses the "
            "component — its prop surface is not what a general React prior predicts "
            "(the variant mechanism is data-color, and some exports are prefixed EXPERIMENTAL_)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"slug": {"type": "string", "description": "Component slug, e.g. 'alert' or 'suggestion'."}},
            "required": ["slug"],
            "additionalProperties": False,
        },
        "handler": tool_get_component,
    },
    {
        "name": "get_pattern",
        "description": (
            "Get the full contract twin for a Designsystemet pattern: which components compose "
            "it, in what order and placement, when errors may be shown, the accessibility "
            "requirements, and the boundaries. Call this before building a screen — components "
            "alone will not produce a correct form."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"slug": {"type": "string", "description": "Pattern slug, e.g. 'skjema-validering'."}},
            "required": ["slug"],
            "additionalProperties": False,
        },
        "handler": tool_get_pattern,
    },
    {
        "name": "find_equivalent",
        "description": (
            "Map something that is not Designsystemet onto the Designsystemet component that "
            "replaces it. Accepts a foreign component name (MUI Autocomplete, GOV.UK Error "
            "Summary, Bootstrap alert), generic UI vocabulary (typeahead, callout, banner), a "
            "Norwegian term, a rendered ds-* class, or a data-registry value from a page built "
            "with Designsystemet. Use it whenever you are porting or copying markup from "
            "elsewhere, so you emit Designsystemet components instead of foreign ones."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"term": {"type": "string", "description": "Foreign name, class, or data-registry value."}},
            "required": ["term"],
            "additionalProperties": False,
        },
        "handler": tool_find_equivalent,
    },
]

HANDLERS = {t["name"]: t["handler"] for t in TOOLS}
TOOL_SPECS = [{k: v for k, v in t.items() if k != "handler"} for t in TOOLS]


# ---------------------------------------------------------------------------
# JSON-RPC 2.0 over newline-delimited stdio


def result(req_id, payload):
    return {"jsonrpc": "2.0", "id": req_id, "result": payload}


def error(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def handle(msg):
    """Return a response dict, or None for notifications."""
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        client_version = params.get("protocolVersion")
        return result(
            req_id,
            {
                "protocolVersion": client_version if isinstance(client_version, str) else PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            },
        )

    if method in ("notifications/initialized", "notifications/cancelled"):
        return None

    if method == "ping":
        return result(req_id, {})

    if method == "tools/list":
        return result(req_id, {"tools": TOOL_SPECS})

    if method == "tools/call":
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            return error(req_id, -32602, "Unknown tool: %s" % name)
        try:
            payload = handler(params.get("arguments") or {})
            is_error = isinstance(payload, dict) and "error" in payload
        except Exception as exc:  # a crashed tool must not kill the server
            payload, is_error = {"error": "%s: %s" % (type(exc).__name__, exc)}, True
        return result(
            req_id,
            {
                "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
                "isError": is_error,
            },
        )

    if req_id is None:
        return None
    return error(req_id, -32601, "Method not found: %s" % method)


def main():
    if TWIN_ROOT is None:
        print(
            "designsystemet-twins: no twin root found "
            "(tried --twins, $DESIGNSYSTEMET_TWINS, ./twins, ./fork/twins). "
            "Tools will return an actionable error.",
            file=sys.stderr,
        )
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            sys.stdout.write(json.dumps(error(None, -32700, "Parse error")) + "\n")
            sys.stdout.flush()
            continue
        response = handle(msg)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
