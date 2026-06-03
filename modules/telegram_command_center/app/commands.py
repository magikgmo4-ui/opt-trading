"""Telegram command registry and handlers.

Provides a dispatch table for bot commands and standardized response formatting.
Commands return (response_text, target_channel) tuples.
target_channel=None means respond in the same chat where the command was received.
"""
from __future__ import annotations
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable

from modules.telegram_command_center.app.formatters import (
    help_text,
    info,
    ops_result,
    routes_summary,
    route_test_result,
    error,
)

REPO_ROOT = Path(__file__).resolve().parents[3]

COMMANDS: dict[str, tuple[str, str | None, str]] = {}
HANDLERS: dict[str, Callable[..., tuple[str, str | None]]] = {}


def register(
    cmd: str,
    description: str,
    handler: Callable,
    *,
    channel: str | None = None,
) -> None:
    COMMANDS[cmd] = (description, channel, handler.__name__)
    HANDLERS[cmd] = handler


def _collect_help_group(cmds: list[str]) -> list[tuple[str, str]]:
    result = []
    for cmd in cmds:
        if cmd in COMMANDS:
            desc, *_ = COMMANDS[cmd]
            result.append((cmd, desc))
    return result


def cmd_help(args: str = "") -> tuple[str, str | None]:
    if args.strip():
        cmd = args.strip().lstrip("/")
        if cmd in COMMANDS:
            desc, channel, _ = COMMANDS[cmd]
            ch = channel or "same chat"
            return (
                f"<b>/{cmd}</b>\n"
                f"{desc}\n"
                f"Responds in: <code>{ch}</code>",
                channel,
            )
        return (f"Unknown command: /{cmd}", None)

    # Build group-specific help sections
    pipeline_cmds = _collect_help_group(["/help", "/status", "/approvals", "/perf"])
    ops_cmds = _collect_help_group(["/help", "/health", "/analyze", "/routes", "/test_routes"])
    general_cmds = _collect_help_group(["/signals"])

    lines = ["<b>Telegram Command Center</b>", ""]
    lines.append("<u>Pipeline group (decisions)</u>")
    for c, d in pipeline_cmds:
        lines.append(f"• <code>{c:15s}</code> {d}")
    lines.append("")
    lines.append("<u>Ops group (tools)</u>")
    for c, d in ops_cmds:
        lines.append(f"• <code>{c:15s}</code> {d}")
    if general_cmds:
        lines.append("")
        lines.append("<u>Any group</u>")
        for c, d in general_cmds:
            lines.append(f"• <code>{c:15s}</code> {d}")
    lines.append("")
    lines.append("Send <code>/help &lt;command&gt;</code> for details.")
    return ("\n".join(lines), None)


def cmd_status(args: str = "") -> tuple[str, str | None]:
    # Quick global status — lightweight probes only
    parts = []
    try:
        import requests
        wh = requests.get("http://127.0.0.1:8000/", timeout=3)
        parts.append(("Webhook", f"{wh.status_code}" if wh.ok else "DOWN"))
    except Exception:
        parts.append(("Webhook", "DOWN"))
    try:
        pf = requests.get("http://127.0.0.1:8010/", timeout=3)
        parts.append(("Perf", f"{pf.status_code}" if pf.ok else "DOWN"))
    except Exception:
        parts.append(("Perf", "DOWN"))

    summary = "all ok" if all("DOWN" not in v for _, v in parts) else "degraded"
    action = "run /health in ops group" if "DOWN" in str(parts) else "none"
    return (
        info("SYSTEM STATUS", [f"• <code>{k:10s}</code> {v}" for k, v in parts], action=action),
        "pipeline",
    )


def cmd_health(args: str = "") -> tuple[str, str | None]:
    script = REPO_ROOT / "modules/runtime_health/healthcheck.py"
    if not script.exists():
        return (ops_result("/health", "ERROR", "healthcheck script not found"), "ops")
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--json", "--no-telegram"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            return (ops_result("/health", "PASS", "all checks passed"), "ops")
        else:
            lines = [l for l in r.stdout.split("\n") if l.strip()][-5:]
            summary = "; ".join(lines) if lines else f"exit code {r.returncode}"
            return (ops_result("/health", "WARN", summary), "ops")
    except subprocess.TimeoutExpired:
        return (ops_result("/health", "TIMEOUT", "healthcheck took >15s"), "ops")
    except Exception as e:
        return (ops_result("/health", "ERROR", str(e)[:200]), "ops")


def cmd_approvals(args: str = "") -> tuple[str, str | None]:
    queue_path = REPO_ROOT / "data/runtime_health/approvals_queue.json"
    if not queue_path.exists():
        return (info("APPROVALS", ["No pending approvals."], action="none"), "pipeline")
    try:
        import json
        data = json.loads(queue_path.read_text())
        items = data.get("approvals", [])
        if not items:
            return (info("APPROVALS", ["No pending approvals."], action="none"), "pipeline")
        details = [f"• <code>{i.get('approval_id', i.get('id','?'))[:20]}</code>" for i in items[:5]]
        if len(items) > 5:
            details.append(f"… and {len(items) - 5} more")
        return (
            info(f"APPROVALS ({len(items)} pending)", details, action="run /approvals <id> for details"),
            "pipeline",
        )
    except Exception as e:
        return (info("APPROVALS", [f"Error: {e}"], action="check alerts group"), "pipeline")


