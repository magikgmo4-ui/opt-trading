#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI Toolbox Fix (patch ui() HTML) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_toolbox_ui_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

python - <<'PY'
from pathlib import Path
import re

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

# Locate def ui(...)
m = re.search(r'\n\s*def\s+ui\s*\([^\)]*\)\s*:\s*\n', s)
if not m:
    raise SystemExit("FAIL: def ui(...) not found")

start = m.end()
# Find first triple-quoted string after ui() def (this is the HTML used by ui())
m2 = re.search(r'("""|\'\'\')', s[start:])
if not m2:
    raise SystemExit("FAIL: no triple-quoted string found after ui()")

q = m2.group(1)
hs = start + m2.end()
endm = re.search(re.escape(q), s[hs:])
if not endm:
    raise SystemExit("FAIL: could not find end triple quotes for ui() HTML")

he = hs + endm.start()
html = s[hs:he]

if "/desk/toolbox" in html:
    print("NOTE: ui() HTML already contains /desk/toolbox — no changes.")
    raise SystemExit(0)

pat = r'(href="/desk/form"[^>]*>[^<]*</a>)'
if not re.search(pat, html):
    raise SystemExit("FAIL: ui() HTML does not contain an anchor to /desk/form (unexpected)")

html2 = re.sub(pat, r'\1 <a href="/desk/toolbox" style="margin-left:10px">toolbox</a>', html, count=1)
s2 = s[:hs] + html2 + s[he:]
p.write_text(s2, encoding="utf-8")
print("OK: injected toolbox link into ui() HTML")
PY

echo "Done."
echo "Next: sudo bash $REPO/scripts/sanity_desk_pro_ui_toolbox_fix.sh"
