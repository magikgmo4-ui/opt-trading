from __future__ import annotations

"""Opening Session Metrics — computed from signal_event.v1 CDP events.

Pure computation (no I/O). Consumes a list of signal_event.v1 dicts filtered to
SPCX and produces:

    opening_metrics: dict with keys:
        opening_gap_pct, premarket_range, premarket_high, premarket_low,
        opening_drive, first5m_range, first15m_range,
        relative_volume_1m, relative_volume_5m, relative_volume_15m,
        distance_vwap_pct, distance_premarket_high_pct, distance_orb_pct,
        extension_pct, risk_score, continuation_score, exhaustion_score

All derived from event metadata. Callable as pure function.
"""

from typing import Any


def compute_opening_metrics(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute opening session metrics from SPCX CDP events.

    Args:
        events: List of signal_event.v1 dicts (already filtered to SPCX).

    Returns:
        Dict of computed metrics. All values are float or None.
    """
    # Extract price levels from events
    price: float | None = None
    vwap: float | None = None
    orb_high: float | None = None
    orb_low: float | None = None
    premarket_high: float | None = None
    premarket_low: float | None = None
    prev_close: float | None = None
    open_price: float | None = None

    triggered: set[str] = set()

    for e in events:
        event_type = str(e.get("event", "")).upper()
        if event_type:
            triggered.add(event_type)

        flags: dict = e.get("flags") or {}

        p = _to_float(e.get("price"))
        v = _to_float(e.get("vwap")) or _to_float(flags.get("vwap"))
        oh = _to_float(e.get("orb_high")) or _to_float(flags.get("orb_high"))
        ol = _to_float(e.get("orb_low")) or _to_float(flags.get("orb_low"))

        if p is not None:
            price = p
        if v is not None:
            vwap = v
        if oh is not None:
            orb_high = oh
        if ol is not None:
            orb_low = ol

        # Extract premarket levels from flags
        pmh = _to_float(flags.get("premarket_high"))
        pml = _to_float(flags.get("premarket_low"))
        pc = _to_float(flags.get("prev_close"))
        op = _to_float(flags.get("open_price"))

        if pmh is not None:
            premarket_high = pmh
        if pml is not None:
            premarket_low = pml
        if pc is not None:
            prev_close = pc
        if op is not None:
            open_price = op

    # Opening Gap %
    opening_gap_pct: float | None = None
    if prev_close is not None and open_price is not None and prev_close != 0:
        opening_gap_pct = round((open_price - prev_close) / prev_close * 100, 4)
    elif prev_close is not None and price is not None and prev_close != 0:
        opening_gap_pct = round((price - prev_close) / prev_close * 100, 4)

    # Premarket range
    premarket_range: float | None = None
    if premarket_high is not None and premarket_low is not None:
        premarket_range = round(premarket_high - premarket_low, 4)

    # Opening drive (first move direction)
    opening_drive: str | None = None
    if opening_gap_pct is not None:
        if opening_gap_pct > 0:
            opening_drive = "up"
        elif opening_gap_pct < 0:
            opening_drive = "down"
        else:
            opening_drive = "flat"

    # First 5m / 15m range (from event flags if present)
    first5m_range: float | None = None
    first15m_range: float | None = None
    relative_volume_1m: float | None = None
    relative_volume_5m: float | None = None
    relative_volume_15m: float | None = None
    for e in events:
        f = e.get("flags") or {}
        rv1 = _to_float(f.get("rvol_1m"))
        rv5 = _to_float(f.get("rvol_5m"))
        rv15 = _to_float(f.get("rvol_15m"))
        f5 = _to_float(f.get("range_5m"))
        f15 = _to_float(f.get("range_15m"))
        if rv1 is not None:
            relative_volume_1m = rv1
        if rv5 is not None:
            relative_volume_5m = rv5
        if rv15 is not None:
            relative_volume_15m = rv15
        if f5 is not None:
            first5m_range = f5
        if f15 is not None:
            first15m_range = f15

    # --- Derived metrics ---

    # Distance VWAP %
    distance_vwap_pct: float | None = None
    if price is not None and vwap is not None and vwap != 0:
        distance_vwap_pct = round((price - vwap) / vwap * 100, 4)

    # Distance Premarket High %
    distance_premarket_high_pct: float | None = None
    if price is not None and premarket_high is not None and premarket_high != 0:
        distance_premarket_high_pct = round(
            (price - premarket_high) / premarket_high * 100, 4
        )

    # Distance ORB %
    distance_orb_pct: float | None = None
    if price is not None and orb_high is not None and orb_high != 0:
        distance_orb_pct = round((price - orb_high) / orb_high * 100, 4)
    elif price is not None and orb_low is not None and orb_low != 0:
        distance_orb_pct = round((price - orb_low) / orb_low * 100, 4)

    # Extension %
    extension_pct: float | None = distance_vwap_pct

    # Risk score (0-100)
    risk_score: int = 0
    if distance_vwap_pct is not None:
        if abs(distance_vwap_pct) > 5.0:
            risk_score += 40
        elif abs(distance_vwap_pct) > 3.0:
            risk_score += 20
    if opening_gap_pct is not None and abs(opening_gap_pct) > 2.0:
        risk_score += 20
    if "OPENING_EXHAUSTION" in triggered:
        risk_score += 30
    if "GAP_FILL_COMPLETED" in triggered:
        risk_score += 10
    risk_score = min(risk_score, 100)

    # Continuation score (0-100)
    continuation_score: int = 0
    if "VWAP_RECLAIM" in triggered:
        continuation_score += 25
    if "ORB_HIGH_BREAK" in triggered:
        continuation_score += 25
    if "PREMARKET_HIGH_BREAK" in triggered:
        continuation_score += 20
    if "GAP_OPEN_UP" in triggered and "GAP_FILL_STARTED" not in triggered:
        continuation_score += 10
    if relative_volume_15m is not None and relative_volume_15m > 1.5:
        continuation_score += 10
    indicator_count = sum(
        1 for t in ["VWAP_RECLAIM", "ORB_HIGH_BREAK", "PREMARKET_HIGH_BREAK", "GAP_OPEN_UP"]
        if t in triggered
    )
    if indicator_count >= 2:
        continuation_score += 10
    continuation_score = min(continuation_score, 100)

    # Exhaustion score (0-100)
    exhaustion_score: int = 0
    if "OPENING_EXHAUSTION" in triggered:
        exhaustion_score += 40
    if "GAP_FILL_COMPLETED" in triggered:
        exhaustion_score += 25
    if "PREMARKET_HIGH_REJECT" in triggered:
        exhaustion_score += 20
    if "PREMARKET_LOW_REJECT" in triggered:
        exhaustion_score += 15
    if distance_vwap_pct is not None and abs(distance_vwap_pct) > 4.0:
        exhaustion_score += 10
    if risk_score > 50:
        exhaustion_score += 10
    exhaustion_score = min(exhaustion_score, 100)

    return {
        "opening_gap_pct": opening_gap_pct,
        "premarket_range": premarket_range,
        "premarket_high": premarket_high,
        "premarket_low": premarket_low,
        "opening_drive": opening_drive,
        "first5m_range": first5m_range,
        "first15m_range": first15m_range,
        "relative_volume_1m": relative_volume_1m,
        "relative_volume_5m": relative_volume_5m,
        "relative_volume_15m": relative_volume_15m,
        "distance_vwap_pct": distance_vwap_pct,
        "distance_premarket_high_pct": distance_premarket_high_pct,
        "distance_orb_pct": distance_orb_pct,
        "extension_pct": extension_pct,
        "risk_score": risk_score,
        "continuation_score": continuation_score,
        "exhaustion_score": exhaustion_score,
    }


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
