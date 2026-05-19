#!/usr/bin/env bash
set -euo pipefail

REPO="/opt/trading"
TARGET="$REPO/modules/desk_pro/api/routes.py"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP="$TARGET.bak_uibox_final_fixed_$TS"

echo "=== Apply Desk Pro UI Toolbox FINAL Patch (fixed) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
echo "Backup: $BACKUP"

sudo cp -a "$TARGET" "$BACKUP"

python - <<'PY'
from pathlib import Path
import re

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

# 1) Force-fix ANY toolbox decorator line
lines = s.splitlines(True)
out = []
for ln in lines:
    if "router.get" in ln and "toolbox" in ln:
        out.append('@router.get("/toolbox", response_class=HTMLResponse)\n')
    else:
        out.append(ln)
s = "".join(out)

# 2) Replace ui() block ONLY (from def ui(): up to the next @router.get("/toolbox"...)
pat = r"def ui\(\):\n[\s\S]*?\n@router\.get\(\"/toolbox\""
m = re.search(pat, s)
if not m:
    raise SystemExit('FAIL: could not locate ui() block up to @router.get("/toolbox")')

new_ui = r'''def ui():
    _dp_log("desk_ui")
    html = render_ui_html()

    # inject toolbox link into Endpoints row (UI uses <span class="pill">... )
    if "/desk/toolbox" not in html:
        if '<span class="pill">/desk/form</span>' in html:
            html = html.replace(
                '<span class="pill">/desk/form</span>',
                '<span class="pill">/desk/form</span><a class="pill" href="/desk/toolbox">/desk/toolbox</a>',
                1
            )
        elif "</body>" in html:
            # fallback: append before </body>
            html = html.replace(
                "</body>",
                '\n<div style="margin-top:12px;padding:10px;border:1px solid #e6e6e6;border-radius:12px">'
                '<strong>Toolbox:</strong> '
                '<a class="pill" href="/desk/toolbox">/desk/toolbox</a>'
                '</div>\n</body>',
                1
            )

    return HTMLResponse(html)


@router.get("/toolbox"'''
s2 = s[:m.start()] + new_ui + s[m.end():]
p.write_text(s2, encoding="utf-8")
print("OK: ui() replaced + toolbox injection added; toolbox decorator hardened")
PY

echo "Done."
