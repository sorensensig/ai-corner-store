#!/usr/bin/env python3
"""The hooks.json command line survives a plugin root containing spaces.

Regression for the 2026-08-14 field failure: ${CLAUDE_PLUGIN_ROOT} was
unquoted, so on iCloud-hosted installs ("…/Mobile Documents/…") the shell
word-split the path, the guard crashed, and — because hook crashes fail
closed — every matched Write/Edit was blocked.

Runs the REAL command string from hooks.json through `sh -c` with
CLAUDE_PLUGIN_ROOT pointing at a symlinked copy of the plugin under a
directory whose name contains a space. Stdlib only.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent

passed = failed = 0


def check(label, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS  {label}")
    else:
        failed += 1
        print(f"FAIL  {label}  {detail}")


def run(cmd, root, payload):
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(root))
    env.pop("DESIGNSYSTEMET_TWINS", None)  # exercise the bundled-registry default
    return subprocess.run(
        ["sh", "-c", cmd], input=json.dumps(payload),
        capture_output=True, text=True, env=env,
    )


def main():
    hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text())
    cmd = hooks["hooks"]["PreToolUse"][0]["hooks"][0]["command"]

    check("every word-initial ${CLAUDE_PLUGIN_ROOT} is quoted",
          ' ${CLAUDE_PLUGIN_ROOT}' not in cmd and not cmd.startswith('${CLAUDE_PLUGIN_ROOT}'),
          cmd)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "plugin root with spaces"
        root.mkdir()
        for entry in ("hooks", "registry"):
            (root / entry).symlink_to(PLUGIN / entry)

        r = run(cmd, root, {"tool_name": "Write", "tool_input": {
            "file_path": "/tmp/notes.txt", "content": "plain text"}})
        check("spacey root: benign write passes through",
              r.returncode == 0 and "deny" not in r.stdout,
              f"rc={r.returncode} stderr={r.stderr.strip()[:200]}")

        r = run(cmd, root, {"tool_name": "Write", "tool_input": {
            "file_path": "/tmp/EmailForm.tsx",
            "content": 'import {Alert} from "@digdir/designsystemet-react";\n'
                       'export const E = () => <Alert variant="error">Feil</Alert>;\n'}})
        check("spacey root: guard still evaluates (Alert misuse denied)",
              '"permissionDecision": "deny"' in r.stdout,
              f"rc={r.returncode} out={r.stdout.strip()[:200]} err={r.stderr.strip()[:200]}")

    print(f"\n{passed}/{passed + failed} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
