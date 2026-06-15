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


STATUS_BADGES = SHARED_STATUS_BADGES


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
    # Profile tabs
    profile_tabs = ""
    for pid, p in _VOICE_PROFILES.items():
        active = " profile-active" if pid == _VOICE_ACTIVE_PROFILE else ""
        profile_tabs += f'<button class="profile-tab{active}" onclick="switchProfile(\'{pid}\')">{p["icon"]} {p["label"]}</button>'

    # Preset bar
    preset_buttons = ""
    for label, commands in _VOICE_PRESETS:
        cmd_json = "[" + ",".join(f"'{c}'" for c in commands) + "]"
        preset_buttons += f'<button class="preset-btn" onclick="runPreset({cmd_json})" title="Batch: {", ".join(commands)}">{label}</button>'

    sections_html = ""
    for section in _VOICE_SECTIONS:
        buttons = ""
        for label, command in section["commands"]:
            sec = section["title"]
            buttons += f'<button class="voice-btn" data-section="{sec}" onclick="voiceQuery(\'{command}\')" title="{command}">{label}</button>\n'
        sections_html += f"""\
<div class="voice-section" data-section="{section['title']}">
  <h3>{section['icon']} {section['title']}</h3>
  <div class="voice-buttons">{buttons}</div>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>LocalCMS — Voice Operator</title>
  <style>
    {STANDARD_CSS}
    .voice-section {{ margin-bottom: 20px; }}
    .voice-section h3 {{ color: #a8c7ff; margin-bottom: 8px; font-size: 14px; }}
    .voice-buttons {{ display: flex; flex-wrap: wrap; gap: 6px; }}
    .voice-btn {{
      background: var(--card-bg, #151a24);
      color: var(--text, #e8eef7);
      border: 1px solid var(--card-border, #2a3345);
      border-radius: var(--card-radius, 10px);
      padding: 8px 14px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.15s;
      white-space: nowrap;
      position: relative;
    }}
    .voice-btn:hover {{ background: #1e2840; border-color: #4477cc; }}
    .voice-btn:active {{ background: #243050; }}
    .voice-btn.loading {{ opacity: 0.5; pointer-events: none; }}
    .voice-btn .star {{ position:absolute;top:2px;right:3px;font-size:9px;opacity:0;transition:opacity 0.15s;color:#ffd700; }}
    .voice-btn:hover .star {{ opacity:0.4; }}
    .voice-btn.fav .star {{ opacity:1; }}
    .voice-btn.fav {{ border-color:#665500; }}
    .voice-section.hidden {{ display:none; }}

    /* Profile tabs */
    .profile-bar {{ display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px; }}
    .profile-tab {{
      background:var(--card-bg,#151a24);color:#888;border:1px solid var(--card-border,#2a3345);
      border-radius:8px;padding:6px 12px;font-size:11px;cursor:pointer;transition:all 0.15s;
    }}
    .profile-tab:hover {{ color:#a8c7ff;border-color:#4477cc; }}
    .profile-tab.profile-active {{ background:#1a2540;color:#a8c7ff;border-color:#4477cc; }}

    /* Preset bar */
    .preset-bar {{ display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px; }}
    .preset-btn {{
      background:linear-gradient(135deg,#1a2540,#151a24);color:#a8c7ff;border:1px solid #334466;
      border-radius:8px;padding:7px 14px;font-size:12px;cursor:pointer;transition:all 0.15s;
    }}
    .preset-btn:hover {{ background:#243050;border-color:#4477cc; }}

    /* Console */
    .console-bar {{ display:flex;gap:8px;margin-bottom:12px;align-items:center; }}
    .console-input {{
      flex:1;background:var(--card-bg,#151a24);color:var(--text,#e8eef7);
      border:1px solid var(--card-border,#2a3345);border-radius:8px;padding:8px 12px;
      font-size:13px;font-family:inherit;outline:none;
    }}
    .console-input:focus {{ border-color:#4477cc; }}
    .console-send {{
      background:#1a3050;color:#a8c7ff;border:1px solid #4477cc;
      border-radius:8px;padding:8px 16px;font-size:12px;cursor:pointer;white-space:nowrap;
    }}
    .console-send:hover {{ background:#243050; }}
    .console-clear {{
      background:transparent;color:#888;border:1px solid #333;
      border-radius:8px;padding:8px 12px;font-size:11px;cursor:pointer;
    }}

    /* Suggestions */
    .suggestions {{ display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;min-height:0; }}
    .suggestion {{ font-size:10px;color:#555;cursor:pointer;padding:2px 6px;border-radius:4px; }}
    .suggestion:hover {{ color:#a8c7ff;background:#1a1f2a; }}

    /* Favorites */
    .favorites-section {{
      margin-bottom:20px;padding:12px;background:var(--card-bg,#151a24);
      border:1px solid #665500;border-radius:var(--card-radius,10px);display:none;
    }}
    .favorites-section.has-favs {{ display:block; }}
    .favorites-section h3 {{ color:#ffd700;margin-bottom:8px;font-size:13px; }}
    .empty-fav {{ color:#555;font-size:11px;font-style:italic; }}

    /* Response */
    .response-area {{
      margin-top:16px;padding:14px;background:var(--card-bg,#151a24);
      border:1px solid var(--card-border,#2a3345);border-radius:var(--card-radius,10px);
      min-height:50px;display:none;
    }}
    .response-area.visible {{ display:block; }}
    .response-meta {{ display:flex;gap:16px;font-size:10px;color:#555;margin-bottom:6px;flex-wrap:wrap; }}
    .response-meta span {{ white-space:nowrap; }}
    .source-badge {{ display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px; }}
    .source-ok {{ background:#1b3a1b;color:#30d158; }}
    .source-stale {{ background:#3a301b;color:#ffa500; }}
    .source-down {{ background:#3a1b1b;color:#ef5350; }}
    .response-intent {{ font-size:11px;color:#666;margin-bottom:2px; }}
    .response-endpoint {{ font-size:10px;color:#444;margin-bottom:8px;font-family:monospace; }}
    .response-text {{ font-size:14px;color:#e8eef7;line-height:1.5; }}
    .response-detail {{ font-size:11px;color:#777;margin-top:8px;line-height:1.4; }}
    .response-mode {{ font-size:9px;color:#ff9800;margin-top:8px;text-transform:uppercase;letter-spacing:1px; }}
    .response-actions {{ margin-top:8px;display:flex;gap:6px; }}
    .resp-retry,.resp-replay {{ font-size:10px;color:#888;background:transparent;border:1px solid #333;border-radius:4px;padding:2px 8px;cursor:pointer; }}
    .resp-retry:hover,.resp-replay:hover {{ color:#a8c7ff;border-color:#4477cc; }}

    /* History */
    .history-area {{ margin-top:20px; }}
    .history-area h3 {{ color:#a8c7ff;font-size:13px;margin-bottom:6px; }}
    .history-item {{ font-size:11px;color:#777;padding:3px 0;border-bottom:1px solid #1a1f2a;cursor:pointer; }}
    .history-item:hover {{ color:#a8c7ff; }}
    .history-time {{ color:#444;margin-right:6px; }}
    .status-bar {{ display:flex;align-items:center;gap:12px;margin-bottom:14px;font-size:11px;color:#888;flex-wrap:wrap; }}
    .tts-indicator {{ display:inline-block;padding:2px 8px;border-radius:4px;font-size:9px; }}
    .tts-active {{ background:#1b3a1b;color:#30d158; }}
    .tts-inactive {{ background:#3a1b1b;color:#ef5350; }}
    .latency {{ font-family:monospace;font-size:10px;color:#555; }}
  </style>
</head>
<body>
<div class="layout">
  <nav class="sidebar">
    <h1>LocalCMS<small>Central UI — opt-trading</small></h1>
    <div style="margin-bottom:16px">
      <div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">Voice Operator</div>
      <a class="nav-item nav-active" href="/voice">🎙️ Voice Operator</a>
    </div>
    <a class="nav-item" href="/">🏠 Dashboard</a>
    <a class="nav-item" href="/spacex">🚀 SpaceX</a>
    <a class="nav-item" href="/signals">📡 Signals</a>
    <a class="nav-item" href="/journal">📋 Journal</a>
    <a class="nav-item" href="/metrics">📊 Metrics</a>
    <div style="margin-top:auto;padding-top:16px;border-top:1px solid #333;font-size:11px;color:#666;margin-left:10px">
      <div><a href="/voice/query?q=Etat+systeme" style="color:#888;text-decoration:none">/voice/query</a></div>
    </div>
  </nav>
  <main class="main">
    <h2>🎙️ Voice Operator</h2>
    <p class="subtitle">Monitor-Only — Validation humaine obligatoire</p>

    <div class="status-bar">
      <span>TTS: <span id="tts-status" class="tts-indicator tts-inactive">inactif</span></span>
      <span id="last-query" style="color:#555"></span>
      <span class="latency" id="latency-display"></span>
      <span style="margin-left:auto;font-size:10px;color:#555">⭐ = clic droit pour favori</span>
    </div>

    <!-- Profile tabs -->
    <div class="profile-bar">{profile_tabs}</div>

    <!-- Presets -->
    <div class="preset-bar">{preset_buttons}</div>

    <!-- Console -->
    <div class="console-bar">
      <input type="text" class="console-input" id="console-input" placeholder="Tapez une commande (ex: Etat systeme, Setup BTC)..." autocomplete="off"
             onkeydown="if(event.key==='Enter')voiceQuery(this.value);if(event.key==='Escape')this.value=''">
      <button class="console-send" onclick="voiceQuery(document.getElementById('console-input').value)">Envoyer</button>
      <button class="console-clear" onclick="clearConsole()">✕</button>
    </div>
    <div class="suggestions" id="suggestions"></div>

    <!-- Favorites -->
    <div id="favorites" class="favorites-section">
      <h3>⭐ Favoris</h3>
      <div class="voice-buttons" id="fav-buttons"></div>
      <div class="empty-fav" id="fav-empty">Clic droit sur un bouton pour l'ajouter aux favoris.</div>
    </div>

    {sections_html}

    <div id="response" class="response-area">
      <div class="response-intent" id="resp-intent"></div>
      <div class="response-endpoint" id="resp-endpoint"></div>
      <div class="response-meta">
        <span class="source-badge" id="resp-source"></span>
        <span id="resp-latency"></span>
        <span id="resp-ts"></span>
      </div>
      <div class="response-text" id="resp-text"></div>
      <div class="response-detail" id="resp-detail"></div>
      <div class="response-mode">MONITOR-ONLY — VALIDATION HUMAINE REQUISE</div>
      <div class="response-actions">
        <button class="resp-replay" onclick="replayLast()">🔊 Rejouer</button>
        <button class="resp-retry" id="resp-retry" style="display:none" onclick="retryLast()">🔄 Reessayer</button>
      </div>
    </div>

    <div class="history-area" id="history-area" style="display:none">
      <h3>📜 Historique</h3>
      <div id="history-list"></div>
    </div>
  </main>
</div>

<script>
const HISTORY_KEY = 'voice_operator_history';
const FAV_KEY = 'voice_operator_favorites';
const CACHE_KEY = 'voice_operator_cache';
let history = [];
let favorites = [];
let lastQuery = null;
let lastResponse = null;

try {{
    const stored = localStorage.getItem(HISTORY_KEY);
    if (stored) history = JSON.parse(stored);
    if (history.length > 0) renderHistory();
}} catch(e) {{}}

try {{
    const stored = localStorage.getItem(FAV_KEY);
    if (stored) favorites = JSON.parse(stored);
    renderFavorites();
    markFavButtons();
}} catch(e) {{}}

if ('speechSynthesis' in window) {{
    document.getElementById('tts-status').className = 'tts-indicator tts-active';
    document.getElementById('tts-status').textContent = 'actif';
}} else {{
    document.getElementById('tts-status').textContent = 'indisponible';
}}

// ── Suggestions ──
const ALL_COMMANDS = [];
document.querySelectorAll('.voice-btn').forEach(b => {{
    const cmd = b.getAttribute('title') || '';
    if (cmd && !ALL_COMMANDS.includes(cmd)) ALL_COMMANDS.push(cmd);
}});

document.getElementById('console-input').addEventListener('input', function() {{
    const val = this.value.trim().toLowerCase();
    const sug = document.getElementById('suggestions');
    if (!val || val.length < 2) {{ sug.innerHTML = ''; return; }}
    const matches = ALL_COMMANDS.filter(c => c.toLowerCase().includes(val)).slice(0, 6);
    sug.innerHTML = matches.map(c =>
        '<span class="suggestion" onclick="voiceQuery(\'' + c.replace(/'/g,"\\\\'") + '\')">' + c + '</span>'
    ).join('');
}});

function clearConsole() {{
    document.getElementById('console-input').value = '';
    document.getElementById('suggestions').innerHTML = '';
}}

// ── Profile switching ──
function switchProfile(pid) {{
    const p = {json.dumps({k: list(v["sections"]) for k,v in _VOICE_PROFILES.items()})};
    const sections = p[pid] || [];
    document.querySelectorAll('.voice-section').forEach(s => {{
        s.classList.toggle('hidden', sections.length > 0 && !sections.includes(s.dataset.section));
    }});
    document.querySelectorAll('.profile-tab').forEach(t => t.classList.remove('profile-active'));
    const tab = Array.from(document.querySelectorAll('.profile-tab')).find(t => t.textContent.includes(pid));
    if (tab) tab.classList.add('profile-active');
    localStorage.setItem('voice_profile', pid);
}}

// Restore profile
const savedProfile = localStorage.getItem('voice_profile') || 'default';
if (savedProfile !== 'default') switchProfile(savedProfile);

// ── Presets ──
async function runPreset(commands) {{
    for (const cmd of commands) {{
        await voiceQuery(cmd);
    }}
}}

// ── Main query ──
let activeRequests = 0;

async function voiceQuery(command, retryCount) {{
    if (!command) return;
    command = command.trim();
    if (!command || command === 'undefined') return;

    const btns = document.querySelectorAll('.voice-btn');
    btns.forEach(b => b.classList.add('loading'));
    document.getElementById('console-input').value = '';

    const startTime = Date.now();
    document.getElementById('last-query').textContent = '⏳ ' + command;
    activeRequests++;

    try {{
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000);
        const resp = await fetch('/voice/query?q=' + encodeURIComponent(command), {{ signal: controller.signal }});
        clearTimeout(timeout);
        const data = await resp.json();
        const latency = Date.now() - startTime;

        lastQuery = command;
        lastResponse = data;

        const responseEl = document.getElementById('response');
        responseEl.classList.add('visible');
        document.getElementById('resp-intent').textContent = 'Intent: ' + (data.intent || '?');
        document.getElementById('resp-endpoint').textContent = 'Endpoint: ' + (data.endpoint || '?') + (data.params && Object.keys(data.params).length ? ' ' + JSON.stringify(data.params) : '');
        document.getElementById('resp-text').textContent = data.one_line || '(pas de reponse)';
        document.getElementById('resp-latency').textContent = latency + 'ms';

        // Source badge
        const srcBadge = document.getElementById('resp-source');
        const src = data.source || (data.ok === false ? 'down' : 'ok');
        srcBadge.className = 'source-badge ' + (src === 'down' ? 'source-down' : src === 'stale' ? 'source-stale' : 'source-ok');
        srcBadge.textContent = src.toUpperCase();
        srcBadge.style.display = 'inline-block';

        // Timestamp
        document.getElementById('resp-ts').textContent = data.generated_at ? data.generated_at.substr(11,8) : '';

        // Details
        const details = [];
        if (data.confidence !== undefined) details.push('Confiance: ' + data.confidence + '%');
        if (data.source_quality) details.push('Qualite: ' + data.source_quality);
        if (data.pipeline_state) details.push('Pipeline: ' + data.pipeline_state);
        document.getElementById('resp-detail').textContent = details.join(' · ');

        // Retry button
        document.getElementById('resp-retry').style.display = (data.ok === false || data.source === 'down') ? 'inline-block' : 'none';

        // Cache valid result
        if (data.ok !== false && data.one_line) {{
            const cache = {{}};
            try {{ cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{{}}'); }} catch(e) {{}}
            cache[data.intent || command] = {{ ts: Date.now(), one_line: data.one_line }};
            localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
        }}

        // History
        history.unshift({{ ts: new Date().toISOString(), command: command, intent: data.intent, one_line: data.one_line, latency: latency }});
        if (history.length > 50) history.length = 50;
        localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
        renderHistory();

        // TTS
        if (document.getElementById('tts-status').classList.contains('tts-active') && data.one_line) {{
            speak(data.one_line);
        }}

        document.getElementById('last-query').textContent = '✓ ' + command;
    }} catch(e) {{
        const latency = Date.now() - startTime;
        document.getElementById('resp-text').textContent = 'Erreur: ' + (e.name === 'AbortError' ? 'Timeout (15s)' : e.message);
        document.getElementById('response').classList.add('visible');
        document.getElementById('resp-latency').textContent = latency + 'ms';
        document.getElementById('resp-source').className = 'source-badge source-down';
        document.getElementById('resp-source').textContent = 'DOWN';
        document.getElementById('resp-retry').style.display = 'inline-block';
        document.getElementById('last-query').textContent = '✗ ' + command;
    }}

    activeRequests--;
    btns.forEach(b => b.classList.remove('loading'));
}}

function retryLast() {{
    if (lastQuery) voiceQuery(lastQuery, true);
}}

function replayLast() {{
    if (lastResponse && lastResponse.one_line && document.getElementById('tts-status').classList.contains('tts-active')) {{
        speak(lastResponse.one_line);
    }}
}}

function speak(text) {{
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'fr-FR'; u.rate = 1.1; u.pitch = 1.0;
    window.speechSynthesis.speak(u);
}}

// ── Favorites ──
function toggleFavorite(command, label) {{
    const idx = favorites.findIndex(f => f.command === command);
    if (idx >= 0) {{ favorites.splice(idx, 1); }}
    else {{ favorites.push({{ command: command, label: label }}); if (favorites.length > 10) favorites.shift(); }}
    localStorage.setItem(FAV_KEY, JSON.stringify(favorites));
    renderFavorites(); markFavButtons();
}}

function renderFavorites() {{
    const section = document.getElementById('favorites');
    const buttons = document.getElementById('fav-buttons');
    const empty = document.getElementById('fav-empty');
    if (favorites.length === 0) {{ section.classList.remove('has-favs'); empty.style.display = 'block'; return; }}
    section.classList.add('has-favs'); empty.style.display = 'none';
    buttons.innerHTML = favorites.map(f =>
        '<button class="voice-btn fav" onclick="voiceQuery(\'' + f.command.replace(/'/g,"\\\\'") + '\')" oncontextmenu="toggleFavorite(\'' + f.command.replace(/'/g,"\\\\'") + '\',\'' + (f.label||f.command).replace(/'/g,"\\\\'") + '\');return false" title="Clic: executer | Clic droit: retirer">' +
        '<span class="star">⭐</span>' + (f.label||f.command) + '</button>'
    ).join('');
}}

function markFavButtons() {{
    document.querySelectorAll('.voice-btn:not(.fav)').forEach(btn => {{
        const cmd = btn.getAttribute('onclick') || '';
        const match = cmd.match(/voiceQuery\\('(.+?)'\\)/);
        if (match && favorites.some(f => f.command === match[1])) {{
            btn.classList.add('fav');
            if (!btn.querySelector('.star')) {{ const s = document.createElement('span'); s.className='star'; s.textContent='⭐'; btn.appendChild(s); }}
        }}
    }});
}}

// Right-click to toggle favorite
document.addEventListener('DOMContentLoaded', function() {{
    setTimeout(function() {{
        document.querySelectorAll('.voice-btn').forEach(function(btn) {{
            if (btn.closest('#fav-buttons')) return;
            btn.addEventListener('contextmenu', function(e) {{
                e.preventDefault();
                const match = (btn.getAttribute('onclick')||'').match(/voiceQuery\\('(.+?)'\\)/);
                if (match) toggleFavorite(match[1], btn.textContent.replace('⭐','').trim());
            }});
        }});
    }}, 200);
}});

// ── History ──
function renderHistory() {{
    const area = document.getElementById('history-area');
    const list = document.getElementById('history-list');
    if (history.length === 0) {{ area.style.display = 'none'; return; }}
    area.style.display = 'block';
    list.innerHTML = history.slice(0, 20).map(h => {{
        const time = h.ts ? h.ts.substr(11,8) : '';
        const lat = h.latency ? ' <span style=\"color:#444\">' + h.latency + 'ms</span>' : '';
        return '<div class="history-item" onclick="voiceQuery(\'' + h.command.replace(/'/g,"\\\\'") + '\')" title="Rejouer">' +
               '<span class="history-time">' + time + '</span>' + h.command + lat + ' → ' + (h.one_line||'').substr(0,100) + '</div>';
    }}).join('');
}}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') {{
        window.speechSynthesis.cancel();
        document.getElementById('last-query').textContent = '⏹ TTS stoppé';
    }}
    if (e.key === '/' && document.activeElement !== document.getElementById('console-input')) {{
        e.preventDefault();
        document.getElementById('console-input').focus();
    }}
    if (e.ctrlKey && e.key === 'k') {{
        e.preventDefault();
        clearConsole();
        document.getElementById('console-input').focus();
    }}
}});
</script>
</body>
</html>"""




@app.get("/voice", response_class=HTMLResponse)
def voice_operator_html():
    return HTMLResponse(content=_voice_operator_html())


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
        result = call(routed.endpoint, routed.params if routed.params else None)
        latency_ms = int((_time.time() - _start) * 1000)

        # Analytics: log command + response
        try:
            from modules.voice_operator.analytics.collector import log_command, log_response
            log_command(q, routed.intent, routed.endpoint)
            log_response(routed.intent, latency_ms, result.get("ok", True), result.get("source_quality", result.get("pipeline_state", "ok")))
        except Exception:
            pass

        return JSONResponse(content={
            "intent": routed.intent,
            "endpoint": routed.endpoint,
            "params": routed.params,
            "one_line": result.get("one_line", str(result)),
            "source": result.get("source_quality", result.get("pipeline_state", "ok")),
            "ok": result.get("ok", True),
            "generated_at": result.get("generated_at", ""),
            "confidence": result.get("confidence"),
            "source_quality": result.get("source_quality"),
            "pipeline_state": result.get("pipeline_state"),
            "latency_ms": latency_ms,
            "mode": "monitor_only",
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
