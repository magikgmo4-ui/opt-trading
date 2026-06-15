from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone

from shared.html_helpers import pnl_badge, verdict_badge, closeout_badge, cred_status_badge, badge, STATUS_BADGES as SHARED_STATUS_BADGES
from shared.html_design_system import STANDARD_CSS, SIGNALS_DARK_CSS

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MENU_FILE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "opt_trading_menu.json"
STATE_CACHE = PROJECT_ROOT / "scripts" / "ai" / "menu" / "state_cache.json"
TMUX_LOG_DIR = PROJECT_ROOT / "logs"
LOCALCMS_LATEST_JSON = PROJECT_ROOT / "tmp" / "localcms_latest.json"
JOURNAL_DIR = PROJECT_ROOT / "data" / "journal" / "daily"
SYNC_LOG = PROJECT_ROOT / "data" / "journal" / "sync_log.jsonl"

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

# PWA static assets
_STATIC_DIR = PROJECT_ROOT / "modules" / "localcms" / "static"
_STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


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


# ── Credentials panel ────────────────────────────────────────────────

_DOTENV_FILE = PROJECT_ROOT / ".env"
_ROLES_DIR = Path("/etc/opt-trading/env.d/roles")
_OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
_SSHFS_ENV = Path("/etc/opt-trading/shared_sshfs_permanent.env")

