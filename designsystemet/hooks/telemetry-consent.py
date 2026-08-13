#!/usr/bin/env python3
"""SessionStart hook: ask for telemetry consent once, ever.

Silent when a decision exists (or the env kill-switch is set). Otherwise it
injects instructions for the agent to ask the user one question and record
the answer. The question text travels with the hook so every install asks it
the same way.
"""

import json
import os

from telemetry import consent

if consent() is None and os.environ.get("DESIGNSYSTEMET_TELEMETRY") != "0":
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "[designsystemet plugin — first run] Telemetry consent is undecided. "
                "Before starting other work, ask the user ONE question (AskUserQuestion, "
                "header 'Telemetry'): \"Help the Designsystemet team improve this plugin "
                "by collecting anonymous usage signals?\" Options: 'Yes, opt in' / 'No'. "
                "Explain in the question: WHAT IS COLLECTED — which component contracts "
                "are looked up and whether they were found, which guard checks fire, "
                "plugin version, date. WHAT IS NEVER COLLECTED — your code, prompts, "
                "file paths, repo or project names, anything identifying. Nothing is "
                "sent anywhere automatically: data stays on this machine, and "
                "/ds-telemetry shows the aggregate which only the user can choose to "
                "share. Record the answer by running "
                "`python3 ${CLAUDE_PLUGIN_ROOT}/hooks/telemetry.py --enable` or "
                "`--disable`, then continue with the user's actual task."
            ),
        }
    }))
