from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import subprocess
import sys
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MENU_FILE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "opt_trading_menu.json"
STATE_CACHE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "state_cache.json"
TMUX_LOG_DIR = PROJECT_ROOT / "logs"
LOCALCMS_LATEST_JSON = PROJECT_ROOT / "tmp" / "localcms_latest.json"
JOURNAL_DIR = PROJECT_ROOT / "data" / "journal" / "daily"

CRITICAL_SESSIONS: frozenset[str] = frozenset({
    "openclaw-core",
    "screeners",
    "strict-workers",
})

ALL_SESSIONS: list[dict] = [
    {"session": "openclaw-core",    "critical": True,  "machine": "db-layer",      "description": "Gateway + Bridge + Health + Logs"},
    {"session": "screeners",        "critical": True,  "machine": "admin-trading",  "description": "TradingView + Webhook + Bot Vision + Telegram"},
    {"session": "strict-workers",   "critical": True,  "machine": "admin-trading",  "description": "8 pipeline workers (DRY_RUN=1)"},
    {"session": "trading-pipeline", "critical": False, "machine": "admin-trading",  "description": "kil_v1 + SimEx + Execution + Risk + Position"},
    {"session": "market-data",      "critical": False, "machine": "admin-trading",  "description": "Binance + CoinGecko + Derivatives + Analyzers + Scanner + Hub"},
    {"session": "apps-connectors",  "critical": False, "machine": "db-layer",      "description": "Airtable + ClickUp + Sheets + Health"},
    {"session": "desk-pro",         "critical": False, "machine": "admin-trading",  "description": "Runner + Orchestrator + Perf + Logs"},
    {"session": "kg-repo",          "critical": False, "machine": "db-layer",      "description": "Memory Bricks + Learning Feeder + Health"},
    {"session": "localcms-ui",      "critical": False, "machine": "db-layer",      "description": "LocalCMS Consumer + Health + Logs"},
]

GLOBAL_MENU_SECTIONS = [
    {"id": "runtime",       "label": "Runtime",       "icon": "⚡"},
    {"id": "trading",       "label": "Trading",       "icon": "📈"},
    {"id": "data",          "label": "Market Data",   "icon": "📊"},
    {"id": "ai",            "label": "AI & Providers","icon": "🧠"},
    {"id": "desk",          "label": "Desk Pro",      "icon": "🖥️"},
    {"id": "vision",        "label": "Vision",        "icon": "👁️"},
    {"id": "perf",          "label": "Performance",   "icon": "📉"},
    {"id": "infra",         "label": "Infrastructure","icon": "🔌"},
    {"id": "registries",    "label": "Registries",    "icon": "🗂️"},
    {"id": "workers",       "label": "Workers",       "icon": "⚙️"},
    {"id": "ops",           "label": "Ops",           "icon": "🔧"},
    {"id": "tooling",       "label": "Tooling",       "icon": "🛠️"},
    {"id": "shared",        "label": "Shared Libs",   "icon": "📦"},
    {"id": "archive",       "label": "Archive",       "icon": "🗄️"},
]

app = FastAPI(title="LocalCMS", version="1.0.0")


def _read_json(path: Path) -> dict | list:
    if not path.exists():
        return {"error": f"File not found: {path.name}"}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return {"error": f"Failed to read {path.name}: {e}"}


