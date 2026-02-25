#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
VENV_PY="$REPO/venv/bin/python"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI Toolbox Fix v3 (inject before return) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
[[ -x "$VENV_PY" ]] || { echo "FAIL: venv python not found at $VENV_PY"; exit 2; }
[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_toolbox_ui_v3_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

"$VENV_PY" - <<'PY'
from pathlib import Path
import re

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

# Find def ui(...) block start
m = re.search(r'^(?P<indent>[ \t]*)def\s+ui\s*\([^\)]*\)\s*:\s*$', s, flags=re.M)
if not m:
    raise SystemExit("FAIL: def ui(...) not found")

ui_indent = m.group("indent")
ui_start = m.end()

# Determine indentation inside function (one level deeper)
inner_indent = ui_indent + "    "

# Find first 'return HTMLResponse' inside ui()
# Search from ui_start forward
ret = re.search(rf'^{re.escape(inner_indent)}return\s+HTMLResponse\(', s[ui_start:], flags=re.M)
if not ret:
    raise SystemExit("FAIL: return HTMLResponse(...) not found inside ui()")

ret_pos = ui_start + ret.start()

marker = f"{inner_indent}# --- TOOLBOX_UI_INJECT_V3 ---"
if marker in s[ui_start:ret_pos]:
    print("NOTE: v3 inject already present; no changes.")
    raise SystemExit(0)

inject = (
    f"{marker}\n"
    f"{inner_indent}try:\n"
    f"{inner_indent}    # ensure toolbox link shows up in /desk/ui\n"
    f"{inner_indent}    if 'html' in locals() and '/desk/toolbox' not in html and '/desk/form' in html:\n"
    f"{inner_indent}        html = html.replace('/desk/form', '/desk/form</a> <a href="/desk/toolbox" style="margin-left:10px">toolbox</a><a', 1)\n"
    f"{inner_indent}except Exception:\n"
    f"{inner_indent}    pass\n\n"
)

s2 = s[:ret_pos] + inject + s[ret_pos:]
p.write_text(s2, encoding="utf-8")
print("OK: injected toolbox runtime patch inside ui() before return")
PY

echo "Done."