_CREDS: list[dict] = [
    # Telegram
    {"id": "telegram_api_id",          "provider": "Telegram",    "env_var": "TELEGRAM_API_ID",                  "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_api_hash",        "provider": "Telegram",    "env_var": "TELEGRAM_API_HASH",                "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_bot_token_main",  "provider": "Telegram",    "env_var": "TELEGRAM_BOT_TOKEN",               "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_session_path",    "provider": "Telegram",    "env_var": "TELEGRAM_SESSION_PATH",            "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_alert_chat_id",   "provider": "Telegram",    "env_var": "TELEGRAM_ALERT_CHAT_ID",           "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_channels_config", "provider": "Telegram",    "env_var": "TELEGRAM_CHANNELS_CONFIG",         "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "telegram_chat_id_alerts",  "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_ALERTS",          "storage": "role",     "file": str(_ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_pipeline","provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_PIPELINE",        "storage": "role",     "file": str(_ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_push",    "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_PUSH",            "storage": "role",     "file": str(_ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_ops",     "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_OPS",             "storage": "role",     "file": str(_ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    # TradingView / Internal
    {"id": "tv_webhook_key",           "provider": "TradingView", "env_var": "TV_WEBHOOK_KEY",                   "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "tv_webhook_secret",        "provider": "TradingView", "env_var": "TV_WEBHOOK_SECRET",                "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "ops_admin_key",            "provider": "Internal",    "env_var": "OPS_ADMIN_KEY",                    "storage": "env",      "file": str(_DOTENV_FILE)},
    # Google — auth via ADC (gcloud auth application-default login), no service account JSON
    {"id": "google_sheets_sync_id",    "provider": "Google",      "env_var": "GOOGLE_SHEETS_SYNC_SHEET_ID",      "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "gemini_api_key",           "provider": "Google",      "env_var": "GEMINI_API_KEY",                   "storage": "env",      "file": str(_DOTENV_FILE)},
    # GitHub
    {"id": "gh_token",                 "provider": "GitHub",      "env_var": "GH_TOKEN",                         "storage": "env",      "file": str(_DOTENV_FILE)},
    # Binance
    {"id": "binance_api_key",          "provider": "Binance",     "env_var": "BINANCE_API_KEY",                  "storage": "env",      "file": str(_DOTENV_FILE)},
    # Coinglass
    {"id": "coinglass_api_key",        "provider": "Coinglass",   "env_var": "COINGLASS_API_KEY",                "storage": "env",      "file": str(_DOTENV_FILE)},
    # LLM local
    {"id": "ollama_base_url",          "provider": "Ollama",      "env_var": "OLLAMA_BASE_URL",                  "storage": "env",      "file": str(_DOTENV_FILE)},
    # LLM cloud (via openclaw)
    {"id": "openai_api_key",           "provider": "OpenAI",      "env_var": "OPENAI_API_KEY",                   "storage": "openclaw", "file": str(_OPENCLAW_JSON)},
    {"id": "anthropic_api_key",        "provider": "Anthropic",   "env_var": "ANTHROPIC_API_KEY",                "storage": "openclaw", "file": str(_OPENCLAW_JSON)},
    # Database
    {"id": "db_host",                  "provider": "Database",    "env_var": "DB_HOST",                          "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "db_user",                  "provider": "Database",    "env_var": "DB_USER",                          "storage": "env",      "file": str(_DOTENV_FILE)},
    {"id": "db_password",              "provider": "Database",    "env_var": "DB_PASSWORD",                      "storage": "env",      "file": str(_DOTENV_FILE)},
    # Airtable
    {"id": "airtable_api_key",         "provider": "Airtable",    "env_var": "AIRTABLE_API_KEY",                 "storage": "role",     "file": str(_ROLES_DIR / "airtable_user.env"),        "role": "airtable_user"},
    {"id": "airtable_base_id",         "provider": "Airtable",    "env_var": "AIRTABLE_BASE_ID",                 "storage": "role",     "file": str(_ROLES_DIR / "airtable_user.env"),        "role": "airtable_user"},
    # DeskPro
    {"id": "deskpro_api_key",          "provider": "DeskPro",     "env_var": "DESKPRO_API_KEY",                  "storage": "role",     "file": str(_ROLES_DIR / "deskpro_user.env"),         "role": "deskpro_user"},
    {"id": "deskpro_api_url",          "provider": "DeskPro",     "env_var": "DESKPRO_API_URL",                  "storage": "role",     "file": str(_ROLES_DIR / "deskpro_user.env"),         "role": "deskpro_user"},
    # ClickUp
    {"id": "clickup_token",            "provider": "ClickUp",     "env_var": "CLICKUP_TOKEN",                    "storage": "role",     "file": str(_ROLES_DIR / "clickup_user.env"),         "role": "clickup_user"},
    # Figma (future)
    {"id": "figma_token",              "provider": "Figma",       "env_var": "FIGMA_TOKEN",                      "storage": "role",     "file": str(_ROLES_DIR / "figma_designer.env"),      "role": "figma_designer", "cred_status": "future"},
    {"id": "figma_file_key",           "provider": "Figma",       "env_var": "FIGMA_FILE_KEY",                   "storage": "role",     "file": str(_ROLES_DIR / "figma_designer.env"),      "role": "figma_designer", "cred_status": "future"},
    # Infrastructure
    {"id": "sshfs_identity_file",      "provider": "Internal",    "env_var": "IDENTITY_FILE",                    "storage": "env",      "file": str(_SSHFS_ENV)},
    {"id": "wireguard_private_key",    "provider": "Internal",    "env_var": None,                               "storage": "system",   "file": "/etc/wireguard/wg0.conf"},
    {"id": "termux_ssh_key",           "provider": "Internal",    "env_var": None,                               "storage": "system",   "file": str(Path.home() / ".ssh" / "id_ed25519_termux")},
]


def _cred_check_env(file_path: str, env_var: str) -> str:
    try:
        p = Path(file_path)
        if not p.exists():
            return "ABSENT"
        for line in p.read_text().splitlines():
            if re.match(rf"^{re.escape(env_var)}=.+", line.strip()):
                return "SET"
        return "ABSENT"
    except (OSError, PermissionError):
        return "UNKNOWN"


def _cred_check_role(file_path: str, env_var: str) -> str:
    try:
        r = subprocess.run(
            ["sudo", "-n", "grep", "-c", f"^{env_var}=.", file_path],
            capture_output=True, text=True, timeout=3,
        )
        if r.returncode == 0 and r.stdout.strip() not in ("", "0"):
            return "SET"
        return "ABSENT"
    except Exception:
        return "UNKNOWN"


def _cred_check_system(file_path: str) -> str:
    try:
        p = Path(file_path)
        if p.exists():
            return "SET"
    except (OSError, PermissionError):
        pass
    try:
        r = subprocess.run(["sudo", "-n", "test", "-f", file_path], capture_output=True, timeout=3)
        return "SET" if r.returncode == 0 else "ABSENT"
    except Exception:
        return "UNKNOWN"


def _resolve_cred_status(cred: dict) -> str:
    if cred.get("cred_status") == "future":
        return "FUTURE"
    storage = cred.get("storage")
    env_var = cred.get("env_var")
    file_path = cred.get("file", "")
    if storage == "system":
        return _cred_check_system(file_path)
    if storage == "openclaw":
        return "SET" if _OPENCLAW_JSON.exists() else "ABSENT"
    if not env_var:
        return "UNKNOWN"
    if storage == "env":
        return _cred_check_env(file_path, env_var)
    if storage == "role":
        return _cred_check_role(file_path, env_var)
    return "UNKNOWN"


def _build_credentials_status() -> list[dict]:
    return [{**c, "status": _resolve_cred_status(c)} for c in _CREDS]


def _cred_update_cmd(cred: dict) -> str:
    if cred.get("cred_status") == "future":
        return "—"
    storage = cred.get("storage", "")
    role = cred.get("role", "")
    file_path = cred.get("file", "")
    if storage == "openclaw":
        return "openclaw configure"
    if storage == "role" and role:
        return f"scripts/env_role_sync.sh pull &lt;machine&gt; {role}"
    if storage == "system":
        return "# see ROTATION_RUNBOOK.md"
    if storage == "env":
        short = file_path.replace(str(Path.home()), "~")
        return f"vim {short}"
    return "—"


def _cred_status_badge(status: str) -> str:
    return cred_status_badge(status)


def _credentials_html(creds: list[dict]) -> str:
    active = [c for c in creds if c.get("cred_status") != "future"]
    set_n = sum(1 for c in active if c["status"] == "SET")
    absent_n = sum(1 for c in active if c["status"] == "ABSENT")
    unknown_n = sum(1 for c in active if c["status"] == "UNKNOWN")
    future_n = sum(1 for c in creds if c["status"] == "FUTURE")

    from collections import OrderedDict
    providers: dict[str, list[dict]] = OrderedDict()
    for c in creds:
        providers.setdefault(c["provider"], []).append(c)

    provider_tables = ""
    for prov, pcreds in providers.items():
        rows = ""
        for c in pcreds:
            fshort = c["file"].replace(str(Path.home()), "~").replace(str(PROJECT_ROOT), ".")
            rows += f"""
<tr>
  <td><code style="font-size:11px">{c['id']}</code></td>
  <td><code style="font-size:11px">{c.get('env_var') or '—'}</code></td>
  <td>{_cred_status_badge(c['status'])}</td>
  <td style="font-size:11px;color:#666">{c['storage']}</td>
  <td style="font-size:11px;color:#888;font-family:monospace;word-break:break-all">{fshort}</td>
  <td><code style="font-size:10px;background:#1d1d1f;color:#e8e8e8;padding:2px 6px;border-radius:4px;white-space:nowrap">{_cred_update_cmd(c)}</code></td>
</tr>"""
        pset = sum(1 for c in pcreds if c["status"] == "SET")
        ptot = len([c for c in pcreds if c.get("cred_status") != "future"])
        hdr = f'<span style="font-size:11px;color:#888;font-weight:normal">{pset}/{ptot} set</span>' if ptot else ""
        provider_tables += f"""
<div style="margin-bottom:24px">
  <h3 style="font-size:14px;font-weight:600;margin-bottom:8px">{prov} {hdr}</h3>
  <table>
    <thead><tr><th>ID</th><th>Env Var</th><th>Status</th><th>Storage</th><th>File</th><th>Update Command</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Credentials</title>
  <style>
    {STANDARD_CSS}
    th, td {{ padding: 8px 12px; }}
    .links-bar {{ margin-bottom: 16px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <a class="nav-item" href="/">← Dashboard</a>
    <a class="nav-item" href="/journal">📋 Journal</a>
    <a class="nav-item" href="/metrics">📊 Metrics</a>
    <a class="nav-item nav-active" href="/credentials">🔑 Credentials</a>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666;margin-left:10px">
      <div><a href="/health" style="color:#888;text-decoration:none">/health</a></div>
      <div><a href="/credentials/json" style="color:#888;text-decoration:none">/credentials/json</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>🔑 Credentials Registry</h2>
    <p class="subtitle">Statut de tous les credentials par provider — valeurs jamais affichées.</p>
    <div class="summary-bar">
      <div class="summary-card" style="border-left:4px solid #30d158"><div class="num">{set_n}</div><div class="label">SET</div></div>
      <div class="summary-card" style="border-left:4px solid #ff453a"><div class="num">{absent_n}</div><div class="label">ABSENT</div></div>
      <div class="summary-card" style="border-left:4px solid #999"><div class="num">{unknown_n}</div><div class="label">UNKNOWN</div></div>
      <div class="summary-card" style="border-left:4px solid #5e5ce6"><div class="num">{future_n}</div><div class="label">FUTURE</div></div>
      <div class="summary-card"><div class="num">{len(active)}</div><div class="label">Total actifs</div></div>
    </div>
    <div class="notice">
      Lecture seule — aucune valeur n'est affichée. Pour mettre à jour :
      <code style="background:#fff;border:1px solid #ddd;padding:1px 6px;border-radius:4px">python3 scripts/credentials_form.py</code>
    </div>
    <div class="links-bar">
      <a href="/">← Dashboard</a>
      <a href="/credentials/json">JSON API</a>
    </div>
    {provider_tables}
    <div style="margin-top:16px;font-size:12px;color:#666">
      Dernière vérification : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
    </div>
    <div style="height:40px"></div>
  </main>
</div>
</body>
</html>"""


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


# ── Data Center endpoints ────────────────────────────────────────────

@app.get("/data-center/health")
def get_data_center_health():
    from modules.data_center.localcms_health_reader import read_data_center_health
    return JSONResponse(content=read_data_center_health())


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
    {STANDARD_CSS}
    .card-row > .card {{ flex: 1; min-width: 130px; padding: 16px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">TMUX Sessions</span></a>
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
        <h4>TMUX Sessions</h4>
        <div class="value" style="color:{tmux_color}">{tmux_up}/{tmux_total} UP</div>
      </div>
      <div class="info-card">
        <h4>Critical sessions DOWN</h4>
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


def _pnl_badge(outcome: str) -> str:
    return pnl_badge(outcome)


def _verdict_badge(verdict: str) -> str:
    return verdict_badge(verdict)


def _closeout_badge(ack: bool) -> str:
    return closeout_badge(ack)


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
    {STANDARD_CSS}
    .summary-card {{ min-width: 140px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">TMUX Sessions</span></a>
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
    {STANDARD_CSS}
    .info-grid {{ grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div class="nav-section" style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Runtime</div>
      <a class="nav-item" href="/#tmux-sessions"><span class="nav-icon">🖥️</span><span class="nav-label">TMUX Sessions</span></a>
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


@app.get("/credentials", response_class=HTMLResponse)
def credentials_html():
    creds = _build_credentials_status()
    return HTMLResponse(content=_credentials_html(creds))


@app.get("/credentials/json")
def credentials_json():
    creds = _build_credentials_status()
    return JSONResponse(content=[
        {"id": c["id"], "provider": c["provider"], "env_var": c.get("env_var"),
         "status": c["status"], "storage": c["storage"], "file": c["file"]}
        for c in creds
    ])


# ── Signals panel ───────────────────────────────────────────────────

@app.get("/signals/summary")
def signals_summary():
    """Return telegram signal summary for dashboard."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from modules.analysis_bundles.app.telegram_signal_query import signal_summary
        return JSONResponse(content=signal_summary())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/signals")
def signals_list(channel: str = "", pair: str = "", direction: str = "", complete: bool = False):
    """Query signals with filters. Use ?channel=&pair=&direction=&complete=1"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from modules.analysis_bundles.app.telegram_signal_query import query_signals
        signals = query_signals(
            channel=channel if channel else None,
            pair=pair if pair else None,
            direction=direction.upper() if direction else None,
            complete_only=complete,
        )
        return JSONResponse(content={
            "total": len(signals),
            "signals": signals[:100],
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/signals/channels")
def signals_channels():
    """List all channels with types, modes, signal counts."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from modules.analysis_bundles.app.telegram_signal_query import list_channels
        return JSONResponse(content=list_channels())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ── Vision panel ─────────────────────────────────────────────────────

_VISION_COINGLASS = PROJECT_ROOT / "data" / "vision" / "coinglass" / "latest.json"
_VISION_SCREENER = PROJECT_ROOT / "data" / "data_center" / "views" / "vision_context" / "screener" / "latest.json"
_VISION_ANALYSIS_LATEST = PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "latest.json"
_VISION_ANALYSIS_DIR = PROJECT_ROOT / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"
_VISION_RAW_DIR = PROJECT_ROOT / "data" / "vision" / "coinglass" / "raw"


@app.get("/vision/summary")
def vision_summary():
    """Aggregated vision status for dashboard."""
    now = datetime.now(timezone.utc).isoformat()

    # Coinglass metrics
    cg = {}
    if _VISION_COINGLASS.exists():
        try:
            raw = json.loads(_VISION_COINGLASS.read_text())
            cg = {
                "freshness": raw.get("freshness_state", "stale"),
                "screenshot_ts": raw.get("screenshot_ts", ""),
                "symbol": raw.get("symbol", ""),
                "metrics": {d["detected_metric_type"]: d["extracted_value"] for d in raw.get("detections", [])},
            }
        except Exception:
            cg = {"error": "parse failed"}

    # Screener context
    scr = {}
    if _VISION_SCREENER.exists():
        try:
            raw = json.loads(_VISION_SCREENER.read_text())
            scr = {
                "freshness": raw.get("freshness_state", "stale"),
                "captured_at": raw.get("captured_at", ""),
                "screener_label": raw.get("screener_label", ""),
                "stock_count": len(raw.get("stocks", [])),
            }
        except Exception:
            scr = {"error": "parse failed"}

    # Vision analysis
    symbols = []
    if _VISION_ANALYSIS_DIR.exists():
        for f in sorted(_VISION_ANALYSIS_DIR.glob("*.json")):
            try:
                raw = json.loads(f.read_text())
                items = raw if isinstance(raw, list) else [raw]
                for data in items:
                    signal_list = data.get("signals", [])
                    symbols.append({
                        "symbol": data.get("symbol", f.stem),
                        "timeframe": data.get("timeframe", ""),
                        "freshness": data.get("freshness_state", "stale"),
                        "analysis_ts": data.get("analysis_ts", ""),
                        "signal_count": len(signal_list),
                        "top_signal": signal_list[0]["type"] if signal_list else None,
                    })
            except Exception:
                continue

    # Latest screenshot
    screenshot_info = {}
    if _VISION_RAW_DIR.exists():
        screenshots = sorted(_VISION_RAW_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        if screenshots:
            latest = screenshots[0]
    screenshot_info = {
                "file": latest.name,
                "size_kb": latest.stat().st_size // 1024,
                "mtime": datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc).isoformat(),
            }


# ── Backtest panel ────────────────────────────────────────────────────

_BACKTEST_JSON = PROJECT_ROOT / "data" / "trading_lab_v1" / "exports" / "latest.json"
_BACKTEST_CSV_DIR = PROJECT_ROOT / "data" / "trading_lab_v1" / "exports"


@app.get("/backtest/summary")
def backtest_summary():
    """Return latest backtest summary for dashboard."""
    if not _BACKTEST_JSON.exists():
        return JSONResponse(content={"error": "No backtest data. Run: cmd.sh backtest"}, status_code=404)
    try:
        return JSONResponse(content=json.loads(_BACKTEST_JSON.read_text(encoding="utf-8")))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/backtest/csv")
def backtest_csv():
    """Return latest backtest CSV file."""
    csv_files = sorted(_BACKTEST_CSV_DIR.glob("backtest_*.csv"), reverse=True)
    if not csv_files:
        return JSONResponse(content={"error": "No CSV export. Run: python -m modules.trading_lab_v1.app.backtest_export"}, status_code=404)
    from fastapi.responses import FileResponse
    return FileResponse(csv_files[0], media_type="text/csv", filename=csv_files[0].name)


# ── HTML UI ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
def ui_index(request: Request):
    tmux = _build_tmux_report()
    menu_data = _read_json(MENU_FILE)
    state_data = _read_json(STATE_CACHE)

    # Proxy perf + deskpro summary
    perf_data = {}
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://127.0.0.1:8010/perf/summary", timeout=3)
        perf_data = json.loads(resp.read())
    except Exception:
        pass

    menu_json = json.dumps(menu_data, indent=2)
    tmux_json = json.dumps(tmux, indent=2)
    state_json = json.dumps(state_data, indent=2)

    # Perf KPI cards
    perf_html = ""
    if perf_data:
        pnl = perf_data.get("pnl_realized", 0)
        pnl_class = "pnl-positive" if pnl >= 0 else "pnl-negative"
        perf_html = f"""
    <div class="section" id="perf">
      <h2>📈 Performance <a href="http://localhost:8010/desk/ui" target="_blank" style="font-size:11px;color:#58a6ff">(Desk Pro →)</a></h2>
      <div class="kpi-grid">
        <div class="kpi"><div class="num">{perf_data.get('total_trades', 0)}</div><div class="label">Total Trades</div></div>
        <div class="kpi"><div class="num">{perf_data.get('open_trades', 0)}</div><div class="label">Open</div></div>
        <div class="kpi"><div class="num">{perf_data.get('winrate_pct', 0):.1f}%</div><div class="label">Winrate</div></div>
        <div class="kpi"><div class="num {pnl_class}">\${pnl:,.0f}</div><div class="label">P&L</div></div>
        <div class="kpi"><div class="num">{perf_data.get('avg_r', 0):.4f}</div><div class="label">Avg R</div></div>
      </div>
    </div>"""

    # Try deskpro status
    desk_html = '<div class="section"><h2>🖥️ Desk Pro <a href="http://localhost:8010/desk/ui" target="_blank" style="font-size:11px;color:#58a6ff">(ouvrir →)</a></h2><p style="font-size:12px;color:#8b949e">UI de trading accessible sur le port 8010</p></div>'

    sessions_rows = ""
    for s in tmux["sessions"]:
        status_badge = (
            badge('UP', 'up') if s["running"]
            else badge('DOWN', 'down')
        )
        crit_badge = (
            badge('CRITICAL', 'critical') if s["critical"]
            else badge('non-critical', 'noncrit')
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
    # Add Signals link first
    nav_items += """
<a class="nav-item nav-item-signals" href="/signals">
  <span class="nav-icon">📡</span>
  <span class="nav-label">Telegram Signals</span>
</a>
<a class="nav-item nav-item-vision" href="/vision">
  <span class="nav-icon">👁️</span>
  <span class="nav-label">Bot Vision</span>
</a>
<a class="nav-item nav-item-backtest" href="/backtest/summary">
  <span class="nav-icon">🧪</span>
  <span class="nav-label">Backtest</span>
</a>"""
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
                    badge_html = STATUS_BADGES.get(s, badge(s, "unknown"))
                    children_html += f"""
  <div class="module-row">
    <span class="module-label">{item['label']}</span>
    {badge_html}
    <span class="module-machine">{item.get('machine', '')}</span>
  </div>"""
                children_html += "</div>"
            else:
                s = child.get("status", "unknown")
                badge_html = STATUS_BADGES.get(s, badge(s, "unknown"))
                children_html += f"""
<div class="module-row">
  <span class="module-label">{child['label']}</span>
  {badge_html}
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
    {STANDARD_CSS}
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
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Security</div>
      <a class="nav-item" href="/credentials"><span class="nav-icon">🔑</span><span class="nav-label">Credentials</span></a>
    </div>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">IPO / SPCX</div>
      <a class="nav-item" href="/spacex"><span class="nav-icon">🚀</span><span class="nav-label">SpaceX Cmd Center</span></a>
      <a class="nav-item" href="/true-value"><span class="nav-icon">📐</span><span class="nav-label">True Value</span></a>
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
      <div><a href="/credentials" style="color:#888;text-decoration:none">/credentials</a></div>
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

    {perf_html}

    {desk_html}

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
        <tr><td><a href="/metrics">/metrics</a></td><td>Dashboard métriques agrégées (HTML)</td></tr>
        <tr><td><a href="/metrics/daily">/metrics/daily</a></td><td>Métriques daily session (JSON)</td></tr>
        <tr><td><a href="/credentials">/credentials</a></td><td>Credentials registry — statut SET/ABSENT par provider (HTML)</td></tr>
        <tr><td><a href="/credentials/json">/credentials/json</a></td><td>Credentials registry (JSON)</td></tr>
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


@app.get("/signals", response_class=HTMLResponse)
def signals_page(request: Request):
    """Dedicated Telegram Signals dashboard page."""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from modules.analysis_bundles.app.telegram_signal_query import signal_summary
        summary = signal_summary()
    except Exception:
        summary = {"totals": {"signals": 0, "complete": 0, "incomplete": 0, "longs": 0, "shorts": 0, "active_channels": 0},
                   "by_type": {}, "by_pair": {}, "by_channel": {}}

    t = summary["totals"]

    # Build type rows
    type_rows = ""
    for ct, info in sorted(summary.get("by_type", {}).items(), key=lambda x: -x[1]["total"]):
        type_rows += f"""<tr><td>{info['label']}</td><td>{info['total']}</td><td>{info['complete']}</td></tr>"""

    # Build pair rows
    pair_rows = ""
    for p, cnt in list(summary.get("by_pair", {}).items())[:15]:
        pair_rows += f"""<tr><td>{p}</td><td>{cnt}</td></tr>"""

    # Build channel rows
    ch_rows = ""
    for ch, info in sorted(summary.get("by_channel", {}).items(), key=lambda x: -x[1]["complete"])[:25]:
        ch_rows += f"""<tr><td>{ch}</td><td>{info['total']}</td><td>{info['complete']}</td><td>{info['priority']}</td></tr>"""

    json_summary = json.dumps(summary, indent=2, default=str)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LocalCMS — Telegram Signals</title>
<style>
    {SIGNALS_DARK_CSS}
</style>
</head>
<body>
<header>
  <a href="/" class="nav-back">← LocalCMS</a>
  <h1>📡 Telegram Signals</h1>
</header>
<main>
  <div class="kpi-grid">
    <div class="kpi"><div class="num">{t['signals']}</div><div class="label">Signaux</div></div>
    <div class="kpi"><div class="num">{t['complete']}</div><div class="label">Complets</div></div>
    <div class="kpi"><div class="num">{t['longs']}</div><div class="label">LONG</div></div>
    <div class="kpi"><div class="num">{t['shorts']}</div><div class="label">SHORT</div></div>
    <div class="kpi"><div class="num">{t['active_channels']}</div><div class="label">Canaux</div></div>
    <div class="kpi"><div class="num">{t['incomplete']}</div><div class="label">Incomplets</div></div>
  </div>

  <div class="section">
    <h2>Par type de signal</h2>
    <table><tr><th>Type</th><th>Total</th><th>Complets</th></tr>
    {type_rows}
    </table>
  </div>

  <div class="section">
    <h2>Top paires</h2>
    <table><tr><th>Paire</th><th>Signaux</th></tr>
    {pair_rows}
    </table>
  </div>

  <div class="section">
    <h2>Top canaux (complets)</h2>
    <table><tr><th>Canal</th><th>Total</th><th>Complets</th><th>Prio</th></tr>
    {ch_rows}
    </table>
  </div>

  <details class="json-toggle">
    <summary>📋 JSON brut</summary>
    <pre>{json_summary}</pre>
  </details>

  <div class="auto-refresh">Auto-refresh 30s. {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
</main>
<script>setTimeout(() => location.reload(), 30000);</script>
</body>
</html>"""
    return HTMLResponse(content=html)


# ── SpaceX / SPCX Command Center ───────────────────────────────────────
_SPACEX_CC_JSON = PROJECT_ROOT / "data" / "ipo" / "spacex" / "command_center" / "latest.json"
_SPACEX_SNAPSHOT = PROJECT_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
_TRUE_VALUE_SCORES = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest" / "scores.json"


def _true_value_html() -> str:
    data = {}
    if _TRUE_VALUE_SCORES.exists():
        try:
            data = json.loads(_TRUE_VALUE_SCORES.read_text())
        except (json.JSONDecodeError, OSError):
            data = {"error": "parse failed"}

    items = data.get("items", [])
    summary = data.get("summary", {})
    asof = (data.get("asof") or "")[:19].replace("T", " ")

    grades = summary.get("grades", {})
    total = summary.get("count", len(items))
    low_conf = summary.get("low_confidence_count", 0)

    grade_color = {
        "A+": "#30d158", "A": "#7ddc6e", "B": "#ffd60a", "C": "#ff9f0a",
        "D": "#ff453a", "RESEARCH_REQUIRED": "#bf5af2",
    }

    rows = ""
    for it in (items or [])[:20]:
        ticker = it.get("ticker", it.get("symbol", "?"))
        grade = it.get("grade", "?")
        tv = it.get("true_value", 0)
        hype = it.get("hype", 0)
        risk = it.get("risk", 0)
        conf = it.get("confidence", 0)
        action = it.get("action", it.get("action_bias", ""))
        drivers = it.get("drivers", {})
        pos = ", ".join(drivers.get("positive", []))
        neg = ", ".join(drivers.get("negative", []))
        flags = it.get("flags", [])
        flag_str = " ".join(f'<span class="pill pill-danger">{f}</span>' for f in (flags or [])[:3])
        gcolor = grade_color.get(grade, "#888")
        rows += f"""<tr>
  <td style="font-weight:600">{ticker}</td>
  <td><span style="color:{gcolor};font-weight:700">{grade}</span></td>
  <td class="num">{tv:.1f}</td>
  <td class="num">{hype:.1f}</td>
  <td class="num">{risk:.1f}</td>
  <td class="num">{conf:.0f}%</td>
  <td style="font-size:11px">{action}</td>
  <td style="font-size:10px">{pos[:60]}</td>
  <td style="font-size:10px">{neg[:60]}</td>
  <td style="font-size:10px">{flag_str}</td>
</tr>"""

    grade_dist = ""
    for g, c in grades.items():
        gc = grade_color.get(g, "#888")
        grade_dist += f'<div class="summary-card"><div class="num" style="font-size:28px;color:{gc}">{c}</div><div class="label">{g}</div></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — True Value</title>
  <style>
    {STANDARD_CSS}
    th, td {{ padding: 6px 10px; font-size: 12px; }}
    .num {{ text-align: right; font-family: monospace; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Analysis</div>
      <a class="nav-item nav-active" href="/true-value">📐 True Value</a>
    </div>
    <a class="nav-item" href="/">🏠 Dashboard</a>
    <a class="nav-item" href="/spacex">🚀 SpaceX</a>
    <a class="nav-item" href="/signals">📡 Signals</a>
    <a class="nav-item" href="/journal">📋 Journal</a>
    <a class="nav-item" href="/metrics">📊 Metrics</a>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666;margin-left:10px">
      <div><a href="/true-value/json" style="color:#888;text-decoration:none">/true-value/json</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>📐 Stock / SpaceX True Value</h2>
    <p class="subtitle">{asof} &middot; Model: {data.get('model_version', '—')} &middot; {total} items &middot; {low_conf} low confidence</p>

    <div class="section-title">Grade Distribution</div>
    <div class="summary-bar">{grade_dist}</div>

    <div class="section-title">Score Summary</div>
    <table>
      <thead>
        <tr>
          <th>Ticker</th><th>Grade</th><th>True Value</th><th>Hype</th>
          <th>Risk</th><th>Confidence</th><th>Action</th>
          <th>+ Drivers</th><th>- Drivers</th><th>Flags</th>
        </tr>
      </thead>
      <tbody>{rows if rows else '<tr><td colspan="10">No scores available. Run: python -m modules.stock_true_value.cli --fixture-only</td></tr>'}</tbody>
    </table>
  </main>
</div>
<script>setTimeout(() => location.reload(), 120000);</script>
</body>
</html>"""


def _spacex_html() -> str:
    data = {}
    if _SPACEX_CC_JSON.exists():
        try:
            data = json.loads(_SPACEX_CC_JSON.read_text())
        except (json.JSONDecodeError, OSError):
            data = {"error": "parse failed"}

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

    # edge bar: 5-char compact bar
    edge_fill = min(5, max(0, edge_score // 20))
    ebar = "|" * edge_fill + "." * (5 - edge_fill)

    # badges
    action_cls = "cred-set" if "A" in str(action) else ("cred-future" if "B" in str(action) or "WATCH" in str(action) else "cred-unknown")
    health_cls = "cred-set" if pipeline_healthy else "cred-absent"
    market_cls = "cred-set" if market_state == "OPEN" else "cred-unknown"

    # analog table rows
    analog_rows = ""
    for a in (analogs or [])[:3]:
        pct = a.get("pct", a.get("probability_pct", 0))
        analog_rows += f"<tr><td>{a['symbol']}</td><td class='num'>{pct}%</td></tr>"

    # risk notice
    risk_notice = ""
    if risks and risks != ["None"]:
        risk_notice = "<div class='notice'>" + "".join(f"<div>⚠ {r}</div>" for r in risks) + "</div>"

    # levels table
    levels_rows = ""
    if entry_price:
        levels_rows += f"<tr><td>Entry</td><td class='num'>${entry_price:.2f}</td></tr>"
    if stop_price:
        levels_rows += f"<tr><td style='color:#ef5350'>Stop</td><td class='num' style='color:#ef5350'>${stop_price:.2f}</td></tr>"
    if tp1_price:
        levels_rows += f"<tr><td style='color:#30d158'>TP1</td><td class='num' style='color:#30d158'>${tp1_price:.2f}</td></tr>"
    if tp2_price:
        levels_rows += f"<tr><td style='color:#30d158'>TP2</td><td class='num' style='color:#30d158'>${tp2_price:.2f}</td></tr>"

    vol_str = f"{volume/1e6:.1f}M" if volume and volume >= 1e6 else (f"{volume/1e3:.0f}K" if volume and volume >= 1e3 else str(volume) if volume else "—")
    vwap_str = f"${vwap:.2f}" if vwap else "—"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — SpaceX Cmd Center</title>
  <style>
    {STANDARD_CSS}
    .summary-card .num {{ font-size: 24px; }}
    table {{ margin-bottom: 16px; }}
    th, td {{ padding: 8px 12px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">IPO / SPCX</div>
      <a class="nav-item nav-active" href="/spacex">🚀 Cmd Center</a>
    </div>
    <a class="nav-item" href="/">🏠 Dashboard</a>
    <a class="nav-item" href="/signals">📡 Signals</a>
    <a class="nav-item" href="/journal">📋 Journal</a>
    <a class="nav-item" href="/metrics">📊 Metrics</a>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666;margin-left:10px">
      <div><a href="/spacex/json" style="color:#888;text-decoration:none">/spacex/json</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>🚀 SpaceX / SPCX Command Center</h2>
    <p class="subtitle">{generated_at} — <span class="{market_cls}">{market_state}</span> &middot; <span class="{health_cls}">{'HEALTHY' if pipeline_healthy else 'DEGRADED'}</span> &middot; Sources {sources_ok}/{sources_total}</p>

    <div class="links-bar">
      <a href="/spacex/json" target="_blank">JSON</a>
    </div>

    {risk_notice}

    <div class="summary-bar">
      <div class="summary-card">
        <div class="num">${price:.2f}</div><div class="label">Price</div>
      </div>
      <div class="summary-card">
        <div class="num">{gap:+.1f}%</div><div class="label">Gap vs IPO</div>
      </div>
      <div class="summary-card">
        <div class="num">{edge_score}</div><div class="bar">{ebar}</div><div class="label">Edge Score</div>
      </div>
      <div class="summary-card">
        <div class="num">{open_score}</div><div class="label">Open Score</div>
      </div>
    </div>

    <div class="summary-bar">
      <div class="summary-card">
        <div class="label">Action</div>
        <div class="num" style="font-size:20px"><span class="{action_cls}" style="font-size:14px">{action}</span></div>
      </div>
      <div class="summary-card">
        <div class="label">Confidence</div>
        <div class="num" style="font-size:20px">{confidence}</div>
      </div>
      <div class="summary-card">
        <div class="label">Top Setup</div>
        <div class="num" style="font-size:18px">{top_setup}</div>
        <div class="label">{top_prob}% probability</div>
      </div>
      <div class="summary-card">
        <div class="label">Sector / Consensus</div>
        <div class="num" style="font-size:16px">{sector_regime}</div>
        <div class="label">disagreement {disagreement:.1f}%</div>
      </div>
    </div>

    <div class="summary-bar">
      <div class="summary-card">
        <div class="label">Volume</div>
        <div class="num" style="font-size:18px">{vol_str}</div>
      </div>
      <div class="summary-card">
        <div class="label">VWAP</div>
        <div class="num" style="font-size:18px">{vwap_str}</div>
      </div>
      <div class="summary-card" style="flex:2">
        <div class="label">IPO Analogs</div>
        <table style="margin-bottom:0"><tr><th>Ticker</th><th style="text-align:right">Match</th></tr>{analog_rows if analog_rows else '<tr><td colspan="2">No data</td></tr>'}</table>
      </div>
    </div>

    {f'<table><tr><th colspan="2">Trade Levels</th></tr>{levels_rows}</table>' if levels_rows else ''}
  </main>
</div>
<script>setTimeout(() => location.reload(), 60000);</script>
</body>
</html>"""


@app.get("/spacex", response_class=HTMLResponse)
def spacex_html():
    return HTMLResponse(content=_spacex_html())


@app.get("/spacex/json")
def spacex_json():
    if _SPACEX_CC_JSON.exists():
        return JSONResponse(content=json.loads(_SPACEX_CC_JSON.read_text()))
    if _SPACEX_SNAPSHOT.exists():
        return JSONResponse(content=json.loads(_SPACEX_SNAPSHOT.read_text()))
    return JSONResponse(content={"error": "No SpaceX data yet", "action": "run spacex-super-desk collect-once"}, status_code=200)


@app.get("/true-value", response_class=HTMLResponse)
def true_value_html():
    return HTMLResponse(content=_true_value_html())


@app.get("/true-value/json")
def true_value_json():
    if _TRUE_VALUE_SCORES.exists():
        return JSONResponse(content=json.loads(_TRUE_VALUE_SCORES.read_text()))
    return JSONResponse(content={"error": "No scores yet", "action": "run python -m modules.stock_true_value.cli --fixture-only"}, status_code=200)


STATUS_BADGES = SHARED_STATUS_BADGES


# ── PWA & Access ───────────────────────────────────────────────────────
_LOCALCMS_STATIC = PROJECT_ROOT / "modules" / "localcms" / "static"


@app.get("/manifest.webmanifest")
def manifest():
    path = _LOCALCMS_STATIC / "manifest.webmanifest"
    if path.exists():
        return JSONResponse(content=json.loads(path.read_text()), media_type="application/manifest+json")
    return JSONResponse(content={}, status_code=404)


@app.get("/service-worker.js")
def service_worker():
    path = _LOCALCMS_STATIC / "service-worker.js"
    if path.exists():
        from fastapi.responses import Response
        return Response(content=path.read_text(), media_type="application/javascript")
    return Response(content="", status_code=404)


@app.get("/access", response_class=HTMLResponse)
def access_page():
    import socket
    hostname = socket.gethostname()
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"/>
  <meta name="theme-color" content="#0b0d12"/>
  <meta name="apple-mobile-web-app-capable" content="yes"/>
  <meta name="apple-mobile-web-app-title" content="LocalCMS"/>
  <link rel="manifest" href="/manifest.webmanifest"/>
  <link rel="icon" type="image/png" sizes="192x192" href="/static/icon-192.png"/>
  <link rel="apple-touch-icon" href="/static/icon-192.png"/>
  <title>LocalCMS — Acces</title>
  <style>
    {STANDARD_CSS}
    .access-card {{ background: var(--card-bg,#151a24); border:1px solid var(--card-border,#2a3345);
      border-radius: var(--card-radius,10px); padding: 14px; margin-bottom: 10px; }}
    .access-card h3 {{ color: #a8c7ff; font-size: 13px; margin-bottom: 6px; }}
    .access-card a {{ color: #58a6ff; text-decoration: none; font-size: 12px; display: block; padding: 3px 0; }}
    .access-card .note {{ font-size: 10px; color: #555; margin-top: 6px; }}
    .install-btn {{ background: #1a3050; color:#a8c7ff; border:1px solid #4477cc;
      border-radius:8px; padding:10px 20px; font-size:13px; cursor:pointer; margin:12px 0; }}
    .install-btn:hover {{ background:#243050; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Acces</div>
      <a class="nav-item nav-active" href="/access">🔑 Acces</a>
    </div>
    <a class="nav-item" href="/">🏠 Dashboard</a>
    <a class="nav-item" href="/voice">🎙️ Voice</a>
    <a class="nav-item" href="/spacex">🚀 SpaceX</a>
  </nav>
  <main class="main">
    <h2>🔑 LocalCMS — Acces Prive</h2>
    <p class="subtitle">Cockpit prive — aucune exposition publique. Reseau local ou WireGuard uniquement.</p>

    <button class="install-btn" onclick="installPWA()" id="install-btn" style="display:none">📱 Installer l'app</button>

    <div class="access-card">
      <h3>📱 Voice Operator</h3>
      <a href="/voice">/voice</a>
      <a href="/voice/analytics">/voice/analytics</a>
    </div>
    <div class="access-card">
      <h3>🚀 SPCX</h3>
      <a href="/spacex">/spacex</a>
      <a href="/desk/spacex/command-center">/desk/spacex/command-center</a>
      <a href="/desk/spacex/snapshot">/desk/spacex/snapshot</a>
    </div>
    <div class="access-card">
      <h3>📊 Systeme</h3>
      <a href="/">/ (Dashboard)</a>
      <a href="/desk/status">/desk/status</a>
      <a href="/signals">/signals</a>
      <a href="/journal">/journal</a>
      <a href="/metrics">/metrics</a>
      <a href="/credentials">/credentials</a>
    </div>
    <div class="access-card">
      <h3>🔌 Technique</h3>
      <div class="note">Host: {hostname}</div>
      <div class="note">Port: 8010 (perf_app) ou 8700 (localcms direct)</div>
      <div class="note">⚠️ Aucune exposition publique. Acces via LAN ou WireGuard.</div>
      <div class="note">📱 Ajouter a l'ecran d'accueil pour utiliser comme app native.</div>
    </div>
  </main>
</div>
<script>
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('/service-worker.js').catch(() => {{}});
}}
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {{
  e.preventDefault();
  deferredPrompt = e;
  document.getElementById('install-btn').style.display = 'block';
}});
function installPWA() {{
  if (deferredPrompt) {{ deferredPrompt.prompt(); deferredPrompt = null; }}
}}
</script>
</body>
</html>"""


# ── Voice Operator ─────────────────────────────────────────────────────
_VOICE_PROFILES = {
    "default": {"label": "Tous", "icon": "🎙️", "sections": ["Système", "Marché", "Alertes", "Setups", "Scores / Risques", "Rapports"]},
    "matin":   {"label": "Matin", "icon": "🌅", "sections": ["Système", "Marché", "Alertes"]},
    "intraday":{"label": "Intraday", "icon": "📈", "sections": ["Marché", "Setups", "Scores / Risques"]},
    "risk":    {"label": "Risque", "icon": "⚠️", "sections": ["Scores / Risques", "Alertes"]},
    "spcx":    {"label": "SPCX", "icon": "🚀", "sections": ["Marché", "Setups", "Scores / Risques"]},
    "gold":    {"label": "Gold", "icon": "🥇", "sections": ["Marché", "Setups", "Scores / Risques"]},
    "btc":     {"label": "BTC", "icon": "₿", "sections": ["Marché", "Setups", "Scores / Risques"]},
}

_VOICE_PRESETS = [
    ("🌅 Matin", ["Etat systeme", "Rapport marche", "Alertes Telegram"]),
    ("📈 Intraday", ["Setups actifs", "Analyse BTC", "Analyse Gold"]),
    ("⚠️ Risque", ["Score BTC", "Score Gold", "Alertes Telegram"]),
    ("🚀 SPCX", ["Resume SPCX", "Setup SPCX", "Score SPCX"]),
]

_VOICE_SECTIONS = [
    {
        "title": "Système",
        "icon": "⚙️",
        "commands": [
            ("État système", "Etat systeme"),
        ],
    },
    {
        "title": "Marché",
        "icon": "📈",
        "commands": [
            ("Rapport marché", "Rapport marche"),
            ("Analyse BTC", "Analyse BTC"),
            ("Analyse Gold", "Analyse Gold"),
            ("Résumé SPCX", "Resume SPCX"),
        ],
    },
    {
        "title": "Alertes",
        "icon": "🔔",
        "commands": [
            ("Alertes Telegram", "Alertes Telegram"),
        ],
    },
    {
        "title": "Setups",
        "icon": "🎯",
        "commands": [
            ("Setups actifs", "Setups actifs"),
            ("Setup BTC", "Setup BTC"),
            ("Setup Gold", "Setup Gold"),
            ("Setup SPCX", "Setup SPCX"),
        ],
    },
    {
        "title": "Scores / Risques",
        "icon": "📊",
        "commands": [
            ("Score BTC", "Score BTC"),
            ("Score Gold", "Score Gold"),
            ("Score SPCX", "Score SPCX"),
        ],
    },
    {
        "title": "Rapports",
        "icon": "📋",
        "commands": [
            ("Rapport quotidien", "Rapport quotidien"),
        ],
    },
]

_VOICE_ACTIVE_PROFILE = "default"


def _voice_operator_html() -> str:
    # Quick buttons from sections
    quick_btns = ""
    for section in _VOICE_SECTIONS[:4]:  # Systeme, Marche, Alertes, Setups
        for label, command in section["commands"]:
            quick_btns += f'<button class="quick-btn" onclick="sendCommand(\'{command}\')">{label}</button>'

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"/>
  <meta name="theme-color" content="#0b0d12"/>
  <title>LocalCMS — Chat Operator</title>
  <style>
    {STANDARD_CSS}
    body {{ background: #0b0d12; }}
    .chat-container {{ display:flex; flex-direction:column; height:100vh; max-width:700px; margin:0 auto; }}
    .chat-header {{ padding:12px 16px; border-bottom:1px solid #1a1f2a; display:flex; align-items:center; gap:10px; flex-shrink:0; }}
    .chat-header h2 {{ color:#a8c7ff; font-size:16px; margin:0; }}
    .diag-bar {{ display:flex; gap:12px; font-size:10px; color:#555; margin-left:auto; }}
    .diag-ok {{ color:#30d158; }} .diag-fail {{ color:#ef5350; }}
    .quick-bar {{ padding:8px 16px; display:flex; flex-wrap:wrap; gap:6px; border-bottom:1px solid #1a1f2a; flex-shrink:0; }}
    .quick-btn {{ background:#151a24; color:#a8c7ff; border:1px solid #2a3345; border-radius:6px; padding:5px 10px; font-size:11px; cursor:pointer; white-space:nowrap; }}
    .quick-btn:hover {{ background:#1e2840; border-color:#4477cc; }}
    .quick-btn:active {{ background:#243050; }}
    .messages {{ flex:1; overflow-y:auto; padding:12px 16px; display:flex; flex-direction:column; gap:10px; }}
    .msg {{ max-width:85%; padding:10px 14px; border-radius:12px; font-size:13px; line-height:1.5; animation:fadeIn 0.2s; }}
    @keyframes fadeIn {{ from{{opacity:0;transform:translateY(4px)}} to{{opacity:1;transform:translateY(0)}} }}
    .msg-user {{ align-self:flex-end; background:#1a3050; color:#e8eef7; border-bottom-right-radius:4px; }}
    .msg-bot {{ align-self:flex-start; background:#151a24; color:#c8d6e5; border:1px solid #2a3345; border-bottom-left-radius:4px; }}
    .msg-error {{ align-self:flex-start; background:#3a1b1b; color:#ef5350; border:1px solid #5a2a2a; }}
    .msg-meta {{ font-size:9px; color:#555; margin-top:4px; display:flex; gap:10px; flex-wrap:wrap; }}
    .msg-actions {{ margin-top:4px; display:flex; gap:6px; }}
    .msg-actions button {{ font-size:9px; background:transparent; color:#888; border:1px solid #333; border-radius:3px; padding:1px 6px; cursor:pointer; }}
    .msg-actions button:hover {{ color:#a8c7ff; border-color:#4477cc; }}
    .monitor-badge {{ font-size:8px; color:#ff9800; text-transform:uppercase; letter-spacing:0.5px; }}
    .input-bar {{ padding:10px 16px; border-top:1px solid #1a1f2a; display:flex; gap:8px; flex-shrink:0; background:#0b0d12; }}
    .input-bar input {{ flex:1; background:#151a24; color:#e8eef7; border:1px solid #2a3345; border-radius:8px; padding:10px 14px; font-size:14px; outline:none; }}
    .input-bar input:focus {{ border-color:#4477cc; }}
    .input-bar button {{ background:#1a3050; color:#a8c7ff; border:1px solid #4477cc; border-radius:8px; padding:10px 16px; font-size:13px; cursor:pointer; white-space:nowrap; }}
    .input-bar button:hover {{ background:#243050; }}
    .input-bar button.secondary {{ background:transparent; color:#888; border-color:#333; }}
    .empty-state {{ text-align:center; color:#444; padding:40px 16px; font-size:13px; }}
    @media (max-width:768px) {{
      .chat-container {{ height:100dvh; }} .chat-header h2 {{ font-size:14px; }}
      .quick-btn {{ font-size:10px; padding:4px 8px; }} .input-bar input {{ font-size:16px; }}
    }}
  </style>
</head>
<body>
<div class="chat-container">
  <div class="chat-header">
    <h2>💬 Chat Operator</h2>
    <div class="diag-bar">
      <span id="diag-backend" class="diag-ok">● backend</span>
      <span id="diag-tts" class="diag-fail">♪ tts</span>
      <span id="diag-latency"></span>
    </div>
  </div>
  <div class="quick-bar">
    {quick_btns}
  </div>
  <div class="messages" id="messages">
    <div class="empty-state">
      Tapez une commande ou cliquez un bouton rapide.<br>
      Ex: "Etat systeme", "Setup BTC", "Resume SPCX"
    </div>
  </div>
  <div class="input-bar">
    <input type="text" id="cmd-input" placeholder="Tapez une commande..." autocomplete="off"
           onkeydown="if(event.key==='Enter')sendCommand(this.value)">
    <button onclick="sendCommand(document.getElementById('cmd-input').value)">Envoyer</button>
    <button class="secondary" onclick="stopTTS()" title="Stop voix">⏹</button>
    <button class="secondary" onclick="clearChat()" title="Effacer">✕</button>
  </div>
</div>

<script>
const HIST_KEY = 'voice_chat_history';
let messages = [];
let lastOneLine = '';
let ttsReady = false;
let lastCmd = '';

// Init
try {{ messages = JSON.parse(localStorage.getItem(HIST_KEY) || '[]'); }} catch(e) {{}}
if ('speechSynthesis' in window) {{ ttsReady = true; document.getElementById('diag-tts').className = 'diag-ok'; }}
renderMessages();

async function sendCommand(cmd) {{
  cmd = (cmd || '').trim();
  if (!cmd) return;
  document.getElementById('cmd-input').value = '';
  lastCmd = cmd;

  addMessage('user', cmd);
  scrollDown();

  const start = Date.now();
  try {{
    const resp = await fetch('/voice/query?q=' + encodeURIComponent(cmd));
    const data = await resp.json();
    const lat = Date.now() - start;

    document.getElementById('diag-backend').className = 'diag-ok';
    document.getElementById('diag-latency').textContent = lat + 'ms';

    const intent = data.intent || '?';
    const endpoint = data.endpoint || '?';
    const oneLine = data.one_line || '(pas de reponse)';
    const source = data.source || '?';
    const rich = data.rich || {{}};
    lastOneLine = rich.spoken_text || oneLine;
    // Add freshness context to spoken text
    const freshSpoken = data.freshness ? data.freshness.spoken : '';
    if (freshSpoken && freshSpoken !== 'donnee live') {{
      lastOneLine = lastOneLine + '. ' + freshSpoken + '.';
    }}

    // Build rich card HTML
    let cardHTML = '';
    const cards = rich.cards || [];
    if (cards.length) {{
      cardHTML = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px">';
      cards.forEach(c => {{
        cardHTML += '<div style="background:#1a1f2a;border-radius:6px;padding:5px 8px;font-size:11px">' +
          '<div style="color:#666;font-size:9px">' + (c.label||'') + '</div>' +
          '<div style="color:#a8c7ff">' + (c.value||'') + '</div></div>';
      }});
      cardHTML += '</div>';
    }}

    // Badges
    let badgeHTML = '';
    const badges = rich.badges || [];
    // Always add freshness badge if present
    const freshness = data.freshness || {{}};
    if (freshness.badge) {{
      const fcss = freshness.css_class || 'freshness-unknown';
      badgeHTML += '<span style="font-size:8px;background:#1a2540;color:#aaa;border-radius:3px;padding:1px 5px">' + freshness.badge + '</span>';
    }}
    if (badges.length) {{
      badges.forEach(b => {{
        badgeHTML += '<span style="font-size:8px;background:#1a2540;color:#aaa;border-radius:3px;padding:1px 5px;margin-left:2px">' + b + '</span>';
      }});
    }}
    if (!badgeHTML) badgeHTML = '<span class="monitor-badge">MONITOR-ONLY</span>';

    let meta = badgeHTML || '<span class="monitor-badge">MONITOR-ONLY</span>';
    meta += ' <span>' + intent + '</span>';
    meta += ' <span style="font-family:monospace;font-size:9px">' + endpoint + '</span>';
    meta += ' <span>' + lat + 'ms</span>';
    if (source !== 'ok' && source !== 'healthy') meta += ' <span style="color:#ffa500">src:' + source + '</span>';

    let actions = '<button onclick="speakLast()">Lire</button>';
    if (data.ok === false) actions += '<button onclick="retryLastCmd()">Reessayer</button>';

    let messageHTML = oneLine;
    if (cardHTML) messageHTML += cardHTML;

    addMessage('bot', messageHTML, meta, actions, data.ok === false ? 'msg-error' : 'msg-bot', true);
    if (ttsReady) speak(lastOneLine);

  }} catch(e) {{
    document.getElementById('diag-backend').className = 'diag-fail';
    document.getElementById('diag-backend').textContent = 'backend FAIL';
    addMessage('bot', 'Erreur: ' + (e.name === 'TypeError' ? 'Backend inaccessible' : e.message),
               '<span>HTTP ERR</span>', '<button onclick="retryLastCmd()">Reessayer</button>', 'msg-error');
  }}
  scrollDown();
}}

function addMessage(role, text, meta, actions, cls, isHtml) {{
  const div = document.createElement('div');
  div.className = 'msg ' + (cls || (role === 'user' ? 'msg-user' : 'msg-bot'));
  const safeText = isHtml ? text : text.replace(/</g,'&lt;').replace(/>/g,'&gt;');
  div.innerHTML = '<div>' + safeText + '</div>' +
    (meta ? '<div class=\"msg-meta\">' + meta + '</div>' : '') +
    (actions ? '<div class=\"msg-actions\">' + actions + '</div>' : '');
  document.getElementById('messages').appendChild(div);

  messages.push({{ role, text, ts: Date.now() }});
  if (messages.length > 50) messages.shift();
  try {{ localStorage.setItem(HIST_KEY, JSON.stringify(messages)); }} catch(e) {{}}
  const es = document.querySelector('.empty-state');
  if (es) es.remove();
}}

function renderMessages() {{
  if (!messages.length) return;
  document.querySelector('.empty-state')?.remove();
  messages.forEach(m => {{
    const div = document.createElement('div');
    div.className = 'msg ' + (m.role === 'user' ? 'msg-user' : 'msg-bot');
    div.innerHTML = '<div>' + (m.text||'').replace(/</g,'&lt;') + '</div>';
    document.getElementById('messages').appendChild(div);
  }});
  scrollDown();
}}

function speak(text) {{
  if (!ttsReady) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'fr-FR';
  u.rate = 0.88;
  u.pitch = 0.95;
  window.speechSynthesis.speak(u);
}}

function speakLast() {{ if (lastOneLine) speak(lastOneLine); }}
function retryLastCmd() {{ if (lastCmd) sendCommand(lastCmd); }}
function stopTTS() {{ window.speechSynthesis.cancel(); }}
function clearChat() {{
  document.getElementById('messages').innerHTML = '<div class="empty-state">Historique efface.</div>';
  messages = [];
  try {{ localStorage.removeItem(HIST_KEY); }} catch(e) {{}}
}}
function scrollDown() {{
  const m = document.getElementById('messages');
  setTimeout(() => m.scrollTop = m.scrollHeight, 50);
}}
</script>
</body>
</html>"""




@app.get("/voice", response_class=HTMLResponse)
def voice_operator_html():
    return HTMLResponse(content=_voice_operator_html())


def _handle_composite(composite_type: str) -> dict:
    """Handle composite/trader commands that aggregate multiple /read/* endpoints."""
    from modules.voice_operator.engine.read_api_client import call
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat()
    rich = {"cards": [], "badges": ["MONITOR-ONLY", "COMPOSITE"], "spoken_text": ""}
    one_line = ""

    # Shared data fetches (lazy, only when needed)
    alerts = setups = spcx = open_trades = None

    def _get_alerts():
        nonlocal alerts
        if alerts is None: alerts = call("/read/alerts")
        return alerts

    def _get_setups():
        nonlocal setups
        if setups is None: setups = call("/read/setups")
        return setups

    def _get_spcx():
        nonlocal spcx
        if spcx is None: spcx = call("/read/spacex")
        return spcx

    def _get_open_trades():
        nonlocal open_trades
        if open_trades is None:
            from modules.voice_operator.api.readers.perf_reader import read_open_trades
            raw = read_open_trades()
            trades = raw.get("open", []) if isinstance(raw, dict) else []
            open_trades = [t for t in trades if t.get("symbol")]
        return open_trades  # always list

    def _get_analysis():
        nonlocal open_trades  # reuse variable
        from pathlib import Path as _Path
        import json as _json
        p = _Path(__file__).resolve().parents[3] / "data" / "deskpro" / "inputs" / "analysis_report" / "latest.json"
        if p.exists():
            try: return _json.loads(p.read_text())
            except: pass
        return {}

    if composite_type == "morning_brief":
        a = _get_alerts()
        s = _get_setups()
        crit = a.get("critical", 0) if isinstance(a, dict) else 0
        active = s.get("active", 0) if isinstance(s, dict) else 0
        a_plus = s.get("a_plus", 0) if isinstance(s, dict) else 0
        ot = _get_open_trades()
        perf_open = len(ot)
        # Deskpro analysis context
        ana = _get_analysis()
        regimes = ana.get("regimes", {}) if isinstance(ana, dict) else {}
        consensus = ana.get("class_consensus", {}) if isinstance(ana, dict) else {}
        signals = ana.get("actionable_signals", [])[:3] if isinstance(ana, dict) else []
        rich["cards"] = [
            {"label": "Setups actifs", "value": f"{active} setups ({a_plus} A+)"},
            {"label": "Trades ouverts", "value": str(perf_open)},
            {"label": "Alertes", "value": f"{crit} critiques"},
        ]
        if regimes:
            for k, v in list(regimes.items())[:3]:
                rich["cards"].append({"label": f"Regime {k}", "value": str(v)[:40]})
        if signals:
            for sig in signals[:2]:
                rich["cards"].append({"label": "Signal", "value": str(sig.get("symbol", sig.get("type", "?")))[:40]})
        rich["spoken_text"] = f"Briefing. {active} setups, {a_plus} A+. {perf_open} trades. {crit} alertes."
        one_line = f"📊 {active} setups | {a_plus} A+ | {perf_open} trades | {crit} alertes"

    elif composite_type == "market_view":
        sp = _get_spcx()
        ot = _get_open_trades()
        perf_trades = ot if isinstance(ot, list) else ot.get("open", [])
        cards = []
        # SPCX
        spx_price = sp.get("price") if isinstance(sp, dict) else None
        cards.append({"label": "SPCX", "value": f"${spx_price:.1f}" if spx_price and spx_price > 0 else "MARKET CLOSED"})
        # Vision analysis symbols (read from data_center views)
        from pathlib import Path
        import json as _json
        vision_dir = Path(__file__).resolve().parents[3] / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"
        vision_symbols = ["BTCUSDT.P", "ETHUSDT.P", "SOLUSDT.P", "OANDA:XAUUSD", "TVC:DXY", "SPY", "TVC:VIX"]
        for sym in vision_symbols:
            vf = vision_dir / f"{sym}.json"
            if vf.exists():
                try:
                    vd = _json.loads(vf.read_text())
                    fresh = vd.get("freshness_state", "") if isinstance(vd, dict) else ""
                    trend = vd.get("trend", vd.get("direction", "")) if isinstance(vd, dict) else ""
                    label = sym.replace("OANDA:", "").replace("TVC:", "").replace("BTCUSDT.P", "BTC").replace("ETHUSDT.P", "ETH").replace("SOLUSDT.P", "SOL")
                    val = f"{trend}" if trend else "Surveille"
                    if fresh == "fresh": val += " LIVE"
                    cards.append({"label": label, "value": val[:30]})
                except: pass
        # Perf trades
        for t in perf_trades[:2]:
            sym = t.get("symbol", "?")
            cards.append({"label": sym, "value": t.get("engine", "actif")})
        rich["cards"] = cards[:10]
        symbols = " · ".join(c["label"] for c in cards[:6])
        rich["spoken_text"] = f"Vue marche. {len(all_top)} symboles suivis. {symbols}."
        one_line = symbols

    elif composite_type == "whats_new":
        a = _get_alerts()
        s = _get_setups()
        n_alerts = a.get("total", 0) if isinstance(a, dict) else 0
        n_setups = s.get("active", 0) if isinstance(s, dict) else 0
        rich["cards"] = [
            {"label": "Alertes", "value": str(n_alerts)},
            {"label": "Setups actifs", "value": str(n_setups)},
        ]
        rich["spoken_text"] = f"Nouveautes. {n_alerts} alertes, {n_setups} setups."
        one_line = f"🆕 {n_alerts} alertes | {n_setups} setups"

    elif composite_type == "risks":
        ana = _get_analysis()
        alerts_list = ana.get("alerts", []) if isinstance(ana, dict) else []
        signals = ana.get("actionable_signals", []) if isinstance(ana, dict) else []
        squeeze = ana.get("squeeze_alert", {}) if isinstance(ana, dict) else {}
        cards = [{"label": "Alertes GPT", "value": str(len(alerts_list))}]
        for sig in signals[:3]:
            cards.append({"label": f"Signal {sig.get('symbol','?')}", "value": str(sig.get('type', sig.get('direction', '?')))[:40]})
        if squeeze:
            cards.append({"label": "Squeeze", "value": str(squeeze.get("status", squeeze.get("level", "?")))[:30]})
        rich["cards"] = cards[:7]
        rich["spoken_text"] = f"Risques. {len(alerts_list)} alertes analyse, {len(signals)} signaux."
        one_line = f"⚠️ {len(signals)} signaux | {len(alerts_list)} alertes"

    elif composite_type == "urgencies":
        a = _get_alerts()
        crit = a.get("critical", 0) if isinstance(a, dict) else 0
        items = a.get("items", []) if isinstance(a, dict) else []
        rich["cards"] = [{"label": "Alertes critiques", "value": str(crit)}]
        for item in items[:2]:
            if item.get("severity") == "critical":
                rich["cards"].append({"label": item.get("source", "?"), "value": item.get("message", "")[:60]})
        rich["spoken_text"] = f"Urgences. {crit} alertes critiques."
        one_line = f"🚨 {crit} alertes critiques"

    elif composite_type == "top_setups":
        s = _get_setups()
        ot = _get_open_trades()
        items = s.get("items", []) if isinstance(s, dict) else []
        perf_trades = ot if isinstance(ot, list) else ot.get("open", [])
        # Merge SPCX setups + perf trades
        all_items = list(items)
        for t in perf_trades[:3]:
            all_items.append({"symbol": t.get("symbol", "?"), "setup_type": t.get("engine", "?"), "grade": "ACTIVE", "source": "tv_webhook"})
        for item in all_items[:5]:
            rich["cards"].append({"label": item.get("symbol", "?"), "value": f"{item.get('setup_type', '?')} · grade {item.get('grade', '?')}"})
        rich["spoken_text"] = f"Top setups. {len(all_items)} actifs."
        one_line = f"🏆 {len(all_items)} actifs"

    elif composite_type == "a_plus_setups":
        s = _get_setups()
        items = s.get("items", []) if isinstance(s, dict) else []
        a_plus = [i for i in items if i.get("grade") == "A+"]
        for item in a_plus[:5]:
            rich["cards"].append({"label": f"A+ {item.get('symbol', '?')}", "value": item.get("setup_type", "?")})
        rich["spoken_text"] = f"Setups A+. {len(a_plus)} actifs."
        one_line = f"⭐ {len(a_plus)} A+"

    elif composite_type == "spcx_full":
        sp = _get_spcx()
        from pathlib import Path
        import json as _json
        cc_path = Path(__file__).resolve().parents[3] / "data" / "ipo" / "spacex" / "command_center" / "latest.json"
        cc = {}
        if cc_path.exists():
            try: cc = _json.loads(cc_path.read_text())
            except: pass
        cards = []
        for k, label in [
            ("price", "Prix"), ("gap_pct", "Gap IPO"), ("volume", "Volume"),
            ("vwap", "VWAP"), ("edge_score", "Edge Score"), ("action", "Action"),
            ("confidence", "Confiance"), ("top_setup", "Top Setup"),
            ("sector_regime", "Secteur"), ("market_state", "Marche"),
            ("sources_ok", "Sources"), ("pipeline_healthy", "Pipeline"),
            ("disagreement", "Disagreement"), ("rsi", "RSI"),
        ]:
            v = sp.get(k) if isinstance(sp, dict) and sp.get(k) is not None else cc.get(k)
            if v is not None:
                if isinstance(v, float):
                    v = f"{v:.1f}" if abs(v) < 100 else f"{v:.0f}"
                cards.append({"label": label, "value": str(v)[:40]})
        # From sp (voice operator enriched)
        for k, label in [("orderflow_score", "Orderflow"), ("ownership_pressure_score", "Ownership"),
                          ("source_quality", "Qualite"), ("vwap_state", "VWAP State")]:
            v = sp.get(k) if isinstance(sp, dict) else None
            if v is not None:
                cards.append({"label": label, "value": str(v)[:40]})
        # IPO analogs
        analogs = cc.get("ipo_analogs", [])[:2]
        for a in analogs:
            cards.append({"label": f"Analog {a.get('symbol','?')}", "value": f"{a.get('pct', a.get('probability_pct', '?'))}%"})
        rich["cards"] = cards[:15]
        rich["spoken_text"] = f"SPCX. Prix {cc.get(\"price\",\"?\")}. VWAP {cc.get(\"vwap\",\"?\")}. Edge score {cc.get(\"edge_score\",\"?\")}. Confiance {cc.get(\"confidence\",\"?\")}. Setup principal {cc.get(\"top_setup\",\"?\")}. Qualite source {sp.get(\"source_quality\",\"?\") if isinstance(sp, dict) else \"?\"}. Aucun signal d execution."
        one_line = f"🚀 SPCX {len(cards)} champs"

    elif composite_type == "spcx_risk":
        sp = _get_spcx()
        from pathlib import Path
        import json as _json
        cc_path = Path(__file__).resolve().parents[3] / "data" / "ipo" / "spacex" / "command_center" / "latest.json"
        cc = {}
        if cc_path.exists():
            try: cc = _json.loads(cc_path.read_text())
            except: pass
        ow = sp.get("ownership_pressure_score", "N/A") if isinstance(sp, dict) else "N/A"
        gap = sp.get("gap_ipo_pct") if isinstance(sp, dict) else cc.get("gap_pct")
        cards = [
            {"label": "Ownership pressure", "value": str(ow)},
            {"label": "Lockup", "value": "2026-12-09 (180j)"},
            {"label": "Insider concentration", "value": "41% / 77.8% vote"},
        ]
        if gap is not None: cards.append({"label": "Gap IPO", "value": f"{gap:+.1f}%" if isinstance(gap, (int, float)) else str(gap)})
        risks = cc.get("risks", [])
        for r in (risks or [])[:3]:
            if r and r != "None":
                cards.append({"label": "Risque", "value": str(r)[:60]})
        rich["cards"] = cards[:8]
        rich["spoken_text"] = f"Risques SPCX. Ownership pressure {ow}."
        one_line = f"⚠️ SPCX risk | Ownership {ow}"

    elif composite_type == "gold_full":
        ot = _get_open_trades()
        perf_trades = ot if isinstance(ot, list) else ot.get("open", [])
        xau_trades = [t for t in perf_trades if "XAU" in str(t.get("symbol", ""))]
        cards = [{"label": "Trades XAU actifs", "value": str(len(xau_trades))}]
        for t in xau_trades[:2]:
            cards.append({"label": t.get("engine", "Setup"), "value": f"Entry {t.get('entry','?')} SL {t.get('stop','?')}"})
        if not xau_trades:
            cards.extend([
                {"label": "Trend H4", "value": "BULLISH"},
                {"label": "Setup", "value": "GOLD_CFD_LONG"},
            ])
        rich["cards"] = cards[:5]
        rich["spoken_text"] = f"Gold. {len(xau_trades)} trades actifs."
        one_line = f"🥇 Gold | {len(xau_trades)} trades | H4 BULLISH"

    elif composite_type == "gold_danger":
        ot = _get_open_trades()
        perf_trades = ot if isinstance(ot, list) else ot.get("open", [])
        xau_trades = [t for t in perf_trades if "XAU" in str(t.get("symbol", ""))]
        cards = [{"label": "Trades XAU", "value": str(len(xau_trades))}]
        for t in xau_trades[:2]:
            cards.append({"label": "SL distance", "value": f"Entry {t.get('entry','?')}"})
        cards.append({"label": "Alertes Gold", "value": "0 critiques"})
        rich["cards"] = cards[:4]
        rich["spoken_text"] = "Gold danger. Verification des stops."
        one_line = f"⚠️ Gold | {len(xau_trades)} trades | Verifier stops"

    elif composite_type == "watchlist_ia":
        rich["cards"] = [
            {"label": "NVDA", "value": "Leader IA"},
            {"label": "PLTR", "value": "Defense/AI"},
            {"label": "ARM", "value": "Semi-conducteurs"},
        ]
        rich["spoken_text"] = "Watchlist IA. NVDA, PLTR, ARM."
        one_line = "🤖 NVDA | PLTR | ARM"

    elif composite_type == "watchlist_spatial":
        rich["cards"] = [
            {"label": "SPCX", "value": "IPO Leader"},
            {"label": "RKLB", "value": "Lanceur"},
            {"label": "ASTS", "value": "Satellite"},
            {"label": "LUNR", "value": "Lunaire"},
        ]
        rich["spoken_text"] = "Watchlist spatial. SPCX, RKLB, ASTS, LUNR."
        one_line = "🛰️ SPCX | RKLB | ASTS | LUNR"

    # ── Priority engine commands ──
    elif composite_type == "priorities":
        s = _get_setups()
        ana = _get_analysis()
        sp = _get_spcx() if isinstance(_get_spcx, type(lambda:0)) else {}
        items = s.get("items", []) if isinstance(s, dict) else []
        from modules.voice_operator.priority_engine import rank_items
        # Build items from all sources
        all_items = list(items)
        if isinstance(sp, dict) and sp.get("price"):
            all_items.append({"symbol": "SPCX", "setup_type": sp.get("top_setup", "?"), "edge_score": sp.get("edge_score", 0), "confidence": sp.get("confidence", 0), "_priority": 0})
        signals = ana.get("actionable_signals", []) if isinstance(ana, dict) else []
        for sig in signals[:3]:
            all_items.append({"symbol": sig.get("symbol", "?"), "setup_type": sig.get("type", "signal"), "confidence": 50})
        ranked = rank_items(all_items)
        for item in ranked[:5]:
            rich["cards"].append({"label": item.get("symbol", "?"), "value": f"{item.get('setup_type', '?')} · priorite {item.get('_priority', 0):.0f}"})
        rich["spoken_text"] = f"Priorites. {len(ranked)} items classes."
        one_line = f"📌 Top {min(3, len(ranked))}: " + " · ".join(i.get("symbol", "?") for i in ranked[:3])

    elif composite_type == "attention":
        s = _get_setups()
        ana = _get_analysis()
        sp = _get_spcx()
        items = s.get("items", []) if isinstance(s, dict) else []
        from modules.voice_operator.priority_engine import rank_attention
        all_items = list(items)
        if isinstance(sp, dict):
            all_items.append({"symbol": "SPCX", "source_quality": sp.get("source_quality", "unknown"), "freshness": "MARKET_CLOSED", "_priority": 30})
        alerts = ana.get("alerts", []) if isinstance(ana, dict) else []
        for a in alerts[:2]:
            all_items.append({"symbol": "ALERT", "setup_type": str(a)[:30], "_priority": 20})
        ranked = rank_attention(all_items)
        for item in ranked[:4]:
            rich["cards"].append({"label": "⚠️ " + str(item.get("symbol", "?")), "value": str(item.get("setup_type", item.get("freshness", "?")))[:40]})
        rich["spoken_text"] = f"Attention. {len(ranked)} points a surveiller."
        one_line = f"⚠️ {len(ranked)} points d'attention"

    elif composite_type == "whats_new":
        a = _get_alerts()
        s = _get_setups()
        n_alerts = a.get("total", 0) if isinstance(a, dict) else 0
        n_setups = s.get("active", 0) if isinstance(s, dict) else 0
        rich["cards"] = [
            {"label": "Alertes", "value": str(n_alerts)},
            {"label": "Setups actifs", "value": str(n_setups)},
        ]
        rich["spoken_text"] = f"Nouveautes. {n_alerts} alertes, {n_setups} setups."
        one_line = f"🆕 {n_alerts} alertes | {n_setups} setups"

    elif composite_type == "top_movers":
        from pathlib import Path as _P
        import json as _J
        vd = _P(__file__).resolve().parents[3] / "data" / "data_center" / "views" / "vision_analysis" / "by_symbol"
        movers = []
        for sym in ["BTCUSDT.P", "ETHUSDT.P", "SOLUSDT.P", "OANDA:XAUUSD", "SPY"]:
            vf = vd / f"{sym}.json"
            if vf.exists():
                try:
                    d = _J.loads(vf.read_text())
                    if isinstance(d, dict):
                        movers.append({"symbol": sym.replace("BTCUSDT.P","BTC").replace("ETHUSDT.P","ETH").replace("SOLUSDT.P","SOL").replace("OANDA:",""),
                                       "trend": d.get("trend", d.get("direction", "?")),
                                       "confidence": d.get("confidence", 50)})
                except: pass
        from modules.voice_operator.priority_engine import rank_items
        ranked = rank_items(movers)
        for m in ranked[:5]:
            rich["cards"].append({"label": m["symbol"], "value": f"{m.get('trend','?')} · {m.get('_priority',0):.0f}"})
        rich["spoken_text"] = f"Top movers. {len(ranked)} actifs."
        one_line = f"📈 " + " · ".join(m["symbol"] for m in ranked[:4])

    elif composite_type == "exec_summary":
        a = _get_alerts()
        s = _get_setups()
        sp = _get_spcx()
        ana = _get_analysis()
        crit = a.get("critical", 0) if isinstance(a, dict) else 0
        active = s.get("active", 0) if isinstance(s, dict) else 0
        signals = ana.get("actionable_signals", []) if isinstance(ana, dict) else []
        spx_setup = sp.get("top_setup", "NONE") if isinstance(sp, dict) else "?"
        parts = [f"{active} setups actifs"]
        if crit: parts.append(f"{crit} alertes critiques")
        parts.append(f"SPCX setup {spx_setup}")
        if signals: parts.append(f"{len(signals)} signaux analyse")
        rich["cards"] = [
            {"label": "Setups", "value": str(active)},
            {"label": "Alertes critiques", "value": str(crit)},
            {"label": "SPCX", "value": str(spx_setup)},
            {"label": "Signaux GPT", "value": str(len(signals))},
        ]
        spoken = ". ".join(parts) + ". "
        if crit: spoken += "Attention, alertes critiques. "
        rich["spoken_text"] = spoken
        one_line = " · ".join(parts)

    else:
        one_line = "Commande composite inconnue"
        rich["spoken_text"] = one_line

    return {"one_line": one_line, "rich": rich, "generated_at": now}


@app.get("/voice/query")
def voice_operator_query(q: str = ""):
    """Route a voice command through intent_router → /read/* → enriched response."""
    import time as _time
    _start = _time.time()

    if not q:
        return JSONResponse(content={"intent": "unknown", "endpoint": "", "one_line": "Aucune commande", "ok": False})

    try:
        from modules.voice_operator.engine.intent_router import route
        from modules.voice_operator.engine.read_api_client import call

        routed = route(q)
        # Handle composite/trader commands
        if routed.endpoint == "/read/composite":
            result = _handle_composite(routed.params.get("type", ""))
            latency_ms = int((_time.time() - _start) * 1000)
            # Add freshness to composite results
            from modules.voice_operator.models.freshness import classify_freshness
            price_val = None
            if result.get("one_line") and "$" in result["one_line"]:
                try:
                    import re
                    m = re.search(r'\$([0-9.]+)', result["one_line"])
                    if m: price_val = float(m.group(1))
                except: pass
            freshness = classify_freshness(price=price_val if price_val and price_val > 0 else None,
                                           source_quality="composite", source="composite")
            return JSONResponse(content={
                "intent": routed.intent,
                "endpoint": routed.endpoint,
                "params": routed.params,
                "one_line": result["one_line"],
                "source": "composite",
                "ok": True,
                "generated_at": result.get("generated_at", ""),
                "latency_ms": latency_ms,
                "mode": "monitor_only",
                "rich": result.get("rich", {}),
                "freshness": {
                    "state": freshness["freshness_state"],
                    "badge": freshness["badge"],
                    "css_class": freshness["css_class"],
                    "spoken": freshness["spoken"],
                    "warning": freshness["warning"],
                },
            })

        result = call(routed.endpoint, routed.params if routed.params else None)

        result = call(routed.endpoint, routed.params if routed.params else None)
        latency_ms = int((_time.time() - _start) * 1000)

        # --- Freshness classification ---
        from modules.voice_operator.models.freshness import classify_freshness, compute_age_minutes
        price_val = result.get("price") if isinstance(result, dict) else None
        freshness = classify_freshness(
            price=price_val,
            source_quality=result.get("source_quality") if isinstance(result, dict) else None,
            source=result.get("source") if isinstance(result, dict) else None,
            data_age_minutes=compute_age_minutes(result.get("generated_at") if isinstance(result, dict) else None),
            pipeline_state=result.get("pipeline_state") if isinstance(result, dict) else None,
        )

        # Extract one_line properly — handle both string and dict results
        raw_one_line = result.get("one_line", "")
        if isinstance(raw_one_line, dict):
            raw_one_line = raw_one_line.get("one_line", raw_one_line.get("summary", str(raw_one_line)))
        if not raw_one_line or not isinstance(raw_one_line, str) or raw_one_line.startswith("{"):
            # Extract from nested data
            items = result.get("items", [])
            if items and isinstance(items, list) and len(items) > 0:
                item = items[0]
                raw_one_line = item.get("one_line", item.get("summary", ""))
            if not raw_one_line or (isinstance(raw_one_line, str) and raw_one_line.startswith("{")):
                raw_one_line = result.get("summary", result.get("one_line", ""))
            # Last resort: build from known fields
            if not raw_one_line or (isinstance(raw_one_line, str) and raw_one_line.startswith("{")):
                sym = result.get("symbol", "")
                setup = result.get("setup_type", "")
                direction = result.get("direction", "")
                raw_one_line = f"{sym} {setup} {direction}".strip() or "Donnees disponibles"

        # Analytics
        try:
            from modules.voice_operator.analytics.collector import log_command, log_response
            log_command(q, routed.intent, routed.endpoint)
            log_response(routed.intent, latency_ms, result.get("ok", True), result.get("source_quality", result.get("pipeline_state", "ok")))
        except Exception:
            pass

        # Build rich cards from result data
        rich = _build_rich_response(result, routed.intent)

        return JSONResponse(content={
            "intent": routed.intent,
            "endpoint": routed.endpoint,
            "params": routed.params,
            "one_line": raw_one_line if isinstance(raw_one_line, str) else str(raw_one_line),
            "source": result.get("source_quality", result.get("pipeline_state", result.get("source", "ok"))),
            "ok": result.get("ok", True),
            "generated_at": result.get("generated_at", ""),
            "confidence": result.get("confidence"),
            "source_quality": result.get("source_quality"),
            "pipeline_state": result.get("pipeline_state"),
            "latency_ms": latency_ms,
            "mode": "monitor_only",
            "rich": rich,
            "freshness": {
                "state": freshness["freshness_state"],
                "badge": freshness["badge"],
                "css_class": freshness["css_class"],
                "spoken": freshness["spoken"],
                "warning": freshness["warning"],
            },
        })
    except Exception as e:
        try:
            from modules.voice_operator.analytics.collector import log_error
            log_error("error", str(e)[:200])
        except Exception:
            pass
        return JSONResponse(content={
            "intent": "error",
            "endpoint": "",
            "one_line": f"Erreur voix: {str(e)[:200]}",
            "source": "down",
            "ok": False,
            "mode": "monitor_only",
        })


def _build_rich_response(result: dict, intent: str) -> dict:
    """Build rich display cards from /read/* response data.
    Extracts available fields without computing anything new.
    """
    cards = []
    badges = ["MONITOR-ONLY", "READ-ONLY"]
    spoken = ""

    # System status
    if intent == "system_status":
        badges.append("DeskPro")
        svc = result.get("services_running", result.get("services", []))
        if isinstance(svc, int):
            cards.append({"label": "Services", "value": str(svc)})
        crit = result.get("critical_alerts", 0)
        cards.append({"label": "Alertes critiques", "value": str(crit)})
        ps = result.get("pipeline_state", result.get("status", "?"))
        cards.append({"label": "Pipeline", "value": str(ps)})
        spoken = result.get("one_line", f"Systeme: {svc} services, {crit} alertes critiques")

    # SPCX summary
    elif intent == "spcx_summary":
        badges.append("SPCX")
        for k, label in [("price", "Prix"), ("vwap_state", "VWAP"), ("trade_ready", "Trade Ready"),
                          ("orderflow_score", "Orderflow"), ("source_quality", "Qualite source")]:
            v = result.get(k)
            if v is not None:
                cards.append({"label": label, "value": str(v)})
        spoken = result.get("summary", result.get("one_line", "SPCX: donnees disponibles"))

    # Setup detail
    elif intent in ("setup_detail", "setups_all"):
        badges.append("DeskPro")
        # Handle nested setup data in items list
        items = result.get("items", [])
        if items:
            item = items[0]
        else:
            item = result
        for k, label in [("symbol", "Symbole"), ("setup_type", "Setup"), ("direction", "Direction"),
                          ("grade", "Grade"), ("entry_zone", "Entree"), ("invalidation", "Inval"),
                          ("target_1", "TP1"), ("trade_ready", "Score"), ("source", "Source")]:
            v = item.get(k)
            if v is not None:
                cards.append({"label": label, "value": str(v)})
        spoken = result.get("one_line", f"Setup: {item.get('setup_type', '?')} {item.get('direction', '')}")

    # Score detail
    elif intent == "score_detail":
        badges.append("DeskPro")
        for k, label in [("trade_ready", "Trade Ready"), ("vwap_score", "VWAP"), ("orderflow_score", "Orderflow"),
                          ("momentum", "Momentum"), ("risk", "Risque"), ("smart_money", "Smart Money")]:
            v = result.get(k)
            if v is not None:
                cards.append({"label": label, "value": str(v)})
        spoken = result.get("one_line", "Scores disponibles")

    # Market / Report
    elif intent in ("market", "report"):
        badges.append("DeskPro")
        spoken = result.get("one_line", "Rapport marche disponible")

    # Alerts
    elif intent in ("alerts", "alerts_critical"):
        badges.append("DeskPro")
        total = result.get("total", len(result.get("items", [])))
        crit = result.get("critical", 0)
        cards.append({"label": "Total", "value": str(total)})
        cards.append({"label": "Critiques", "value": str(crit)})
        spoken = result.get("one_line", f"{total} alertes")

    spoken = spoken if spoken else result.get("one_line", "Reponse disponible")
    return {"cards": cards, "badges": badges, "spoken_text": spoken}


@app.get("/voice/analytics", response_class=HTMLResponse)
def voice_analytics_html():
    """Voice Operator usage analytics dashboard."""
    from modules.voice_operator.analytics.aggregator import compute_stats

    stats_all = compute_stats(days=0)
    stats_7d = compute_stats(days=7)
    stats_1d = compute_stats(days=1)

    def _render_stats(s, label):
        cmds = "".join(
            f'<tr><td>{c["command"]}</td><td class="num">{c["count"]}</td></tr>'
            for c in s.get("top_commands", [])[:5]
        ) or '<tr><td colspan="2">Aucune donnee</td></tr>'

        l = s.get("latency", {})
        source_rows = ""
        for src, h in s.get("source_health", {}).items():
            cls = "source-ok" if h["errors"] == 0 else "source-down"
            source_rows += f'<tr><td><span class="source-badge {cls}">{src.upper()}</span></td><td class="num">{h["responses"]}</td><td class="num">{h["errors"]}</td></tr>'

        return f"""\
<div class="stat-block">
<h4>{label}</h4>
<div class="summary-bar">
  <div class="summary-card"><div class="num">{s['total_commands']}</div><div class="label">Commandes</div></div>
  <div class="summary-card"><div class="num">{s['error_rate_pct']}%</div><div class="label">Erreurs</div></div>
  <div class="summary-card"><div class="num">{s['tts_ratio_pct']}%</div><div class="label">TTS</div></div>
  <div class="summary-card"><div class="num">{l.get('avg_ms',0)}ms</div><div class="label">Lat. moy</div></div>
  <div class="summary-card"><div class="num">{l.get('p95_ms',0)}ms</div><div class="label">Lat. p95</div></div>
</div>
<table>
  <thead><tr><th colspan="2">Top commandes</th></tr></thead>
  <tbody>{cmds}</tbody>
</table>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Voice Analytics</title>
  <style>
    {STANDARD_CSS}
    .stat-block {{ margin-bottom: 28px; }}
    .stat-block h4 {{ color: #a8c7ff; margin-bottom: 10px; font-size: 15px; }}
    table {{ width: auto; }}
    th, td {{ padding: 6px 12px; font-size: 12px; }}
    .num {{ text-align: right; font-family: monospace; }}
    .source-badge {{ display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px; }}
    .source-ok {{ background:#1b3a1b;color:#30d158; }}
    .source-down {{ background:#3a1b1b;color:#ef5350; }}
    .refresh-note {{ font-size:10px;color:#555;margin-top:24px; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Voice Operator</div>
      <a class="nav-item" href="/voice">🎙️ Voice Operator</a>
      <a class="nav-item nav-active" href="/voice/analytics">📊 Analytics</a>
    </div>
    <a class="nav-item" href="/">🏠 Dashboard</a>
    <a class="nav-item" href="/spacex">🚀 SpaceX</a>
    <a class="nav-item" href="/signals">📡 Signals</a>
    <a class="nav-item" href="/journal">📋 Journal</a>
    <a class="nav-item" href="/metrics">📊 Metrics</a>
  </nav>
  <main class="main">
    <h2>📊 Voice Operator Analytics</h2>
    <p class="subtitle">Usage reel — aucune telemetrie externe</p>

    {_render_stats(stats_1d, "Aujourd'hui")}
    {_render_stats(stats_7d, "7 jours")}
    {_render_stats(stats_all, "Total")}

    <div class="refresh-note">Auto-refresh: 60s. Evenements stockes dans data/logs/voice_events.jsonl</div>
  </main>
</div>
<script>setTimeout(() => location.reload(), 60000);</script>
</body>
</html>"""
