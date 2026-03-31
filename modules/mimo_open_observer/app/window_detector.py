from __future__ import annotations

from datetime import datetime
from typing import Optional

from .models import Bar, RawEvent


TRIPLETS = [(0, 1, 2), (1, 2, 3), (2, 3, 4)]


def find_first_fvg(bars: list[Bar]) -> Optional[dict]:
    for a, b, c in TRIPLETS:
        b1, b2, b3 = bars[a], bars[b], bars[c]
        if b3.low > b1.high:
            return {
                "direction": "bullish",
                "fvg_top": b3.low,
                "fvg_bottom": b1.high,
                "signal_bar_index": c,
                "signal_ts": b3.ts_close,
                "price_at_signal": b3.close,
                "triplet": (a, b, c),
            }
        if b3.high < b1.low:
            return {
                "direction": "bearish",
                "fvg_top": b1.low,
                "fvg_bottom": b3.high,
                "signal_bar_index": c,
                "signal_ts": b3.ts_close,
                "price_at_signal": b3.close,
                "triplet": (a, b, c),
            }
    return None


def compute_sweep(bars: list[Bar], signal_bar_index: int, direction: str) -> dict:
    """
    V0 sweep rule (both sides, per pseudocode 06):

    sweep = True if any bar from index 0 through signal_bar_index (inclusive)
    breaches bar[0]'s high or bar[0]'s low.

    sweep_side:
      - "high"  → only bar[0].high was taken
      - "low"   → only bar[0].low was taken
      - "both"  → both extremes taken
      - "none"  → neither taken

    Note: for bullish FVG the signal bar's low is typically above bar[0]'s
    high (gap structure), so a high-side register at the signal bar itself
    is expected and structural.  The meaningful sweep test for bullish is
    whether the LOW side was taken before the signal.  Symmetrically for
    bearish.  This is documented but left as-is for V0.
    """
    ref_high = bars[0].high
    ref_low = bars[0].low
    check_bars = bars[: signal_bar_index + 1]

    swept_high = any(bar.high > ref_high for bar in check_bars)
    swept_low = any(bar.low < ref_low for bar in check_bars)

    if swept_high and swept_low:
        side = "both"
    elif swept_high:
        side = "high"
    elif swept_low:
        side = "low"
    else:
        side = "none"

    return {"sweep": swept_high or swept_low, "sweep_side": side}


def detect_window(
    symbol: str,
    window_open_ts: datetime,
    config: dict,
) -> RawEvent:
    from .data_provider import get_m1_bars
    from .utils_time import add_minutes

    scope_cfg = config.get("scope", {})
    bars_count = scope_cfg.get("bars", 5)
    window_close_ts = add_minutes(window_open_ts, bars_count)

    bars = get_m1_bars(symbol, window_open_ts, window_close_ts, config)

    window_type = config.get("windows", {}).get("open_1800", {}).get("type", "OPEN_1800")
    scope_type = scope_cfg.get("type", "M1x5")
    tz_name = config.get("timezone", "America/Montreal")
    weekday = window_open_ts.strftime("%A")

    event_id = f"{symbol}__OPEN_1800__{window_open_ts.isoformat()}__{scope_type}"

    if len(bars) < bars_count:
        return RawEvent(
            event_id=event_id,
            symbol=symbol,
            timezone=tz_name,
            window_type=window_type,
            window_open_ts=window_open_ts,
            scope=scope_type,
            weekday=weekday,
        )

    window_bars = bars[:bars_count]
    ref = window_bars[0]

    fvg = find_first_fvg(window_bars)

    if fvg is None:
        return RawEvent(
            event_id=event_id,
            symbol=symbol,
            timezone=tz_name,
            window_type=window_type,
            window_open_ts=window_open_ts,
            scope=scope_type,
            weekday=weekday,
            ref_open=ref.open,
            ref_high=ref.high,
            ref_low=ref.low,
            ref_close=ref.close,
        )

    sweep_info = compute_sweep(
        window_bars, fvg["signal_bar_index"], fvg["direction"]
    )

    return RawEvent(
        event_id=event_id,
        symbol=symbol,
        timezone=tz_name,
        window_type=window_type,
        window_open_ts=window_open_ts,
        scope=scope_type,
        weekday=weekday,
        ref_open=ref.open,
        ref_high=ref.high,
        ref_low=ref.low,
        ref_close=ref.close,
        fvg_detected=True,
        fvg_direction=fvg["direction"],
        fvg_top=fvg["fvg_top"],
        fvg_bottom=fvg["fvg_bottom"],
        fvg_created_at=window_bars[fvg["triplet"][2]].ts_close,
        signal_ts=fvg["signal_ts"],
        price_at_signal=fvg["price_at_signal"],
        sweep=sweep_info["sweep"],
        sweep_side=sweep_info["sweep_side"],
    )