def _list_tmux_sessions() -> list[str]:
    try:
        r = subprocess.run(
            ["tmux", "list-sessions", "-F", "#S"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode != 0:
            return []
        return [s.strip() for s in r.stdout.splitlines() if s.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return []


def _build_tmux_report() -> dict:
    active = _list_tmux_sessions()
    active_set = frozenset(active)
    expected_ids = frozenset(s["session"] for s in ALL_SESSIONS)
    up = expected_ids & active_set
    missing = expected_ids - active_set
    critical_down = missing & CRITICAL_SESSIONS
    non_critical_down = missing - CRITICAL_SESSIONS

    sessions_detail = []
    for s in ALL_SESSIONS:
        sid = s["session"]
        running = sid in active_set
        sessions_detail.append({
            "session": sid,
            "running": running,
            "critical": s["critical"],
            "machine": s["machine"],
            "description": s["description"],
        })

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "all_ok": len(missing) == 0,
        "needs_alert": len(critical_down) > 0,
        "total_expected": len(ALL_SESSIONS),
        "total_up": len(up),
        "total_missing": len(missing),
        "critical_down": sorted(critical_down),
        "non_critical_down": sorted(non_critical_down),
        "sessions": sessions_detail,
    }


# ── API endpoints ────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"ok": True, "module": "localcms", "version": "1.0.0"}


@app.get("/menu")
def get_menu():
    data = _read_json(MENU_FILE)
    return JSONResponse(content=data)


@app.get("/menu/state")
def get_menu_state():
    data = _read_json(STATE_CACHE)
    return JSONResponse(content=data)


@app.get("/runtime/tmux")
def get_runtime_tmux():
    report = _build_tmux_report()
    return JSONResponse(content=report)


@app.get("/runtime/tmux/live")
def get_runtime_tmux_live():
    active = _list_tmux_sessions()
    return JSONResponse(content={
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_sessions": sorted(active),
    })


# ── Journal endpoints ────────────────────────────────────────────────

def _list_journal_entries() -> list[dict]:
    if not JOURNAL_DIR.exists():
        return []
    entries = []
    for f in sorted(JOURNAL_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(f.read_text())
            entries.append({
                "run_id": data.get("run_id", f.stem),
                "started_at": data.get("started_at", ""),
                "duration_s": data.get("duration_s", 0),
                "all_ok": data.get("all_ok", False),
                "closeout_acknowledged": data.get("closeout_acknowledged", False),
                "tmux_count": data.get("tmux_after", {}).get("count", 0),
                "localcms_ok": data.get("localcms_ok", False),
                "validation_verdict": data.get("validation_verdict", ""),
                "pnl_outcome": data.get("pnl_paper", {}).get("outcome", ""),
                "signal": data.get("signal_source", {}).get("signal", ""),
                "symbol": data.get("signal_source", {}).get("symbol", ""),
            })
        except (json.JSONDecodeError, OSError):
            continue
    return entries


@app.get("/journal/daily")
def get_journal_daily():
    entries = _list_journal_entries()
    return JSONResponse(content={
        "journal_type": "daily_session",
        "total": len(entries),
        "entries": entries,
    })


@app.get("/journal/daily/{run_id}")
def get_journal_entry(run_id: str):
    path = JOURNAL_DIR / f"{run_id}.json"
    if not path.exists():
        return JSONResponse(content={"error": f"Journal entry not found: {run_id}"}, status_code=404)
    try:
        data = json.loads(path.read_text())
        return JSONResponse(content=data)
    except (json.JSONDecodeError, OSError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ── HTML UI ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
def ui_index(request: Request):
    tmux = _build_tmux_report()
    menu_data = _read_json(MENU_FILE)
    state_data = _read_json(STATE_CACHE)

    menu_json = json.dumps(menu_data, indent=2)
    tmux_json = json.dumps(tmux, indent=2)
    state_json = json.dumps(state_data, indent=2)

    sessions_rows = ""
    for s in tmux["sessions"]:
        status_badge = (
            '<span class="badge badge-up">UP</span>'
            if s["running"]
            else '<span class="badge badge-down">DOWN</span>'
        )
        crit_badge = (
            '<span class="badge badge-critical">CRITICAL</span>'
            if s["critical"]
            else '<span class="badge badge-noncrit">non-critical</span>'
        )
        sessions_rows += f"""\
<tr>
  <td>{s["session"]}</td>
  <td>{status_badge}</td>
  <td>{crit_badge}</td>
  <td>{s["machine"]}</td>
  <td>{s["description"]}</td>
</tr>"""

    critical_down_html = ""
    if tmux["critical_down"]:
        for c in tmux["critical_down"]:
            critical_down_html += f'<span class="pill pill-danger">{c}</span> '
    else:
        critical_down_html = '<span class="pill pill-ok">none</span>'

    non_critical_down_html = ""
    if tmux["non_critical_down"]:
        for c in tmux["non_critical_down"]:
            non_critical_down_html += f'<span class="pill pill-warn">{c}</span> '
    else:
        non_critical_down_html = '<span class="pill pill-ok">none</span>'

    nav_items = ""
    for domain in menu_data.get("menu", []):
        nav_items += f"""
<a class="nav-item" href="#{domain['id']}">
  <span class="nav-icon">{domain.get('icon', '📄')}</span>
  <span class="nav-label">{domain['label']}</span>
</a>"""

    domain_cards = ""
    for domain in menu_data.get("menu", []):
        children_html = ""
        for child in domain.get("children", []):
            if "children" in child:
                children_html += f"""
<div class="subgroup">
  <div class="subgroup-title">{child['label']}</div>"""
                for item in child["children"]:
                    s = item.get("status", "unknown")
                    badge = STATUS_BADGES.get(s, f'<span class="badge badge-unknown">{s}</span>')
                    children_html += f"""
  <div class="module-row">
    <span class="module-label">{item['label']}</span>
    {badge}
    <span class="module-machine">{item.get('machine', '')}</span>
  </div>"""
                children_html += "</div>"
            else:
                s = child.get("status", "unknown")
                badge = STATUS_BADGES.get(s, f'<span class="badge badge-unknown">{s}</span>')
                children_html += f"""
<div class="module-row">
  <span class="module-label">{child['label']}</span>
  {badge}
  <span class="module-machine">{child.get('machine', '')}</span>
</div>"""
        domain_cards += f"""
<div class="domain-card" id="{domain['id']}">
  <h3 class="domain-title">{domain.get('icon', '')} {domain['label']}</h3>
  {children_html}
</div>"""

    critical_count = sum(1 for s in tmux["sessions"] if s["critical"] and not s["running"])
    total_critical = sum(1 for s in tmux["sessions"] if s["critical"])

    summary_class = "summary-ok" if tmux["all_ok"] else ("summary-warn" if critical_count == 0 else "summary-critical")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Central UI</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; background: #f5f5f7; color: #1d1d1f; }}
    .layout {{ display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }}
    .sidebar {{ background: #1d1d1f; color: #f5f5f7; padding: 20px 12px; overflow-y: auto; position: sticky; top: 0; height: 100vh; }}
    .sidebar h1 {{ font-size: 16px; font-weight: 600; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #333; }}
    .sidebar h1 small {{ display: block; font-size: 11px; font-weight: 400; color: #888; margin-top: 2px; }}
    .nav-item {{ display: flex; align-items: center; gap: 8px; padding: 6px 10px; border-radius: 8px; color: #ccc; text-decoration: none; font-size: 13px; margin-bottom: 2px; transition: background .15s; }}
    .nav-item:hover {{ background: #333; color: #fff; }}
    .nav-icon {{ font-size: 16px; width: 20px; text-align: center; }}
    .nav-label {{ flex: 1; }}
    .main {{ padding: 24px 32px; max-width: 1200px; }}
    .main h2 {{ font-size: 22px; margin-bottom: 8px; }}
    .main .subtitle {{ color: #666; font-size: 14px; margin-bottom: 24px; }}
    .summary-bar {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
    .summary-card {{ flex: 1; min-width: 160px; padding: 16px; border-radius: 12px; border: 1px solid #e6e6e6; background: #fff; }}
    .summary-card .num {{ font-size: 28px; font-weight: 700; }}
    .summary-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    .summary-ok {{ border-left: 4px solid #30d158; }}
    .summary-warn {{ border-left: 4px solid #ff9f0a; }}
    .summary-critical {{ border-left: 4px solid #ff453a; }}
    .section-title {{ font-size: 16px; font-weight: 600; margin: 24px 0 12px; }}
    .domain-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .domain-card {{ background: #fff; border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px 16px; }}
    .domain-title {{ font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #1d1d1f; }}
    .subgroup {{ margin: 8px 0 4px 12px; }}
    .subgroup-title {{ font-size: 12px; font-weight: 600; color: #666; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px; }}
    .module-row {{ display: flex; align-items: center; gap: 8px; padding: 3px 0; font-size: 13px; }}
    .module-label {{ flex: 1; }}
    .module-machine {{ font-size: 11px; color: #999; font-family: monospace; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e6e6e6; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; font-size: 13px; }}
    th {{ background: #fafafa; font-weight: 600; color: #666; text-transform: uppercase; font-size: 11px; letter-spacing: .5px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
    .badge-up {{ background: #d1fae5; color: #065f46; }}
    .badge-down {{ background: #ffe4e6; color: #9f1239; }}
    .badge-critical {{ background: #fef3c7; color: #92400e; font-size: 10px; }}
    .badge-noncrit {{ background: #e0e7ff; color: #3730a3; font-size: 10px; }}
    .badge-operational {{ background: #d1fae5; color: #065f46; }}
    .badge-impl {{ background: #dbeafe; color: #1e40af; }}
    .badge-partial {{ background: #fef3c7; color: #92400e; }}
    .badge-to_build {{ background: #f3e8ff; color: #6b21a8; }}
    .badge-closed {{ background: #e5e7eb; color: #374151; }}
    .badge-deprecated {{ background: #fce7f3; color: #9d174d; }}
    .badge-minimal {{ background: #fef3c7; color: #92400e; }}
    .badge-unknown {{ background: #f3f4f6; color: #6b7280; }}
    .pill {{ display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; margin: 2px 4px 2px 0; }}
    .pill-danger {{ background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3; }}
    .pill-warn {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    .pill-ok {{ background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }}
    .code-block {{ background: #1d1d1f; color: #e8e8e8; padding: 12px; border-radius: 10px; font-size: 12px; overflow-x: auto; }}
    .links-bar {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0; }}
    .links-bar a {{ color: #1d1d1f; padding: 4px 10px; border: 1px solid #ddd; border-radius: 8px; text-decoration: none; font-size: 12px; }}
    .links-bar a:hover {{ background: #eee; }}
    .auto-refresh {{ color: #666; font-size: 12px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>
      LocalCMS
      <small>Central UI — opt-trading</small>
    </h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="#tmux-sessions">
        <span class="nav-icon">🖥️</span><span class="nav-label">TMUX Sessions</span>
      </a>
      <a class="nav-item" href="#health-status">
        <span class="nav-icon">❤️</span><span class="nav-label">Health Status</span>
      </a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Menu</div>
      {nav_items}
    </div>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666">
      <div><a href="/health" style="color:#888;text-decoration:none">/health</a></div>
      <div><a href="/menu" style="color:#888;text-decoration:none">/menu</a></div>
      <div><a href="/menu/state" style="color:#888;text-decoration:none">/menu/state</a></div>
      <div><a href="/runtime/tmux" style="color:#888;text-decoration:none">/runtime/tmux</a></div>
      <div><a href="/runtime/tmux/live" style="color:#888;text-decoration:none">/runtime/tmux/live</a></div>
    </div>
  </nav>

  <main class="main">
    <h2>Central UI</h2>
    <p class="subtitle">Cockpit de navigation système — lecture seule. 14 domaines, 9 sessions TMUX, état health.</p>

    <div class="summary-bar">
      <div class="summary-card {summary_class}">
        <div class="num">{tmux['total_up']}/{tmux['total_expected']}</div>
        <div class="label">TMUX Sessions UP</div>
      </div>
      <div class="summary-card">
        <div class="num">{total_critical - critical_count}/{total_critical}</div>
        <div class="label">Critical Sessions UP</div>
      </div>
      <div class="summary-card">
        <div class="num">{len(menu_data.get('menu', []))}</div>
        <div class="label">Menu Domains</div>
      </div>
    </div>

    <div class="links-bar">
      <a href="/scripts/tmux/health_check.py">health_check.py</a>
      <a href="/scripts/tmux/health_aggregator.sh">health_aggregator.sh</a>
      <a href="/scripts/tmux/start_all.sh">start_all.sh</a>
      <a href="/scripts/tmux/stop_all.sh">stop_all.sh</a>
      <a href="/scripts/tmux/restart_session.sh">restart_session.sh</a>
      <a href="/scripts/tmux/attach.sh">attach.sh</a>
      <a href="/scripts/ai/menu/opt_trading_menu.json">opt_trading_menu.json</a>
      <a href="/scripts/ai/menu/menu_state_aggregator.sh">menu_state_aggregator.sh</a>
      <a href="/logs">logs/</a>
      <a href="/desk/ui" target="_blank">Desk Pro →</a>
    </div>

    <div class="section-title" id="health-status">❤️ Health Status</div>
    <div style="display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap">
      <div><strong>Critical DOWN:</strong> {critical_down_html}</div>
      <div><strong>Non-critical DOWN:</strong> {non_critical_down_html}</div>
    </div>

    <div class="section-title" id="tmux-sessions">🖥️ TMUX Sessions</div>
    <table>
      <thead><tr><th>Session</th><th>Status</th><th>Type</th><th>Machine</th><th>Description</th></tr></thead>
      <tbody>{sessions_rows}</tbody>
    </table>

    <div class="section-title">📋 Global Menu — 14 Domaines</div>
    <div class="domain-grid">
      {domain_cards}
    </div>

    <div class="section-title">🔗 Liens Utiles</div>
    <table>
      <thead><tr><th>Ressource</th><th>Chemin</th></tr></thead>
      <tbody>
        <tr><td>Menu JSON</td><td><code>scripts/ai/menu/opt_trading_menu.json</code></td></tr>
        <tr><td>State Schema</td><td><code>scripts/ai/menu/state_schema.json</code></td></tr>
        <tr><td>State Cache</td><td><code>scripts/ai/menu/state_cache.json</code></td></tr>
        <tr><td>State Aggregator</td><td><code>scripts/ai/menu/menu_state_aggregator.sh</code></td></tr>
        <tr><td>Health Check</td><td><code>scripts/tmux/health_check.py</code></td></tr>
        <tr><td>Health Aggregator</td><td><code>scripts/tmux/health_aggregator.sh</code></td></tr>
        <tr><td>Start All</td><td><code>scripts/tmux/start_all.sh</code></td></tr>
        <tr><td>Stop All</td><td><code>scripts/tmux/stop_all.sh</code></td></tr>
        <tr><td>Restart Session</td><td><code>scripts/tmux/restart_session.sh</code></td></tr>
        <tr><td>Attach</td><td><code>scripts/tmux/attach.sh</code></td></tr>
      </tbody>
    </table>

    <div class="section-title">🛠️ API Endpoints</div>
    <table>
      <thead><tr><th>Endpoint</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td><a href="/health">/health</a></td><td>LocalCMS health check</td></tr>
        <tr><td><a href="/menu">/menu</a></td><td>Menu JSON (14 domaines, 85+ modules)</td></tr>
        <tr><td><a href="/menu/state">/menu/state</a></td><td>Module state cache (health polling)</td></tr>
        <tr><td><a href="/runtime/tmux">/runtime/tmux</a></td><td>TMUX sessions report (9 sessions, critical/non-critical)</td></tr>
        <tr><td><a href="/runtime/tmux/live">/runtime/tmux/live</a></td><td>Live TMUX session list</td></tr>
      </tbody>
    </table>

    <div class="auto-refresh" style="margin-top:24px">
      Page auto-refresh every 30s. Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
    </div>
    <div style="height:40px"></div>
  </main>
</div>
<script>
  setTimeout(() => location.reload(), 30000);
</script>
</body>
</html>"""
    return HTMLResponse(content=html)


STATUS_BADGES = {
    "operational": '<span class="badge badge-operational">● operational</span>',
    "impl": '<span class="badge badge-impl">○ impl</span>',
    "partial": '<span class="badge badge-partial">◌ partial</span>',
    "to_build": '<span class="badge badge-to_build">⊕ to_build</span>',
    "closed": '<span class="badge badge-closed">✕ closed</span>',
    "deprecated": '<span class="badge badge-deprecated">↓ deprecated</span>',
    "minimal": '<span class="badge badge-minimal">○ minimal</span>',
}
