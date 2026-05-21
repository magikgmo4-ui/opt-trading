"""simulator.py — Simulate SL/TP on bar data, compute result_R, MFE, MAE."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from .detectors import Setup


@dataclass
class TradeResult:
    setup: Setup
    score: int
    entry_price: float
    sl: float
    tp1: float
    tp2: float
    risk_R: float = 1.0
    result_R: float = 0.0
    mae_R: float = 0.0
    mfe_R: float = 0.0
    time_in_trade_bars: int = 0
    exit_reason: str = ""
    followed_plan: bool = True


_SMC_VARIANTS = {"SMC_SWEEP_ONLY", "COMBINED_SMC_ORB_VWAP"}
_ACTIVE_SESSIONS = {"london", "ny", "overlap"}


def simulate_trade(
    setup: Setup,
    score: int,
    df: pd.DataFrame,
    min_rr: float = 1.8,
    atr_sl_mult: float = 1.0,
    atr_tp_mult: float = 1.8,
    spread_pts: float = 0.03,
    slippage_pts: float = 0.01,
    max_bars: int = 48,
    min_score: int = 7,
) -> Optional[TradeResult]:
    """Simulate a single trade. Returns None if setup is filtered out."""
    if score < min_score:
        return None

    # SMC setups: only trade active sessions (london, ny, overlap)
    if setup.variant in _SMC_VARIANTS and setup.session not in _ACTIVE_SESSIONS:
        return None

    atr = setup.atr
    if atr <= 0:
        return None

    cost = spread_pts + slippage_pts
    direction = setup.direction
    sweep_extreme = setup.extra.get("sweep_extreme") if setup.extra else None

    if direction == "long":
        entry = setup.entry_price + cost
        # SL anchored below swept swing low when available; fallback to ATR-based
        if sweep_extreme is not None:
            sl = sweep_extreme - atr * 0.3
        else:
            sl = entry - atr * atr_sl_mult
        tp1 = entry + atr * atr_tp_mult
        tp2 = entry + atr * atr_tp_mult * 2
    else:
        entry = setup.entry_price - cost
        # SL anchored above swept swing high when available; fallback to ATR-based
        if sweep_extreme is not None:
            sl = sweep_extreme + atr * 0.3
        else:
            sl = entry + atr * atr_sl_mult
        tp1 = entry - atr * atr_tp_mult
        tp2 = entry - atr * atr_tp_mult * 2

    risk = abs(entry - sl)
    if risk <= 0:
        return None

    result = TradeResult(
        setup=setup, score=score,
        entry_price=entry, sl=sl, tp1=tp1, tp2=tp2, risk_R=risk,
    )

    # Walk forward bars from entry
    start_i = setup.entry_bar
    mae = 0.0
    mfe = 0.0

    for j in range(1, min(max_bars, len(df) - start_i)):
        bar = df.iloc[start_i + j]

        if direction == "long":
            exc = bar["low"] - entry
            pnl_low = exc / risk
            pnl_high = (bar["high"] - entry) / risk
            mae = min(mae, pnl_low)
            mfe = max(mfe, pnl_high)
            if bar["low"] <= sl:
                result.result_R = -1.0
                result.exit_reason = "SL"
                result.time_in_trade_bars = j
                break
            if bar["high"] >= tp1:
                result.result_R = atr_tp_mult
                result.exit_reason = "TP1"
                result.time_in_trade_bars = j
                break
        else:
            pnl_high = (entry - bar["high"]) / risk
            pnl_low = (entry - bar["low"]) / risk
            mae = min(mae, pnl_high)
            mfe = max(mfe, pnl_low)
            if bar["high"] >= sl:
                result.result_R = -1.0
                result.exit_reason = "SL"
                result.time_in_trade_bars = j
                break
            if bar["low"] <= tp1:
                result.result_R = atr_tp_mult
                result.exit_reason = "TP1"
                result.time_in_trade_bars = j
                break
    else:
        # Timeout — close at last bar
        last = df.iloc[min(start_i + max_bars, len(df) - 1)]
        if direction == "long":
            result.result_R = (last["close"] - entry) / risk
        else:
            result.result_R = (entry - last["close"]) / risk
        result.exit_reason = "TIMEOUT"
        result.time_in_trade_bars = max_bars

    result.mae_R = round(mae, 4)
    result.mfe_R = round(mfe, 4)
    result.result_R = round(result.result_R, 4)
    return result


def simulate_all(
    setups: List[Setup],
    scores: List[int],
    df: pd.DataFrame,
    **kwargs,
) -> List[TradeResult]:
    results = []
    for setup, score in zip(setups, scores):
        r = simulate_trade(setup, score, df, **kwargs)
        if r is not None:
            results.append(r)
    return results