def cmd_perf(args: str = "") -> tuple[str, str | None]:
    try:
        import requests
        r = requests.get("http://127.0.0.1:8010/kpis", timeout=5)
        if r.ok:
            data = r.json()
            items = [
                ("Trades", str(data.get("total_trades", "?"))),
                ("Win rate", f"{data.get('win_rate', 0)}%"),
                ("Max DD", f"{data.get('max_dd_pct', 0)}%"),
                ("Net PnL", str(data.get("net_pnl", "?"))),
            ]
            return (info("PERFORMANCE", [f"• <code>{k:10s}</code> {v}" for k, v in items]), "pipeline")
        return (info("PERFORMANCE", [f"Perf API: HTTP {r.status_code}"], action="check ops"), "pipeline")
    except Exception as e:
        return (info("PERFORMANCE", [f"Perf API unreachable: {e}"], action="check ops"), "pipeline")


def cmd_signals(args: str = "") -> tuple[str, str | None]:
    # Check observation_events for recent signals
    events_path = REPO_ROOT / "state/observation_events.jsonl"
    if not events_path.exists():
        return (info("SIGNALS", ["No observation events file found."], action="none"), "pipeline")
    try:
        import json
        lines = events_path.read_text().strip().split("\n")
        recent = [json.loads(l) for l in lines[-5:] if l.strip()]
        if not recent:
            return (info("SIGNALS", ["No recent signals."], action="none"), "pipeline")
        items = []
        for e in reversed(recent):
            sym = e.get("symbol", e.get("ticker", "?"))
            side = e.get("side", e.get("action", "?"))
            ts = e.get("timestamp", e.get("ts", ""))[-8:]
            items.append(f"• <code>{sym:12s}</code> {side:5s} at {ts}")
        return (info(f"SIGNALS (last {len(recent)})", items, action="review in pipeline"), "pipeline")
    except Exception as e:
        return (info("SIGNALS", [f"Error: {e}"], action="check ops"), "pipeline")


def cmd_analyze(args: str = "") -> tuple[str, str | None]:
    script = REPO_ROOT / "modules/desk_analyze/analyze_latest.py"
    if not script.exists():
        return (ops_result("/analyze", "ERROR", "analyze_latest.py not found"), "ops")
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--no-openai"],
            capture_output=True, text=True, timeout=30,
        )
        output = (r.stdout or "").strip() or (r.stderr or "").strip() or f"[analyze] rc={r.returncode}"
        if len(output) > 3800:
            output = output[:3777] + "\n…(trunc)"
        return (ops_result("/analyze", "OK" if r.returncode == 0 else "FAIL", output), "ops")
    except subprocess.TimeoutExpired:
        return (ops_result("/analyze", "TIMEOUT", "analysis took >30s"), "ops")
    except Exception as e:
        return (ops_result("/analyze", "ERROR", str(e)[:200]), "ops")


def cmd_routes(args: str = "") -> tuple[str, str | None]:
    channels = {
        "alerts": "critical system alerts",
        "pipeline": "trading decisions",
        "push": "market data / screenshots",
        "ops": "tools / command outputs",
    }
    return (routes_summary(channels), "ops")


def cmd_test_routes(args: str = "") -> tuple[str, str | None]:
    results = []
    for ch in ("alerts", "pipeline", "push", "ops"):
        try:
            from shared.telegram_channels import send_to_channel
            t0 = time.time()
            r = send_to_channel(ch, f"🧪 Route test from /test_routes", source="test_routes")
            elapsed = (time.time() - t0) * 1000
            ok = bool(r.get("ok"))
            results.append(route_test_result(ch, ok, elapsed))
        except Exception as e:
            results.append(f"❌ <b>Route test</b>\nChannel: <code>{ch}</code>\nError: {e}")
    return ("\n\n".join(results), "ops")


def dispatch(text: str) -> tuple[str, str | None]:
    """Dispatch a command text to the appropriate handler.

    Returns: (response_message, target_channel)
    - target_channel=None means respond in the same chat
    - target_channel="pipeline" means send to pipeline group
    """
    text = text.strip()
    if not text.startswith("/"):
        return ("", None)

    parts = text.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd in HANDLERS:
        return HANDLERS[cmd](args)

    # Check partial match for /help <cmd>
    if args.strip():
        return cmd_help(text)

    return (f"Unknown command: {cmd}\nSend /help for available commands.", None)


# ── Register all commands ────────────────────────────────────────────────────

register("/help", "Show available commands and usage", cmd_help, channel=None)
register("/status", "Quick system status (webhook + perf)", cmd_status, channel="pipeline")
register("/health", "Full runtime health report", cmd_health, channel="ops")
register("/approvals", "List pending trading approvals", cmd_approvals, channel="pipeline")
register("/perf", "Performance summary (PnL, DD, win rate)", cmd_perf, channel="pipeline")
register("/signals", "Last 5 observation signals", cmd_signals, channel=None)
register("/analyze", "Run desk analysis (no OpenAI)", cmd_analyze, channel="ops")
register("/routes", "Show current Telegram channel routing", cmd_routes, channel="ops")
register("/test_routes", "Test all 4 Telegram channels", cmd_test_routes, channel="ops")
