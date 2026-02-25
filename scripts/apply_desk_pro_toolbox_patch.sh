#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro Toolbox Patch ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"

[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_toolbox_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

python - <<'PY'
import re, pathlib, sys

target = pathlib.Path("/opt/trading/modules/desk_pro/api/routes.py")
s = target.read_text(encoding="utf-8")

# 1) Ensure HTMLResponse import
if "HTMLResponse" not in s:
    m = re.search(r"from\s+fastapi\.responses\s+import\s+([^\n]+)", s)
    if m:
        line = m.group(0)
        imports = m.group(1)
        if "HTMLResponse" not in imports:
            s = s.replace(line, line + ", HTMLResponse", 1)
    else:
        m2 = re.search(r"(from\s+fastapi\s+import\s+[^\n]+\n)", s)
        if m2:
            insert_at = m2.end(1)
            s = s[:insert_at] + "from fastapi.responses import HTMLResponse\n" + s[insert_at:]
        else:
            s = "from fastapi.responses import HTMLResponse\n" + s

# 2) Insert toolbox route if absent
if "/toolbox" in s:
    print("Toolbox route already present; no changes.")
    target.write_text(s, encoding="utf-8")
    sys.exit(0)

toolbox_block = r'''
@router.get("/toolbox", response_class=HTMLResponse)
def desk_toolbox():
    """Boîte à outils info (Commandes + Endpoints + Tunnel SSH)."""
    html = """
    <html>
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Desk Pro — Boîte à outils info</title>
        <style>
          body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px; }
          h1 { margin: 0 0 6px; }
          .muted { color: #666; margin: 0 0 16px; }
          .card { border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px 16px; margin: 12px 0; }
          code, pre { background: #f6f6f6; border-radius: 10px; }
          pre { padding: 12px; overflow-x: auto; }
          .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
          @media (max-width: 900px) { .row { grid-template-columns: 1fr; } }
          a { text-decoration: none; }
          .pill { display:inline-block; padding:6px 10px; border:1px solid #ddd; border-radius:999px; margin:4px 6px 0 0; color:#111; }
        </style>
      </head>
      <body>
        <h1>Desk Pro — Boîte à outils info</h1>
        <p class="muted">Raccourcis, endpoints, et accès Windows via tunnel SSH.</p>

        <div class="card">
          <div><strong>Endpoints</strong></div>
          <div style="margin-top:8px">
            <a class="pill" href="/desk/ui">/desk/ui</a>
            <a class="pill" href="/desk/health">/desk/health</a>
            <a class="pill" href="/desk/snapshot">/desk/snapshot</a>
            <a class="pill" href="/desk/form">/desk/form</a>
          </div>
        </div>

        <div class="row">
          <div class="card">
            <div><strong>Windows → UI (recommandé)</strong></div>
            <p class="muted">Dans PowerShell Windows (garde la session ouverte) :</p>
            <pre>ssh -L 18010:127.0.0.1:8010 ghost@admin-trading</pre>
            <p class="muted">Puis dans le navigateur Windows :</p>
            <pre>http://127.0.0.1:18010/desk/ui</pre>
          </div>

          <div class="card">
            <div><strong>Raccourcis (Debian)</strong></div>
            <pre>menu-desk_pro
cmd-desk_pro sanity
cmd-desk_pro health
cmd-desk_pro logs 200</pre>
            <p class="muted">Réinstaller les shortcuts :</p>
            <pre>sudo bash /opt/trading/scripts/install_desk_pro_shortcuts.sh</pre>
          </div>
        </div>

        <div class="card">
          <div><strong>Diagnostic rapide (Debian)</strong></div>
          <pre>cmd-desk_pro health
cmd-desk_pro sanity
curl -sS http://127.0.0.1:8010/desk/health</pre>
        </div>

        <div class="card">
          <div><strong>Notes</strong></div>
          <ul>
            <li>Si le port local est occupé sur Windows, change 18010 → 28010, etc.</li>
            <li>Ne lance pas <code>netstat/findstr</code> dans Debian; c'est côté Windows.</li>
          </ul>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
'''

# Insert after existing /ui route if possible; else append.
inserted = False
m = re.search(r'@router\.get\(\"/ui\"[^\n]*\)\n(?:.*\n){1,200}?\n', s)
if m:
    pos = m.end(0)
    s = s[:pos] + toolbox_block + "\n" + s[pos:]
    inserted = True

if not inserted:
    s = s.rstrip() + "\n\n" + toolbox_block + "\n"

target.write_text(s, encoding="utf-8")
print("OK: Toolbox route inserted at /desk/toolbox")
PY

echo "Done."
echo "Next: sudo bash $REPO/scripts/sanity_desk_pro_toolbox.sh"
