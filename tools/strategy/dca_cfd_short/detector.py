"""detector.py — Three CFD short signal options on D1 bars.

Signal A — RSI peak + lower low:
    max(RSI[-rsi_lookback:-1]) > rsi_thresh  (was overbought recently)
    AND  close < min(low[-1], low[-2])        (now breaking lower)

    Rationale: RSI > thresh and lower-low simultaneously is near-impossible
    (overbought implies price rising). We look for: RSI peaked above threshold
    in recent bars, then price starts failing — the reversal signal.

Signal B — ATR extension + CHOCH:
    (close - MA20) > ext_k × ATR14  AND  CHOCH confirmed (swing high + close breaks low)

Signal C — Both A AND B on same bar (highest conviction).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class Signal:
    idx: int                    # position in DataFrame
    date: pd.Timestamp
    close: float
    atr: float
    signal_type: str            # "A" | "B" | "C"


def detect_signal_a(
    df: pd.DataFrame,
    rsi_thresh: float = 70.0,
    rsi_lookback: int = 5,
) -> List[Signal]:
    """RSI peaked above thresh in recent bars, then close makes a lower low."""
    signals = []
    for i in range(rsi_lookback + 2, len(df)):
        row = df.iloc[i]
        rsi_window = df["rsi14"].iloc[i - rsi_lookback : i]
        rsi_peaked = rsi_window.max() > rsi_thresh if rsi_window.notna().any() else False
        lower_low  = (pd.notna(row["low_1"]) and pd.notna(row["low_2"])
                      and row["close"] < min(row["low_1"], row["low_2"]))
        if rsi_peaked and lower_low:
            signals.append(Signal(i, df.index[i], row["close"], row["atr14"], "A"))
    return signals


def detect_signal_b(df: pd.DataFrame, ext_k: float = 2.0) -> List[Signal]:
    signals = []
    for i in range(2, len(df)):
        row = df.iloc[i]
        if (pd.notna(row["ext_atr"]) and row["ext_atr"] > ext_k
                and row["choch"]):
            signals.append(Signal(i, df.index[i], row["close"], row["atr14"], "B"))
    return signals


def detect_signal_c(
    df: pd.DataFrame,
    rsi_thresh: float = 70.0,
    ext_k: float = 2.0,
) -> List[Signal]:
    """Both A and B conditions met on same bar."""
    a_idx = {s.idx for s in detect_signal_a(df, rsi_thresh)}
    b_idx = {s.idx for s in detect_signal_b(df, ext_k)}
    both = sorted(a_idx & b_idx)
    signals = []
    for i in both:
        row = df.iloc[i]
        signals.append(Signal(i, df.index[i], row["close"], row["atr14"], "C"))
    return signals


def detect_all(
    df: pd.DataFrame,
    rsi_thresh: float = 70.0,
    ext_k: float = 2.0,
) -> dict[str, List[Signal]]:
    return {
        "A": detect_signal_a(df, rsi_thresh),
        "B": detect_signal_b(df, ext_k),
        "C": detect_signal_c(df, rsi_thresh, ext_k),
    }
