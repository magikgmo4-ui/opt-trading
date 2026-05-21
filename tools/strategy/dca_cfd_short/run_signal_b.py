#!/usr/bin/env python3
"""run_signal_b.py — Signal B standalone with partial exit management.

Signal B: price extension > ext_k × ATR above MA20  +  CHOCH (swing high + break).

Exit management (partial, 3 tranches):
  Tranche 1 (1/3 position): TP1 = tp1_mult × SL_dist  (tightened, default 0.75)
    → at TP1 hit: close 1/3, move SL to breakeven on remainder
  Tranche 2 (1/3 position): TP2 = 2.0 × SL_dist
    → at TP2 hit: close another 1/3
  Tranche 3 (1/3 position): TP3 = 3.0 × SL_dist  (1:3 ratio on initial risk)
    → at TP3 hit: close final 1/3
  SL before TP1: close all at SL → full loss
  SL after TP1 (BE): close remainder at entry → neutral on remainder

CFD: 0.01 lot = 1 oz, leverage ×500.
  margin  = entry_price / 500   (per oz)
  pnl_usd = price_move × qty_oz

Usage:
    python tools/strategy/dca_cfd_short/run_signal_b.py \
        --d1-2020 data/market/xauusd_d1_2020_2023.csv \
        --m5-2024 data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_cfd_short
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_cfd_short.indicators import add_indicators
from tools.strategy.dca_cfd_short.detector import detect_signal_b
from tools.strategy.dca_spot.load_data import load_d1_canonical, load_m5_canonical, resample_to_d1

LEVERAGE = 500
QTY_OZ   = 1.0      # per tranche (1/3 of a 3-tranche position = 0.33 oz each)
TRANCHE  = QTY_OZ / 3.0


@dataclass
class TradeB:
    signal_date:   pd.Timestamp
    entry_date:    pd.Timestamp
    entry_price:   float
    sl_initial:    float     # SL before TP1
    sl_be:         float     # SL moved to BE after TP1 hit
    tp1_price:     float
    tp2_price:     float
    tp3_price:     float
    sl_dist:       float
    # Outcomes per tranche
    t1_exit:       str       # "SL" | "TP1" | "TIMEOUT"
    t1_exit_price: float
    t1_pnl_usd:   float
    t2_exit:       Optional[str]   # None if T1=SL (no T2 trade after SL)
    t2_exit_price: Optional[float]
    t2_pnl_usd:   Optional[float]
    t3_exit:       Optional[str]
    t3_exit_price: Optional[float]
    t3_pnl_usd:   Optional[float]
    # Aggregate
    total_pnl_usd: float
    bars_held:     int
    margin_req:    float


def _sim_tranche(
    df: pd.DataFrame,
    entry_idx: int,
    entry_price: float,
    sl: float,
    tp: float,
    max_bars: int,
    qty: float,
) -> tuple[str, float, float, int]:
    """Returns (exit_type, exit_price, pnl_usd, bars_held)."""
    n = len(df)
    for j in range(entry_idx + 1, min(entry_idx + 1 + max_bars, n)):
        bar = df.iloc[j]
        hi, lo = float(bar["high"]), float(bar["low"])
        sl_hit = hi >= sl
        tp_hit = lo <= tp
        if sl_hit and tp_hit:
            exit_p = sl
            return "SL", exit_p, (entry_price - exit_p) * qty, j - entry_idx
        elif sl_hit:
            return "SL", sl, (entry_price - sl) * qty, j - entry_idx
        elif tp_hit:
            return "TP", tp, (entry_price - tp) * qty, j - entry_idx
    last = min(entry_idx + max_bars, n - 1)
    exit_p = float(df.iloc[last]["close"])
    return "TIMEOUT", exit_p, (entry_price - exit_p) * qty, last - entry_idx


def simulate_signal_b(
    df: pd.DataFrame,
    signals,
    sl_atr_mult: float = 1.0,
    tp1_mult:    float = 0.75,
    max_bars:    int   = 20,
) -> List[TradeB]:
    trades = []
    n = len(df)

    for sig in signals:
        entry_idx = sig.idx + 1
        if entry_idx >= n:
            continue

        entry_bar   = df.iloc[entry_idx]
        entry_price = float(entry_bar["open"])
        sl_dist     = sl_atr_mult * sig.atr

        sl_init = entry_price + sl_dist        # initial SL (short: above entry)
        tp1     = entry_price - tp1_mult * sl_dist
        tp2     = entry_price - 2.0   * sl_dist
        tp3     = entry_price - 3.0   * sl_dist

        margin = entry_price / LEVERAGE        # per oz (3 tranches total)

        # ── Tranche 1: T1 (1/3) — exits at TP1 or initial SL ──────────────
        t1_type, t1_price, t1_pnl, t1_bars = _sim_tranche(
            df, entry_idx, entry_price, sl_init, tp1, max_bars, TRANCHE
        )

        t2_type = t2_price = t2_pnl = None
        t3_type = t3_price = t3_pnl = None
        bars_total = t1_bars

        if t1_type == "SL":
            # All tranches lost — no TP1 reached
            t2_pnl = (entry_price - sl_init) * TRANCHE   # same SL hit
            t3_pnl = (entry_price - sl_init) * TRANCHE
            t2_type, t2_price = "SL", sl_init
            t3_type, t3_price = "SL", sl_init
        else:
            # TP1 hit — SL on T2/T3 moves to breakeven (entry)
            sl_be = entry_price

            # ── Tranche 2: exits at TP2 or breakeven SL ─────────────────
            t2_type, t2_price, t2_pnl, t2_bars = _sim_tranche(
                df, entry_idx + t1_bars, entry_price, sl_be, tp2, max_bars, TRANCHE
            )
            bars_total = max(bars_total, t1_bars + t2_bars)

            # ── Tranche 3: exits at TP3 or breakeven SL ─────────────────
            t3_start = entry_idx + t1_bars if t2_type != "TIMEOUT" else entry_idx + t1_bars
            t3_type, t3_price, t3_pnl, t3_bars = _sim_tranche(
                df, entry_idx + t1_bars, entry_price, sl_be, tp3, max_bars, TRANCHE
            )
            bars_total = max(bars_total, t1_bars + t3_bars)

        total_pnl = round(t1_pnl + (t2_pnl or 0) + (t3_pnl or 0), 2)

        trades.append(TradeB(
            signal_date   = sig.date,
            entry_date    = df.index[entry_idx],
            entry_price   = round(entry_price, 3),
            sl_initial    = round(sl_init, 3),
            sl_be         = round(entry_price, 3),
            tp1_price     = round(tp1, 3),
            tp2_price     = round(tp2, 3),
            tp3_price     = round(tp3, 3),
            sl_dist       = round(sl_dist, 2),
            t1_exit       = t1_type,
            t1_exit_price = round(t1_price, 3),
            t1_pnl_usd    = round(t1_pnl, 2),
            t2_exit       = t2_type,
            t2_exit_price = round(t2_price, 3) if t2_price else None,
            t2_pnl_usd    = round(t2_pnl, 2)   if t2_pnl  else None,
            t3_exit       = t3_type,
            t3_exit_price = round(t3_price, 3) if t3_price else None,
            t3_pnl_usd    = round(t3_pnl, 2)   if t3_pnl  else None,
            total_pnl_usd = total_pnl,
            bars_held     = bars_total,
            margin_req    = round(margin * 3, 2),  # 3 tranches total margin
        ))

    return trades


def print_summary(trades: List[TradeB], tp1_mult: float, sl_atr_mult: float) -> None:
    n = len(trades)
    if not n:
        print("  no trades")
        return

    n_full_sl = sum(1 for t in trades if t.t1_exit == "SL")
    n_tp1     = sum(1 for t in trades if t.t1_exit == "TP")
    n_tp2_hit = sum(1 for t in trades if t.t2_exit == "TP")
    n_tp3_hit = sum(1 for t in trades if t.t3_exit == "TP")
    n_be_sl   = sum(1 for t in trades if t.t1_exit == "TP"
                    and (t.t2_exit in ("SL", "TIMEOUT") or t.t3_exit in ("SL", "TIMEOUT")))

    total_pnl    = sum(t.total_pnl_usd for t in trades)
    avg_pnl      = total_pnl / n
    avg_sl_dist  = sum(t.sl_dist for t in trades) / n
    avg_bars     = sum(t.bars_held for t in trades) / n
    avg_margin   = sum(t.margin_req for t in trades) / n

    wins  = [t for t in trades if t.total_pnl_usd > 0]
    losses= [t for t in trades if t.total_pnl_usd <= 0]
    wr    = len(wins) / n * 100
    avg_w = sum(t.total_pnl_usd for t in wins)   / len(wins)   if wins   else 0
    avg_l = sum(t.total_pnl_usd for t in losses) / len(losses) if losses else 0
    exp   = wr / 100 * avg_w + (1 - wr / 100) * avg_l

    print(f"\n── SIGNAL B  (sl={sl_atr_mult}×ATR  tp1={tp1_mult}×risk  tp2=2×risk  tp3=3×risk) ──")
    print(f"  n_signals           : {n}  (~{n/5:.1f}/year over 5 years)")
    print(f"  Full SL (before TP1): {n_full_sl} ({n_full_sl/n*100:.1f}%)")
    print(f"  TP1 reached         : {n_tp1}  ({n_tp1/n*100:.1f}%)  → SL moves to BE")
    print(f"    of which TP2 hit  : {n_tp2_hit} ({n_tp2_hit/n_tp1*100:.1f}% of TP1 hits)" if n_tp1 else "")
    print(f"    of which TP3 hit  : {n_tp3_hit} ({n_tp3_hit/n_tp1*100:.1f}% of TP1 hits)" if n_tp1 else "")
    print(f"  Win rate (total PnL > 0): {wr:.1f}%")
    print(f"  Avg win   : ${avg_w:.2f}  |  Avg loss : ${avg_l:.2f}")
    print(f"  Expectancy/trade    : ${exp:.2f}")
    print(f"  Total PnL (5y, 1oz) : ${total_pnl:.2f}")
    print(f"  Avg SL distance     : {avg_sl_dist:.1f} pts  (= avg SL cost ${avg_sl_dist:.2f}/trade on 1oz)")
    print(f"  Avg bars held       : {avg_bars:.1f} D1 bars")
    print(f"  Margin/trade (3oz)  : ${avg_margin:.2f}  (entry/500 × 3 tranches)")
    print(f"  Capital to cover 3 consecutive full SL: ${avg_sl_dist * 3:.0f}")
    print(f"  at 20% reserve → min total capital : ${avg_sl_dist * 3 / 0.20:.0f}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d1-2020", help="D1 CSV 2020-2023")
    parser.add_argument("--m5-2024", help="M5 CSV 2024-2025")
    parser.add_argument("--out",     required=True)
    parser.add_argument("--ext-k",   type=float, default=2.0)
    parser.add_argument("--sl-atr",  type=float, default=1.0)
    parser.add_argument("--tp1-mult",type=float, default=0.75,
                        help="TP1 = tp1_mult × SL_dist (default 0.75, tighter than 1:1)")
    parser.add_argument("--max-bars",type=int,   default=20)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load] D1 data")
    frames = []
    if args.d1_2020:
        df2 = load_d1_canonical(args.d1_2020)
        frames.append(df2[["open", "high", "low", "close", "volume"]])
        print(f"  2020-2023: {len(df2)} bars")
    if args.m5_2024:
        dfm = load_m5_canonical(args.m5_2024)
        df4 = resample_to_d1(dfm)
        frames.append(df4[["open", "high", "low", "close", "volume"]])
        print(f"  2024-2025: {len(df4)} bars")
    df = pd.concat(frames).sort_index()
    df = df[~df.index.duplicated(keep="first")]
    print(f"  combined : {len(df)} bars  ({df.index[0].date()} → {df.index[-1].date()})")

    print("[indicators]")
    df = add_indicators(df)

    print(f"[detect signal B]  ext_k={args.ext_k}")
    signals = detect_signal_b(df, ext_k=args.ext_k)
    print(f"  {len(signals)} occurrences")

    trades = simulate_signal_b(
        df, signals,
        sl_atr_mult=args.sl_atr,
        tp1_mult=args.tp1_mult,
        max_bars=args.max_bars,
    )

    print_summary(trades, args.tp1_mult, args.sl_atr)

    # Trade log
    rows = []
    for t in trades:
        rows.append({
            "signal_date":   t.signal_date.date(),
            "entry_date":    t.entry_date.date(),
            "entry_price":   t.entry_price,
            "sl_initial":    t.sl_initial,
            "tp1":           t.tp1_price,
            "tp2":           t.tp2_price,
            "tp3":           t.tp3_price,
            "sl_dist_pts":   t.sl_dist,
            "t1_exit":       t.t1_exit,
            "t1_price":      t.t1_exit_price,
            "t1_pnl_usd":    t.t1_pnl_usd,
            "t2_exit":       t.t2_exit,
            "t2_price":      t.t2_exit_price,
            "t2_pnl_usd":    t.t2_pnl_usd,
            "t3_exit":       t.t3_exit,
            "t3_price":      t.t3_exit_price,
            "t3_pnl_usd":    t.t3_pnl_usd,
            "total_pnl_usd": t.total_pnl_usd,
            "bars_held":     t.bars_held,
            "margin_usd":    t.margin_req,
        })
    df_out = pd.DataFrame(rows)
    csv_path = out_dir / "signal_b_trades.csv"
    df_out.to_csv(csv_path, index=False)
    print(f"\n[out] {csv_path}")

    # Per-trade detail
    print("\n── TRADE DETAIL ─────────────────────────────────────────────────────")
    print(df_out[[
        "entry_date", "entry_price", "sl_initial", "tp1", "tp3",
        "t1_exit", "t2_exit", "t3_exit", "total_pnl_usd", "bars_held"
    ]].to_string(index=False))

    # TP1 sensitivity
    print("\n── TP1 SENSITIVITY (sl=1×ATR, tp3 always 3×risk) ───────────────────")
    print(f"  {'tp1_mult':>10}  {'SL%':>6}  {'TP1%':>6}  {'WR%':>6}  {'exp/trade':>10}  {'total_5y':>10}")
    for mult in [0.5, 0.75, 1.0, 1.5]:
        t2 = simulate_signal_b(df, signals, sl_atr_mult=args.sl_atr,
                                tp1_mult=mult, max_bars=args.max_bars)
        n = len(t2)
        if not n:
            continue
        n_sl  = sum(1 for t in t2 if t.t1_exit == "SL")
        n_tp1 = sum(1 for t in t2 if t.t1_exit == "TP")
        wins  = [t for t in t2 if t.total_pnl_usd > 0]
        losses= [t for t in t2 if t.total_pnl_usd <= 0]
        wr    = len(wins) / n * 100
        avg_w = sum(t.total_pnl_usd for t in wins)   / len(wins)   if wins   else 0
        avg_l = sum(t.total_pnl_usd for t in losses) / len(losses) if losses else 0
        exp   = wr / 100 * avg_w + (1 - wr / 100) * avg_l
        total = sum(t.total_pnl_usd for t in t2)
        print(f"  {mult:>10.2f}  {n_sl/n*100:>6.1f}  {n_tp1/n*100:>6.1f}  "
              f"{wr:>6.1f}  {exp:>10.2f}  {total:>10.2f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
