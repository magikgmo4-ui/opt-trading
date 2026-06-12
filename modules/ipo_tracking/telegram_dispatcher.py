from __future__ import annotations
from typing import Any


def send_spacex_alert(snapshot: dict[str, Any], *, channel: str = "push") -> dict[str, Any]:
    try:
        from shared.telegram_channels import send_to_channel
    except ImportError:
        return {"ok": False, "error": "telegram_channels not available"}

    symbol = snapshot.get("symbol", "SPCX")
    scores = snapshot.get("scores", {})
    signals = snapshot.get("signals", [])

    lines = [
        f"<b>{symbol} Super Desk</b>",
        "",
    ]
    if snapshot.get("price"):
        lines.append(f"Price: ${snapshot['price']:,.2f}")
    if snapshot.get("gap_vs_ipo_pct") is not None:
        lines.append(f"Gap vs IPO: {snapshot['gap_vs_ipo_pct']:.1f}%")
    lines.append("")

    for k, v in scores.items():
        if v is not None:
            lines.append(f"{k}: <code>{v:.3f}</code>" if isinstance(v, (int, float)) else f"{k}: {v}")

    if signals:
        lines.append("")
        lines.append("<b>Signals:</b> " + " | ".join(signals))

    lines.append("")
    lines.append("<i>Monitor-only. No execution.</i>")

    return send_to_channel(
        channel=channel,
        message="\n".join(lines),
        source="spacex_super_desk",
        tags={"symbol": symbol, "mode": "monitor_only"},
    )


def send_spacex_threshold_alert(
    event: str,
    severity: str,
    *,
    channel: str = "alerts",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        from shared.telegram_channels import send_to_channel
    except ImportError:
        return {"ok": False, "error": "telegram_channels not available"}

    emoji = {"high": "\ud83d\udd34", "medium": "\ud83d\udfe1", "low": "\ud83d\udfe2"}.get(severity, "\u26a0\ufe0f")
    msg = f"{emoji} <b>{event}</b> (severity: {severity})"
    if extra:
        for k, v in extra.items():
            msg += f"\n{k}: {v}"

    return send_to_channel(
        channel=channel,
        message=msg,
        source="spacex_super_desk",
        tags={"event": event, "severity": severity, **(extra or {})},
    )
