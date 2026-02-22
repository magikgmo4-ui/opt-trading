#!/usr/bin/env bash
set -euo pipefail
cd /opt/trading

target="modules/desk_pro/api/routes.py"
[[ -f "$target" ]] || { echo "FAIL: missing $target"; exit 2; }

if grep -qE '"/ui"' "$target"; then
  echo "OK: UI route already present"
  exit 0
fi

ts="$(date +%Y%m%d_%H%M%S)"
cp -a "$target" "$target.bak.$ts"
echo "Backup: $target.bak.$ts"

python - <<'PY'
from pathlib import Path
import re

p = Path("modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8", errors="replace")

# Ensure HTMLResponse import
if "from fastapi.responses import HTMLResponse" not in s:
    s = s.replace("from fastapi import APIRouter", "from fastapi import APIRouter\nfrom fastapi.responses import HTMLResponse")

# Ensure UI renderer import
imp = "from modules.desk_pro.ui.page import render_ui_html"
if imp not in s:
    # insert after imports block (after last import line)
    lines = s.splitlines()
    last_imp = -1
    for i, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            last_imp = i
        else:
            if i > 0 and last_imp >= 0:
                break
    lines.insert(last_imp + 1, imp)
    s = "\n".join(lines) + ("\n" if not s.endswith("\n") else "")

# Append route
route = "\n\n@router.get(\"/ui\", response_class=HTMLResponse)\ndef ui():\n    return HTMLResponse(render_ui_html())\n"
if "/ui" not in s:
    s = s.rstrip() + route

p.write_text(s, encoding="utf-8")
print("Patched routes.py with /desk/ui")
PY

echo "OK: patched /desk/ui"
