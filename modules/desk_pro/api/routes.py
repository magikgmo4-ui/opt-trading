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
from modules.desk_pro.service.vision_panel import (
    read_news_panel_data,
    read_screener_panel_data,
    read_telegram_claim_panel_data,
    read_vision_panel_data,
)
from modules.desk_pro.ui.page import render_ui_html

WEBHOOK_BASE = "http://127.0.0.1:8000"
DESK_ERRORS_MAX = 50
ALERT_COOLDOWN_SEC = int(__import__("os").environ.get("ALERT_COOLDOWN_SEC", "300"))
ALERTS_JSONL = Path("/opt/trading/tmp/desk_pro_alerts.jsonl")
_desk_errors: list[dict] = []
_alert_state: dict = {"last_status": None, "last_ts": None, "cooldown_until": None}

# ----- Alert destinations (optional, read from env at dispatch time) -----
def _env_str(k: str) -> str:
    return __import__("os").environ.get(k, "").strip()

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

def _compute_health(d: dict) -> dict:
    checks = []
    wh = d.get("webhook")
    if wh is None:
        checks.append({"check": "webhook", "status": "fail", "reason": "unreachable"})
    else:
        checks.append({"check": "webhook", "status": "pass"})

    perf = d.get("perf")
    if perf is None:
        checks.append({"check": "perf", "status": "fail", "reason": "unreachable"})
    else:
        checks.append({"check": "perf", "status": "pass"})

    whm = d.get("webhook_metrics") or {}
    age = whm.get("last_event_age_sec")
    if age is None:
        checks.append({"check": "webhook_activity", "status": "warn", "reason": "no events yet"})
    elif age > 7200:
        checks.append({"check": "webhook_activity", "status": "fail", "reason": f"{age}s since last event"})
    elif age > 3600:
        checks.append({"check": "webhook_activity", "status": "warn", "reason": f"{age}s since last event"})
    else:
        checks.append({"check": "webhook_activity", "status": "pass"})

    ec = d.get("error_count", 0)
    if ec > 20:
        checks.append({"check": "probe_errors", "status": "fail", "reason": f"{ec} errors"})
    elif ec > 5:
        checks.append({"check": "probe_errors", "status": "warn", "reason": f"{ec} errors"})
    else:
        checks.append({"check": "probe_errors", "status": "pass"})

    for k, v in (d.get("sources") or {}).items():
        if v == "down":
            checks.append({"check": f"source_{k}", "status": "fail", "reason": f"mode={v}"})

    has_fail = any(c["status"] == "fail" for c in checks)
    has_warn = any(c["status"] == "warn" for c in checks)
    if has_fail:
        overall = "down"
    elif has_warn:
        overall = "degraded"
    else:
        overall = "healthy"

    return {"status": overall, "checks": checks}

def _check_alert(health_status: str) -> dict:
    now = datetime.datetime.utcnow()
    cooldown_ts = _alert_state.get("cooldown_until")
    if cooldown_ts and now < cooldown_ts:
        return {
            "triggered": False,
            "reason": "cooldown",
            "cooldown_remaining_sec": int((cooldown_ts - now).total_seconds()),
            "last_status": _alert_state.get("last_status"),
            "last_ts": _alert_state["last_ts"].isoformat() + "Z" if _alert_state.get("last_ts") else None,
        }
    if health_status in ("degraded", "down"):
        alert = {
            "ts": now.isoformat() + "Z",
            "status": health_status,
        }
        try:
            ALERTS_JSONL.parent.mkdir(parents=True, exist_ok=True)
            with open(str(ALERTS_JSONL), "a", encoding="utf-8") as f:
                f.write(json.dumps(alert) + "\n")
        except Exception:
            pass
        dispatch = _dispatch_alert(alert)
        _alert_state["last_status"] = health_status
        _alert_state["last_ts"] = now
        _alert_state["cooldown_until"] = now + datetime.timedelta(seconds=ALERT_COOLDOWN_SEC)
        return {"triggered": True, "status": health_status, "ts": alert["ts"], "cooldown_sec": ALERT_COOLDOWN_SEC, "dispatch": dispatch}
    _alert_state["last_status"] = health_status
    _alert_state["last_ts"] = now
    return {"triggered": False, "reason": "healthy"}

def _read_alerts(limit: int = 10) -> list:
    if not ALERTS_JSONL.exists():
        return []
    try:
        lines = ALERTS_JSONL.read_text(encoding="utf-8").splitlines()
        return [json.loads(l) for l in lines[-limit:]]
    except Exception:
        return []

