"""indicators.py — VWAP, ATR, session flags, ORB range."""
from __future__ import annotations

import numpy as np
import pandas as pd


def add_session_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Tag each bar with its trading session (UTC-based)."""
    hour = df.index.hour
    minute = df.index.minute
    t = hour * 60 + minute

    conditions = [
        (t >= 8 * 60) & (t < 12 * 60),   # London
        (t >= 13 * 60 + 30) & (t < 16 * 60),  # Overlap
        (t >= 16 * 60) & (t < 21 * 60),   # NY
        (t >= 23 * 60) | (t < 2 * 60),    # Asia
    ]
    choices = ["london", "overlap", "ny", "asia"]
    df = df.copy()
    df["session"] = np.select(conditions, choices, default="off")
    return df


def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
    """Cumulative VWAP reset per session."""
    df = df.copy()
    typical = (df["high"] + df["low"] + df["close"]) / 3
    df["_tp_vol"] = typical * df["volume"].replace(0, 1)
    df["_cum_tpvol"] = df.groupby(df["session"])["_tp_vol"].cumsum()
    df["_cum_vol"] = df.groupby(df["session"])["volume"].transform(
        lambda x: x.replace(0, 1).cumsum()
    )
    df["vwap"] = df["_cum_tpvol"] / df["_cum_vol"]
    df = df.drop(columns=["_tp_vol", "_cum_tpvol", "_cum_vol"])
    return df


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """ATR(period) using Wilder's smoothing."""
    df = df.copy()
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift(1)).abs()
    lc = (df["low"] - df["close"].shift(1)).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    df["atr"] = tr.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    return df


def add_orb(df: pd.DataFrame, orb_minutes: int = 30) -> pd.DataFrame:
    """Opening Range high/low over first orb_minutes of each session."""
    df = df.copy()
    df["orb_high"] = float("nan")
    df["orb_low"] = float("nan")
    df["orb_complete"] = False

    session_starts = {"london": (8, 0), "ny": (13, 30)}

    for sess, (h, m) in session_starts.items():
        mask_sess = df["session"].isin([sess, "overlap"])
        sess_dates = df[mask_sess].index.normalize().unique()
        for date in sess_dates:
            start = pd.Timestamp(date.year, date.month, date.day, h, m, tz="UTC")
            end = start + pd.Timedelta(minutes=orb_minutes)
            orb_mask = (df.index >= start) & (df.index < end) & (df["session"].isin([sess, "overlap"]))
            post_mask = (df.index >= end) & (df.index.normalize() == date) & (df["session"].isin([sess, "overlap", "ny"]))
            if orb_mask.sum() == 0:
                continue
            orb_h = df.loc[orb_mask, "high"].max()
            orb_l = df.loc[orb_mask, "low"].min()
            df.loc[post_mask, "orb_high"] = orb_h
            df.loc[post_mask, "orb_low"] = orb_l
            df.loc[post_mask, "orb_complete"] = True

    return df


def add_swing_points(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Local swing high/low over 2*n+1 window."""
    df = df.copy()
    df["swing_high"] = df["high"] == df["high"].rolling(2 * n + 1, center=True).max()
    df["swing_low"] = df["low"] == df["low"].rolling(2 * n + 1, center=True).min()
    return df


def add_all(df: pd.DataFrame, orb_minutes: int = 30, atr_period: int = 14, swing_n: int = 5) -> pd.DataFrame:
    df = add_session_flag(df)
    df = add_vwap(df)
    df = add_atr(df, period=atr_period)
    df = add_orb(df, orb_minutes=orb_minutes)
    df = add_swing_points(df, n=swing_n)
    return df
