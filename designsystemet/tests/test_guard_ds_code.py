#!/usr/bin/env python3
"""Table-test for guard-ds-code.py — one row per check, expected vs got.

    python3 tests/test_guard_ds_code.py [--twins <path>]

Twin root: --twins, else $DESIGNSYSTEMET_TWINS, else the workspace default.
Exit 1 on any row that does not match. Stdlib only.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOK = HERE.parent / "hooks" / "guard-ds-code.py"
DEFAULT_TWINS = Path.home() / "Documents/dev/work/Digdir/designsystemet/twins"


def twins():
    if "--twins" in sys.argv:
        return sys.argv[sys.argv.index("--twins") + 1]
    return os.environ.get("DESIGNSYSTEMET_TWINS") or str(DEFAULT_TWINS)


DS_IMPORT = "import { Alert } from '@digdir/designsystemet-react';\n"

GOOD_FORM = DS_IMPORT + """
import { Field, Label, ValidationMessage, ErrorSummary,
  EXPERIMENTAL_Suggestion as Suggestion } from '@digdir/designsystemet-react';

export function Skjema() {
  return (
    <form>
      <Field>
        <Label htmlFor="dest">Reisemal</Label>
        <Suggestion>
          <Suggestion.Input id="dest" aria-invalid="true" aria-describedby="dest-err" />
        </Suggestion>
        <ValidationMessage id="dest-err">Velg et reisemal</ValidationMessage>
      </Field>
      <ErrorSummary>
        <ErrorSummary.List>
          <ErrorSummary.Item><ErrorSummary.Link href="#dest">Velg et reisemal</ErrorSummary.Link></ErrorSummary.Item>
        </ErrorSummary.List>
      </ErrorSummary>
      <Button variant="primary" type="submit">Send</Button>
    </form>
  );
}
"""


def w(path, content):
    return {"tool_name": "Write", "tool_input": {"file_path": path, "content": content}}


def e(path, new):
    return {"tool_name": "Edit", "tool_input": {"file_path": path, "new_string": new}}


CASES = [
    ("correct form passes", w("/x/Skjema.tsx", GOOD_FORM), False),
    ("Button variant= is allowed", w("/x/B.tsx", DS_IMPORT + '<Button variant="primary">Send</Button>'), False),
    ("Alert variant= denied", w("/x/A.tsx", DS_IMPORT + '<Alert variant="danger">Feil</Alert>'), True),
    ("Alert severity= denied", w("/x/A.tsx", DS_IMPORT + '<Alert severity="error">Feil</Alert>'), True),
    ("bogus data-color denied", w("/x/A.tsx", DS_IMPORT + '<Alert data-color="error">Feil</Alert>'), True),
    ("valid data-color passes", w("/x/A.tsx", DS_IMPORT + '<Alert data-color="danger">Feil</Alert>'), False),
    ("bad Suggestion import denied",
     w("/x/S.tsx", "import { Suggestion } from '@digdir/designsystemet-react';\n<Suggestion />"), True),
    ("aliased Suggestion import passes",
     w("/x/S.tsx", "import { EXPERIMENTAL_Suggestion as Suggestion } from '@digdir/designsystemet-react';\n<Suggestion />"), False),
    ("raw hex denied", w("/x/A.tsx", DS_IMPORT + '<Alert style={{ color: "#ff0000" }}>Feil</Alert>'), True),
    ("ds token passes",
     w("/x/A.tsx", DS_IMPORT + '<Alert style={{ color: "var(--ds-color-danger-text-default)" }}>Feil</Alert>'), False),
    ("validation without ErrorSummary denied",
     w("/x/F.tsx", DS_IMPORT + '<ValidationMessage>Feil</ValidationMessage>'), True),
    ("non-DS file ignored", w("/x/Other.tsx", 'export const c = "#ff0000";'), False),
    ("non-code file ignored", w("/x/notes.md", DS_IMPORT + '<Alert variant="danger" />'), False),
    ("Edit fragment: invented prop denied",
     e("/x/A.tsx", '<Alert variant="danger">Feil</Alert>\nimport "@digdir/designsystemet-react";'), True),
    ("Edit fragment: no composition check",
     e("/x/A.tsx", DS_IMPORT + '<ValidationMessage>Feil</ValidationMessage>'), False),
    ("v2: Paragraph-rendered error without aria-invalid denied — the 24-trial miss",
     w("/x/F.tsx", DS_IMPORT + """
function Skjema() {
  const [errors, setErrors] = useState({});
  const onSubmit = (e) => { e.preventDefault(); setErrors(validate()); };
  return (<form onSubmit={onSubmit}>
    <Textfield label="Fullt navn" />
    {errors.navn && <Paragraph>Feltet m\u00e5 fylles ut</Paragraph>}
    <Button type="submit">Send</Button>
  </form>);
}"""), True),
    ("v2: same form correctly wired passes",
     w("/x/F.tsx", DS_IMPORT + """
function Skjema() {
  const [errors, setErrors] = useState({});
  const onSubmit = (e) => { e.preventDefault(); setErrors(validate()); };
  return (<form onSubmit={onSubmit}>
    <ErrorSummary>{...}</ErrorSummary>
    <Textfield label="Fullt navn" required aria-invalid={!!errors.navn} error={errors.navn} />
    <Button type="submit">Send</Button>
  </form>);
}"""), False),
    ("v2: required marking in text without required attr denied",
     w("/x/F.tsx", DS_IMPORT + '<Textfield label="Fullt navn (obligatorisk)" />'), True),
    ("v2: required marking with required attr passes",
     w("/x/F.tsx", DS_IMPORT + '<Textfield label="Fullt navn (obligatorisk)" required />'), False),
]


def main():
    root = twins()
    if not (Path(root) / "patterns").is_dir():
        sys.exit("No twins at %s — pass --twins or set $DESIGNSYSTEMET_TWINS." % root)

    fails = 0
    for name, payload, expect_deny in CASES:
        p = subprocess.run([sys.executable, str(HOOK), "--twins", root], input=json.dumps(payload),
                           capture_output=True, text=True, timeout=20)
        out = p.stdout.strip()
        denied = bool(out) and json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"
        ok = denied == expect_deny
        fails += not ok
        print("%s  %-45s expected=%-5s got=%s" % (
            "PASS" if ok else "FAIL", name, "deny" if expect_deny else "allow", "deny" if denied else "allow"))
        if not ok and out:
            print("      reason:", json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"].split("\n")[0])
        if p.stderr.strip():
            print("      stderr:", p.stderr.strip()[:200])

    print("\n%d/%d passed" % (len(CASES) - fails, len(CASES)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
