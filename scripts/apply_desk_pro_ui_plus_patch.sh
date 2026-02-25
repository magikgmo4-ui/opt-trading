#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
TARGET="$REPO/modules/desk_pro/api/routes.py"

echo "=== Apply Desk Pro UI+Diagnostics+Logs Patch ==="
echo "Repo:   $REPO"
echo "Target: $TARGET"

[[ -f "$TARGET" ]] || { echo "FAIL: routes.py not found at $TARGET"; exit 2; }

ts="$(date +%Y%m%d_%H%M%S)"
bak="${TARGET}.bak_uiplus_${ts}"
cp -a "$TARGET" "$bak"
echo "Backup: $bak"

python - <<'PY'
import re, datetime
from pathlib import Path

p = Path("/opt/trading/modules/desk_pro/api/routes.py")
s = p.read_text(encoding="utf-8")

# 1) Ensure imports
def ensure_import(line: str):
    global s
    if line in s:
        return
    # insert near top (after shebang/comments if any)
    parts = s.splitlines(True)
    insert_at = 0
    for i, ln in enumerate(parts[:30]):
        if ln.startswith("from ") or ln.startswith("import "):
            insert_at = i
            break
    parts.insert(insert_at, line + "\n")
    s = "".join(parts)

ensure_import("import datetime")
ensure_import("from pathlib import Path")
ensure_import("from fastapi import Request")

# 2) Logger helper
if "_dp_log(" not in s:
    logger_block = '''
# === Desk Pro UI logger (minimal) ===
def _dp_log(msg: str) -> None:
    try:
        logdir = Path("/opt/trading/tmp")
        logdir.mkdir(parents=True, exist_ok=True)
        fp = logdir / "desk_pro_ui.log"
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        prev = fp.read_text(encoding="utf-8") if fp.exists() else ""
        fp.write_text(prev + f"[{ts}] {msg}\\n", encoding="utf-8")
    except Exception:
        pass
'''
    m = re.search(r"router\s*=\s*APIRouter\([^\)]*\)\s*\n", s)
    if m:
        pos = m.end(0)
        s = s[:pos] + "\n" + logger_block.strip() + "\n" + s[pos:]
    else:
        s = logger_block.strip() + "\n\n" + s

# 3) Inject _dp_log into /ui handler
m = re.search(r'@router\.get\(\s*["\']/ui["\'][^\)]*\)\s*\n\s*def\s+([A-Za-z0-9_]+)\s*\(', s)
if m:
    fname = m.group(1)
    # find end of def line
    defline = re.search(rf'(def\s+{re.escape(fname)}\s*\([^\)]*\)\s*:\s*\n)', s[m.start():])
    if defline:
        start = m.start() + defline.end(1)
        if "_dp_log(" not in s[start:start+200]:
            s = s[:start] + '    _dp_log("desk_ui")\n' + s[start:]

# 4) Add /logs/latest endpoint
if '"/logs/latest"' not in s:
    logs_block = '''
@router.get("/logs/latest")
def desk_logs_latest(n: int = 200):
    # Returns last N lines of /opt/trading/tmp/desk_pro_ui.log
    _dp_log(f"logs_latest n={n}")
    fp = Path("/opt/trading/tmp/desk_pro_ui.log")
    if not fp.exists():
        return {"ok": True, "lines": [], "note": "no log yet"}
    txt = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
    n = max(1, min(int(n), 2000))
    return {"ok": True, "lines": txt[-n:]}
'''
    s = s.rstrip() + "\n\n" + logs_block.strip() + "\n"

# 5) UI HTML: add toolbox pill + diagnostics card (best-effort string replace)
# Add toolbox pill in the endpoints pills (if present)
if "/desk/toolbox" not in s:
    s = s.replace('href="/desk/form">/desk/form</a>',
                  'href="/desk/form">/desk/form</a>\n            <a class="pill" href="/desk/toolbox">/desk/toolbox</a>',
                  1)

# Add Diagnostics block into UI HTML before </body> (if /ui page is HTML)
if "Desk Pro — Diagnostics" not in s and "</body>" in s:
    diag_html = r'''
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
    s = s.replace("</body>", diag_html + "\n</body>", 1)

p.write_text(s, encoding="utf-8")
print("OK: routes.py patched (UI+Diagnostics+Logs)")
PY

echo "Done."
echo "Next: sudo bash $REPO/scripts/sanity_desk_pro_ui_plus.sh"
