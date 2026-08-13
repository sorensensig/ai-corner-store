#!/usr/bin/env python3
"""Consent state and event store for the plugin's opt-in telemetry.

Everything lives in one local directory (override with
$DESIGNSYSTEMET_TELEMETRY_DIR, default ~/.config/designsystemet-plugin):

  telemetry.json          {"enabled": bool, "decidedAt": iso-date, "installId": uuid}
  telemetry-events.jsonl  one event per line, appended only while enabled

Events carry usage signals, never content: which contract was looked up and
whether it was found, which guard check fired, the plugin version, and the
date. No code, no prompts, no file paths, no repo names.

Nothing is transmitted by this module or anything else in the plugin. The
/ds-telemetry command shows the collected aggregate; sending it anywhere is a
step the user takes deliberately.

  telemetry.py --status | --enable | --disable
  telemetry.py --log '<event-json>'     (no-op unless enabled)

$DESIGNSYSTEMET_TELEMETRY=0 disables collection regardless of stored consent.
"""

import datetime
import json
import os
import sys
import uuid
from pathlib import Path


def store_dir():
    override = os.environ.get("DESIGNSYSTEMET_TELEMETRY_DIR")
    return Path(override) if override else Path.home() / ".config" / "designsystemet-plugin"


def consent():
    """None = never asked; otherwise the stored dict."""
    try:
        return json.loads((store_dir() / "telemetry.json").read_text())
    except (OSError, ValueError):
        return None


def enabled():
    if os.environ.get("DESIGNSYSTEMET_TELEMETRY") == "0":
        return False
    c = consent()
    return bool(c and c.get("enabled"))


def decide(enable):
    d = store_dir()
    d.mkdir(parents=True, exist_ok=True)
    state = consent() or {}
    state.update(
        enabled=enable,
        decidedAt=datetime.date.today().isoformat(),
        installId=state.get("installId") or str(uuid.uuid4()),
    )
    (d / "telemetry.json").write_text(json.dumps(state, indent=2) + "\n")
    return state


def log(event):
    """Append one event if enabled. Never raises: telemetry must not be able
    to break the hook or guard that calls it."""
    try:
        if not enabled():
            return
        event = {"t": datetime.date.today().isoformat(), **event}
        with open(store_dir() / "telemetry-events.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
    except Exception:
        pass


def main():
    args = sys.argv[1:]
    if "--enable" in args:
        print(json.dumps(decide(True)))
    elif "--disable" in args:
        print(json.dumps(decide(False)))
    elif "--log" in args:
        log(json.loads(args[args.index("--log") + 1]))
    else:
        c = consent()
        print(json.dumps({"decided": c is not None, "enabled": enabled(),
                          "events": sum(1 for _ in open(store_dir() / "telemetry-events.jsonl"))
                          if (store_dir() / "telemetry-events.jsonl").exists() else 0}))


if __name__ == "__main__":
    main()