def _telegram_send(text: str) -> dict:
    token = _env_str("TELEGRAM_BOT_TOKEN")
    chat_id = _env_str("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return {"sent": False, "reason": "not configured"}
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
            return {"sent": body.get("ok", False), "reason": "telegram"}
    except Exception as e:
        return {"sent": False, "reason": str(e)}

_TELEGRAM_API_HOST = "api.telegram.org"

def _webhook_send(alert: dict) -> dict:
    url = _env_str("ALERT_WEBHOOK_URL")
    if not url:
        return {"sent": False, "reason": "not configured"}
    if _TELEGRAM_API_HOST in url:
        return {"sent": False, "reason": "webhook_url_is_telegram_api — use TELEGRAM_BOT_TOKEN for Telegram"}
    try:
        payload = json.dumps(alert).encode()
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"sent": resp.status == 200, "reason": f"webhook status={resp.status}"}
    except Exception as e:
        return {"sent": False, "reason": str(e)}

def _dispatch_alert(alert: dict) -> list:
    results = []
    tg = _telegram_send(f"Desk Pro ALERT: status={alert.get('status')}")
    results.append({"destination": "telegram", **tg})
    wh = _webhook_send(alert)
    results.append({"destination": "webhook", **wh})
    return results

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
    result = {
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
    health = _compute_health(result)
    result["health"] = health
    result["alert"] = _check_alert(health["status"])
    return result

@router.get("/errors")
def desk_errors(limit: int = 20):
    return {
        "ok": True,
        "count": len(_desk_errors),
        "errors": list(reversed(_desk_errors[-limit:])),
    }

@router.get("/alerts")
def desk_alerts(limit: int = 10):
    return {
        "ok": True,
        "destinations": {
            "telegram": bool(_env_str("TELEGRAM_BOT_TOKEN") and _env_str("TELEGRAM_CHAT_ID")),
            "webhook": bool(_env_str("ALERT_WEBHOOK_URL")),
        },
        "state": {
            "last_status": _alert_state.get("last_status"),
            "last_ts": _alert_state["last_ts"].isoformat() + "Z" if _alert_state.get("last_ts") else None,
            "cooldown_until": _alert_state["cooldown_until"].isoformat() + "Z" if _alert_state.get("cooldown_until") else None,
        },
        "alerts": _read_alerts(limit=limit),
    }

@router.post("/alert/test")
def desk_alert_test():
    alert = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "status": "test",
        "message": "Desk Pro test alert — this is a smoke test",
    }
    dispatch = _dispatch_alert(alert)
    results = []
    for d in dispatch:
        status = "delivered" if d.get("sent") else ("failed" if d.get("reason") != "not configured" else "skipped")
        results.append({"destination": d["destination"], "status": status, "reason": d.get("reason")})
    return {"ok": True, "alert": alert, "dispatch": results}

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

@router.get("/vision")
def desk_vision():
    """Return current vision_context.coinglass.v1 data for the Desk Pro panel."""
    return read_vision_panel_data()


@router.get("/vision/news")
def desk_vision_news():
    return read_news_panel_data()


@router.get("/vision/screener")
def desk_vision_screener():
    return read_screener_panel_data()


@router.get("/vision/telegram-claim")
def desk_vision_telegram_claim():
    return read_telegram_claim_panel_data()


@router.get("/voice")
def desk_voice(q: str = ""):
    """Voice Operator — text command router.

    Query param ?q= accepts natural language commands.
    Supported: "score spcx", "help", "?"
    Returns: matched, intent, response (human-readable), data (raw payload).
    Read-only. monitor_only enforced.
    """
    from modules.desk_pro.service.voice_operator import dispatch_command
    return dispatch_command(q)


@router.get("/spacex/score")
def desk_spacex_score():
    """SPCX composite score — reads recent CDP + webhook events and scores the setup.

    Voice Operator command: "Score SPCX"

    Returns the full score_spcx() payload enriched with data_source metadata.
    Read-only. monitor_only=True always.
    """
    from modules.desk_pro.service.spcx_score_reader import read_spcx_score
    return read_spcx_score()

    Returns: score (0-100), grade (C/B/A/A+), setup_state, levels, risk_notes, monitor_only.
    """
    from modules.desk_pro.service.spcx_score_reader import read_spcx_score
    return read_spcx_score()


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
