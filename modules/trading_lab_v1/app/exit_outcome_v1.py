#!/usr/bin/env python3
"""
Deterministic exit outcome resolver for trading_lab_v1 virtual trades.

Given a trade (entry, sl, direction, rr_planned) and post-entry OHLCV candles,
scans each candle for TP or SL hit and returns a measurable outcome.

Conservative ambiguity rule: if TP and SL are both touched in the same candle
(e.g., a wide-range candle that engulfs both levels), result = 'loss'.
This avoids overstating performance on ambiguous data.
"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def calc_tp(entry: float, sl: float, rr: float, direction: str) -> float:
    """Return the take-profit price given entry, sl, rr and direction."""
    risk = abs(entry - sl)
    if direction == "bullish":
        return round(entry + risk * rr, 4)
    return round(entry - risk * rr, 4)


def resolve_exit_outcome(
    entry: float,
    sl: float,
    rr_planned: float,
    direction: str,
    post_candles: list[dict],
    max_bars: int = 60,
) -> dict:
    """
    Scan post-entry candles and return an outcome dict.

    Returns dict with keys:
      result         : 'win' | 'loss' | 'timeout'
      r_realized     : float or None (timeout → None)
      exit_price     : float or None
      exit_ts        : ISO str or None
      bars_held      : int
      outcome_reason : str
      tp             : float (calculated TP for reference)
    """
    tp = calc_tp(entry, sl, rr_planned, direction)
    scanned = post_candles[:max_bars]

    for i, candle in enumerate(scanned):
        if direction == "bullish":
            sl_hit = candle["low"] <= sl
            tp_hit = candle["high"] >= tp
        else:
            sl_hit = candle["high"] >= sl
            tp_hit = candle["low"] <= tp

        if sl_hit and tp_hit:
            return {
                "result": "loss",
                "r_realized": -1.0,
                "exit_price": sl,
                "exit_ts": candle["ts"].isoformat(timespec="seconds"),
                "bars_held": i + 1,
                "outcome_reason": "sl_tp_same_candle_conservative_loss",
                "tp": tp,
            }
        if tp_hit:
            return {
                "result": "win",
                "r_realized": rr_planned,
                "exit_price": tp,
                "exit_ts": candle["ts"].isoformat(timespec="seconds"),
                "bars_held": i + 1,
                "outcome_reason": "tp_hit",
                "tp": tp,
            }
        if sl_hit:
            return {
                "result": "loss",
                "r_realized": -1.0,
                "exit_price": sl,
                "exit_ts": candle["ts"].isoformat(timespec="seconds"),
                "bars_held": i + 1,
                "outcome_reason": "sl_hit",
                "tp": tp,
            }

    reason = "max_bars_reached" if len(scanned) >= max_bars else "no_post_entry_candles"
    return {
        "result": "timeout",
        "r_realized": None,
        "exit_price": None,
        "exit_ts": None,
        "bars_held": len(scanned),
        "outcome_reason": reason,
        "tp": tp,
    }


def get_post_entry_candles(all_rows: list[dict], entry_ts_str: str, tz_name: str) -> list[dict]:
    """Return all candles strictly after the entry timestamp."""
    entry_dt = datetime.fromisoformat(entry_ts_str)
    if entry_dt.tzinfo is None:
        entry_dt = entry_dt.replace(tzinfo=ZoneInfo(tz_name))
    return [r for r in all_rows if r["ts"] > entry_dt]
