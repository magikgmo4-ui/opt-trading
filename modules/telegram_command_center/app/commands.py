"""Telegram command registry and handlers.

Commands return (response_text, target_channel, action) tuples.
target_channel=None means respond in the same chat where the command was received.
"""
from __future__ import annotations
import os
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable

from modules.telegram_command_center.app.formatters import (
    help_text,
    info,
    ops_result,
    routes_summary,
    route_test_result,
    error,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
CommandResponse = tuple[str, str | None, dict[str, Any] | None]

COMMANDS: dict[str, tuple[str, str | None, str]] = {}
HANDLERS: dict[str, Callable[..., CommandResponse]] = {}
ALIASES = {
    "/start": "/help",
    "/commands": "/help",
    "/test_route": "/test_routes",
    "/healthcheck": "/health",
    "/test_screenshot": "/snapshot",
}
CHANNEL_LABELS = {
    "alerts": "OT_ALERTS_CRITICAL",
    "pipeline": "OT_PIPELINE_GATES",
    "push": "OT_PUSH_MARKET_DATA",
    "ops": "OT_OPS_TOOLS",
    "legacy": "trading monitor et admin-trading",
    "unknown": "ce groupe",
}
ALLOWED_COMMANDS = {
    "alerts": {"/help"},
    "pipeline": {"/help", "/status", "/signals", "/approvals", "/perf"},
    "push": {"/help"},
    "ops": {"/help", "/routes", "/test_routes", "/health", "/analyze", "/snapshot"},
    "legacy": {"/help"},
    "unknown": {"/help"},
}


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


def _canonical_command(cmd: str) -> str:
    if cmd.startswith("/") and "@" in cmd:
        cmd = cmd.split("@", 1)[0]
    return ALIASES.get(cmd, cmd)


def _detect_context(chat_id: str | None) -> str:
    if not chat_id:
        return "direct"
    try:
        from shared.telegram_channels import get_chat_id
    except Exception:
        get_chat_id = None  # type: ignore
    for channel, env_name in (
        ("alerts", "TELEGRAM_CHAT_ID_ALERTS"),
        ("pipeline", "TELEGRAM_CHAT_ID_PIPELINE"),
        ("push", "TELEGRAM_CHAT_ID_PUSH"),
        ("ops", "TELEGRAM_CHAT_ID_OPS"),
    ):
        channel_chat = ""
        if get_chat_id is not None:
            try:
                channel_chat = get_chat_id(channel)
            except Exception:
                channel_chat = ""
        if not channel_chat:
            channel_chat = os.getenv(env_name) or ""
        if chat_id == channel_chat:
            return channel
    default_chat = ""
    if get_chat_id is not None:
        try:
            default_chat = get_chat_id("default")
        except Exception:
            default_chat = ""
    if not default_chat:
        default_chat = os.getenv("TELEGRAM_CHAT_ID") or ""
    if chat_id == default_chat:
        return "legacy"
    return "unknown"


def _guide_for_context(context: str, target_channel: str | None) -> str:
    if context == "alerts":
        return "Groupe reserve aux alertes. Utilise OT_PIPELINE_GATES ou OT_OPS_TOOLS."
    if context == "push":
        return "Groupe data silencieux. Utilise OT_OPS_TOOLS pour les commandes."
    if context == "legacy":
        return (
            "Ce groupe est legacy. Commandes decisionnelles dans OT_PIPELINE_GATES, "
            "commandes techniques dans OT_OPS_TOOLS."
        )
    if target_channel == "ops":
        return "Commande a utiliser dans OT_OPS_TOOLS."
    if target_channel == "pipeline":
        return "Commande a utiliser dans OT_PIPELINE_GATES."
    return "Utilise /help pour voir les commandes disponibles."


def _help_for_context(context: str) -> str:
    if context == "legacy":
        return (
            "Telegram Command Center\n"
            "Ce groupe est legacy.\n"
            "Commandes decisionnelles: OT_PIPELINE_GATES\n"
            "Commandes techniques: OT_OPS_TOOLS"
        )
    if context == "alerts":
        return (
            "Telegram Command Center\n"
            "Groupe reserve aux alertes.\n"
            "Utilise OT_PIPELINE_GATES ou OT_OPS_TOOLS pour les commandes."
        )
    if context == "push":
        return (
            "Telegram Command Center\n"
            "Groupe data silencieux.\n"
            "Utilise OT_OPS_TOOLS pour les commandes."
        )
    if context == "pipeline":
        pipeline_cmds = _collect_help_group(["/help", "/status", "/signals", "/approvals", "/perf"])
        return "Telegram Command Center\n" + help_text(pipeline_cmds)
    if context == "ops":
        ops_cmds = _collect_help_group(["/help", "/routes", "/test_routes", "/health", "/analyze", "/snapshot"])
        return "Telegram Command Center\n" + help_text(ops_cmds)
    cmds = _collect_help_group(["/help", "/status", "/health", "/routes"])
    return "Telegram Command Center\n" + help_text(cmds)


def _latest_headless_context() -> str | None:
    latest_dir = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
    summary_path = latest_dir / "summary.json"
    analysis_path = latest_dir / "analysis.txt"
    published_path = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis" / "latest.json"
    if not summary_path.exists() or not analysis_path.exists():
        return None
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception:
        summary = {}
    try:
        published = json.loads(published_path.read_text(encoding="utf-8")) if published_path.exists() else {}
    except Exception:
        published = {}
    analysis_text = analysis_path.read_text(encoding="utf-8", errors="ignore").strip()
    run_id = str(summary.get("run_id", "unknown"))
    source = Path(str(summary.get("source_screenshot", ""))).name or "unknown"
    signal_count = len((published.get("signals") or [])) if isinstance(published, dict) else 0
    excerpt_lines = [line.strip() for line in analysis_text.splitlines() if line.strip()][:8]
    lines = [
        f"Latest headless run: {run_id}",
        f"Source screenshot: {source}",
        f"Published signals: {signal_count}",
        "",
        *excerpt_lines,
    ]
    return "\n".join(lines).strip()


def _http_probe(url: str, timeout: float = 3.0) -> tuple[bool, int | None]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return True, int(getattr(resp, "status", 200) or 200)
    except Exception:
        return False, None


def _http_json(url: str, timeout: float = 5.0) -> tuple[int | None, dict[str, Any] | None]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200) or 200)
            return status, json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None, None


