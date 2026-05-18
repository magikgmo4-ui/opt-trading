from __future__ import annotations
from fastapi import Request
from pathlib import Path
import datetime
import time
import json
import urllib.request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from modules.desk_pro.models import DeskForm, Snapshot, ScoreResult
from modules.desk_pro.service.aggregator import build_snapshot
from modules.desk_pro.service.scoring import compute_probability
from modules.desk_pro.ui.page import render_ui_html

WEBHOOK_BASE = "http://127.0.0.1:8000"
DESK_ERRORS_MAX = 50
_desk_errors: list[dict] = []

def _probe_url(url: str, timeout: int = 3) -> dict | None:
    label = url.split("?")[0] if "?" in url else url
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except Exception as e:
        _desk_errors.append({
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "probe": label,
            "error": str(e),
        })
        if len(_desk_errors) > DESK_ERRORS_MAX:
            _desk_errors.pop(0)
        return None

def _source_mode(url_path: str) -> str:
    """Determine data source mode for a given endpoint path."""
    if "webhook" in url_path or "perf" in url_path:
        return "live"
    if "snapshot" in url_path or "fixture" in url_path:
        return "fixture"
    return "mock"

router = APIRouter(prefix="/desk", tags=["desk-pro"])


# === Desk Pro UI logger (minimal) ===
def _dp_log(msg: str) -> None:
    try:
        logdir = Path("/opt/trading/tmp")
        logdir.mkdir(parents=True, exist_ok=True)
        fp = logdir / "desk_pro_ui.log"
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        prev = fp.read_text(encoding="utf-8") if fp.exists() else ""
        fp.write_text(prev + f"[{ts}] {msg}\n", encoding="utf-8")
    except Exception:
        pass
@router.get("/health")
def health():
    return {"ok": True, "module": "desk_pro", "mode": "step2_mock"}

@router.get("/status")
def pipeline_status():
    desk = {"ok": True, "module": "desk_pro", "mode": "step2_mock"}
    perf = _probe_url("http://127.0.0.1:8010/perf/summary")
    perf_open = _probe_url("http://127.0.0.1:8010/perf/open")
    webhook_state = _probe_url(f"{WEBHOOK_BASE}/api/state")
    webhook_risk = _probe_url(f"{WEBHOOK_BASE}/api/risk/status")
    webhook_metrics = _probe_url(f"{WEBHOOK_BASE}/api/metrics?limit=5&window_min=5")
    webhook_events = _probe_url(f"{WEBHOOK_BASE}/api/events?limit=3")
    webhook = None
    if webhook_state or webhook_risk:
        webhook = {
            "ok": True,
            "trade_allowed": (webhook_risk or {}).get("trade_allowed"),
            "active_engine": (webhook_state or {}).get("active_engine"),
            "risk_limits": (webhook_risk or {}).get("risk_limits"),
        }
    sources = {
        "snapshot": _source_mode("snapshot"),
        "health": _source_mode("health"),
        "perf_summary": _source_mode("perf"),
        "perf_open": _source_mode("perf"),
        "webhook_state": _source_mode("webhook"),
        "webhook_events": _source_mode("webhook"),
    }
    errors = []
    for e in reversed(_desk_errors[-10:]):
        errors.append(e)
    return {
        "desk_pro": desk,
        "perf": perf,
        "perf_open": perf_open,
        "webhook": webhook,
        "webhook_metrics": webhook_metrics,
        "recent_webhook_events": (webhook_events or {}).get("events"),
        "sources": sources,
        "error_count": len(_desk_errors),
        "recent_errors": errors,
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
    }

@router.get("/errors")
def desk_errors(limit: int = 20):
    return {
        "ok": True,
        "count": len(_desk_errors),
        "errors": list(reversed(_desk_errors[-limit:])),
    }

@router.get("/snapshot", response_model=Snapshot)
def snapshot(source: str = "fixture"):
    t0 = time.time()
    snap = build_snapshot(source=source)
    ms = int((time.time() - t0) * 1000)
    snap.meta["build_ms"] = str(ms)
    return snap

@router.post("/form", response_model=ScoreResult)
def form_score(form: DeskForm):
    snap = build_snapshot()
    return compute_probability(form, snap)

@router.get("/ui", response_class=HTMLResponse)
def ui():
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
            <a class="pill" href="/desk/form">/desk/form</a> <a href="/desk/toolbox" style="margin-left:10px">toolbox</a>
            <a class="pill" href="/desk/toolbox">/desk/toolbox</a>
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

</body>
    </html>
    """
    return HTMLResponse(content=html)

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
