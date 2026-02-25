#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI Inject Patch (Toolbox+Diagnostics) ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"
[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_uiinject_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

python - <<'PY'
import re
from pathlib import Path

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

ui = re.search(r'@router\.get\(\s*["\']/ui["\'][^\)]*\)\s*\n\s*def\s+([A-Za-z0-9_]+)\s*\([^\)]*\)\s*:\s*\n', s)
if not ui:
    raise SystemExit("FAIL: could not find /ui handler in routes.py")

start = ui.end()

# Find html triple-quoted string inside /ui handler
m = re.search(r'html\s*=\s*("""|\'\'\')', s[start:])
if not m:
    raise SystemExit("FAIL: could not find html triple-quoted string in /ui handler")

q = m.group(1)
hs = start + m.end()  # pos after opening quotes

endm = re.search(re.escape(q), s[hs:])
if not endm:
    raise SystemExit("FAIL: could not find end of html string")

he = hs + endm.start()
html = s[hs:he]

# Add toolbox pill link
if "/desk/toolbox" not in html:
    html = re.sub(r'(<a[^>]+href="/desk/form"[^>]*>\s*/desk/form\s*</a>)',
                  r'\1\n            <a class="pill" href="/desk/toolbox">/desk/toolbox</a>',
                  html, count=1)

# Inject Diagnostics block before </body>
if "Desk Pro — Diagnostics" not in html and "</body>" in html:
    diag = r'''
        <div class="card">
          <h3>Desk Pro — Diagnostics</h3>
          <div class="row">
            <div>
              <div class="muted">Status (live via /desk/health)</div>
              <pre id="dp_health">loading...</pre>
              <button id="dp_health_btn">Refresh status</button>
            </div>
            <div>
              <div class="muted">Commandes (Debian)</div>
              <pre id="dp_cmds">menu-desk_pro
cmd-desk_pro sanity
cmd-desk_pro health
cmd-desk_pro logs 200</pre>
              <button id="dp_copy_cmds">Copy commands</button>
            </div>
          </div>
          <div style="margin-top:10px">
            <div class="muted">Dernières lignes log UI</div>
            <pre id="dp_logs">loading...</pre>
            <button id="dp_logs_btn">Refresh logs</button>
          </div>
        </div>

        <script>
          async function dpFetchHealth() {
            try {
              const r = await fetch('/desk/health');
              const j = await r.json();
              document.getElementById('dp_health').textContent = JSON.stringify(j, null, 2);
            } catch(e) {
              document.getElementById('dp_health').textContent = 'ERROR: ' + e;
            }
          }
          async function dpFetchLogs() {
            try {
              const r = await fetch('/desk/logs/latest?n=200');
              const j = await r.json();
              document.getElementById('dp_logs').textContent = (j.lines || []).join('\n');
            } catch(e) {
              document.getElementById('dp_logs').textContent = 'ERROR: ' + e;
            }
          }
          document.addEventListener('DOMContentLoaded', () => {
            const hb = document.getElementById('dp_health_btn');
            const lb = document.getElementById('dp_logs_btn');
            const cb = document.getElementById('dp_copy_cmds');
            if (hb) hb.onclick = dpFetchHealth;
            if (lb) lb.onclick = dpFetchLogs;
            if (cb) cb.onclick = async () => {
              const t = document.getElementById('dp_cmds').textContent;
              try { await navigator.clipboard.writeText(t); cb.textContent='Copied!'; setTimeout(()=>cb.textContent='Copy commands', 1200); } catch(e) {}
            };
            dpFetchHealth();
            dpFetchLogs();
          });
        </script>
'''
    html = html.replace("</body>", diag + "\n</body>", 1)

s2 = s[:hs] + html + s[he:]
p.write_text(s2, encoding="utf-8")
print("OK: injected toolbox pill + diagnostics into /desk/ui HTML")
PY

echo "Done."
echo "Restart uvicorn if needed, then open /desk/ui"