def cmd_help(args: str = "", *, context: str = "unknown") -> CommandResponse:
    if args.strip():
        cmd = _canonical_command("/" + args.strip().lstrip("/"))
        if cmd in COMMANDS:
            desc, channel, _ = COMMANDS[cmd]
            ch = channel or "same chat"
            return (
                f"{cmd}\n{desc}\nUse in: {ch}",
                None,
                None,
            )
        return (f"Unknown command: {cmd}", None, None)
    return (_help_for_context(context), None, None)


def cmd_status(args: str = "") -> CommandResponse:
    # Quick global status — lightweight probes only
    parts = []
    wh_ok, wh_status = _http_probe("http://127.0.0.1:8000/", timeout=3)
    parts.append(("Webhook", str(wh_status) if wh_ok and wh_status else "DOWN"))
    pf_ok, pf_status = _http_probe("http://127.0.0.1:8010/", timeout=3)
    parts.append(("Perf", str(pf_status) if pf_ok and pf_status else "DOWN"))

    summary = "all ok" if all("DOWN" not in v for _, v in parts) else "degraded"
    action = "run /health in ops group" if "DOWN" in str(parts) else "none"
    return (
        info("SYSTEM STATUS", [f"- {k:10s} {v}" for k, v in parts], action=action),
        "pipeline",
        None,
    )


