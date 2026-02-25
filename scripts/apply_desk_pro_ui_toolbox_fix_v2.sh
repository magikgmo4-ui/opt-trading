#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
VENV_PY="$REPO/venv/bin/python"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI Toolbox Fix v2 (patch ui() HTML) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
[[ -x "$VENV_PY" ]] || { echo "FAIL: venv python not found at $VENV_PY"; exit 2; }
[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_toolbox_ui_v2_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

"$VENV_PY" - <<'PY'
from pathlib import Path
import re

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

# Locate def ui(...)
m = re.search(r'\n\s*def\s+ui\s*\([^\)]*\)\s*:\s*\n', s)
if not m:
    raise SystemExit("FAIL: def ui(...) not found")

start = m.end()

# Find the FIRST triple-quoted string after ui() that contains <!doctype html
best = None
for m2 in re.finditer(r'("""|\'\'\')', s[start:]):
    q = m2.group(1)
    hs = start + m2.end()
    endm = re.search(re.escape(q), s[hs:])
    if not endm:
        continue
    he = hs + endm.start()
    blob = s[hs:he]
    if "<!doctype html" in blob and "<html" in blob:
        best = (q, hs, he, blob)
        break

if not best:
    raise SystemExit("FAIL: could not find ui() HTML triple-quoted block (doctype/html)")

q, hs, he, html = best

if "/desk/toolbox" in html:
    print("NOTE: ui() HTML already contains /desk/toolbox — no changes.")
    raise SystemExit(0)

if "/desk/form" not in html:
    raise SystemExit("FAIL: ui() HTML does not contain /desk/form (unexpected)")

# Robust injection: insert toolbox link right AFTER the first occurrence of /desk/form anchor if possible
pat_anchor = r'(href="/desk/form"[^>]*>[^<]*</a>)'
if re.search(pat_anchor, html):
    html2 = re.sub(pat_anchor, r'\1 <a href="/desk/toolbox" style="margin-left:10px">toolbox</a>', html, count=1)
else:
    # fallback: crude insertion after first '/desk/form'
    html2 = html.replace("/desk/form", "/desk/form\" style=\"margin-left:10px\">/desk/form</a> <a href=\"/desk/toolbox\" style=\"margin-left:10px\">toolbox</a> <a href=\"", 1)

if "/desk/toolbox" not in html2:
    raise SystemExit("FAIL: injection did not add /desk/toolbox")

s2 = s[:hs] + html2 + s[he:]
p.write_text(s2, encoding="utf-8")
print("OK: injected toolbox link into ui() HTML (v2)")
PY

echo "Done."
