---
description: >
  Show, change, or share the plugin's opt-in telemetry. Displays the collected
  aggregate (lookups, misses, guard denials), lets the user opt in or out, and
  formats a summary the user can choose to send to the Designsystemet team.
  Data never leaves the machine unless the user sends it.
argument-hint: "[status | on | off | report]"
---

# /ds-telemetry — opt-in usage telemetry

All state lives in `~/.config/designsystemet-plugin/` (or
`$DESIGNSYSTEMET_TELEMETRY_DIR`). The tool is
`${CLAUDE_PLUGIN_ROOT}/hooks/telemetry.py`.

## What to do per argument

- **status** (default): run `telemetry.py --status` and report it plainly:
  decided or not, enabled or not, how many events collected. Remind the user
  what is and is not collected (see below).
- **on** / **off**: run `telemetry.py --enable` / `--disable` and confirm.
- **report**: read `telemetry-events.jsonl` and present the aggregate — counts
  by event type, the most-looked-up contracts, lookups that found nothing
  (vocabulary/coverage gaps), and which guard checks fire most. Then offer to
  format it as a comment the user can post on the Designsystemet AI-readiness
  issue. Do not post anything yourself; sending is the user's action.

## What is collected (only after opt-in)

Which contracts are looked up and whether they were found, which guard checks
fire, plugin version, date, and a random install id. Never: code, prompts,
file paths, repo or project names, anything identifying.

`DESIGNSYSTEMET_TELEMETRY=0` switches collection off regardless of consent.