def cmd_health(args: str = "") -> CommandResponse:
    script = REPO_ROOT / "modules/runtime_health/healthcheck.py"
    if not script.exists():
        return (ops_result("/health", "ERROR", "healthcheck script not found"), "ops", None)
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--json", "--no-telegram"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            return (ops_result("/health", "PASS", "all checks passed"), "ops", None)
        else:
            lines = [l for l in r.stdout.split("\n") if l.strip()][-5:]
            summary = "; ".join(lines) if lines else f"exit code {r.returncode}"
            return (ops_result("/health", "WARN", summary), "ops", None)
    except subprocess.TimeoutExpired:
        return (ops_result("/health", "TIMEOUT", "healthcheck took >15s"), "ops", None)
    except Exception as e:
        return (ops_result("/health", "ERROR", str(e)[:200]), "ops", None)


def cmd_approvals(args: str = "") -> CommandResponse:
    queue_path = REPO_ROOT / "data/runtime_health/approvals_queue.json"
    if not queue_path.exists():
        return (info("APPROVALS", ["No pending approvals."], action="none"), "pipeline", None)
    try:
        import json
        data = json.loads(queue_path.read_text())
        items = data.get("approvals", [])
        if not items:
            return (info("APPROVALS", ["No pending approvals."], action="none"), "pipeline", None)
        details = [f"- {i.get('approval_id', i.get('id','?'))[:20]}" for i in items[:5]]
        if len(items) > 5:
            details.append(f"… and {len(items) - 5} more")
        return (
            info(f"APPROVALS ({len(items)} pending)", details, action="run /approvals <id> for details"),
            "pipeline",
            None,
        )
    except Exception as e:
        return (info("APPROVALS", [f"Error: {e}"], action="check alerts group"), "pipeline", None)


def cmd_perf(args: str = "") -> CommandResponse:
    status, data = _http_json("http://127.0.0.1:8010/kpis", timeout=5)
    if status == 200 and data is not None:
        items = [
            ("Trades", str(data.get("total_trades", "?"))),
            ("Win rate", f"{data.get('win_rate', 0)}%"),
            ("Max DD", f"{data.get('max_dd_pct', 0)}%"),
            ("Net PnL", str(data.get("net_pnl", "?"))),
        ]
        return (info("PERFORMANCE", [f"- {k:10s} {v}" for k, v in items]), "pipeline", None)
    if status is not None:
        return (info("PERFORMANCE", [f"Perf API: HTTP {status}"], action="check ops"), "pipeline", None)
    return (info("PERFORMANCE", ["Perf API unreachable."], action="check ops"), "pipeline", None)


def cmd_signals(args: str = "") -> CommandResponse:
    # Check observation_events for recent signals
    events_path = REPO_ROOT / "state/observation_events.jsonl"
    if not events_path.exists():
        return (info("SIGNALS", ["No observation events file found."], action="none"), "pipeline", None)
    try:
        import json
        lines = events_path.read_text().strip().split("\n")
        recent = [json.loads(l) for l in lines[-5:] if l.strip()]
        if not recent:
            return (info("SIGNALS", ["No recent signals."], action="none"), "pipeline", None)
        items = []
        for e in reversed(recent):
            sym = e.get("symbol", e.get("ticker", "?"))
            side = e.get("side", e.get("action", "?"))
            ts = e.get("timestamp", e.get("ts", ""))[-8:]
            items.append(f"- {sym:12s} {side:5s} at {ts}")
        return (info(f"SIGNALS (last {len(recent)})", items, action="review in pipeline"), "pipeline", None)
    except Exception as e:
        return (info("SIGNALS", [f"Error: {e}"], action="check ops"), "pipeline", None)


