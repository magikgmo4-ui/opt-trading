"""indicators.py — D1 indicators for CFD short signal detection."""
from __future__ import annotations

import pandas as pd


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = gain / loss.replace(0, float("nan"))
    return 100 - 100 / (1 + rs)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    prev = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev).abs(),
        (df["low"] - prev).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rsi14"]   = rsi(df["close"], 14)
    df["atr14"]   = atr(df, 14)
    df["ma20"]    = df["close"].rolling(20, min_periods=10).mean()
    # Extension: how many ATRs above MA20
    df["ext_atr"] = (df["close"] - df["ma20"]) / df["atr14"]
    # Lower low: close < min(low of prior N bars)
    df["low_1"]   = df["low"].shift(1)
    df["low_2"]   = df["low"].shift(2)
    # Swing high: prior bar is a local 3-bar peak
    df["swing_high_bar"] = (
        (df["high"].shift(1) > df["high"].shift(2)) &
        (df["high"].shift(1) > df["high"])
    )
    # CHOCH on D1: swing high formed + current close breaks below low of swing bar
    df["choch"] = df["swing_high_bar"] & (df["close"] < df["low"].shift(1))
    return df
