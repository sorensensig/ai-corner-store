#!/usr/bin/env python3
"""Protocol test for twins_server.py — drives it over stdio like a real MCP client.

    python3 tests/test_twins_server.py [--twins <path>]

One row per expectation. Exit 1 on any mismatch. Stdlib only.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = HERE.parent / "mcp" / "twins_server.py"
DEFAULT_TWINS = Path.home() / "Documents/dev/work/Digdir/designsystemet/twins"


def twins():
    if "--twins" in sys.argv:
        return sys.argv[sys.argv.index("--twins") + 1]
    return os.environ.get("DESIGNSYSTEMET_TWINS") or str(DEFAULT_TWINS)


def call(rid, tool, args):
    return {"jsonrpc": "2.0", "id": rid, "method": "tools/call",
            "params": {"name": tool, "arguments": args}}


MSGS = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "test", "version": "0"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    call(3, "list_twins", {}),
    call(4, "get_component", {"slug": "suggestion"}),
    call(5, "get_pattern", {"slug": "skjema-validering"}),
    call(6, "find_equivalent", {"term": "MUI Autocomplete"}),
    call(7, "find_equivalent", {"term": "GOV.UK Error Summary"}),
    call(8, "find_equivalent", {"term": "ds-alert"}),
    call(9, "find_equivalent", {"term": "https://example.no/twins/components/alert.json"}),
    call(10, "find_equivalent", {"term": "wobbly thing"}),
    call(11, "get_component", {"slug": "../../etc/passwd"}),
    call(12, "get_component", {"slug": "date-picker"}),
    {"jsonrpc": "2.0", "id": 13, "method": "tools/call", "params": {"name": "nope", "arguments": {}}},
]


def body_of(res):
    return json.loads(res["content"][0]["text"])


# id -> (label, predicate over the response)
EXPECT = {
    1: ("initialize handshake",
        lambda r: r["result"]["serverInfo"]["name"] == "designsystemet-twins"),
    2: ("tools/list names the four tools",
        lambda r: [t["name"] for t in r["result"]["tools"]]
        == ["list_twins", "get_component", "get_pattern", "find_equivalent"]),
    3: ("list_twins covers the full registry incl. the pilot three",
        lambda r: {"alert", "suggestion", "skjema-validering"}
        <= {t["slug"] for t in body_of(r["result"])["twins"]}
        and len(body_of(r["result"])["twins"]) >= 40),
    4: ("get_component returns the Suggestion contract",
        lambda r: (lambda v: (v.get("exportedAs") if isinstance(v, dict) else v) == "EXPERIMENTAL_Suggestion")(
            body_of(r["result"])["importName"]["value"])),
    5: ("get_pattern returns the assertions the scorer reads",
        lambda r: len(body_of(r["result"])["assertions"]["value"]) >= 8),
    6: ("find_equivalent maps a foreign component",
        lambda r: body_of(r["result"])["matches"][0]["slug"] == "suggestion"),
    7: ("find_equivalent resolves GOV.UK Error Summary to the twinned component",
        lambda r: body_of(r["result"])["matches"][0]["slug"] == "error-summary"
        and body_of(r["result"])["matches"][0]["has_twin"] is True),
    8: ("find_equivalent resolves a rendered ds-* class",
        lambda r: body_of(r["result"])["matches"][0]["slug"] == "alert"),
    9: ("find_equivalent resolves a data-registry URL",
        lambda r: body_of(r["result"])["matches"][0]["slug"] == "alert"),
    10: ("unknown term returns no match and forbids guessing",
         lambda r: body_of(r["result"])["matches"] == []
         and "do not guess" in body_of(r["result"])["next"]),
    11: ("path traversal in a slug is rejected",
         lambda r: r["result"]["isError"] is True),
    12: ("a known-but-untwinned slug (date-picker) warns instead of guessing",
         lambda r: "skjema-validering" in body_of(r["result"])["note"]
         and "no DatePicker" in body_of(r["result"])["note"]),
    13: ("unknown tool is a protocol error",
         lambda r: r.get("error", {}).get("code") == -32602),
}


def main():
    root = twins()
    if not (Path(root) / "components").is_dir():
        sys.exit("No twins at %s — pass --twins or set $DESIGNSYSTEMET_TWINS." % root)

    payload = "\n".join(json.dumps(m) for m in MSGS) + "\n"
    p = subprocess.run([sys.executable, str(SERVER), "--twins", root], input=payload,
                       capture_output=True, text=True, timeout=30)
    if p.stderr.strip():
        print("stderr:", p.stderr.strip())

    got = {}
    for line in p.stdout.splitlines():
        r = json.loads(line)
        if r.get("id") is not None:
            got[r["id"]] = r

    fails = 0
    for rid, (label, predicate) in EXPECT.items():
        r = got.get(rid)
        try:
            ok = r is not None and predicate(r)
        except (KeyError, IndexError, TypeError, ValueError):
            ok = False
        fails += not ok
        print("%s  %s" % ("PASS" if ok else "FAIL", label))
        if not ok and r is not None:
            print("      got:", json.dumps(r)[:220])

    print("\n%d/%d passed" % (len(EXPECT) - fails, len(EXPECT)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
