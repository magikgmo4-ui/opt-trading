#!/usr/bin/env bash
set -euo pipefail
REPO="${REPO:-/opt/trading}"
VENV_PY="$REPO/venv/bin/python"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI Toolbox Fix v4 (inject before return) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
[[ -x "$VENV_PY" ]] || { echo "FAIL: venv python not found at $VENV_PY"; exit 2; }
[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_toolbox_ui_v4_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

"$VENV_PY" - <<'PY'
from pathlib import Path
import re

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

m = re.search(r'^(?P<indent>[ \t]*)def\s+ui\s*\([^\)]*\)\s*:\s*$', s, flags=re.M)
if not m:
    raise SystemExit("FAIL: def ui(...) not found")

ui_indent = m.group("indent")
ui_start = m.end()
inner = ui_indent + "    "

# find first return HTMLResponse( inside ui()
ret = re.search(rf'^{re.escape(inner)}return\s+HTMLResponse\(', s[ui_start:], flags=re.M)
if not ret:
    raise SystemExit("FAIL: return HTMLResponse(...) not found inside ui()")

ret_pos = ui_start + ret.start()

marker = f"{inner}# --- TOOLBOX_UI_INJECT_V4 ---"
if marker in s[ui_start:ret_pos]:
    print("NOTE: v4 inject already present; no changes.")
    raise SystemExit(0)

# We'll inject a safe snippet that only runs if local var html exists.
# Use triple quotes to avoid quote escaping issues.
inject = (
    f"{marker}\n"
    f"{inner}try:\n"
    f"{inner}    if 'html' in locals() and '/desk/toolbox' not in html and '/desk/form' in html:\n"
    f"{inner}        _ins = ' <a href=\"/desk/toolbox\" style=\"margin-left:10px\">toolbox</a>'\n"
    f"{inner}        # insert toolbox link right after first occurrence of /desk/form\n"
    f"{inner}        html = html.replace('/desk/form', '/desk/form' + _ins, 1)\n"
    f"{inner}except Exception:\n"
    f"{inner}    pass\n\n"
)

s2 = s[:ret_pos] + inject + s[ret_pos:]
p.write_text(s2, encoding="utf-8")
print("OK: injected v4 toolbox runtime patch inside ui() before return")
PY

echo "Done."
