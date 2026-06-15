from __future__ import annotations

"""SPCX composite score scorer.

Pure function — no side effects, no I/O, no broker calls.
Consumes a list of signal_event.v1 dicts (e.g. produced by cdp_normalizer.py)
and returns a scored setup summary for the SPCX symbol.

Output contract:
    {
        "symbol":      "SPCX",
        "score":       int,           # 0-100
        "grade":       str,           # C / B / A / A+
        "events":      list[str],     # triggered event types, in weight order
        "bias":        str,           # bullish / bearish / mixed / neutral
        "setup_state": str,           # watch / active / invalidated
        "levels": {
            "price":    float | None,
            "vwap":     float | None,
            "orb_high": float | None,
            "orb_low":  float | None,
        },
        "risk_notes":  list[str],     # e.g. ["extended_above_vwap"]
        "invalidation": dict,         # level + note per invalidation trigger
        "monitor_only": True,         # always True — no execution
    }
"""

from typing import Any

# ---------------------------------------------------------------------------
# Score weights
# ---------------------------------------------------------------------------

_WEIGHTS: dict[str, int] = {
    "VWAP_RECLAIM": 25,
    "ORB_HIGH_BREAK": 25,
    "BREAK_174": 20,      # breakout_high from TradingView (SPCX_BREAK_174 / SPCX_BREAK_180)
    "VOLUME_SURGE": 15,
    "PREMARKET_GAP": 10,
    "SPACEX_WIRE": 5,
    "BOT_VISION_CONF": 5,
    "BREAKDOWN": 0,       # registre mais poids nul (bearish, non additif au score bullish)
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _grade(score: int) -> str:
    if score >= 80:
        return "A+"
    if score >= 60:
        return "A"
    if score >= 40:
        return "B"
    return "C"


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _setup_state(
    triggered: set[str],
    price: float | None,
    vwap: float | None,
    orb_high: float | None,
) -> str:
    """Determine setup_state from active signals and price levels.

    Precedence:
    1. invalidated -- VWAP_RECLAIM was triggered but price is now below VWAP
    2. active      -- price is above both ORB high and VWAP with both breaks confirmed
    3. watch       -- signals present but conditions for active/invalidated not met
    """
    if (
        "VWAP_RECLAIM" in triggered
        and price is not None
        and vwap is not None
        and price < vwap
    ):
        return "invalidated"

    if (
        "ORB_HIGH_BREAK" in triggered
        and "VWAP_RECLAIM" in triggered
        and price is not None
        and vwap is not None
        and orb_high is not None
        and price > orb_high
        and price > vwap
    ):
        return "active"

    return "watch"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def score_spcx(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute SPCX composite score from a list of signal_event.v1 dicts.

    Non-SPCX events are silently ignored.
    Repeated alerts for the same event type are deduplicated (last wins).
    No external calls are made.

    Args:
        events: List of signal_event.v1 dicts.

    Returns:
        Scored setup dict -- see module docstring for full contract.
    """
    # 1. Filter to SPCX
    spcx_events = [
        e for e in events
        if str(e.get("symbol", "")).upper() == "SPCX"
    ]

    # 2. Deduplicate: last occurrence per event type wins
    seen: dict[str, dict] = {}
    for e in spcx_events:
        event_type = str(e.get("event", "")).upper()
        if event_type:
            seen[event_type] = e

    # 3. Score -- iterate _WEIGHTS to preserve stable event ordering in output
    score = 0
    triggered: list[str] = []
    for event_type, weight in _WEIGHTS.items():
        if event_type in seen:
            score += weight
            triggered.append(event_type)

    # 4. Extract best-available levels from all deduplicated events
    price: float | None = None
    vwap: float | None = None
    orb_high: float | None = None
    orb_low: float | None = None
    bias_votes: list[str] = []

    for e in seen.values():
        p = _to_float(e.get("price"))
        v = _to_float(e.get("vwap"))
        oh = _to_float(e.get("orb_high"))
        ol = _to_float(e.get("orb_low"))
        if p is not None:
            price = p
        if v is not None:
            vwap = v
        if oh is not None:
            orb_high = oh
        if ol is not None:
            orb_low = ol
        b = e.get("bias", "")
        if b:
            bias_votes.append(str(b).lower())

    # 5. Bias consensus
    if not bias_votes:
        bias = "neutral"
    elif all(b == "bullish" for b in bias_votes):
        bias = "bullish"
    elif all(b == "bearish" for b in bias_votes):
        bias = "bearish"
    else:
        bias = "mixed"

    # 6. Risk notes
    risk_notes: list[str] = []
    if price is not None and vwap is not None and vwap != 0:
        distance_pct = (price - vwap) / vwap * 100
        if distance_pct > 5.0:
            risk_notes.append("extended_above_vwap")
        elif distance_pct < -5.0:
            risk_notes.append("extended_below_vwap")

    # 7. Setup state
    triggered_set = set(triggered)
    state = _setup_state(triggered_set, price, vwap, orb_high)

    # 8. Invalidation levels
    invalidation: dict[str, Any] = {}
    if "VWAP_RECLAIM" in triggered_set and vwap is not None:
        invalidation["vwap_loss"] = {
            "level": vwap,
            "note": "price closes below VWAP",
        }
    if "ORB_HIGH_BREAK" in triggered_set and orb_high is not None:
        invalidation["orb_loss"] = {
            "level": orb_high,
            "note": "price recedes below ORB high",
        }

    return {
        "symbol": "SPCX",
        "score": score,
        "grade": _grade(score),
        "events": triggered,
        "bias": bias,
        "setup_state": state,
        "levels": {
            "price": price,
            "vwap": vwap,
            "orb_high": orb_high,
            "orb_low": orb_low,
        },
        "risk_notes": risk_notes,
        "invalidation": invalidation,
        "monitor_only": True,
    }
