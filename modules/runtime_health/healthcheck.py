#!/usr/bin/env python3
"""
opt-trading Runtime Health Supervisor — Phase 1 diagnostic-only
Checks: systemd services/timers, venv, env, ports, HTTP, paths, artifacts, logs, orchestrator
Output: /opt/trading/data/runtime_health/latest.json + healthcheck.jsonl
Exit: 0=PASS or WARN, 1=FAIL bloquant
"""

import argparse
import json
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

_IS_WINDOWS = platform.system() == "Windows"

try:
    import urllib.request as _urllib_request
    import urllib.error as _urllib_error
except ImportError:
    _urllib_request = None
    _urllib_error = None

try:
    import yaml as _yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "runtime_root": "/opt/trading",
    "data_dir": "/opt/trading/data/runtime_health",
    "python_fallback": "/usr/bin/python3",
    "services": {
        "required": [
            "tv-webhook.service",
            "tv-perf.service",
            "bot_vision_step2.service",
        ],
        "optional": ["simex-bitget.service"],
    },
    "timers": {
        "required": [
            "bot_vision_step2_prune.timer",
            "bot_vision_step2_send.timer",
            "macro_xau.timer",
        ],
        "optional": [],
    },
    "venvs": [
        {"path": "/opt/trading/venv", "label": "main", "required": True},
        {
            "path": "/opt/trading/.venvs/bot_vision_step2",
            "label": "bot_vision_step2",
            "required": False,
        },
    ],
    "env": {
        "required": ["TELEGRAM_BOT_TOKEN", "ALLOWED_CHAT_ID", "OPENAI_API_KEY"],
        "optional": ["TV_WEBHOOK_KEY", "TELEGRAM_CHAT_ID"],
        "files": [
            "/opt/trading/.env",
            "/etc/trading/telegram.env",
            "/etc/trading/runtime.env",
            "/opt/trading/env/telegram.env",
            "/opt/trading/env/runtime.env",
            "/opt/trading/modules/bot_vision_step2/config/bot_vision.env",
        ],
    },
    "ports": {
        "optional": [
            {"label": "webhook", "host": "127.0.0.1", "port": 8000},
            {"label": "desk_pro", "host": "127.0.0.1", "port": 8010},
            {"label": "openclaw_gateway", "host": "127.0.0.1", "port": 18789},
        ]
    },
    "http": {
        "optional": [
            {"label": "webhook_health", "url": "http://127.0.0.1:8000/health"},
            {"label": "perf_summary", "url": "http://127.0.0.1:8010/perf/summary"},
        ]
    },
    "paths": {
        "required": [
            {"path": "/opt/trading", "writable": False},
            {"path": "/var/log/trading", "writable": False},
            {"path": "/srv/sftp/shared_files/shared/vision_inbox", "writable": False},
            {
                "path": "/srv/sftp/shared_files/shared/vision_processed",
                "writable": False,
            },
            {"path": "/opt/trading/data/desk_pro/vision", "writable": True},
        ],
        "optional": [
            {"path": "/opt/trading/desk/snapshots", "writable": False},
        ],
    },
    "artifacts": {
        "optional": [
            {
                "path": "/opt/trading/data/desk_pro/vision",
                "label": "desk_vision_dir",
                "max_age_minutes": 120,
            },
            {
                "path": "/opt/trading/desk/snapshots",
                "label": "desk_snapshots_dir",
                "max_age_minutes": 120,
            },
        ]
    },
    "logs": {
        "journal_units": [
            "tv-webhook.service",
            "tv-perf.service",
            "bot_vision_step2.service",
        ],
        "log_files": {
            "optional": [
                "/var/log/trading/webhook.log",
                "/var/log/trading/perf.log",
                "/var/log/trading/bot_vision_step2.log",
            ]
        },
        "since": "10 minutes ago",
    },
    "orchestrator": {
        "tmux_sessions": {
            "optional": ["openclaw", "trading", "desk"],
        }
    },
    "telegram": {
        "enabled": True,
        "notify_on_states": ["WARN", "FAIL"],
        "state_change_only": True,
        "message_prefix": "[opt-trading]",
    },
}


