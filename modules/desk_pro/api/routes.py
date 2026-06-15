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

def _telegram_send(text: str, channel: str = "alerts") -> dict:
    try:
        from modules.env.env import load_env
        load_env()
        from shared.telegram_channels import send_to_channel
        result = send_to_channel(channel, text, source="desk_pro")
        return {"sent": result.get("ok", False), "reason": "telegram"}
    except Exception as e:
        return {"sent": False, "reason": str(e)}

_TELEGRAM_API_HOST = "api.telegram.org"

def _webhook_send(alert: dict) -> dict:
    url = _env_str("ALERT_WEBHOOK_URL")
    if not url:
        return {"sent": False, "reason": "not configured"}
    if _TELEGRAM_API_HOST in url:
        return {"sent": False, "reason": "webhook_url_is_telegram_api ÔÇö use TELEGRAM_BOT_TOKEN for Telegram"}
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
        "message": "Desk Pro test alert ÔÇö this is a smoke test",
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
    """Bo├«te ├á outils info (Commandes + Endpoints + Tunnel SSH)."""
    html = """
    <html>
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Desk Pro ÔÇö Bo├«te ├á outils info</title>
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
        <h1>Desk Pro ÔÇö Bo├«te ├á outils info</h1>
        <p class="muted">Raccourcis, endpoints, et acc├¿s Windows via tunnel SSH.</p>

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
            <div><strong>Windows ÔåÆ UI (recommand├®)</strong></div>
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
            <p class="muted">R├®installer les shortcuts :</p>
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
            <li>Si le port local est occup├® sur Windows, change 18010 ÔåÆ 28010, etc.</li>
            <li>Ne lance pas <code>netstat/findstr</code> dans Debian; c'est c├┤t├® Windows.</li>
          </ul>
        </div>
      
        <div class="card">
          <h3>Desk Pro ÔÇö Diagnostics</h3>
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
            <div class="muted">Derni├¿res lignes log UI</div>
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


@router.get("/spacex")
def desk_spacex():
    spath = Path("data/data_center/views/spacex_super_desk/latest.json")
    if spath.exists():
        return json.loads(spath.read_text(encoding="utf-8"))
    return {"ok": False, "error": "no spacex_super_desk data yet", "action": "run spacex-super-desk collect-once"}


@router.get("/spacex/snapshot")
def desk_spacex_snapshot():
    spath = Path("data/ipo/spacex/scored/latest_snapshot.json")
    if spath.exists():
        return json.loads(spath.read_text(encoding="utf-8"))
    return {"ok": False, "error": "no snapshot yet"}


@router.get("/spacex/command-center")
def desk_spacex_command_center():
    cpath = Path("data/ipo/spacex/command_center/latest.json")
    if cpath.exists():
        return json.loads(cpath.read_text(encoding="utf-8"))
    spath = Path("data/ipo/spacex/scored/latest_snapshot.json")
    if spath.exists():
        from modules.ipo_tracking.command_center import command_center_json
        return command_center_json()
    return {"ok": False, "error": "no data yet"}


@router.get("/spacex/ui", response_class=HTMLResponse)
def desk_spacex_ui():
    try:
        from modules.localcms.app.main import _spacex_data
        data = _spacex_data()
    except Exception:
        cpath = Path("data/ipo/spacex/command_center/latest.json")
        data = json.loads(cpath.read_text()) if cpath.exists() else {}

    price = data.get("price") or 135
    gap = data.get("gap_pct", 0) or 0
    volume = data.get("volume")
    vwap = data.get("vwap")
    edge_score = data.get("edge_score", 0)
    open_score = data.get("open_score", 0)
    action = data.get("action", "—")
    confidence = data.get("confidence", "—")
    top_setup = data.get("top_setup", "—")
    top_prob = data.get("top_setup_prob_pct", 0)
    sector_regime = data.get("sector_regime", "—")
    disagreement = data.get("disagreement", 0) or 0
    analogs = data.get("ipo_analogs", [])
    pipeline_healthy = data.get("pipeline_healthy", False)
    sources_ok = data.get("sources_ok", 0)
    sources_total = data.get("sources_total", 5)
    risks = data.get("risks", [])
    market_state = data.get("market_state", "PRE_MARKET")
    generated_at = (data.get("generated_at") or "")[:19].replace("T", " ")
    entry_price = data.get("entry")
    stop_price = data.get("stop")
    tp1_price = data.get("tp1")
    tp2_price = data.get("tp2")

    edge_fill = min(5, max(0, edge_score // 20))
    ebar = "|" * edge_fill + "." * (5 - edge_fill)

    action_cls = "cred-set" if "A" in str(action) else ("cred-future" if "B" in str(action) or "WATCH" in str(action) else "cred-unknown")
    health_cls = "cred-set" if pipeline_healthy else "cred-absent"
    market_cls = "cred-set" if market_state == "OPEN" else "cred-unknown"

    analog_rows = ""
    for a in (analogs or [])[:3]:
        pct = a.get("pct", a.get("probability_pct", 0))
        analog_rows += f"<tr><td>{a['symbol']}</td><td class='num'>{pct}%</td></tr>"

    risk_notice = ""
    if risks and risks != ["None"]:
        risk_notice = "<div class='notice'>" + "".join(f"<div>⚠ {r}</div>" for r in risks) + "</div>"

    levels_rows = ""
    if entry_price: levels_rows += f"<tr><td>Entry</td><td class='num'>${entry_price:.2f}</td></tr>"
    if stop_price: levels_rows += f"<tr><td style='color:#ef5350'>Stop</td><td class='num' style='color:#ef5350'>${stop_price:.2f}</td></tr>"
    if tp1_price: levels_rows += f"<tr><td style='color:#30d158'>TP1</td><td class='num' style='color:#30d158'>${tp1_price:.2f}</td></tr>"
    if tp2_price: levels_rows += f"<tr><td style='color:#30d158'>TP2</td><td class='num' style='color:#30d158'>${tp2_price:.2f}</td></tr>"

    vol_str = f"{volume/1e6:.1f}M" if volume and volume >= 1e6 else (f"{volume/1e3:.0f}K" if volume and volume >= 1e3 else str(volume) if volume else "—")

    return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SPCX Command Center</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f5f5f7;color:#1d1d1f;padding:20px;max-width:900px;margin:0 auto}}
h1{{font-size:20px;margin-bottom:4px}}
.subtitle{{color:#666;font-size:13px;margin-bottom:20px}}
.summary-bar{{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}}
.summary-card{{flex:1;min-width:130px;padding:14px;border-radius:12px;border:1px solid #e6e6e6;background:#fff}}
.summary-card .num{{font-size:22px;font-weight:700}}
.summary-card .label{{font-size:11px;color:#666;margin-top:3px}}
.summary-card .bar{{font-family:monospace;font-size:13px;color:#30d158;letter-spacing:2px;margin-top:3px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;border:1px solid #e6e6e6;margin-bottom:14px}}
th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid #eee;font-size:13px}}
th{{background:#fafafa;font-weight:600;color:#666;text-transform:uppercase;font-size:11px}}
.cred-set{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:#d1fae5;color:#065f46}}
.cred-absent{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:#ffe4e6;color:#9f1239}}
.cred-unknown{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:#f3f4f6;color:#6b7280}}
.cred-future{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;background:#e0e7ff;color:#3730a3}}
.notice{{background:#fef3c7;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;font-size:13px;margin-bottom:16px;color:#92400e}}
.links-bar{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}}
.links-bar a{{color:#1d1d1f;padding:4px 10px;border:1px solid #ddd;border-radius:8px;text-decoration:none;font-size:12px}}
.links-bar a:hover{{background:#eee}}
</style></head>
<body>
<h1>🚀 SpaceX / SPCX Command Center</h1>
<p class="subtitle">{generated_at} — <span class="{market_cls}">{market_state}</span> · <span class="{health_cls}">{'HEALTHY' if pipeline_healthy else 'DEGRADED'}</span> · Sources {sources_ok}/{sources_total}</p>

<div class="links-bar">
  <a href="/desk/spacex/command-center" target="_blank">JSON</a>
  <a href="/desk/ui">Desk UI</a>
</div>

{risk_notice}

<div class="summary-bar">
  <div class="summary-card"><div class="num">${price:.2f}</div><div class="label">Price</div></div>
  <div class="summary-card"><div class="num">{gap:+.1f}%</div><div class="label">Gap vs IPO</div></div>
  <div class="summary-card"><div class="num">{edge_score}</div><div class="bar">{ebar}</div><div class="label">Edge Score</div></div>
  <div class="summary-card"><div class="num">{open_score}</div><div class="label">Open Score</div></div>
</div>

<div class="summary-bar">
  <div class="summary-card"><div class="label">Action</div><div class="num" style="font-size:18px"><span class="{action_cls}" style="font-size:13px">{action}</span></div></div>
  <div class="summary-card"><div class="label">Confidence</div><div class="num" style="font-size:18px">{confidence}</div></div>
  <div class="summary-card"><div class="label">Top Setup</div><div class="num" style="font-size:16px">{top_setup}</div><div class="label">{top_prob}% probability</div></div>
  <div class="summary-card"><div class="label">Sector</div><div class="num" style="font-size:16px">{sector_regime}</div><div class="label">disagreement {disagreement:.1f}%</div></div>
</div>

<div class="summary-bar">
  <div class="summary-card"><div class="label">Volume</div><div class="num" style="font-size:16px">{vol_str}</div></div>
  <div class="summary-card"><div class="label">VWAP</div><div class="num" style="font-size:16px">{'${:,.2f}'.format(vwap) if vwap else '—'}</div></div>
  <div class="summary-card" style="flex:2"><div class="label">IPO Analogs</div>
    <table style="margin-bottom:0"><tr><th>Ticker</th><th style="text-align:right">Match</th></tr>{analog_rows if analog_rows else '<tr><td colspan="2">No data</td></tr>'}</table>
  </div>
</div>

{'<table><tr><th colspan="2">Trade Levels</th></tr>'+levels_rows+'</table>' if levels_rows else ''}

<script>setTimeout(() => location.reload(), 60000);</script>
</body></html>""")


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

    Returns the full score_spcx() payload enriched with data_source metadata.
    Read-only. monitor_only=True always.
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
