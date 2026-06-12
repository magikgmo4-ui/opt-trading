from __future__ import annotations


def render_telegram_message(snapshot: dict) -> str:
    asset = snapshot.get("asset", {})
    tech = snapshot.get("technical", {})
    scores = snapshot.get("scores", {})
    alerts = snapshot.get("alerts", [])
    return "\n".join([
        f"[SPACEX SUPER DESK] {asset.get('symbol', 'SPCX')}",
        f"Mode: {snapshot.get('mode', 'monitor_only')}",
        f"Price: {tech.get('price')}",
        f"IPO gap: {tech.get('ipo_gap_pct')}%",
        f"Trade ready: {scores.get('trade_ready_score')}",
        f"Accumulation: {scores.get('accumulation_score')}",
        f"Setup: {scores.get('selected_setup')}",
        f"Alerts: {', '.join(a.get('event', '?') for a in alerts) if alerts else 'none'}",
        "No auto-order. Manual decision only.",
    ])
