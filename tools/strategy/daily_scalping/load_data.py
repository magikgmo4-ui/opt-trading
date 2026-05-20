"""load_data.py — Load and normalize OHLCV CSV files for backtest."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


_REQUIRED_COLS = {"timestamp", "open", "high", "low", "close"}


def load_ohlcv(path: str | Path, tz: str = "UTC") -> pd.DataFrame:
    """Load OHLCV CSV, parse timestamp, sort, set DatetimeIndex."""
    df = pd.read_csv(path)
    missing = _REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df = df.set_index("timestamp")
    if "volume" not in df.columns:
        df["volume"] = 0
    for col in ("open", "high", "low", "close"):
        df[col] = df[col].astype(float)
    return df


def merge_timeframes(
    df_exec: pd.DataFrame,
    df_ctx: pd.DataFrame,
    suffix_exec: str = "_m5",
    suffix_ctx: str = "_m15",
) -> pd.DataFrame:
    """Forward-fill context (M15) onto execution (M5) bars — no lookahead."""
    ctx_renamed = df_ctx.rename(columns={c: c + suffix_ctx for c in df_ctx.columns})
    merged = pd.merge_asof(
        df_exec.reset_index(),
        ctx_renamed.reset_index().rename(columns={"timestamp": "ts_ctx"}),
        left_on="timestamp",
        right_on="ts_ctx",
        direction="backward",
    )
    merged = merged.set_index("timestamp").drop(columns=["ts_ctx"], errors="ignore")
    return merged
