from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
import json
import shlex
import socket
import subprocess
from datetime import date, datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MENU_FILE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "opt_trading_menu.json"
STATE_CACHE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "state_cache.json"
STATE_CACHE_GENERATOR = PROJECT_ROOT / "scripts" / "ai" / "menu" / "menu_state_aggregator.sh"
STATE_CACHE_MAX_AGE_S = 300
TMUX_LOG_DIR = PROJECT_ROOT / "logs"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SHARED_DESK_DIR = Path("/shared/desk_pro/latest")
LOCALCMS_LATEST_JSON = PROJECT_ROOT / "tmp" / "localcms_latest.json"
JOURNAL_DIR = PROJECT_ROOT / "data" / "journal" / "daily"
SYNC_LOG = PROJECT_ROOT / "data" / "journal" / "sync_log.jsonl"

CRITICAL_SESSIONS: frozenset[str] = frozenset({
    "admin-trading/tv-webhook.service",
    "admin-trading/tv-perf.service",
    "admin-trading/bot_vision_step2.service",
    "fantome/shared-sshfs.service",
    "fantome/localcms.service",
    "fantome/openclaw-gateway.service",
    "fantome/opt-trading-fleet-orchestrator.timer",
    "fantome/opt-trading-runtime-health.timer",
})

