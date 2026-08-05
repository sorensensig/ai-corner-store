#!/usr/bin/env bash
# check-release-registration.sh — a new release folder is not "added" until every
# place that has to know about it knows about it.
#
# WHY THIS EXISTS
# `laws-of-ux` merged as a complete, reviewed release folder and was still invisible:
# absent from marketplace.json (so `/plugin install laws-of-ux` did nothing) and absent
# from release.yml's matrix (so no GitHub Release would ever be cut for it). Its own
# README documented an install command that could not work.
#
# release.yml already carried the instruction, in its own header comment:
#   "Adding a future release = add its folder to the RELEASES list below."
# It was read, and it still did not happen. An instruction that has to be remembered at
# the moment someone is absorbed in shipping the actual content will eventually not fire
# — so this is a gate rather than a sentence.
#
# WHAT COUNTS AS A RELEASE
# Any top-level directory containing `.claude-plugin/plugin.json`. Nothing to register
# by hand here: the check discovers releases from the filesystem, so a new folder is
# picked up automatically and the burden is on the registrations to catch up.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

MARKETPLACE=".claude-plugin/marketplace.json"
WORKFLOW=".github/workflows/release.yml"
README="README.md"

FAIL=0        # any failure, across all releases
THIS=0        # failures for the release currently being checked
note() { echo "  ✗ $1"; FAIL=1; THIS=1; }

command -v python3 >/dev/null 2>&1 || { echo "python3 required"; exit 1; }

releases=()
for d in */; do
  d="${d%/}"
  [ -f "$d/.claude-plugin/plugin.json" ] && releases+=("$d")
done

[ ${#releases[@]} -gt 0 ] || { echo "no release folders found — nothing to check"; exit 0; }

echo "Checking ${#releases[@]} release folder(s): ${releases[*]}"
echo

for r in "${releases[@]}"; do
  echo "$r"
  THIS=0

  # 1. plugin.json's own name must match its folder, or every downstream
  #    reference to it is ambiguous.
  pj_name=$(python3 -c "
import json,sys
try: print(json.load(open('$r/.claude-plugin/plugin.json')).get('name',''))
except Exception: print('')
" 2>/dev/null)
  if [ "$pj_name" != "$r" ]; then
    note "plugin.json name is '$pj_name', expected '$r' (must match the folder)"
  fi

  # 2. marketplace.json — without this, the release cannot be installed at all.
  in_mkt=$(python3 -c "
import json
try:
    d=json.load(open('$MARKETPLACE'))
    print('yes' if any(p.get('name')=='$r' for p in d.get('plugins',[])) else 'no')
except Exception: print('error')
" 2>/dev/null)
  case "$in_mkt" in
    yes) : ;;
    no)  note "not listed in $MARKETPLACE — '/plugin install $r' will not work" ;;
    *)   note "could not parse $MARKETPLACE" ;;
  esac

  # 3. release.yml's matrix — without this, no GitHub Release is ever cut for it,
  #    and the version in plugin.json silently means nothing.
  #
  # Parsed, not grepped. A regex over the bracketed list has to special-case the
  # first element (no preceding separator) and the last (no trailing comma), and
  # the obvious pattern silently passes a release it should flag. Splitting the
  # list and comparing exact strings has no such edge.
  in_matrix=$(python3 -c "
import re, sys
try: text = open(sys.argv[1]).read()
except Exception: print('error'); sys.exit()
m = re.search(r'release:\s*\[([^\]]*)\]', text)
if not m: print('nomatrix'); sys.exit()
items = [x.strip().strip(chr(34)).strip(chr(39)) for x in m.group(1).split(',')]
print('yes' if sys.argv[2] in items else 'no')
" "$WORKFLOW" "$r" 2>/dev/null)
  case "$in_matrix" in
    yes)      : ;;
    no)       note "not in the release matrix in $WORKFLOW — no release will be cut on version bump" ;;
    nomatrix) note "could not find a 'release: [...]' matrix in $WORKFLOW" ;;
    *)        note "could not read $WORKFLOW" ;;
  esac

  # 4. the Releases table in the root README — the human-facing half.
  if ! grep -qE "\]\(\./$r\)" "$README" 2>/dev/null; then
    note "not linked from the Releases table in $README"
  fi

  [ "$THIS" -eq 0 ] && echo "  ✓ registered everywhere"
  echo
done

if [ "$FAIL" -ne 0 ]; then
  cat <<'MSG'
A release folder exists that is not registered everywhere it needs to be.
See RELEASING.md — adding a release means four places, three of them functional:

  1. <release>/.claude-plugin/plugin.json   name matches the folder
  2. .claude-plugin/marketplace.json        so it can be installed
  3. .github/workflows/release.yml          so releases are cut on version bump
  4. README.md                              so a human can find it

MSG
  exit 1
fi

echo "All releases registered."
