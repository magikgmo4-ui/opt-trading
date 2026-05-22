#!/usr/bin/env python3
"""run_eval.py — Compare CFD short signal options A / B / C on D1 XAUUSD.

Signal A : RSI(14) > 75 + close < min(low[-1], low[-2])
Signal B : extension > 2×ATR from MA20 + CHOCH confirmed
Signal C : A AND B simultaneously (highest conviction)

Each signal enters short at next bar open.
SL = entry + 1×ATR, TP1/TP2/TP3 = 1×/2×/3× risk (1:3 ratio at TP3).
CFD: 0.01 lot = 1 oz, leverage ×500.

Evaluates: hit rates, expectancy, capital/margin adequacy.

Usage:
    python tools/strategy/dca_cfd_short/run_eval.py \
        --d1-2020 data/market/xauusd_d1_2020_2023.csv \
        --m5-2024 data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_cfd_short
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_cfd_short.indicators import add_indicators
from tools.strategy.dca_cfd_short.detector import detect_all
from tools.strategy.dca_cfd_short.simulator import simulate_shorts, metrics

from tools.strategy.dca_spot.load_data import load_d1_canonical, load_m5_canonical, resample_to_d1


def load_combined(d1_path: str | None, m5_path: str | None) -> pd.DataFrame:
    frames = []
    if d1_path:
        df = load_d1_canonical(d1_path)
        frames.append(df[["open", "high", "low", "close", "volume"]])
        print(f"  2020-2023 : {len(df)} bars  ({df.index[0].date()} → {df.index[-1].date()})")
    if m5_path:
        df_m5 = load_m5_canonical(m5_path)
        df_d1 = resample_to_d1(df_m5)
        frames.append(df_d1[["open", "high", "low", "close", "volume"]])
        print(f"  2024-2025 : {len(df_d1)} bars  ({df_d1.index[0].date()} → {df_d1.index[-1].date()})")
    combined = pd.concat(frames).sort_index()
    combined = combined[~combined.index.duplicated(keep="first")]
    return combined


def print_comparison(results: list[dict]) -> None:
    cols = [
        "label", "n_signals",
        "pct_sl", "pct_tp1", "pct_tp2", "pct_tp3",
        "win_rate_pct", "expectancy_usd", "total_pnl_usd",
        "avg_sl_dist_pts", "avg_tp3_dist_pts", "avg_bars_held",
        "avg_margin_usd", "avg_sl_cost_usd",
    ]
    df = pd.DataFrame(results)[cols]
    print(df.to_string(index=False))


def print_capital_analysis(results: list[dict]) -> None:
    print("\n── CAPITAL & MARGIN ANALYSIS ────────────────────────────────────────")
    print("  CFD: 0.01 lot = 1 oz, leverage ×500")
    for r in results:
        if r["n_signals"] == 0:
            continue
        label = r["label"]
        margin = r["avg_margin_usd"]
        sl_cost = r["avg_sl_cost_usd"]
        freq_years = r["n_signals"] / 5  # ~5 years of data
        print(f"\n  [{label}]  n={r['n_signals']}  (~{freq_years:.1f} signals/year)")
        print(f"    margin/trade  : ${margin:.2f}  (entry / 500)")
        print(f"    max SL loss   : ${sl_cost:.2f} / trade  (1 oz × SL_dist)")
        print(f"    min capital needed to absorb 3 consecutive SL : "
              f"${sl_cost * 3:.2f}")
        print(f"    at 20% reserve: total capital needed = ${sl_cost * 3 / 0.20:.2f}")
        print(f"    verdict: {'MARGIN NEGLIGIBLE — only SL equity matters' if margin < 10 else 'margin meaningful'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d1-2020", help="D1 CSV 2020-2023 (yfinance)")
    parser.add_argument("--m5-2024", help="M5 CSV 2024-2025 (Dukascopy)")
    parser.add_argument("--out",     required=True)
    parser.add_argument("--rsi-thresh", type=float, default=75.0)
    parser.add_argument("--ext-k",      type=float, default=2.0)
    parser.add_argument("--sl-atr",     type=float, default=1.0,
                        help="SL = entry + sl_atr × ATR14")
    parser.add_argument("--max-bars",   type=int,   default=20)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load] D1 data")
    df = load_combined(args.d1_2020, args.m5_2024)
    print(f"  combined : {len(df)} D1 bars  "
          f"({df.index[0].date()} → {df.index[-1].date()})")

    print("[indicators]")
    df = add_indicators(df)

    print(f"[detect] RSI_thresh={args.rsi_thresh}  ext_k={args.ext_k}")
    signals = detect_all(df, rsi_thresh=args.rsi_thresh, ext_k=args.ext_k)
    for label, sigs in signals.items():
        print(f"  Signal {label}: {len(sigs)} occurrences")

    results = []
    all_trades = []
    for label, sigs in signals.items():
        trades = simulate_shorts(df, sigs, sl_atr_mult=args.sl_atr, max_bars_hold=args.max_bars)
        m = metrics(trades, label)
        results.append(m)
        for t in trades:
            all_trades.append({
                "signal":       label,
                "signal_date":  t.signal_date.date(),
                "entry_date":   t.entry_date.date(),
                "entry_price":  t.entry_price,
                "sl_price":     t.sl_price,
                "tp1_price":    t.tp1_price,
                "tp2_price":    t.tp2_price,
                "tp3_price":    t.tp3_price,
                "exit_price":   t.exit_price,
                "exit_type":    t.exit_type,
                "bars_held":    t.bars_held,
                "pnl_pts":      t.pnl_pts,
                "pnl_usd":      t.pnl_usd,
                "sl_dist":      t.sl_dist,
                "margin_req":   t.margin_req,
            })

    # Save trade log
    trades_df = pd.DataFrame(all_trades)
    csv_path = out_dir / "cfd_short_trades.csv"
    trades_df.to_csv(csv_path, index=False)
    print(f"\n[out] {csv_path}  ({len(trades_df)} trades)")

    # Comparison table
    print("\n── SIGNAL COMPARISON ────────────────────────────────────────────────")
    print(f"  SL_mult={args.sl_atr}×ATR  |  TP1=1×risk  TP2=2×risk  TP3=3×risk  "
          f"|  max_hold={args.max_bars} bars")
    print_comparison(results)

    # Per-signal trade list
    for label in ["A", "B", "C"]:
        sub = trades_df[trades_df["signal"] == label].copy()
        if sub.empty:
            continue
        print(f"\n── SIGNAL {label} — {len(sub)} trades ───────────────────────────────────")
        print(sub[["entry_date", "entry_price", "sl_price", "tp3_price",
                   "exit_type", "pnl_pts", "pnl_usd", "bars_held"]].to_string(index=False))

    # Capital analysis
    print_capital_analysis(results)

    # Sensitivity grid on SL multiplier
    print("\n── SL SENSITIVITY (sl_atr_mult: 0.5 / 1.0 / 1.5 / 2.0) ────────────")
    for label, sigs in signals.items():
        if not sigs:
            continue
        row = [f"  Signal {label}"]
        for mult in [0.5, 1.0, 1.5, 2.0]:
            t2 = simulate_shorts(df, sigs, sl_atr_mult=mult, max_bars_hold=args.max_bars)
            m2 = metrics(t2, "")
            n_sl = m2.get("pct_sl", 0)
            exp  = m2.get("expectancy_usd", 0)
            row.append(f"sl×{mult}: SL={n_sl}%  exp=${exp:.2f}")
        print("  |  ".join(row))

    return 0


if __name__ == "__main__":
    sys.exit(main())