ALL_SESSIONS: list[dict] = [
    {"session": "admin-trading/tv-webhook.service", "unit": "tv-webhook.service", "critical": True, "machine": "admin-trading", "description": "TradingView webhook receiver on port 8000"},
    {"session": "admin-trading/tv-perf.service", "unit": "tv-perf.service", "critical": True, "machine": "admin-trading", "description": "Desk Pro/performance API on port 8010"},
    {"session": "admin-trading/bot_vision_step2.service", "unit": "bot_vision_step2.service", "critical": True, "machine": "admin-trading", "description": "Vision automation runtime"},
    {"session": "admin-trading/bot_vision_step2_prune.timer", "unit": "bot_vision_step2_prune.timer", "critical": False, "machine": "admin-trading", "description": "Vision cleanup timer"},
    {"session": "admin-trading/bot-vision-coinglass-capture.timer", "unit": "bot-vision-coinglass-capture.timer", "critical": False, "machine": "admin-trading", "description": "Coinglass capture timer"},
    {"session": "db-layer/shared-sshfs.service", "unit": "shared-sshfs.service", "critical": False, "machine": "db-layer", "description": "Original db-layer /shared mount; inactive while db-layer is off"},
    {"session": "db-layer/algo-hf-api.service", "unit": "algo-hf-api.service", "critical": False, "machine": "db-layer", "description": "Algo/Hugging Face API"},
    {"session": "db-layer/snap.ollama.listener.service", "unit": "snap.ollama.listener.service", "critical": False, "machine": "db-layer", "description": "Ollama snap listener"},
    {"session": "student/ollama.service", "unit": "ollama.service", "critical": False, "machine": "student", "description": "Student LLM runtime"},
    {"session": "student/opt-trading-localcms.service", "unit": "opt-trading-localcms.service", "critical": False, "machine": "student", "description": "Fallback LocalCMS dashboard on port 8700"},
    {"session": "fantome/shared-sshfs.service", "unit": "shared-sshfs.service", "critical": True, "machine": "fantome", "description": "Emergency read-only /shared route from admin-trading"},
    {"session": "fantome/localcms.service", "unit": "localcms.service", "critical": True, "machine": "fantome", "description": "Emergency primary LocalCMS dashboard on port 8700"},
    {"session": "fantome/openclaw-gateway.service", "unit": "openclaw-gateway.service", "critical": True, "machine": "fantome", "description": "OpenClaw gateway on loopback port 18789"},
    {"session": "fantome/opt-trading-fleet-orchestrator.timer", "unit": "opt-trading-fleet-orchestrator.timer", "critical": True, "machine": "fantome", "description": "Emergency fleet orchestration timer"},
    {"session": "fantome/opt-trading-runtime-health.timer", "unit": "opt-trading-runtime-health.timer", "critical": True, "machine": "fantome", "description": "Emergency runtime health timer"},
    {"session": "fantome/fail2ban.service", "unit": "fail2ban.service", "critical": False, "machine": "fantome", "description": "SSH protection only; no trading runtime expected"},
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


def _refresh_state_cache() -> str | None:
    if not STATE_CACHE_GENERATOR.exists():
        return f"Generator not found: {STATE_CACHE_GENERATOR.name}"
    try:
        r = subprocess.run(
            ["bash", str(STATE_CACHE_GENERATOR)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=PROJECT_ROOT,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        return str(e)

    if r.returncode == 0:
        return None

    detail = (r.stderr or r.stdout).strip()
    return detail or f"Generator exited with status {r.returncode}"


def _load_state_cache() -> dict | list:
    data = _read_json(STATE_CACHE)
    needs_refresh = isinstance(data, dict) and "error" in data

    try:
        if not needs_refresh and STATE_CACHE.exists():
            age_s = (datetime.now(timezone.utc).timestamp() - STATE_CACHE.stat().st_mtime)
            needs_refresh = age_s > STATE_CACHE_MAX_AGE_S
    except OSError:
        needs_refresh = True

    if not needs_refresh:
        return data

    refresh_error = _refresh_state_cache()
    if refresh_error is None:
        return _read_json(STATE_CACHE)

    if isinstance(data, dict):
        return {**data, "refresh_error": refresh_error}
    return {"error": f"File not found: {STATE_CACHE.name}", "refresh_error": refresh_error}


def _safe_child(base: Path, relative_path: str) -> Path | None:
    try:
        candidate = (base / relative_path).resolve()
        candidate.relative_to(base.resolve())
    except (OSError, ValueError):
        return None
    return candidate


def _readable_file_response(path: Path) -> FileResponse:
    media_type = "text/plain; charset=utf-8"
    if path.suffix == ".json":
        media_type = "application/json"
    elif path.suffix in {".html", ".htm"}:
        media_type = "text/html; charset=utf-8"
    return FileResponse(path, media_type=media_type, filename=path.name)


def _directory_listing_html(base: Path, current: Path, title: str, url_prefix: str) -> HTMLResponse:
    if not current.exists():
        return HTMLResponse(content=f"<h2>{title} not found</h2>", status_code=404)
    if not current.is_dir():
        return HTMLResponse(content=f"<h2>{title} is not a directory</h2>", status_code=400)

    rows = []
    for child in sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        rel = child.relative_to(base).as_posix()
        href = f"{url_prefix}/{rel}" if rel else url_prefix
        display = child.name + ("/" if child.is_dir() else "")
        kind = "dir" if child.is_dir() else "file"
        size = "-" if child.is_dir() else str(child.stat().st_size)
        rows.append(f"<tr><td><a href='{href}'>{display}</a></td><td>{kind}</td><td>{size}</td></tr>")

    parent_link = ""
    if current != base:
        parent_rel = current.parent.relative_to(base).as_posix()
        parent_href = url_prefix if parent_rel == "." else f"{url_prefix}/{parent_rel}"
        parent_link = f"<p><a href='{parent_href}'>..</a></p>"

    html = (
        f"<html><body><h2>{title}</h2>{parent_link}"
        "<table border='1' cellpadding='6' cellspacing='0'>"
        "<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead>"
        f"<tbody>{''.join(rows) or '<tr><td colspan=3>(empty)</td></tr>'}</tbody></table></body></html>"
    )
    return HTMLResponse(content=html)


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


def _current_hostnames() -> frozenset[str]:
    names = {socket.gethostname(), socket.getfqdn(), "localhost", "127.0.0.1"}
    try:
        r = subprocess.run(["hostname"], capture_output=True, text=True, timeout=2)
        if r.returncode == 0 and r.stdout.strip():
            names.add(r.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return frozenset(n for n in names if n)


def _systemctl_statuses(machine: str, units: list[str]) -> dict[str, tuple[bool, str]]:
    cmd = ["systemctl", "is-active", *units]
    if machine not in _current_hostnames():
        remote_cmd = shlex.join(cmd)
        cmd = [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=2",
            machine,
            remote_cmd,
        ]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return {unit: (False, "timeout") for unit in units}
    except (FileNotFoundError, OSError) as e:
        return {unit: (False, f"check_error:{e}") for unit in units}

    lines = [line.strip() for line in r.stdout.splitlines() if line.strip()]
    fallback = r.stderr.strip().splitlines()[0] if r.stderr.strip() else f"exit={r.returncode}"
    statuses: dict[str, tuple[bool, str]] = {}
    for index, unit in enumerate(units):
        value = lines[index] if index < len(lines) else fallback
        statuses[unit] = (value == "active", value)
    return statuses


def _build_tmux_report() -> dict:
    expected_ids = frozenset(s["session"] for s in ALL_SESSIONS)

    units_by_machine: dict[str, list[str]] = {}
    for s in ALL_SESSIONS:
        units_by_machine.setdefault(s["machine"], []).append(s["unit"])

    statuses_by_machine = {
        machine: _systemctl_statuses(machine, units)
        for machine, units in units_by_machine.items()
    }

    up: set[str] = set()
    sessions_detail = []
    for s in ALL_SESSIONS:
        sid = s["session"]
        running, status = statuses_by_machine[s["machine"]].get(s["unit"], (False, "missing"))
        if running:
            up.add(sid)
        sessions_detail.append({
            "session": sid,
            "running": running,
            "status": status,
            "critical": s["critical"],
            "machine": s["machine"],
            "description": s["description"],
        })

    missing = expected_ids - frozenset(up)
    critical_down = missing & CRITICAL_SESSIONS
    non_critical_down = missing - CRITICAL_SESSIONS

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
    data = _load_state_cache()
    return JSONResponse(content=data)


@app.get("/runtime/tmux")
def get_runtime_tmux():
    report = _build_tmux_report()
    return JSONResponse(content=report)


@app.get("/runtime/tmux/live")
def get_runtime_tmux_live():
    report = _build_tmux_report()
    return JSONResponse(content={
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "active_checks": sorted(s["session"] for s in report["sessions"] if s["running"]),
        "checks": report["sessions"],
    })


# ── Data Center endpoints ────────────────────────────────────────────

@app.get("/data-center/health")
def get_data_center_health():
    try:
        from modules.data_center.localcms_health_reader import read_data_center_health
    except ModuleNotFoundError as e:
        return JSONResponse(content={
            "ok": False,
            "consumer_id": "localcms__data_center_health",
            "source": "data_center_registry",
            "error": str(e),
            "warning": "modules.data_center is not deployed on this machine",
            "read_at": datetime.now(timezone.utc).isoformat(),
        }, status_code=503)

    return JSONResponse(content=read_data_center_health())


# ── Opening Session Dashboard (Phase 6) ─────────────────────────────────

@app.get("/data-center/opening-session")
def get_opening_session():
    """Opening Session dashboard — live SPCX opening metrics from DeskPro."""
    try:
        from modules.desk_pro.service.spcx_score_reader import read_spcx_score
    except ModuleNotFoundError as e:
        return JSONResponse(content={
            "ok": False,
            "error": str(e),
            "warning": "modules.desk_pro not deployed on this machine",
            "read_at": datetime.now(timezone.utc).isoformat(),
        }, status_code=503)

    result = read_spcx_score()
    om = result.get("opening_metrics") or {}
    oc = result.get("opening_components") or {}

    return JSONResponse(content={
        "ok": True,
        "consumer_id": "localcms__opening_session",
        "source": "desk_pro.spcx_score_reader",
        "read_at": datetime.now(timezone.utc).isoformat(),
        "symbol": "SPCX",
        "score": result.get("score", 0),
        "grade": result.get("grade", "C"),
        "setup_state": result.get("setup_state", "watch"),
        "opening_metrics": {
            "opening_gap_pct": om.get("opening_gap_pct"),
            "premarket_range": om.get("premarket_range"),
            "premarket_high": om.get("premarket_high"),
            "premarket_low": om.get("premarket_low"),
            "opening_drive": om.get("opening_drive"),
            "distance_vwap_pct": om.get("distance_vwap_pct"),
            "distance_premarket_high_pct": om.get("distance_premarket_high_pct"),
            "distance_orb_pct": om.get("distance_orb_pct"),
            "extension_pct": om.get("extension_pct"),
            "relative_volume_15m": om.get("relative_volume_15m"),
            "risk_score": om.get("risk_score"),
            "continuation_score": om.get("continuation_score"),
            "exhaustion_score": om.get("exhaustion_score"),
        },
        "opening_components": {
            "dynamic_boost": oc.get("dynamic_boost", 0),
            "details": oc.get("details", []),
        },
        "events": result.get("events", []),
        "risk_notes": result.get("risk_notes", []),
        "invalidation": result.get("invalidation", {}),
        "monitor_only": True,
    })


@app.get("/data-center/opening-session/html")
def get_opening_session_html():
    """HTML dashboard for Opening Session metrics."""
    try:
        from modules.desk_pro.service.spcx_score_reader import read_spcx_score
    except ModuleNotFoundError:
        return HTMLResponse(
            content="<h2>DeskPro not available</h2><p>modules.desk_pro not deployed here.</p>",
            status_code=503,
        )

    result = read_spcx_score()
    om = result.get("opening_metrics") or {}
    oc = result.get("opening_components") or {}
    score = result.get("score", 0)
    grade = result.get("grade", "C")
    state = result.get("setup_state", "watch")
    events = ", ".join(result.get("events", [])) or "none"
    risk_notes = ", ".join(result.get("risk_notes", [])) or "none"

    gap = f"{om.get('opening_gap_pct', 0):+.2f}%" if om.get("opening_gap_pct") is not None else "--"
    drive = om.get("opening_drive", "--")
    pmh = f"{om.get('premarket_high', 0):.2f}" if om.get("premarket_high") is not None else "--"
    pml = f"{om.get('premarket_low', 0):.2f}" if om.get("premarket_low") is not None else "--"
    dv = f"{om.get('distance_vwap_pct', 0):+.2f}%" if om.get("distance_vwap_pct") is not None else "--"
    dorb = f"{om.get('distance_orb_pct', 0):+.2f}%" if om.get("distance_orb_pct") is not None else "--"
    rvol = f"{om.get('relative_volume_15m', 0):.1f}x" if om.get("relative_volume_15m") is not None else "--"
    rs = om.get("risk_score", 0)
    cs = om.get("continuation_score", 0)
    es = om.get("exhaustion_score", 0)

    grade_color = "#2e7d32" if grade in ("A", "A+") else "#e65100" if grade == "B" else "#c62828"

    html = f"""<!doctype html>
<html lang="fr">
<head><meta charset="utf-8"><title>Opening Session — SPCX</title>
<style>
  body{{font-family:system-ui,sans-serif;margin:20px;max-width:900px;background:#fafafa}}
  h1{{margin:0 0 4px 0}} .muted{{color:#666;font-size:13px}}
  .card{{border:1px solid #ddd;border-radius:10px;padding:14px;margin:12px 0;background:#fff}}
  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th,td{{border-bottom:1px solid #eee;padding:6px;text-align:left}}
  .score{{font-size:36px;font-weight:700;color:{grade_color}}}
  .badge{{display:inline-block;padding:2px 10px;border-radius:999px;color:#fff;font-size:12px}}
  .badge-green{{background:#2e7d32}} .badge-orange{{background:#e65100}} .badge-red{{background:#c62828}} .badge-gray{{background:#888}}
  .metric-card{{text-align:center;border:1px solid #eee;border-radius:8px;padding:10px;background:#f9f9f9}}
  .metric-value{{font-size:22px;font-weight:700}} .metric-label{{font-size:11px;color:#888;margin-top:2px}}
</style></head>
<body>
  <h1>Opening Session — SPCX</h1>
  <div class="muted">Live depuis DeskPro | monitor_only</div>

  <div class="card" style="display:flex;align-items:center;gap:16px">
    <div class="score">{score}</div>
    <div><span class="badge badge-green">{grade}</span> <span class="badge {'badge-green' if state=='active' else 'badge-orange' if state=='watch' else 'badge-red'}">{state.upper()}</span></div>
    <div class="muted">Gap: {gap} | Drive: {drive}</div>
  </div>

  <div class="card">
    <h3 style="margin:0 0 8px 0">Premarket</h3>
    <table>
      <tr><td>High</td><td>{pmh}</td><td>Low</td><td>{pml}</td></tr>
      <tr><td>Dist VWAP</td><td>{dv}</td><td>Dist ORB</td><td>{dorb}</td></tr>
      <tr><td>RVOL 15m</td><td>{rvol}</td><td></td><td></td></tr>
    </table>
  </div>

  <div class="grid">
    <div class="metric-card"><div class="metric-value" style="color:{'#c62828' if rs>=60 else '#e65100' if rs>=30 else '#2e7d32'}">{rs}</div><div class="metric-label">Risque</div></div>
    <div class="metric-card"><div class="metric-value" style="color:{'#2e7d32' if cs>=60 else '#e65100' if cs>=30 else '#888'}">{cs}</div><div class="metric-label">Continuation</div></div>
    <div class="metric-card"><div class="metric-value" style="color:{'#c62828' if es>=60 else '#e65100' if es>=30 else '#888'}">{es}</div><div class="metric-label">Épuisement</div></div>
    <div class="metric-card"><div class="metric-value">{oc.get('dynamic_boost', 0):+d}</div><div class="metric-label">Dynamic Boost</div></div>
  </div>

  <div class="card">
    <h3 style="margin:0 0 8px 0">Événements</h3>
    <div class="muted">{events}</div>
    <h3 style="margin:8px 0">Alertes live</h3>
    <div class="muted">{risk_notes}</div>
  </div>

  <div class="card">
    <h3 style="margin:0 0 8px 0">Chronologie</h3>
    <div class="muted">Événements déclenchés dans l'ordre de poids :</div>
    <ul>{"".join(f"<li>{e}</li>" for e in result.get("events", [])) or "<li class='muted'>aucun événement</li>"}</ul>
  </div>

  <div class="card">
    <div style="display:flex;gap:8px;font-size:12px">
      <a href="/data-center/opening-session">JSON</a>
      <span class="muted">|</span>
      <a href="/desk/ui">DeskPro</a>
    </div>
  </div>
</body></html>"""
    return HTMLResponse(content=html)


@app.get("/scripts/{relative_path:path}")
def get_script_asset(relative_path: str):
    path = _safe_child(SCRIPTS_DIR, relative_path)
    if path is None or not path.exists():
        return HTMLResponse(content=f"<h2>Script not found: {relative_path}</h2>", status_code=404)
    if path.is_dir():
        return _directory_listing_html(SCRIPTS_DIR, path, f"Scripts: {relative_path}", "/scripts")
    return _readable_file_response(path)


@app.get("/logs")
def get_logs_root():
    return _directory_listing_html(TMUX_LOG_DIR, TMUX_LOG_DIR, "Logs", "/logs")


@app.get("/logs/{relative_path:path}")
def get_log_asset(relative_path: str):
    path = _safe_child(TMUX_LOG_DIR, relative_path)
    if path is None or not path.exists():
        return HTMLResponse(content=f"<h2>Log path not found: {relative_path}</h2>", status_code=404)
    if path.is_dir():
        return _directory_listing_html(TMUX_LOG_DIR, path, f"Logs: {relative_path}", "/logs")
    return _readable_file_response(path)


@app.get("/desk/ui")
def get_desk_shared_dashboard():
    dashboard = SHARED_DESK_DIR / "dashboard_latest.html"
    if not dashboard.exists():
        return HTMLResponse(content="<h2>Desk shared dashboard not found</h2>", status_code=404)
    return _readable_file_response(dashboard)


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


_PHASE1_THRESHOLD_RUNS = 30
_PHASE1_THRESHOLD_DAYS = 14


def _build_metrics() -> dict:
    all_entries = []
    if JOURNAL_DIR.exists():
        for f in sorted(JOURNAL_DIR.glob("*.json"), reverse=True):
            try:
                all_entries.append(json.loads(f.read_text()))
            except (json.JSONDecodeError, OSError):
                continue

    total = len(all_entries)
    pass_count = sum(1 for e in all_entries if e.get("all_ok"))
    fail_count = total - pass_count
    win_count = sum(1 for e in all_entries if e.get("pnl_paper", {}).get("outcome") == "win")
    loss_count = sum(1 for e in all_entries if e.get("pnl_paper", {}).get("outcome") == "loss")
    breakeven_count = sum(1 for e in all_entries if e.get("pnl_paper", {}).get("outcome") == "breakeven")
    pnl_values = [
        e["pnl_paper"]["net_pnl"]
        for e in all_entries
        if isinstance(e.get("pnl_paper", {}).get("net_pnl"), (int, float))
    ]
    pnl_cumulative = round(sum(pnl_values), 4)
    win_rate = round(win_count / total, 4) if total > 0 else 0.0

    # Phase 1 observation block
    observation_start: date | None = None
    run_ids = [e.get("run_id", "") for e in all_entries if e.get("run_id")]
    if run_ids:
        oldest = min(run_ids)
        try:
            observation_start = date(int(oldest[:4]), int(oldest[4:6]), int(oldest[6:8]))
        except (ValueError, IndexError):
            observation_start = None
    days_elapsed = (date.today() - observation_start).days if observation_start else 0
    closeout_required_count = sum(1 for e in all_entries if e.get("closeout_required", False))
    observation = {
        "observation_start": observation_start.isoformat() if observation_start else None,
        "days_elapsed": days_elapsed,
        "runs_to_threshold": max(0, _PHASE1_THRESHOLD_RUNS - total),
        "days_to_threshold": max(0, _PHASE1_THRESHOLD_DAYS - days_elapsed),
        "eligible": total >= _PHASE1_THRESHOLD_RUNS and fail_count == 0 and days_elapsed >= _PHASE1_THRESHOLD_DAYS,
        "closeout_required_count": closeout_required_count,
        "threshold_runs": _PHASE1_THRESHOLD_RUNS,
        "threshold_days": _PHASE1_THRESHOLD_DAYS,
    }

    last_run = None
    if all_entries:
        e = all_entries[0]
        last_run = {
            "run_id": e.get("run_id", ""),
            "session_id": e.get("session_id", ""),
            "started_at": (e.get("started_at", "") or "")[:19],
            "all_ok": e.get("all_ok", False),
            "outcome": e.get("pnl_paper", {}).get("outcome", ""),
            "net_pnl": e.get("pnl_paper", {}).get("net_pnl", 0),
            "validation_verdict": e.get("validation_verdict", ""),
            "signal": f"{e.get('signal_source', {}).get('signal', '')} {e.get('signal_source', {}).get('symbol', '')}".strip(),
            "localcms_ok": e.get("localcms_ok"),
            "closeout_required": e.get("closeout_required", False),
        }

    sync_dry = sync_written = sync_blocked = sync_failed = 0
    if SYNC_LOG.exists():
        try:
            with open(SYNC_LOG) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        s = json.loads(line).get("status", "")
                        if s == "dry_run_skipped":
                            sync_dry += 1
                        elif s == "synced":
                            sync_written += 1
                        elif "BLOCKED" in s:
                            sync_blocked += 1
                        else:
                            sync_failed += 1
                    except json.JSONDecodeError:
                        continue
        except OSError:
            pass

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_runs": total,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "win_count": win_count,
        "loss_count": loss_count,
        "breakeven_count": breakeven_count,
        "pnl_cumulative": pnl_cumulative,
        "win_rate": win_rate,
        "observation": observation,
        "last_run": last_run,
        "sheets_sync": {
            "dry_run": sync_dry,
            "written": sync_written,
            "blocked": sync_blocked,
            "failed": sync_failed,
        },
    }


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


@app.get("/metrics/daily")
def get_metrics_daily():
    return JSONResponse(content=_build_metrics())


def _metrics_html(m: dict, tmux: dict) -> str:
    last = m.get("last_run") or {}
    ss = m.get("sheets_sync", {})
    win_rate_pct = f"{m['win_rate'] * 100:.1f}%"
    pnl_sign = "+" if m["pnl_cumulative"] >= 0 else ""
    pnl_color = "#30d158" if m["pnl_cumulative"] >= 0 else "#ff453a"

    last_outcome = last.get("outcome", "")
    last_verdict = last.get("validation_verdict", "")
    last_pnl = last.get("net_pnl", 0)
    last_pnl_str = f"{'+' if last_pnl >= 0 else ''}{last_pnl:.2f}" if isinstance(last_pnl, (int, float)) else str(last_pnl)

    tmux_up = tmux.get("total_up", 0)
    tmux_total = tmux.get("total_expected", 0)
    tmux_ok = tmux_up == tmux_total
    tmux_color = "#30d158" if tmux_ok else "#ff9f0a"

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Metrics</title>
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
    .card-row {{ display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }}
    .card {{ flex: 1; min-width: 130px; padding: 16px; border-radius: 12px; border: 1px solid #e6e6e6; background: #fff; }}
    .card .num {{ font-size: 28px; font-weight: 700; }}
    .card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    .card-pass {{ border-left: 4px solid #30d158; }}
    .card-fail {{ border-left: 4px solid #ff453a; }}
    .card-blue {{ border-left: 4px solid #007aff; }}
    .card-win {{ border-left: 4px solid #30d158; }}
    .card-loss {{ border-left: 4px solid #ff453a; }}
    .card-neutral {{ border-left: 4px solid #8e8e93; }}
    .section-title {{ font-size: 16px; font-weight: 600; margin: 24px 0 12px; }}
    .info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .info-card {{ background: #fff; border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px 16px; }}
    .info-card h4 {{ font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }}
    .info-card .value {{ font-size: 14px; font-weight: 600; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
    .badge-up {{ background: #d1fae5; color: #065f46; }}
    .badge-down {{ background: #ffe4e6; color: #9f1239; }}
    .badge-unknown {{ background: #f3f4f6; color: #6b7280; }}
    .badge-minimal {{ background: #fef3c7; color: #92400e; }}
    a {{ color: #007aff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">Runtime Checks</span></a>
      <a class="nav-item" href="/#health-status"><span class="nav-icon">❤️</span><span class="nav-label">Health Status</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Journal</div>
      <a class="nav-item" href="/journal"><span class="nav-icon">📋</span><span class="nav-label">Daily Sessions</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Metrics</div>
      <a class="nav-item" href="/metrics" style="color:#fff;background:#333"><span class="nav-icon">📊</span><span class="nav-label">Dashboard</span></a>
    </div>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666">
      <div><a href="/ui" style="color:#888;text-decoration:none">Main Dashboard</a></div>
      <div><a href="/metrics/daily" style="color:#888;text-decoration:none">/metrics/daily</a></div>
      <div><a href="/journal/daily" style="color:#888;text-decoration:none">/journal/daily</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>📊 Metrics Dashboard</h2>
    <p class="subtitle">Agrégats daily session — lecture seule. Généré à {m['generated_at'][:19]} UTC.</p>

    <div class="section-title">Runs</div>
    <div class="card-row">
      <div class="card card-blue">
        <div class="num">{m['total_runs']}</div>
        <div class="label">Total runs</div>
      </div>
      <div class="card card-pass">
        <div class="num">{m['pass_count']}</div>
        <div class="label">PASS (all_ok)</div>
      </div>
      <div class="card card-fail">
        <div class="num">{m['fail_count']}</div>
        <div class="label">FAIL</div>
      </div>
    </div>

    <div class="section-title">P&L Paper</div>
    <div class="card-row">
      <div class="card" style="border-left:4px solid {pnl_color}">
        <div class="num" style="color:{pnl_color}">{pnl_sign}{m['pnl_cumulative']:.2f}</div>
        <div class="label">P&L cumulé (paper)</div>
      </div>
      <div class="card card-win">
        <div class="num">{m['win_count']}</div>
        <div class="label">Wins</div>
      </div>
      <div class="card card-loss">
        <div class="num">{m['loss_count']}</div>
        <div class="label">Losses</div>
      </div>
      <div class="card card-neutral">
        <div class="num">{m['breakeven_count']}</div>
        <div class="label">Breakeven</div>
      </div>
      <div class="card card-blue">
        <div class="num">{win_rate_pct}</div>
        <div class="label">Win rate</div>
      </div>
    </div>

    <div class="section-title">Dernière session</div>
    <div class="info-grid">
      <div class="info-card">
        <h4>Run ID</h4>
        <div class="value" style="font-family:monospace">{last.get('run_id', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Date</h4>
        <div class="value">{last.get('started_at', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Signal</h4>
        <div class="value">{last.get('signal', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Verdict</h4>
        <div class="value">{_verdict_badge(last_verdict)}</div>
      </div>
      <div class="info-card">
        <h4>Outcome</h4>
        <div class="value">{_pnl_badge(last_outcome)} {last_pnl_str}</div>
      </div>
      <div class="info-card">
        <h4>All OK</h4>
        <div class="value">{'PASS' if last.get('all_ok') else 'FAIL'}</div>
      </div>
    </div>

    <div class="section-title">État runtime</div>
    <div class="info-grid">
      <div class="info-card">
        <h4>Runtime checks</h4>
        <div class="value" style="color:{tmux_color}">{tmux_up}/{tmux_total} UP</div>
      </div>
      <div class="info-card">
        <h4>Critical checks DOWN</h4>
        <div class="value">{'none' if not tmux.get('critical_down') else ', '.join(tmux['critical_down'])}</div>
      </div>
    </div>

    <div class="section-title">Google Sheets sync</div>
    <div class="card-row">
      <div class="card card-neutral">
        <div class="num">{ss.get('dry_run', 0)}</div>
        <div class="label">Dry-run</div>
      </div>
      <div class="card card-pass">
        <div class="num">{ss.get('written', 0)}</div>
        <div class="label">Written (controlled)</div>
      </div>
      <div class="card card-fail">
        <div class="num">{ss.get('blocked', 0)}</div>
        <div class="label">Blocked</div>
      </div>
      <div class="card card-fail">
        <div class="num">{ss.get('failed', 0)}</div>
        <div class="label">Failed</div>
      </div>
    </div>

    <div style="margin-top:24px">
      <a href="/metrics/daily">📄 JSON API → /metrics/daily</a>
      &nbsp;·&nbsp;
      <a href="/journal">📋 Journal → /journal</a>
    </div>
  </main>
</div>
</body>
</html>"""


@app.get("/metrics", response_class=HTMLResponse)
def metrics_html():
    m = _build_metrics()
    tmux = _build_tmux_report()
    return HTMLResponse(content=_metrics_html(m, tmux))


# ── Journal HTML views ───────────────────────────────────────────────

_JOURNAL_SIDEBAR_LINKS = """
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Journal</div>
      <a class="nav-item" href="/journal">
        <span class="nav-icon">📋</span><span class="nav-label">Daily Sessions</span>
      </a>
    </div>
"""


def _pnl_badge(outcome: str) -> str:
    if outcome == "win":
        return '<span class="badge badge-up">WIN</span>'
    if outcome == "loss":
        return '<span class="badge badge-down">LOSS</span>'
    if outcome == "breakeven":
        return '<span class="badge badge-minimal">BREAKEVEN</span>'
    return f'<span class="badge badge-unknown">{outcome}</span>'


def _verdict_badge(verdict: str) -> str:
    if verdict == "APPROVED":
        return '<span class="badge badge-up">APPROVED</span>'
    if verdict == "REJECTED":
        return '<span class="badge badge-down">REJECTED</span>'
    return f'<span class="badge badge-unknown">{verdict}</span>'


def _closeout_badge(ack: bool) -> str:
    if ack:
        return '<span class="badge badge-up">✓ CLOSED</span>'
    return '<span class="badge badge-down">⚠ PENDING</span>'


def _journal_html(entries: list[dict]) -> str:
    rows = ""
    for e in entries:
        pnl = e.get("pnl_outcome", "")
        verdict = e.get("validation_verdict", "")
        closeout = e.get("closeout_acknowledged", False)
        started = e.get("started_at", "")[:19] if e.get("started_at") else ""
        rows += f"""\
<tr>
  <td><a href="/journal/{e['run_id']}" style="font-family:monospace;font-weight:600">{e['run_id']}</a></td>
  <td>{started}</td>
  <td>{e.get('duration_s', 0):.1f}s</td>
  <td>{_verdict_badge(verdict)}</td>
  <td>{_pnl_badge(pnl)}</td>
  <td>{e.get('signal', '')} {e.get('symbol', '')}</td>
  <td>{_closeout_badge(closeout)}</td>
</tr>"""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Journal</title>
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
    .summary-card {{ flex: 1; min-width: 140px; padding: 16px; border-radius: 12px; border: 1px solid #e6e6e6; background: #fff; }}
    .summary-card .num {{ font-size: 28px; font-weight: 700; }}
    .summary-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    .summary-ok {{ border-left: 4px solid #30d158; }}
    .summary-warn {{ border-left: 4px solid #ff9f0a; }}
    .summary-critical {{ border-left: 4px solid #ff453a; }}
    .summary-blue {{ border-left: 4px solid #007aff; }}
    .section-title {{ font-size: 16px; font-weight: 600; margin: 24px 0 12px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e6e6e6; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; font-size: 13px; }}
    th {{ background: #fafafa; font-weight: 600; color: #666; text-transform: uppercase; font-size: 11px; letter-spacing: .5px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
    .badge-up {{ background: #d1fae5; color: #065f46; }}
    .badge-down {{ background: #ffe4e6; color: #9f1239; }}
    .badge-unknown {{ background: #f3f4f6; color: #6b7280; }}
    .badge-minimal {{ background: #fef3c7; color: #92400e; }}
    .links-bar {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0; }}
    .links-bar a {{ color: #1d1d1f; padding: 4px 10px; border: 1px solid #ddd; border-radius: 8px; text-decoration: none; font-size: 12px; }}
    .links-bar a:hover {{ background: #eee; }}
    .code-block {{ background: #1d1d1f; color: #e8e8e8; padding: 12px; border-radius: 10px; font-size: 12px; overflow-x: auto; }}
    tr:hover {{ background: #f9f9fb; }}
    a {{ color: #007aff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">Runtime Checks</span></a>
      <a class="nav-item" href="/#health-status"><span class="nav-icon">❤️</span><span class="nav-label">Health Status</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Journal</div>
      <a class="nav-item" href="/journal"><span class="nav-icon">📋</span><span class="nav-label">Daily Sessions</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Metrics</div>
      <a class="nav-item" href="/metrics"><span class="nav-icon">📊</span><span class="nav-label">Dashboard</span></a>
    </div>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666">
      <div><a href="/ui" style="color:#888;text-decoration:none">Main Dashboard</a></div>
      <div><a href="/health" style="color:#888;text-decoration:none">/health</a></div>
      <div><a href="/journal/daily" style="color:#888;text-decoration:none">/journal/daily</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>📋 Daily Session Journal</h2>
    <p class="subtitle">E2E dry-run pipeline — historique des sessions quotidiennes traçables.</p>

    <div class="summary-bar">
      <div class="summary-card summary-blue">
        <div class="num">{len(entries)}</div>
        <div class="label">Total Sessions</div>
      </div>
      <div class="summary-card summary-ok">
        <div class="num">{sum(1 for e in entries if e.get('pnl_outcome') == 'win')}</div>
        <div class="label">Wins</div>
      </div>
      <div class="summary-card summary-critical">
        <div class="num">{sum(1 for e in entries if e.get('pnl_outcome') == 'loss')}</div>
        <div class="label">Losses</div>
      </div>
      <div class="summary-card">
        <div class="num">{sum(1 for e in entries if e.get('closeout_acknowledged'))}</div>
        <div class="label">Closeouts</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Run ID</th><th>Started</th><th>Duration</th><th>Verdict</th>
          <th>P&L</th><th>Signal</th><th>Closeout</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>

    <div style="margin-top:24px">
      <a href="/journal/daily">📄 JSON API → /journal/daily</a>
    </div>
  </main>
</div>
</body>
</html>"""


def _journal_detail_html(entry: dict) -> str:
    pnl = entry.get("pnl_paper", {})
    signal = entry.get("signal_source", {})
    proposition = entry.get("proposition_summary", {})
    tmux_before = entry.get("tmux_before", {})
    tmux_after = entry.get("tmux_after", {})
    lcms_before = entry.get("localcms_before", {})
    lcms_after = entry.get("localcms_after", {})
    steps = entry.get("steps", [])

    tmux_before_count = tmux_before.get("count", "?")
    tmux_after_count = tmux_after.get("count", "?")
    tmux_before_active = ", ".join(tmux_before.get("active", []))
    tmux_after_active = ", ".join(tmux_after.get("active", []))

    lcms_before_ok = sum(1 for v in lcms_before.values() if isinstance(v, dict) and v.get("ok"))
    lcms_before_total = len(lcms_before)
    lcms_after_ok = sum(1 for v in lcms_after.values() if isinstance(v, dict) and v.get("ok"))
    lcms_after_total = len(lcms_after)

    steps_html = ""
    for s in steps:
        step_name = s.get("step", "?")
        result = s.get("result", {})
        result_str = json.dumps(result, indent=2, default=str)[:600]
        steps_html += f"""
<tr>
  <td style="font-family:monospace;font-weight:600">{step_name}</td>
  <td><pre style="background:#1d1d1f;color:#e8e8e8;padding:8px;border-radius:6px;font-size:11px;overflow-x:auto;margin:0;max-height:200px">{result_str}</pre></td>
</tr>"""

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Journal {entry.get('run_id', '')}</title>
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
    .section-title {{ font-size: 16px; font-weight: 600; margin: 24px 0 12px; }}
    .info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .info-card {{ background: #fff; border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px 16px; }}
    .info-card h4 {{ font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 6px; }}
    .info-card .value {{ font-size: 14px; font-weight: 600; }}
    .info-card .value-mono {{ font-family: monospace; font-size: 13px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; border: 1px solid #e6e6e6; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; font-size: 13px; }}
    th {{ background: #fafafa; font-weight: 600; color: #666; text-transform: uppercase; font-size: 11px; letter-spacing: .5px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
    .badge-up {{ background: #d1fae5; color: #065f46; }}
    .badge-down {{ background: #ffe4e6; color: #9f1239; }}
    .badge-unknown {{ background: #f3f4f6; color: #6b7280; }}
    .badge-minimal {{ background: #fef3c7; color: #92400e; }}
    .pill {{ display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; margin: 2px 4px 2px 0; }}
    .pill-ok {{ background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }}
    .pill-warn {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    a {{ color: #007aff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">Runtime Checks</span></a>
      <a class="nav-item" href="/#health-status"><span class="nav-icon">❤️</span><span class="nav-label">Health Status</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Journal</div>
      <a class="nav-item" href="/journal"><span class="nav-icon">📋</span><span class="nav-label">Daily Sessions</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Metrics</div>
      <a class="nav-item" href="/metrics"><span class="nav-icon">📊</span><span class="nav-label">Dashboard</span></a>
    </div>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666">
      <div><a href="/journal" style="color:#888;text-decoration:none">← Back to Journal</a></div>
      <div><a href="/journal/daily/{entry.get('run_id', '')}" style="color:#888;text-decoration:none">JSON detail</a></div>
    </div>
  </nav>
  <main class="main">
    <div style="margin-bottom:8px">
      <a href="/journal" style="font-size:13px">← Back to Journal</a>
    </div>
    <h2>📋 {entry.get('run_id', 'N/A')}</h2>
    <p class="subtitle">Daily Session — {entry.get('started_at', '')[:19] if entry.get('started_at') else ''}</p>

    <div class="info-grid">
      <div class="info-card">
        <h4>Signal</h4>
        <div class="value">{signal.get('signal', 'N/A')} {signal.get('symbol', '')}</div>
      </div>
      <div class="info-card">
        <h4>Proposition</h4>
        <div class="value">{proposition.get('action', 'N/A')} (confidence: {proposition.get('confidence', 'N/A')})</div>
      </div>
      <div class="info-card">
        <h4>Validation</h4>
        <div class="value">{_verdict_badge(entry.get('validation_verdict', ''))}</div>
      </div>
      <div class="info-card">
        <h4>Execution</h4>
        <div class="value">{entry.get('trade_executor_status', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>P&L Paper</h4>
        <div class="value">{_pnl_badge(pnl.get('outcome', ''))} net={pnl.get('net_pnl', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Datasheet</h4>
        <div class="value">dry_run={pnl.get('dry_run', entry.get('dry_run', '?'))} written={entry.get('datasheet_writer', {}).get('written', '?')}</div>
      </div>
      <div class="info-card">
        <h4>Learning</h4>
        <div class="value">bridge={entry.get('learning_feeder', {}).get('bridge_status', '?')} brick={entry.get('learning_feeder', {}).get('brick_stored', '?')}</div>
      </div>
      <div class="info-card">
        <h4>Closeout</h4>
        <div class="value">{_closeout_badge(entry.get('closeout_acknowledged', False))}</div>
      </div>
    </div>

    <div class="section-title">📊 Pipeline Steps</div>
    <table>
      <thead><tr><th>Step</th><th>Result</th></tr></thead>
      <tbody>{steps_html}</tbody>
    </table>

    <div class="section-title">🖥️ TMUX Snapshots</div>
    <div class="info-grid">
      <div class="info-card">
        <h4>Before</h4>
        <div class="value">{tmux_before_count} sessions</div>
        <div style="font-size:11px;color:#666;margin-top:4px;word-break:break-all">{tmux_before_active}</div>
      </div>
      <div class="info-card">
        <h4>After</h4>
        <div class="value">{tmux_after_count} sessions</div>
        <div style="font-size:11px;color:#666;margin-top:4px;word-break:break-all">{tmux_after_active}</div>
      </div>
    </div>

    <div class="section-title">❤️ LocalCMS Snapshots</div>
    <div class="info-grid">
      <div class="info-card">
        <h4>Before</h4>
        <div class="value">{lcms_before_ok}/{lcms_before_total} endpoints OK</div>
      </div>
      <div class="info-card">
        <h4>After</h4>
        <div class="value">{lcms_after_ok}/{lcms_after_total} endpoints OK</div>
      </div>
    </div>

    <div class="section-title">ℹ️ Metadata</div>
    <div class="info-grid">
      <div class="info-card">
        <h4>Run ID</h4>
        <div class="value-mono">{entry.get('run_id', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Session ID</h4>
        <div class="value-mono" style="font-size:11px">{entry.get('session_id', 'N/A')}</div>
      </div>
      <div class="info-card">
        <h4>Duration</h4>
        <div class="value">{entry.get('duration_s', 0):.1f}s (pipeline: {entry.get('pipeline_duration_s', 0):.1f}s)</div>
      </div>
      <div class="info-card">
        <h4>Journal Type</h4>
        <div class="value">{entry.get('journal_type', 'N/A')}</div>
      </div>
    </div>
  </main>
</div>
</body>
</html>"""


@app.get("/journal", response_class=HTMLResponse)
def journal_html():
    entries = _list_journal_entries()
    return HTMLResponse(content=_journal_html(entries))


@app.get("/journal/{run_id}", response_class=HTMLResponse)
def journal_detail_html(run_id: str):
    path = JOURNAL_DIR / f"{run_id}.json"
    if not path.exists():
        return HTMLResponse(content=f"<h2>Journal entry not found: {run_id}</h2><a href='/journal'>← Back</a>", status_code=404)
    try:
        data = json.loads(path.read_text())
        return HTMLResponse(content=_journal_detail_html(data))
    except (json.JSONDecodeError, OSError) as e:
        return HTMLResponse(content=f"<h2>Error reading journal: {e}</h2><a href='/journal'>← Back</a>", status_code=500)


# ── HTML UI ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
def ui_index(request: Request):
    tmux = _build_tmux_report()
    menu_data = _read_json(MENU_FILE)
    state_data = _load_state_cache()

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
        <span class="nav-icon">🖥️</span><span class="nav-label">Runtime Checks</span>
      </a>
      <a class="nav-item" href="#health-status">
        <span class="nav-icon">❤️</span><span class="nav-label">Health Status</span>
      </a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Journal</div>
      <a class="nav-item" href="/journal">
        <span class="nav-icon">📋</span><span class="nav-label">Daily Sessions</span>
      </a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Metrics</div>
      <a class="nav-item" href="/metrics"><span class="nav-icon">📊</span><span class="nav-label">Dashboard</span></a>
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
      <div><a href="/journal" style="color:#888;text-decoration:none">/journal</a></div>
      <div><a href="/journal/daily" style="color:#888;text-decoration:none">/journal/daily</a></div>
      <div><a href="/metrics" style="color:#888;text-decoration:none">/metrics</a></div>
    </div>
  </nav>

  <main class="main">
    <h2>Central UI</h2>
    <p class="subtitle">Cockpit de navigation système — lecture seule. 14 domaines, checks runtime systemd, état health.</p>

    <div class="summary-bar">
      <div class="summary-card {summary_class}">
        <div class="num">{tmux['total_up']}/{tmux['total_expected']}</div>
        <div class="label">Runtime Checks UP</div>
      </div>
      <div class="summary-card">
        <div class="num">{total_critical - critical_count}/{total_critical}</div>
        <div class="label">Critical Checks UP</div>
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

    <div class="section-title" id="tmux-sessions">🖥️ Runtime Checks</div>
    <table>
      <thead><tr><th>Check</th><th>Status</th><th>Type</th><th>Machine</th><th>Description</th></tr></thead>
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
        <tr><td><a href="/runtime/tmux">/runtime/tmux</a></td><td>Runtime systemd checks report (critical/non-critical)</td></tr>
        <tr><td><a href="/runtime/tmux/live">/runtime/tmux/live</a></td><td>Live runtime checks list</td></tr>
        <tr><td><a href="/metrics">/metrics</a></td><td>Dashboard métriques agrégées (HTML)</td></tr>
        <tr><td><a href="/metrics/daily">/metrics/daily</a></td><td>Métriques daily session (JSON)</td></tr>
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
