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
    "PREMARKET_HIGH_BREAK": 15,
    "PREMARKET_LOW_BREAK": 5,
    "PREMARKET_HIGH_REJECT": 0,
    "PREMARKET_LOW_REJECT": 0,
    "PREMARKET_GAP": 10,      # legacy alias kept for backward compatibility
    "GAP_OPEN_UP": 15,
    "GAP_OPEN_DOWN": 0,
    "GAP_FILL_STARTED": 10,
    "GAP_FILL_COMPLETED": 0,
    "SPACEX_WIRE": 5,
    "BOT_VISION_CONF": 5,
    "OPENING_EXHAUSTION": 0,
    "BREAKDOWN": 0,       # registre mais poids nul (bearish, non additif au score bullish)
}

# Phase 3 — Score component descriptors for SPCX opening session
_SCORE_COMPONENTS: dict[str, str] = {
    "Opening Strength": "GAP_OPEN_UP",
    "Opening Weakness": "GAP_OPEN_DOWN",
    "Gap Quality": "GAP_FILL_STARTED",
    "Gap Failure": "GAP_FILL_COMPLETED",
    "Premarket Acceptance": "PREMARKET_HIGH_BREAK",
    "Premarket Rejection": "PREMARKET_HIGH_REJECT",
    "VWAP Acceptance": "VWAP_RECLAIM",
    "Momentum Continuation": "ORB_HIGH_BREAK",
    "Exhaustion Risk": "OPENING_EXHAUSTION",
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


def score_spcx(
    events: list[dict[str, Any]],
    opening_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute SPCX composite score from a list of signal_event.v1 dicts.

    Non-SPCX events are silently ignored.
    Repeated alerts for the same event type are deduplicated (last wins).
    No external calls are made.

    When opening_metrics is provided (from compute_opening_metrics()), the
    output is enriched with opening session scores that are dynamic during
    the first 30 minutes of trading.

    Args:
        events: List of signal_event.v1 dicts.
        opening_metrics: Optional dict from compute_opening_metrics().

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

    # 3b. Opening session enrichment — dynamic score boost during first 30 min
    opening_components: dict[str, Any] = {}
    if opening_metrics is not None:
        opening_components = _compute_opening_components(opening_metrics, seen)
        score += opening_components.get("dynamic_boost", 0)
        score = min(score, 120)  # cap at 120 with boost

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

    # Add opening-specific risk notes
    if opening_metrics:
        rs = opening_metrics.get("risk_score", 0)
        if rs >= 70:
            risk_notes.append("high_risk_opening")
        elif rs >= 40:
            risk_notes.append("moderate_risk_opening")
        if opening_metrics.get("exhaustion_score", 0) >= 60:
            risk_notes.append("exhaustion_risk_high")
        if opening_metrics.get("opening_drive") == "down":
            risk_notes.append("gap_open_down")

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
    if "PREMARKET_HIGH_BREAK" in triggered_set and opening_metrics:
        pmh = opening_metrics.get("premarket_high")
        if pmh is not None:
            invalidation["premarket_loss"] = {
                "level": pmh,
                "note": "price recedes below premarket high",
            }

    result: dict[str, Any] = {
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

    # 9. Opening session enrichment (Phase 3)
    if opening_metrics:
        result["opening_metrics"] = opening_metrics
        result["opening_components"] = opening_components

    return result


def _compute_opening_components(
    metrics: dict[str, Any],
    seen: dict[str, dict],
) -> dict[str, Any]:
    """Compute opening session score components and dynamic boost.

    The score becomes dynamic during the first 30 minutes based on:
    - Opening Strength / Weakness
    - Gap Quality / Failure
    - Premarket Acceptance / Rejection
    - VWAP Acceptance
    - Momentum Continuation
    - Exhaustion Risk
    """
    triggered_set = set(seen.keys())
    boost = 0
    details: list[str] = []

    # Opening Strength
    if metrics.get("opening_drive") == "up" or "GAP_OPEN_UP" in triggered_set:
        boost += 10
        details.append("opening_strength")
    elif metrics.get("opening_drive") == "down" or "GAP_OPEN_DOWN" in triggered_set:
        boost += 0
        details.append("opening_weakness")

    # Gap Quality
    if "GAP_FILL_STARTED" in triggered_set:
        boost += 5
        details.append("gap_fill_quality")
    if "GAP_FILL_COMPLETED" in triggered_set:
        boost -= 5
        details.append("gap_failure")

    # Premarket Acceptance
    if "PREMARKET_HIGH_BREAK" in triggered_set:
        boost += 10
        details.append("premarket_acceptance")
    if "PREMARKET_HIGH_REJECT" in triggered_set:
        boost -= 5
        details.append("premarket_rejection")

    # VWAP Acceptance
    if "VWAP_RECLAIM" in triggered_set:
        boost += 10
        details.append("vwap_acceptance")

    # Momentum Continuation
    if "ORB_HIGH_BREAK" in triggered_set:
        boost += 10
        details.append("momentum_continuation")
    cs = metrics.get("continuation_score", 0)
    if cs >= 60:
        boost += 5
        details.append("strong_continuation")

    # Exhaustion Risk
    es = metrics.get("exhaustion_score", 0)
    if es >= 60:
        boost -= 10
        details.append("exhaustion_risk_high")
    if "OPENING_EXHAUSTION" in triggered_set:
        boost -= 15
        details.append("opening_exhaustion")

    component_scores: dict[str, Any] = {
        name: (event_type in triggered_set)
        for name, event_type in _SCORE_COMPONENTS.items()
    }

    return {
        "dynamic_boost": boost,
        "components": component_scores,
        "details": details,
    }
