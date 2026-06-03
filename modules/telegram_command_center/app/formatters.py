"""Standardized message formatters per Telegram channel.

Each formatter returns short, actionable plain-text messages suitable for mobile Telegram.
"""
from __future__ import annotations
from typing import Any


def alert(title: str, source: str, status: str, impact: str, action: str) -> str:
    return (
        f"🔴 ALERT: {title}\n"
        f"Source: {source}\n"
        f"Status: {status}\n"
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
        "🟡 DECISION REQUIRED",
        f"Asset: {asset}",
        f"Direction: {direction}",
        f"Entry: {entry}",
        f"SL: {sl}",
        f"TP: {tp_line}",
    ]
    if confidence:
        lines.append(f"Confidence: {confidence}")
    if rationale:
        lines.append(f"Rationale: {rationale}")
    lines.append("")
    lines.append("Action: APPROVE / REJECT")
    return "\n".join(lines)


def info(title: str, details: list[str], action: str = "none") -> str:
    lines = [f"📊 {title}"]
    for d in details:
        lines.append(d)
    lines.append(f"Action: {action}")
    return "\n".join(lines)


def snapshot(items: list[tuple[str, str]], summary: str = "", action: str = "none") -> str:
    lines = ["📊 MARKET SNAPSHOT"]
    for label, value in items:
        lines.append(f"{label}: {value}")
    if summary:
        lines.append(f"Summary: {summary}")
    lines.append(f"Action: {action}")
    return "\n".join(lines)


def ops_result(command: str, status: str, details: str = "") -> str:
    lines = [
        "✅ OPS RESULT",
        f"Command: {command}",
        f"Status: {status}",
    ]
    if details:
        lines.append(f"Details: {details}")
    return "\n".join(lines)


def error(command: str, reason: str) -> str:
    return (
        f"⚠️ Command error\n"
        f"Command: {command}\n"
        f"Reason: {reason}"
    )


def routes_summary(channels: dict[str, str]) -> str:
    lines = ["🗺 Telegram routes"]
    for ch, desc in channels.items():
        lines.append(f"- {ch:10s} -> {desc}")
    return "\n".join(lines)


def help_text(commands: list[tuple[str, str]]) -> str:
    lines = ["Available commands"]
    for cmd, desc in commands:
        lines.append(f"- {cmd:15s} {desc}")
    return "\n".join(lines)


def route_test_result(channel: str, ok: bool, duration_ms: float) -> str:
    status_icon = "✅" if ok else "❌"
    return (
        f"{status_icon} Route test\n"
        f"Channel: {channel}\n"
        f"Result: {'OK' if ok else 'FAIL'}\n"
        f"Duration: {duration_ms:.0f}ms"
    )
