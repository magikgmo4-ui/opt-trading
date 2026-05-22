"""simulator.py — CFD short trade simulation on D1 bars.

Entry : next bar's open after signal (no look-ahead).
SL    : entry + sl_atr_mult × ATR  (price goes up = loss for short)
TP1   : entry - 1 × SL_dist        (1:1)
TP2   : entry - 2 × SL_dist        (1:2)
TP3   : entry - 3 × SL_dist        (1:3 — stated target)

Bar resolution: check each subsequent bar's high (SL) and low (TP).
  - If bar.high >= SL and bar.low <= TP_k: SL wins (conservative).
  - TP levels checked in order: TP1 → TP2 → TP3.
  - Partial exit model: record first TP reached; full exit at SL or TP3.
  - max_bars_hold: close at market if no exit within N bars.

CFD mechanics (XAUUSD):
  0.01 lot = 1 oz.  Leverage x500.
  margin_req  = entry_price / leverage   (per oz)
  pnl_usd     = (entry - exit) × qty_oz  (positive for profitable short)
  sl_loss_usd = SL_dist × qty_oz
  tp3_gain_usd = TP_dist × qty_oz
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd

from tools.strategy.dca_cfd_short.detector import Signal


LEVERAGE = 500
QTY_OZ   = 1.0      # 0.01 lot = 1 oz


@dataclass
class Trade:
    signal_type: str
    signal_date: pd.Timestamp
    entry_date:  pd.Timestamp
    entry_price: float
    sl_price:    float
    tp1_price:   float
    tp2_price:   float
    tp3_price:   float
    exit_price:  float
    exit_type:   str        # "SL" | "TP1" | "TP2" | "TP3" | "TIMEOUT"
    bars_held:   int
    pnl_pts:     float      # + = profit (short made money as price fell)
    pnl_usd:     float
    margin_req:  float      # USD margin to open the trade
    sl_dist:     float      # SL distance in pts
    tp3_dist:    float      # TP3 distance in pts


def simulate_shorts(
    df: pd.DataFrame,
    signals: List[Signal],
    sl_atr_mult: float = 1.0,
    max_bars_hold: int = 20,
) -> List[Trade]:
    trades = []
    n = len(df)

    for sig in signals:
        entry_idx = sig.idx + 1
        if entry_idx >= n:
            continue

        entry_bar  = df.iloc[entry_idx]
        entry_price = float(entry_bar["open"])
        sl_dist    = sl_atr_mult * sig.atr
        tp_dist    = sl_dist * 3          # 1:3 ratio → TP3 = 3× risk

        sl  = entry_price + sl_dist       # short: SL above entry
        tp1 = entry_price - sl_dist       # 1:1
        tp2 = entry_price - 2 * sl_dist   # 1:2
        tp3 = entry_price - tp_dist       # 1:3

        exit_price = None
        exit_type  = "TIMEOUT"
        bars_held  = 0

        for j in range(entry_idx + 1, min(entry_idx + 1 + max_bars_hold, n)):
            bar = df.iloc[j]
            bars_held += 1
            bar_high = float(bar["high"])
            bar_low  = float(bar["low"])

            sl_hit  = bar_high >= sl
            tp1_hit = bar_low  <= tp1
            tp2_hit = bar_low  <= tp2
            tp3_hit = bar_low  <= tp3

            if sl_hit and tp3_hit:
                # Both in same bar → SL (conservative)
                exit_price = sl
                exit_type  = "SL"
                break
            elif sl_hit:
                exit_price = sl
                exit_type  = "SL"
                break
            elif tp3_hit:
                exit_price = tp3
                exit_type  = "TP3"
                break
            elif tp2_hit:
                exit_price = tp2
                exit_type  = "TP2"
                break
            elif tp1_hit:
                exit_price = tp1
                exit_type  = "TP1"
                break

        if exit_price is None:
            # Timeout: close at last bar's close
            last_idx   = min(entry_idx + max_bars_hold, n - 1)
            exit_price = float(df.iloc[last_idx]["close"])
            bars_held  = last_idx - entry_idx

        pnl_pts = entry_price - exit_price   # positive if price fell (short profit)
        pnl_usd = pnl_pts * QTY_OZ

        trades.append(Trade(
            signal_type  = sig.signal_type,
            signal_date  = sig.date,
            entry_date   = df.index[entry_idx],
            entry_price  = round(entry_price, 3),
            sl_price     = round(sl, 3),
            tp1_price    = round(tp1, 3),
            tp2_price    = round(tp2, 3),
            tp3_price    = round(tp3, 3),
            exit_price   = round(exit_price, 3),
            exit_type    = exit_type,
            bars_held    = bars_held,
            pnl_pts      = round(pnl_pts, 3),
            pnl_usd      = round(pnl_usd, 2),
            margin_req   = round(entry_price / LEVERAGE, 2),
            sl_dist      = round(sl_dist, 3),
            tp3_dist     = round(tp_dist, 3),
        ))

    return trades


def metrics(trades: List[Trade], label: str) -> dict:
    if not trades:
        return {"label": label, "n_signals": 0, "n_sl": 0, "pct_sl": 0,
                "n_tp1": 0, "pct_tp1": 0, "n_tp2": 0, "pct_tp2": 0,
                "n_tp3": 0, "pct_tp3": 0, "win_rate_pct": 0,
                "avg_win_usd": 0, "avg_loss_usd": 0, "expectancy_usd": 0,
                "total_pnl_usd": 0, "avg_pnl_usd": 0,
                "avg_sl_dist_pts": 0, "avg_tp3_dist_pts": 0,
                "avg_bars_held": 0, "avg_margin_usd": 0,
                "max_margin_usd": 0, "avg_sl_cost_usd": 0}

    n = len(trades)
    n_sl  = sum(1 for t in trades if t.exit_type == "SL")
    n_tp1 = sum(1 for t in trades if t.exit_type == "TP1")
    n_tp2 = sum(1 for t in trades if t.exit_type == "TP2")
    n_tp3 = sum(1 for t in trades if t.exit_type == "TP3")
    n_tmo = sum(1 for t in trades if t.exit_type == "TIMEOUT")

    total_pnl    = sum(t.pnl_usd for t in trades)
    avg_pnl      = total_pnl / n
    avg_sl_dist  = sum(t.sl_dist for t in trades) / n
    avg_tp3_dist = sum(t.tp3_dist for t in trades) / n
    avg_margin   = sum(t.margin_req for t in trades) / n
    max_margin   = max(t.margin_req for t in trades)
    avg_bars     = sum(t.bars_held for t in trades) / n

    wins  = [t for t in trades if t.pnl_usd > 0]
    losses = [t for t in trades if t.pnl_usd <= 0]
    avg_win  = sum(t.pnl_usd for t in wins) / len(wins)   if wins   else 0.0
    avg_loss = sum(t.pnl_usd for t in losses) / len(losses) if losses else 0.0
    win_rate = len(wins) / n * 100
    expectancy = win_rate / 100 * avg_win + (1 - win_rate / 100) * avg_loss

    # Capital adequacy: at 20% reserve on a $1 capital unit
    # Reserve = 0.2 × capital; max_simultaneous = 1 trade (no stacking in this model)
    # Required equity to absorb SL = avg_sl_dist × 1 oz
    avg_sl_usd = avg_sl_dist * QTY_OZ

    return {
        "label":          label,
        "n_signals":      n,
        "n_sl":           n_sl,
        "pct_sl":         round(n_sl  / n * 100, 1),
        "n_tp1":          n_tp1,
        "pct_tp1":        round(n_tp1 / n * 100, 1),
        "n_tp2":          n_tp2,
        "pct_tp2":        round(n_tp2 / n * 100, 1),
        "n_tp3":          n_tp3,
        "pct_tp3":        round(n_tp3 / n * 100, 1),
        "n_timeout":      n_tmo,
        "win_rate_pct":   round(win_rate, 1),
        "avg_win_usd":    round(avg_win, 2),
        "avg_loss_usd":   round(avg_loss, 2),
        "expectancy_usd": round(expectancy, 2),
        "total_pnl_usd":  round(total_pnl, 2),
        "avg_pnl_usd":    round(avg_pnl, 2),
        "avg_sl_dist_pts": round(avg_sl_dist, 1),
        "avg_tp3_dist_pts": round(avg_tp3_dist, 1),
        "avg_bars_held":  round(avg_bars, 1),
        "avg_margin_usd": round(avg_margin, 2),
        "max_margin_usd": round(max_margin, 2),
        "avg_sl_cost_usd": round(avg_sl_usd, 2),
    }