def cmd_analyze(args: str = "") -> CommandResponse:
    latest_context = _latest_headless_context()
    if latest_context:
        return (ops_result("/analyze", "OK", latest_context), "ops", None)
    script = REPO_ROOT / "modules/desk_analyze/analyze_latest.py"
    if not script.exists():
        return (ops_result("/analyze", "ERROR", "analyze_latest.py not found"), "ops", None)
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--no-openai"],
            capture_output=True, text=True, timeout=30,
        )
        output = (r.stdout or "").strip() or (r.stderr or "").strip() or f"[analyze] rc={r.returncode}"
        if len(output) > 3800:
            output = output[:3777] + "\n…(trunc)"
        return (ops_result("/analyze", "OK" if r.returncode == 0 else "FAIL", output), "ops", None)
    except subprocess.TimeoutExpired:
        return (ops_result("/analyze", "TIMEOUT", "analysis took >30s"), "ops", None)
    except Exception as e:
        return (ops_result("/analyze", "ERROR", str(e)[:200]), "ops", None)


def cmd_routes(args: str = "") -> CommandResponse:
    channels = {
        "alerts": f"{CHANNEL_LABELS['alerts']} - critical system alerts",
        "pipeline": f"{CHANNEL_LABELS['pipeline']} - trading decisions",
        "push": f"{CHANNEL_LABELS['push']} - market data / screenshots",
        "ops": f"{CHANNEL_LABELS['ops']} - tools / command outputs",
    }
    return (routes_summary(channels), "ops", None)


def cmd_test_routes(args: str = "") -> CommandResponse:
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
            results.append(f"❌ Route test\nChannel: {ch}\nError: {e}")
    return ("\n\n".join(results), "ops", None)


def cmd_snapshot(args: str = "") -> CommandResponse:
    fixture_path = REPO_ROOT / "tests/fixtures/vision/coinglass/screenshot_mock_liquidations.png"
    if not fixture_path.exists():
        return (ops_result("/snapshot", "ERROR", "test image fixture not found"), None, None)
    return (
        "Snapshot test queued for OT_PUSH_MARKET_DATA.",
        None,
        {
            "kind": "send_photo_channel",
            "channel": "push",
            "photo_path": str(fixture_path),
            "caption": "snapshot test fixture",
        },
    )


def dispatch(text: str, *, chat_id: str | None = None) -> CommandResponse:
    """Dispatch a command text to the appropriate handler.

    Returns: (response_message, target_channel, action)
    - target_channel=None means respond in the same chat
    - target_channel="pipeline" means send to pipeline group
    """
    text = text.strip()
    if not text.startswith("/"):
        return ("", None, None)

    parts = text.split(maxsplit=1)
    cmd = _canonical_command(parts[0].lower())
    args = parts[1] if len(parts) > 1 else ""
    context = _detect_context(chat_id)

    if cmd in HANDLERS:
        if cmd == "/help":
            return HANDLERS[cmd](args, context=context)
        target_channel = COMMANDS.get(cmd, ("", None, ""))[1]
        if context != "direct" and cmd not in ALLOWED_COMMANDS.get(context, {"/help"}):
            return (_guide_for_context(context, target_channel), None, None)
        return HANDLERS[cmd](args)

    # Check partial match for /help <cmd>
    if args.strip():
        return cmd_help(text, context=context)

    return (f"Unknown command: {cmd}\nSend /help for available commands.", None, None)


# ── Register all commands ────────────────────────────────────────────────────

register("/help", "Show available commands and usage", cmd_help, channel=None)
register("/status", "Quick system status (webhook + perf)", cmd_status, channel="pipeline")
register("/health", "Full runtime health report", cmd_health, channel="ops")
register("/approvals", "List pending trading approvals", cmd_approvals, channel="pipeline")
register("/perf", "Performance summary (PnL, DD, win rate)", cmd_perf, channel="pipeline")
register("/signals", "Last 5 observation signals", cmd_signals, channel="pipeline")
register("/analyze", "Run desk analysis (no OpenAI)", cmd_analyze, channel="ops")
register("/routes", "Show current Telegram channel routing", cmd_routes, channel="ops")
register("/test_routes", "Test all 4 Telegram channels", cmd_test_routes, channel="ops")
register("/snapshot", "Send a real test image to OT_PUSH_MARKET_DATA", cmd_snapshot, channel="ops")
