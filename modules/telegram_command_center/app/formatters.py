"""Standardized message formatters per Telegram channel.

Each formatter returns a short, actionable HTML message suitable for its channel.
Follows the formats defined in GO_TELEGRAM_USER_EXPERIENCE_CHILD_COMMAND_CENTER_01.
"""
from __future__ import annotations
from typing import Any


def alert(title: str, source: str, status: str, impact: str, action: str) -> str:
    return (
        f"🔴 <b>ALERT</b>\n"
        f"Source: <code>{source}</code>\n"
        f"Status: <b>{status}</b>\n"
        f"Impact: {impact}\n"
        f"Action: {action}"
    )


def decision_required(
    asset: str,
    direction: str,
    entry: str | float,
    sl: str | float,
    tp: str | float | list[str | float],
    confidence: str = "",
    rationale: str = "",
) -> str:
    tp_line = tp
    if isinstance(tp, list):
        tp_line = " / ".join(str(t) for t in tp)
    lines = [
        "🟡 <b>DECISION REQUIRED</b>",
        f"Asset: <code>{asset}</code>",
        f"Direction: <b>{direction}</b>",
        f"Entry: <code>{entry}</code>",
        f"SL: <code>{sl}</code>",
        f"TP: <code>{tp_line}</code>",
    ]
    if confidence:
        lines.append(f"Confidence: <code>{confidence}</code>")
    if rationale:
        lines.append(f"Rationale: {rationale}")
    lines.append("")
    lines.append("Action: <b>APPROVE</b> / <b>REJECT</b>")
    return "\n".join(lines)


def info(title: str, details: list[str], action: str = "none") -> str:
    lines = [f"📊 <b>{title}</b>"]
    for d in details:
        lines.append(d)
    lines.append(f"Action: {action}")
    return "\n".join(lines)


def snapshot(items: list[tuple[str, str]], summary: str = "", action: str = "none") -> str:
    lines = ["📊 <b>MARKET SNAPSHOT</b>"]
    for label, value in items:
        lines.append(f"{label}: <code>{value}</code>")
    if summary:
        lines.append(f"Summary: {summary}")
    lines.append(f"Action: {action}")
    return "\n".join(lines)


def ops_result(command: str, status: str, details: str = "") -> str:
    lines = [
        "✅ <b>OPS RESULT</b>",
        f"Command: <code>{command}</code>",
        f"Status: <b>{status}</b>",
    ]
    if details:
        lines.append(f"Details: {details}")
    return "\n".join(lines)


def error(command: str, reason: str) -> str:
    return (
        f"⚠️ <b>Command error</b>\n"
        f"Command: <code>{command}</code>\n"
        f"Reason: {reason}"
    )


def routes_summary(channels: dict[str, str]) -> str:
    lines = ["🗺 <b>Telegram routes</b>"]
    for ch, desc in channels.items():
        lines.append(f"• <code>{ch:10s}</code> → {desc}")
    return "\n".join(lines)


def help_text(commands: list[tuple[str, str]]) -> str:
    lines = ["<b>Available commands</b>"]
    for cmd, desc in commands:
        lines.append(f"• <code>{cmd:15s}</code> {desc}")
    return "\n".join(lines)


def route_test_result(channel: str, ok: bool, duration_ms: float) -> str:
    status_icon = "✅" if ok else "❌"
    return (
        f"{status_icon} <b>Route test</b>\n"
        f"Channel: <code>{channel}</code>\n"
        f"Result: <b>{'OK' if ok else 'FAIL'}</b>\n"
        f"Duration: <code>{duration_ms:.0f}ms</code>"
    )