def load_config(config_path: str) -> dict:
    """Load YAML config with fallback to DEFAULT_CONFIG."""
    if config_path and os.path.isfile(config_path):
        if _HAS_YAML:
            try:
                with open(config_path, "r") as fh:
                    data = _yaml.safe_load(fh)
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        else:
            # Try to parse minimal yaml manually (simple key: value only)
            pass
    return DEFAULT_CONFIG


# ---------------------------------------------------------------------------
# Individual check functions
# ---------------------------------------------------------------------------


def _run(cmd: list, timeout: int = 5) -> tuple:
    """Run a subprocess, return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -1, "", f"command not found: {cmd[0]}"
    except Exception as exc:
        return -1, "", str(exc)


def check_systemd_service(name: str, required: bool = True) -> dict:
    """Check a systemd service: is-active + is-enabled."""
    rc_active, active_out, _ = _run(["systemctl", "is-active", name])
    rc_enabled, enabled_out, _ = _run(["systemctl", "is-enabled", name])

    active = active_out or "unknown"
    enabled = enabled_out or "unknown"

    if active == "active":
        status = "PASS"
        detail = f"active, {enabled}"
    elif active in ("inactive", "failed"):
        status = "FAIL" if required else "WARN"
        detail = f"{active}, {enabled}"
    else:
        status = "WARN" if required else "WARN"
        detail = f"{active}, {enabled}"

    return {
        "check": f"service:{name}",
        "status": status,
        "active": active,
        "enabled": enabled,
        "required": required,
        "detail": detail,
    }


def check_systemd_timer(name: str, required: bool = True) -> dict:
    """Check a systemd timer: ActiveState + NextElapseUSecRealtime."""
    rc, out, err = _run(
        [
            "systemctl",
            "show",
            name,
            "--property=ActiveState,NextElapseUSecRealtime,LastTriggerUSec",
        ]
    )

    props = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()

    active_state = props.get("ActiveState", "unknown")
    next_elapse = props.get("NextElapseUSecRealtime", "unknown")
    last_trigger = props.get("LastTriggerUSec", "unknown")

    if active_state == "active":
        status = "PASS"
    elif rc == -1:
        status = "WARN"
        active_state = f"error: {err}"
    else:
        status = "FAIL" if required else "WARN"

    return {
        "check": f"timer:{name}",
        "status": status,
        "active_state": active_state,
        "next_elapse": next_elapse,
        "last_trigger": last_trigger,
        "required": required,
    }


def check_venv(path: str, label: str = "", required: bool = True) -> dict:
    """Check venv existence and python version."""
    venv_path = Path(path)
    python_bin = venv_path / "bin" / "python3"
    if not python_bin.exists():
        python_bin = venv_path / "bin" / "python"
    if not python_bin.exists():
        python_bin = venv_path / "Scripts" / "python.exe"
    if not python_bin.exists():
        python_bin = venv_path / "Scripts" / "python"

    if not venv_path.exists():
        return {
            "check": f"venv:{label or path}",
            "status": "FAIL" if required else "WARN",
            "path": path,
            "exists": False,
            "required": required,
            "detail": "venv directory not found",
        }

    if not python_bin.exists():
        return {
            "check": f"venv:{label or path}",
            "status": "FAIL" if required else "WARN",
            "path": path,
            "exists": True,
            "required": required,
            "detail": "python binary not found in venv",
        }

    rc, version_out, _ = _run([str(python_bin), "--version"])
    if rc == 0:
        status = "PASS"
        detail = version_out
    else:
        status = "WARN"
        detail = "python --version failed"

    return {
        "check": f"venv:{label or path}",
        "status": status,
        "path": path,
        "exists": True,
        "python_version": version_out if rc == 0 else None,
        "required": required,
        "detail": detail,
    }


def _env_file_keys(paths: list[str]) -> set[str]:
    """Return keys present in env files. Values are never returned or logged."""
    keys: set[str] = set()
    for path_str in paths:
        p = Path(path_str)
        if not p.exists() or not p.is_file():
            continue
        try:
            for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key = line.split("=", 1)[0].strip()
                if key and key.replace("_", "").isalnum() and not key[0].isdigit():
                    keys.add(key)
        except OSError:
            continue
    return keys


def check_env_key(key: str, required: bool = True, file_keys: set[str] | None = None) -> dict:
    """Check presence of env key. NEVER logs the value."""
    in_process = key in os.environ
    in_file = key in (file_keys or set())
    present = in_process or in_file
    status = "PASS" if present else ("FAIL" if required else "WARN")
    return {
        "check": f"env:{key}",
        "status": status,
        "key": key,
        "present": present,
        "source": "process" if in_process else ("env_file" if in_file else "missing"),
        "required": required,
        # value is intentionally omitted
    }


def check_port(host: str, port: int, label: str = "", required: bool = False) -> dict:
    """Check TCP connectivity to host:port."""
    try:
        conn = socket.create_connection((host, port), timeout=2)
        conn.close()
        status = "PASS"
        detail = "reachable"
    except (ConnectionRefusedError, socket.timeout, OSError) as exc:
        status = "FAIL" if required else "WARN"
        detail = str(exc)

    return {
        "check": f"port:{label or f'{host}:{port}'}",
        "status": status,
        "host": host,
        "port": port,
        "required": required,
        "detail": detail,
    }


def check_http(url: str, label: str = "", required: bool = False) -> dict:
    """Check HTTP endpoint reachability."""
    check_name = f"http:{label or url}"
    if _urllib_request is None:
        return {
            "check": check_name,
            "status": "WARN",
            "url": url,
            "required": required,
            "detail": "urllib not available",
        }

    try:
        req = _urllib_request.Request(url, method="GET")
        with _urllib_request.urlopen(req, timeout=3) as resp:
            http_status = resp.status
            status = "PASS" if http_status < 400 else ("FAIL" if required else "WARN")
            detail = f"HTTP {http_status}"
    except _urllib_error.HTTPError as exc:
        http_status = exc.code
        status = "FAIL" if required else "WARN"
        detail = f"HTTP {http_status}"
    except Exception as exc:
        http_status = None
        status = "FAIL" if required else "WARN"
        detail = str(exc)

    return {
        "check": check_name,
        "status": status,
        "url": url,
        "http_status": http_status,
        "required": required,
        "detail": detail,
    }


def check_path(path_str: str, writable: bool = False, required: bool = True) -> dict:
    """Check path existence and optional write access."""
    p = Path(path_str)
    exists = p.exists()

    if not exists:
        return {
            "check": f"path:{path_str}",
            "status": "FAIL" if required else "WARN",
            "path": path_str,
            "exists": False,
            "writable": None,
            "required": required,
            "detail": "path does not exist",
        }

    is_writable = None
    if writable:
        is_writable = os.access(path_str, os.W_OK)
        if not is_writable:
            return {
                "check": f"path:{path_str}",
                "status": "FAIL" if required else "WARN",
                "path": path_str,
                "exists": True,
                "writable": False,
                "required": required,
                "detail": "path not writable",
            }

    return {
        "check": f"path:{path_str}",
        "status": "PASS",
        "path": path_str,
        "exists": True,
        "writable": is_writable,
        "required": required,
        "detail": "ok",
    }


def check_artifact(path_str: str, max_age_minutes: int, label: str = "", required: bool = False) -> dict:
    """Check artifact freshness by mtime."""
    check_name = f"artifact:{label or path_str}"
    p = Path(path_str)

    if not p.exists():
        return {
            "check": check_name,
            "status": "FAIL" if required else "WARN",
            "path": path_str,
            "exists": False,
            "required": required,
            "detail": "path does not exist",
        }

    # For directories: use the most recently modified item inside
    if p.is_dir():
        items = sorted(p.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        if not items:
            return {
                "check": check_name,
                "status": "WARN",
                "path": path_str,
                "exists": True,
                "required": required,
                "detail": "directory is empty",
            }
        mtime = items[0].stat().st_mtime
    else:
        mtime = p.stat().st_mtime

    age_seconds = time.time() - mtime
    age_minutes = age_seconds / 60.0

    if age_minutes > max_age_minutes:
        status = "FAIL" if required else "WARN"
        detail = f"age={age_minutes:.1f}m > max={max_age_minutes}m"
    else:
        status = "PASS"
        detail = f"age={age_minutes:.1f}m"

    return {
        "check": check_name,
        "status": status,
        "path": path_str,
        "exists": True,
        "age_minutes": round(age_minutes, 2),
        "max_age_minutes": max_age_minutes,
        "required": required,
        "detail": detail,
    }


def check_log_errors_journal(unit: str, since: str = "10 minutes ago") -> dict:
    """Check journalctl for errors from a unit in the last window."""
    rc, out, err = _run(
        ["journalctl", "-u", unit, "-p", "err", f"--since={since}", "--no-pager", "-q"],
        timeout=10,
    )

    if rc == -1:
        return {
            "check": f"journal_errors:{unit}",
            "status": "WARN",
            "unit": unit,
            "since": since,
            "required": True,
            "error_lines": 0,
            "detail": f"journalctl unavailable: {err}",
        }

    lines = [l for l in out.splitlines() if l.strip()]
    count = len(lines)
    status = "WARN" if count > 0 else "PASS"

    return {
        "check": f"journal_errors:{unit}",
        "status": status,
        "unit": unit,
        "since": since,
        "required": True,
        "error_lines": count,
        "detail": f"{count} error line(s)" if count else "no errors",
    }


def check_logfile_errors(path_str: str, pattern: str = "ERROR", tail: int = 100) -> dict:
    """Check a log file for error pattern in last N lines."""
    check_name = f"logfile_errors:{path_str}"
    p = Path(path_str)

    if not p.exists():
        return {
            "check": check_name,
            "status": "WARN",
            "path": path_str,
            "exists": False,
            "detail": "log file not found",
        }

    rc, out, err = _run(["tail", "-n", str(tail), path_str], timeout=5)
    if rc != 0:
        return {
            "check": check_name,
            "status": "WARN",
            "path": path_str,
            "exists": True,
            "detail": f"tail failed: {err}",
        }

    matching = [line for line in out.splitlines() if pattern in line]
    count = len(matching)
    status = "WARN" if count > 0 else "PASS"

    return {
        "check": check_name,
        "status": status,
        "path": path_str,
        "exists": True,
        "pattern": pattern,
        "tail_lines": tail,
        "match_count": count,
        "detail": f"{count} '{pattern}' line(s) in last {tail}" if count else "no errors",
    }


def check_tmux_session(session: str, required: bool = False) -> dict:
    """Check if a tmux session exists."""
    rc, out, err = _run(["tmux", "has-session", "-t", session], timeout=3)
    exists = rc == 0
    status = "PASS" if exists else ("FAIL" if required else "WARN")

    return {
        "check": f"tmux:{session}",
        "status": status,
        "session": session,
        "exists": exists,
        "required": required,
        "detail": "session active" if exists else "session not found",
    }


# ---------------------------------------------------------------------------
# Block runners
# ---------------------------------------------------------------------------


def _block_status(results: list) -> str:
    """Compute operational block status, ignoring advisory-only results."""
    statuses = {
        r["status"]
        for r in results
        if not r.get("advisory", False)
    }
    if "FAIL" in statuses:
        return "FAIL"
    if "WARN" in statuses:
        return "WARN"
    return "PASS"


def _mark_advisories(checks: dict[str, list]) -> dict:
    """Mark non-PASS optional checks as advisory without hiding them."""
    by_block: dict[str, int] = {}
    examples: list[str] = []
    total = 0

    for block, results in checks.items():
        block_count = 0
        for result in results:
            status = result.get("status")
            is_optional = result.get("required") is False
            if is_optional and status != "PASS":
                result["advisory"] = True
                result["operational_status"] = "PASS"
                block_count += 1
                total += 1
                if len(examples) < 12:
                    examples.append(result.get("check", "unknown"))
            else:
                result["advisory"] = False
                result["operational_status"] = status
        if block_count:
            by_block[block] = block_count

    return {
        "total": total,
        "by_block": by_block,
        "examples": examples,
    }


def run_systemd_services(cfg: dict) -> list:
    results = []
    svc_cfg = cfg.get("services", {})
    for name in svc_cfg.get("required", []):
        results.append(check_systemd_service(name, required=True))
    for name in svc_cfg.get("optional", []):
        results.append(check_systemd_service(name, required=False))
    return results


def run_systemd_timers(cfg: dict) -> list:
    results = []
    timer_cfg = cfg.get("timers", {})
    for name in timer_cfg.get("required", []):
        results.append(check_systemd_timer(name, required=True))
    for name in timer_cfg.get("optional", []):
        results.append(check_systemd_timer(name, required=False))
    return results


def run_venvs(cfg: dict) -> list:
    results = []
    for venv in cfg.get("venvs", []):
        results.append(
            check_venv(
                venv["path"],
                label=venv.get("label", ""),
                required=venv.get("required", True),
            )
        )
    return results


def run_env(cfg: dict) -> list:
    results = []
    env_cfg = cfg.get("env", {})
    file_keys = _env_file_keys(env_cfg.get("files", []))
    for key in env_cfg.get("required", []):
        results.append(check_env_key(key, required=True, file_keys=file_keys))
    for key in env_cfg.get("optional", []):
        results.append(check_env_key(key, required=False, file_keys=file_keys))
    return results


def run_ports(cfg: dict) -> list:
    results = []
    ports_cfg = cfg.get("ports", {})
    for entry in ports_cfg.get("required", []):
        results.append(
            check_port(entry["host"], entry["port"], label=entry.get("label", ""), required=True)
        )
    for entry in ports_cfg.get("optional", []):
        results.append(
            check_port(entry["host"], entry["port"], label=entry.get("label", ""), required=False)
        )
    return results


def run_http(cfg: dict) -> list:
    results = []
    http_cfg = cfg.get("http", {})
    for entry in http_cfg.get("required", []):
        results.append(check_http(entry["url"], label=entry.get("label", ""), required=True))
    for entry in http_cfg.get("optional", []):
        results.append(check_http(entry["url"], label=entry.get("label", ""), required=False))
    return results


def run_paths(cfg: dict) -> list:
    results = []
    paths_cfg = cfg.get("paths", {})
    for entry in paths_cfg.get("required", []):
        results.append(check_path(entry["path"], writable=entry.get("writable", False), required=True))
    for entry in paths_cfg.get("optional", []):
        results.append(check_path(entry["path"], writable=entry.get("writable", False), required=False))
    return results


def run_artifacts(cfg: dict) -> list:
    results = []
    art_cfg = cfg.get("artifacts", {})
    for entry in art_cfg.get("required", []):
        results.append(
            check_artifact(
                entry["path"],
                entry["max_age_minutes"],
                label=entry.get("label", ""),
                required=True,
            )
        )
    for entry in art_cfg.get("optional", []):
        results.append(
            check_artifact(
                entry["path"],
                entry["max_age_minutes"],
                label=entry.get("label", ""),
                required=False,
            )
        )
    return results


def run_logs(cfg: dict) -> list:
    results = []
    logs_cfg = cfg.get("logs", {})
    since = logs_cfg.get("since", "10 minutes ago")

    for unit in logs_cfg.get("journal_units", []):
        results.append(check_log_errors_journal(unit, since=since))

    log_files_cfg = logs_cfg.get("log_files", {})
    for path_str in log_files_cfg.get("required", []):
        r = check_logfile_errors(path_str)
        r["required"] = True
        results.append(r)
    for path_str in log_files_cfg.get("optional", []):
        r = check_logfile_errors(path_str)
        r["required"] = False
        # downgrade FAIL to WARN for optional files
        if r["status"] == "FAIL":
            r["status"] = "WARN"
        results.append(r)
    return results


def run_orchestrator(cfg: dict) -> list:
    results = []
    orch_cfg = cfg.get("orchestrator", {})
    tmux_cfg = orch_cfg.get("tmux_sessions", {})
    for session in tmux_cfg.get("required", []):
        results.append(check_tmux_session(session, required=True))
    for session in tmux_cfg.get("optional", []):
        results.append(check_tmux_session(session, required=False))
    return results


# ---------------------------------------------------------------------------
# Telegram notification
# ---------------------------------------------------------------------------


def send_telegram(token: str, chat_id: str, message: str) -> bool:
    """Send a Telegram message. Returns True on success."""
    if _urllib_request is None:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "HTML"}).encode()
    req = _urllib_request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with _urllib_request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def maybe_notify_telegram(
    cfg: dict,
    overall_status: str,
    block_statuses: dict,
    previous_status: str | None,
    run_id: str,
    no_telegram: bool,
) -> None:
    """Send Telegram alert if conditions are met. Never logs tokens."""
    if no_telegram:
        return

    tg_cfg = cfg.get("telegram", {})
    if not tg_cfg.get("enabled", True):
        return

    notify_on = set(tg_cfg.get("notify_on_states", ["WARN", "FAIL"]))
    state_change_only = tg_cfg.get("state_change_only", True)
    prefix = tg_cfg.get("message_prefix", "[opt-trading]")

    if overall_status not in notify_on:
        return

    if state_change_only and previous_status is not None:
        if previous_status == overall_status:
            return

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("ALLOWED_CHAT_ID", "")

    if not token or not chat_id:
        return

    # Build message (no secrets in message)
    hostname = socket.gethostname()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    change_str = ""
    if previous_status and previous_status != overall_status:
        change_str = f" ({previous_status} → {overall_status})"

    failing_blocks = [k for k, v in block_statuses.items() if v == "FAIL"]
    warning_blocks = [k for k, v in block_statuses.items() if v == "WARN"]

    lines = [
        f"{prefix} <b>{overall_status}</b>{change_str}",
        f"Host: <code>{hostname}</code>  |  {ts}",
        f"Run: <code>{run_id[:8]}</code>",
    ]
    if failing_blocks:
        lines.append(f"FAIL blocks: {', '.join(failing_blocks)}")
    if warning_blocks:
        lines.append(f"WARN blocks: {', '.join(warning_blocks)}")

    message = "\n".join(lines)
    send_telegram(token, chat_id, message)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def compute_overall_status(block_statuses: dict, checks: dict, cfg: dict) -> str:
    """
    FAIL if any operational block fails.
    WARN if any operational block warns.
    Advisory-only optional checks do not degrade operational status.
    PASS otherwise.
    """
    all_statuses = set(block_statuses.values())
    if "FAIL" in all_statuses:
        return "FAIL"
    if "WARN" in all_statuses:
        return "WARN"
    return "PASS"


def load_previous_status(data_dir: str) -> str | None:
    """Load overall_status from latest.json if it exists."""
    latest = Path(data_dir) / "latest.json"
    if not latest.exists():
        return None
    try:
        with open(latest, "r") as fh:
            data = json.load(fh)
        return data.get("overall_status")
    except Exception:
        return None


def write_outputs(report: dict, data_dir: str, dry_run: bool) -> None:
    """Write latest.json and append to healthcheck.jsonl."""
    if dry_run:
        return

    out_dir = Path(data_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    latest_path = out_dir / "latest.json"
    with open(latest_path, "w") as fh:
        json.dump(report, fh, indent=2, default=str)

    jsonl_path = out_dir / "healthcheck.jsonl"
    line = {
        "timestamp": report["timestamp"],
        "run_id": report["run_id"],
        "hostname": report["hostname"],
        "overall_status": report["overall_status"],
        "block_statuses": report["block_statuses"],
        "advisory_total": report.get("advisory_summary", {}).get("total", 0),
        "elapsed_seconds": report["elapsed_seconds"],
    }
    with open(jsonl_path, "a") as fh:
        fh.write(json.dumps(line, default=str) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="opt-trading Runtime Health Supervisor — Phase 1"
    )
    parser.add_argument("--config", default="", help="Path to runtime_health.yml")
    parser.add_argument("--map", default="", help="Path to machine_runtime_map.yml")
    parser.add_argument("--machine", default="", help="Override machine name (default: hostname)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run checks but do not write output files",
    )
    parser.add_argument(
        "--no-telegram",
        action="store_true",
        help="Suppress Telegram notifications",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    t_start = time.monotonic()

    # Resolve config path
    config_path = args.config
    if not config_path:
        this_dir = Path(__file__).parent
        config_path = str(this_dir / "config" / "runtime_health.yml")

    cfg = load_config(config_path)

    # Load machine map and override config scope if machine is known
    machine_name: str = ""
    hostname = socket.gethostname()
    machine_identity_check: dict = {}
    forbidden_checks: list = []

    try:
        from modules.runtime_health.machine_map import MachineMap, check_machine_identity
        map_path = args.map
        if not map_path:
            repo_root = Path(__file__).resolve().parents[2]
            map_path = str(repo_root / "config" / "machine_runtime_map.yml")

        mm = MachineMap.load(map_path)
        override = args.machine or os.environ.get("MACHINE_ROLE", "").strip()
        raw_name = override if override else hostname
        scope = mm.scope_for(raw_name)
        if scope is not None:
            machine_name = mm.canonical_name_for(raw_name)
        elif raw_name != hostname:
            scope = mm.scope_for(hostname)
            machine_name = mm.canonical_name_for(hostname) if scope else hostname
        else:
            machine_name = hostname

        machine_identity_check = check_machine_identity(
            hostname, machine_name, scope, mm.version, mm.map_path
        )

        if scope is not None:
            cfg = mm.build_config_from_scope(scope, cfg)
            forbidden_checks = mm.check_forbidden_services(scope)
    except Exception:
        machine_name = hostname

    data_dir = cfg.get("data_dir", "/opt/trading/data/runtime_health")

    # Load previous status for change-only notifications
    previous_status = load_previous_status(data_dir)

    # Run all check blocks
    checks: dict[str, list] = {}

    if machine_identity_check:
        checks["MACHINE_IDENTITY"] = [machine_identity_check]

    checks["SYSTEMD_SERVICES"] = run_systemd_services(cfg)
    checks["SYSTEMD_TIMERS"] = run_systemd_timers(cfg)

    if forbidden_checks:
        checks["FORBIDDEN_SERVICES"] = forbidden_checks

    checks["VENV"] = run_venvs(cfg)
    checks["ENV"] = run_env(cfg)
    checks["PORTS"] = run_ports(cfg)
    checks["HTTP"] = run_http(cfg)
    checks["PATHS"] = run_paths(cfg)
    checks["ARTIFACTS"] = run_artifacts(cfg)
    checks["LOGS"] = run_logs(cfg)
    checks["ORCHESTRATOR"] = run_orchestrator(cfg)

    advisory_summary = _mark_advisories(checks)
    block_statuses = {block: _block_status(results) for block, results in checks.items()}
    overall_status = compute_overall_status(block_statuses, checks, cfg)

    elapsed = round(time.monotonic() - t_start, 3)
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    report = {
        "timestamp": timestamp,
        "hostname": hostname,
        "machine": machine_name,
        "run_id": run_id,
        "overall_status": overall_status,
        "block_statuses": block_statuses,
        "advisory_summary": advisory_summary,
        "checks": checks,
        "elapsed_seconds": elapsed,
    }

    # Write outputs
    write_outputs(report, data_dir, dry_run=args.dry_run)

    # Print summary to stdout (no secrets)
    print(json.dumps(
        {
            "timestamp": timestamp,
            "hostname": hostname,
            "machine": machine_name,
            "run_id": run_id,
            "overall_status": overall_status,
            "block_statuses": block_statuses,
            "advisory_summary": advisory_summary,
            "elapsed_seconds": elapsed,
        },
        indent=2,
    ))

    # Telegram notification
    maybe_notify_telegram(
        cfg,
        overall_status,
        block_statuses,
        previous_status,
        run_id,
        no_telegram=args.no_telegram,
    )

    # Exit codes: 0=PASS/WARN, 1=FAIL
    return 0 if overall_status in ("PASS", "WARN") else 1


if __name__ == "__main__":
    sys.exit(main())
