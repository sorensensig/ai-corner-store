#!/usr/bin/env python3
"""PostToolUse hook on the twins MCP tools: record which contracts get looked
up and whether they were found. No-op unless the user opted in."""

import json
import sys

from telemetry import log


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return

    tool = payload.get("tool_name") or ""
    if "designsystemet-twins" not in tool:
        return
    short = tool.rsplit("__", 1)[-1]
    args = payload.get("tool_input") or {}
    response = payload.get("tool_response") or {}
    text = json.dumps(response)

    log({
        "event": "lookup",
        "tool": short,
        "query": args.get("slug") or args.get("term"),
        "found": '"error"' not in text[:200],
    })


if __name__ == "__main__":
    main()
