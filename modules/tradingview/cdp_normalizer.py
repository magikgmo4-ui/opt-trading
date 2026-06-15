"""CDP TradingView alert normalizer — maps TradingView webhook payload to signal_event.v1.

Monitor-only, evidence-only. No order execution, no broker, no auto trading.
"""

from __future__ import annotations

from typing import Any

# Allowed events — exhaustive list
VALID_EVENTS = frozenset({
    "vwap_reclaim", "vwap_loss",
    "premarket_high_break", "premarket_low_loss",
    "orb_break_high", "orb_break_low",
    "relative_volume_gt_2", "relative_volume_gt_3",
    "volume_spike", "volume_on_breakout",
    "bos_bull", "bos_bear",
    "choch_bull", "choch_bear",
    "fvg_created", "fvg_filled",
    "liquidity_sweep_high", "liquidity_sweep_low",
    "breakout_high", "breakdown_low",
    "dxy_breakout", "dxy_breakdown",
    "vix_spike", "qqq_risk_on", "qqq_risk_off",
})


def normalize_cdp_alert(payload: dict) -> dict[str, Any]:
    """Normalize a TradingView CDP webhook payload into signal_event.v1 format.

    Args:
        payload: Raw TradingView webhook JSON with fields:
            ticker, interval, event, close, volume, time

    Returns:
        signal_event.v1 dict with monitor-only guard.
    """
    event = payload.get("event", payload.get("signal", ""))
    if event not in VALID_EVENTS:
        return {"ok": False, "error": f"unknown event: {event}", "valid_events": sorted(VALID_EVENTS)}

    normalized = {
        "source": "tradingview_cdp",
        "contract_class": "signal_event.v1",
        "symbol": payload.get("ticker", payload.get("symbol", "?")),
        "timeframe": str(payload.get("interval", "5")),
        "event": event,
        "price": payload.get("close", payload.get("price")),
        "volume": payload.get("volume"),
        "timestamp": payload.get("time", payload.get("timestamp", "")),
        "flags": {},
        "risk_mode": "monitor_only",
        "route": "data_center.signal_event",
    }

    # Set event-specific flag
    normalized["flags"][event] = True

    # Additional flags from payload
    for flag_key in ("vwap_reclaim", "vwap_loss", "orb_break", "bos", "choch", "fvg", "volume_spike",
                     "liquidity_sweep", "premarket_high_break", "breakout", "breakdown"):
        if flag_key in payload:
            normalized["flags"][flag_key] = bool(payload[flag_key])

    return {"ok": True, "payload": normalized}


def validate_monitor_only(payload: dict) -> dict:
    """Guard: verify no execution-related fields are present."""
    forbidden = {"action", "order", "execute", "buy", "sell", "tp", "sl", "entry", "exit", "size", "qty"}
    found = forbidden & set(k.lower() for k in payload.keys())
    if found:
        return {"ok": False, "error": f"forbidden fields: {found}"}
    if payload.get("risk_mode") != "monitor_only":
        return {"ok": False, "error": f"risk_mode must be monitor_only, got: {payload.get('risk_mode')}"}
    return {"ok": True}
