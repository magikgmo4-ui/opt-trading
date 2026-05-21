"""indicators.py — Precompute all D1 reference levels for the tiered DCA."""
from __future__ import annotations

import pandas as pd


def _atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev_close).abs(),
        (df["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()


def _week_key(index: pd.DatetimeIndex) -> pd.Series:
    iso = index.isocalendar()
    return (iso["year"].astype(str) + "_" + iso["week"].astype(str).str.zfill(2)).values


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ATR(14) D1
    df["atr_d1"] = _atr(df, 14)

    # Week key for grouping
    df["_wk"] = _week_key(df.index)

    # W-2 close reference: close of two ISO weeks ago
    weekly_close = df.groupby("_wk")["close"].last()
    unique_weeks = list(weekly_close.index)
    w2_map = {w: weekly_close.get(unique_weeks[i - 2]) if i >= 2 else float("nan")
              for i, w in enumerate(unique_weeks)}
    df["ref_w2"] = df["_wk"].map(w2_map)

    # MA4w reference: 4-week (20-bar) rolling close mean
    df["ma4w"] = df["close"].rolling(20, min_periods=10).mean()

    # 4-week high (20-bar rolling max of high) — for medium correction
    df["high_4w"] = df["high"].rolling(20, min_periods=10).max()

    # 4-month high (80-bar rolling max of high) — for large correction
    df["high_4m"] = df["high"].rolling(80, min_periods=40).max()

    # Correction % from 4w high (negative = drawdown)
    df["corr_4w_pct"] = (df["close"] - df["high_4w"]) / df["high_4w"] * 100

    # Correction % from 4m high
    df["corr_4m_pct"] = (df["close"] - df["high_4m"]) / df["high_4m"] * 100

    # is_week_end: last trading bar of each ISO week (needed for L1 fallback)
    df["is_week_end"] = df["_wk"] != df["_wk"].shift(-1)
    df["is_week_end"] = df["is_week_end"].fillna(True)

    df = df.drop(columns=["_wk"])
    return df
