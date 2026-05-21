"""cycle_detector.py — Wyckoff 4-phase detection from price pivots + F&G confirmation.

Approach: price-pivot primary, F&G secondary.

1. Smooth close with 10-week EWM to remove noise
2. Detect local maxima / minima on smoothed series (window=20 bars = 4 weeks)
3. Between pivots:
   - Local min → local max : MARKUP (or ACCUMULATION if F&G low at bottom)
   - Local max → local min : MARKDOWN (or DISTRIBUTION if F&G high at top)
4. Accumulation = markup preceded by extreme fear (F&G avg < 35 at pivot bottom)
   Distribution = markdown preceded by extreme greed (F&G avg > 65 at pivot top)

This gives meaningful phases even in multi-year bull runs because pivots
are detected from actual price reversals, not sentiment alone.
"""
from __future__ import annotations

import pandas as pd
import numpy as np


def _smooth(series: pd.Series, span: int = 50) -> pd.Series:
    return series.ewm(span=span, min_periods=10, adjust=False).mean()


def _local_pivots(smooth: pd.Series, window: int = 20) -> tuple[list[int], list[int]]:
    """Return (local_min_idx, local_max_idx) lists."""
    vals = smooth.values
    n = len(vals)
    mins, maxs = [], []
    for i in range(window, n - window):
        segment = vals[i - window: i + window + 1]
        if vals[i] == segment.min():
            mins.append(i)
        if vals[i] == segment.max():
            maxs.append(i)
    # Deduplicate nearby pivots (merge within window/2)
    def dedup(idxs: list[int], gap: int) -> list[int]:
        if not idxs:
            return []
        out = [idxs[0]]
        for idx in idxs[1:]:
            if idx - out[-1] >= gap:
                out.append(idx)
        return out
    return dedup(mins, window // 2), dedup(maxs, window // 2)


def detect_phases(df: pd.DataFrame, fng: pd.DataFrame) -> pd.Series:
    smooth = _smooth(df["close"], span=50)
    local_mins, local_maxs = _local_pivots(smooth, window=20)

    # Build pivot sequence: (bar_idx, kind)  kind = "min" | "max"
    pivots = sorted(
        [(i, "min") for i in local_mins] + [(i, "max") for i in local_maxs],
        key=lambda x: x[0]
    )

    n = len(df)
    phases = ["accumulation"] * n

    if len(pivots) < 2:
        return pd.Series(phases, index=df.index, name="phase")

    def avg_fng_window(start: int, end: int) -> float:
        vals = fng["fng"].iloc[max(0, start): min(n, end + 1)]
        return float(vals.mean()) if not vals.isna().all() else 50.0

    def classify_segment(from_idx: int, to_idx: int,
                         from_kind: str, to_kind: str) -> str:
        fng_from = avg_fng_window(max(0, from_idx - 10), from_idx + 10)
        fng_to   = avg_fng_window(max(0, to_idx   - 10), to_idx   + 10)
        if from_kind == "min" and to_kind == "max":
            # Price rising
            return "accumulation" if fng_from < 35 else "markup"
        else:
            # Price falling
            return "distribution" if fng_to > 65 or fng_from > 65 else "markdown"

    # Fill phases between consecutive pivots
    for k in range(len(pivots) - 1):
        i0, kind0 = pivots[k]
        i1, kind1 = pivots[k + 1]
        label = classify_segment(i0, i1, kind0, kind1)
        for j in range(i0, i1):
            phases[j] = label

    # Fill tail (last pivot to end)
    last_i, last_kind = pivots[-1]
    tail_label = "accumulation" if last_kind == "min" else "distribution"
    for j in range(last_i, n):
        phases[j] = tail_label

    # Fill head (start to first pivot)
    first_i, first_kind = pivots[0]
    head_label = "accumulation" if first_kind == "min" else "markup"
    for j in range(0, first_i):
        phases[j] = head_label

    return pd.Series(phases, index=df.index, name="phase")


def phase_summary(phases: pd.Series, df: pd.DataFrame, fng: pd.DataFrame) -> pd.DataFrame:
    rows = []
    current = phases.iloc[0]
    start_idx = 0
    phase_list = phases.tolist()

    for i in range(1, len(phase_list) + 1):
        if i == len(phase_list) or phase_list[i] != current:
            end_idx = i - 1
            n_bars  = end_idx - start_idx + 1
            avg_fng = fng["fng"].iloc[start_idx:end_idx + 1].mean()
            rows.append({
                "phase":       current,
                "start":       df.index[start_idx].date(),
                "end":         df.index[end_idx].date(),
                "n_bars":      n_bars,
                "n_weeks":     round(n_bars / 5, 1),
                "price_start": round(float(df["close"].iloc[start_idx]), 2),
                "price_end":   round(float(df["close"].iloc[end_idx]), 2),
                "pct_chg":     round((df["close"].iloc[end_idx] -
                                      df["close"].iloc[start_idx]) /
                                     df["close"].iloc[start_idx] * 100, 1),
                "avg_fng":     round(float(avg_fng), 1) if not pd.isna(avg_fng) else None,
            })
            if i < len(phase_list):
                current   = phase_list[i]
                start_idx = i

    return pd.DataFrame(rows)
