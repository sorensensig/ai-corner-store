#!/usr/bin/env python3
"""Table-test for the opt-in telemetry: consent flow, event capture, and the
guarantees that matter — nothing is written before opt-in, the kill-switch
wins, and the guard still denies when telemetry is broken. Stdlib only.

    python3 tests/test_telemetry.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOKS = HERE.parent / "hooks"
REGISTRY = HERE.parent / "registry"

DENYING_WRITE = json.dumps({
    "tool_name": "Write",
    "tool_input": {"file_path": "/x/A.tsx",
                   "content": "import { Alert } from '@digdir/designsystemet-react';\n<Alert variant=\"danger\">Feil</Alert>"},
})
MCP_LOOKUP = json.dumps({
    "tool_name": "mcp__plugin_designsystemet_designsystemet-twins__get_component",
    "tool_input": {"slug": "textfield"},
    "tool_response": {"content": [{"type": "text", "text": "{\"name\": \"Textfield\"}"}]},
})


def run(script, argv=(), stdin=None, env=None):
    e = {**os.environ, **(env or {})}
    return subprocess.run([sys.executable, str(HOOKS / script), *argv],
                         input=stdin, capture_output=True, text=True, timeout=20, env=e)


def events(d):
    f = Path(d) / "telemetry-events.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines()] if f.exists() else []


def main():
    fails = 0

    def check(name, ok):
        nonlocal fails
        fails += not ok
        print("%s  %s" % ("PASS" if ok else "FAIL", name))

    with tempfile.TemporaryDirectory() as d:
        env = {"DESIGNSYSTEMET_TELEMETRY_DIR": d}

        out = run("telemetry-consent.py", env=env).stdout
        check("undecided: consent hook asks", "Telemetry consent is undecided" in out)

        run("telemetry-log.py", stdin=MCP_LOOKUP, env=env)
        check("undecided: lookup writes nothing", events(d) == [])

        run("telemetry.py", ["--disable"], env=env)
        check("declined: consent hook is silent", run("telemetry-consent.py", env=env).stdout == "")
        run("telemetry-log.py", stdin=MCP_LOOKUP, env=env)
        check("declined: lookup writes nothing", events(d) == [])

        run("telemetry.py", ["--enable"], env=env)
        run("telemetry-log.py", stdin=MCP_LOOKUP, env=env)
        ev = events(d)
        check("opted in: lookup recorded", len(ev) == 1 and ev[0]["event"] == "lookup"
              and ev[0]["query"] == "textfield" and ev[0]["found"] is True)
        check("event carries no content fields",
              set(ev[0]) <= {"t", "event", "tool", "query", "found", "check"})

        p = run("guard-ds-code.py", ["--twins", str(REGISTRY)], stdin=DENYING_WRITE, env=env)
        check("opted in: guard deny recorded, deny still fires",
              '"deny"' in p.stdout and any(e.get("event") == "guard-deny"
                                           and e.get("check") == "no-invented-props" for e in events(d)))

        n = len(events(d))
        run("telemetry-log.py", stdin=MCP_LOOKUP, env={**env, "DESIGNSYSTEMET_TELEMETRY": "0"})
        check("kill-switch: no write despite opt-in", len(events(d)) == n)
        check("kill-switch: consent hook silent even when undecided",
              run("telemetry-consent.py",
                  env={"DESIGNSYSTEMET_TELEMETRY_DIR": d + "/fresh",
                       "DESIGNSYSTEMET_TELEMETRY": "0"}).stdout == "")

        st = json.loads(run("telemetry.py", env=env).stdout)
        check("status reports decided/enabled/count",
              st == {"decided": True, "enabled": True, "events": n})

    print("\n%d failed" % fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
