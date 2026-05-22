#!/usr/bin/env python3
"""run_cfd_grid.py — Exhaustive grid over all CFD short signal parameters.

Grid:
  Signal A: rsi_thresh × rsi_lookback × sl_atr × tp1_mult
  Signal B: ext_k × sl_atr × tp1_mult
  Signal C: rsi_thresh × ext_k × sl_atr × tp1_mult

Each combo evaluated on 3 periods: 2020-2023, 2024-2025, combined.
Partial-exit model (3 tranches): TP1=tp1_mult×risk, TP2=2×risk, TP3=3×risk.
After TP1 hit → SL moves to breakeven on T2/T3.

Usage:
    python tools/strategy/dca_cfd_short/run_cfd_grid.py \
        --d1-2020 data/market/xauusd_d1_2020_2023.csv \
        --m5-2024 data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_cfd_short
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_cfd_short.indicators import add_indicators
from tools.strategy.dca_cfd_short.detector import detect_signal_a, detect_signal_b, detect_signal_c
from tools.strategy.dca_cfd_short.run_signal_b import simulate_signal_b, TRANCHE
from tools.strategy.dca_spot.load_data import load_d1_canonical, load_m5_canonical, resample_to_d1

# ── Grid parameters ────────────────────────────────────────────────────────────
RSI_THRESHOLDS  = [65, 70, 75]
RSI_LOOKBACKS   = [3, 5, 7]
EXT_KS          = [1.5, 2.0, 2.5]
SL_ATRS         = [0.5, 1.0, 1.5]
TP1_MULTS       = [0.5, 0.75, 1.0]
MAX_BARS        = 20


def _metrics(trades, label: str, period: str, params: dict) -> dict:
    n = len(trades)
    if not n:
        return {"label": label, "period": period, **params, "n_signals": 0,
                "n_per_year": 0, "pct_full_sl": None, "pct_tp1": None,
                "pct_tp2": None, "pct_tp3": None, "pct_be_sl": None,
                "win_rate": None, "avg_win": None, "avg_loss": None,
                "expectancy": None, "total_pnl": None, "avg_sl_pts": None,
                "avg_bars": None}

    years = {"2020-2023": 4, "2024-2025": 2, "combined": 6}.get(period, 5)

    n_full_sl = sum(1 for t in trades if t.t1_exit == "SL")
    n_tp1     = sum(1 for t in trades if t.t1_exit == "TP")
    n_tp2     = sum(1 for t in trades if t.t2_exit == "TP")
    n_tp3     = sum(1 for t in trades if t.t3_exit == "TP")
    n_be_sl   = sum(1 for t in trades if t.t1_exit == "TP"
                    and t.t2_exit in ("SL", "TIMEOUT")
                    and t.t3_exit in ("SL", "TIMEOUT"))

    wins   = [t for t in trades if t.total_pnl_usd > 0]
    losses = [t for t in trades if t.total_pnl_usd <= 0]
    wr     = len(wins) / n * 100
    avg_w  = sum(t.total_pnl_usd for t in wins)   / len(wins)   if wins   else 0
    avg_l  = sum(t.total_pnl_usd for t in losses) / len(losses) if losses else 0
    exp    = wr / 100 * avg_w + (1 - wr / 100) * avg_l
    total  = sum(t.total_pnl_usd for t in trades)

    return {
        "label":       label,
        "period":      period,
        **params,
        "n_signals":   n,
        "n_per_year":  round(n / years, 1),
        "pct_full_sl": round(n_full_sl / n * 100, 1),
        "pct_tp1":     round(n_tp1     / n * 100, 1),
        "pct_tp2":     round(n_tp2     / n * 100, 1),
        "pct_tp3":     round(n_tp3     / n * 100, 1),
        "pct_be_sl":   round(n_be_sl   / n * 100, 1),
        "win_rate":    round(wr, 1),
        "avg_win":     round(avg_w, 2),
        "avg_loss":    round(avg_l, 2),
        "expectancy":  round(exp, 2),
        "total_pnl":   round(total, 2),
        "avg_sl_pts":  round(sum(t.sl_dist for t in trades) / n, 1),
        "avg_bars":    round(sum(t.bars_held for t in trades) / n, 1),
    }


def run_signal_a_grid(dfs: dict) -> list[dict]:
    rows = []
    combos = list(itertools.product(RSI_THRESHOLDS, RSI_LOOKBACKS, SL_ATRS, TP1_MULTS))
    total = len(combos) * len(dfs)
    done = 0
    for rsi_t, rsi_lb, sl_a, tp1_m in combos:
        params = {"rsi_thresh": rsi_t, "rsi_lookback": rsi_lb,
                  "ext_k": "-", "sl_atr": sl_a, "tp1_mult": tp1_m}
        for period, df in dfs.items():
            sigs = detect_signal_a(df, rsi_thresh=rsi_t, rsi_lookback=rsi_lb)
            trades = simulate_signal_b(df, sigs, sl_atr_mult=sl_a,
                                       tp1_mult=tp1_m, max_bars=MAX_BARS)
            rows.append(_metrics(trades, "A", period, params))
            done += 1
        if done % 30 == 0:
            print(f"  A: {done}/{total}", flush=True)
    return rows


def run_signal_b_grid(dfs: dict) -> list[dict]:
    rows = []
    combos = list(itertools.product(EXT_KS, SL_ATRS, TP1_MULTS))
    total = len(combos) * len(dfs)
    done = 0
    for ext_k, sl_a, tp1_m in combos:
        params = {"rsi_thresh": "-", "rsi_lookback": "-",
                  "ext_k": ext_k, "sl_atr": sl_a, "tp1_mult": tp1_m}
        for period, df in dfs.items():
            sigs = detect_signal_b(df, ext_k=ext_k)
            trades = simulate_signal_b(df, sigs, sl_atr_mult=sl_a,
                                       tp1_mult=tp1_m, max_bars=MAX_BARS)
            rows.append(_metrics(trades, "B", period, params))
            done += 1
        if done % 20 == 0:
            print(f"  B: {done}/{total}", flush=True)
    return rows


def run_signal_c_grid(dfs: dict) -> list[dict]:
    rows = []
    combos = list(itertools.product(RSI_THRESHOLDS, EXT_KS, SL_ATRS, TP1_MULTS))
    total = len(combos) * len(dfs)
    done = 0
    for rsi_t, ext_k, sl_a, tp1_m in combos:
        params = {"rsi_thresh": rsi_t, "rsi_lookback": 5,
                  "ext_k": ext_k, "sl_atr": sl_a, "tp1_mult": tp1_m}
        for period, df in dfs.items():
            sigs = detect_signal_c(df, rsi_thresh=rsi_t, ext_k=ext_k)
            trades = simulate_signal_b(df, sigs, sl_atr_mult=sl_a,
                                       tp1_mult=tp1_m, max_bars=MAX_BARS)
            rows.append(_metrics(trades, "C", period, params))
            done += 1
        if done % 30 == 0:
            print(f"  C: {done}/{total}", flush=True)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d1-2020", required=True)
    parser.add_argument("--m5-2024", required=True)
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load]")
    df_2020 = load_d1_canonical(args.d1_2020)
    df_2020 = df_2020[["open", "high", "low", "close", "volume"]]

    df_m5   = load_m5_canonical(args.m5_2024)
    df_2024 = resample_to_d1(df_m5)[["open", "high", "low", "close", "volume"]]

    df_comb = pd.concat([df_2020, df_2024]).sort_index()
    df_comb = df_comb[~df_comb.index.duplicated(keep="first")]

    print("[indicators]")
    dfs = {
        "2020-2023": add_indicators(df_2020.copy()),
        "2024-2025": add_indicators(df_2024.copy()),
        "combined":  add_indicators(df_comb.copy()),
    }
    for p, d in dfs.items():
        print(f"  {p}: {len(d)} bars")

    print("\n[grid Signal A]")
    rows_a = run_signal_a_grid(dfs)
    print(f"\n[grid Signal B]")
    rows_b = run_signal_b_grid(dfs)
    print(f"\n[grid Signal C]")
    rows_c = run_signal_c_grid(dfs)

    all_rows = rows_a + rows_b + rows_c
    df_r = pd.DataFrame(all_rows)

    csv_path = out_dir / "cfd_grid_results.csv"
    df_r.to_csv(csv_path, index=False)
    print(f"\n[out] {csv_path}  ({len(df_r)} rows)")

    # ── Summary: best per signal × period ────────────────────────────────────
    print("\n── BEST BY EXPECTANCY (combined period, n_signals ≥ 5) ──────────────")
    disp = ["label", "period", "rsi_thresh", "rsi_lookback", "ext_k",
            "sl_atr", "tp1_mult", "n_signals", "n_per_year",
            "pct_full_sl", "pct_tp1", "pct_tp2", "pct_tp3",
            "win_rate", "expectancy", "total_pnl", "avg_sl_pts"]
    comb = df_r[(df_r["period"] == "combined") & (df_r["n_signals"] >= 5)].copy()
    for sig in ["A", "B", "C"]:
        sub = comb[comb["label"] == sig].nlargest(5, "expectancy")
        if sub.empty:
            continue
        print(f"\n  Top 5 Signal {sig}:")
        print(sub[disp].to_string(index=False))

    print("\n── PERIOD SPLIT — best B by period ──────────────────────────────────")
    for period in ["2020-2023", "2024-2025", "combined"]:
        sub = df_r[(df_r["label"] == "B") & (df_r["period"] == period)
                   & (df_r["n_signals"] >= 3)].nlargest(3, "expectancy")
        if sub.empty:
            continue
        print(f"\n  [{period}] top 3:")
        print(sub[disp].to_string(index=False))

    print("\n── MARGINAL EFFECTS (Signal B, combined) ────────────────────────────")
    b_comb = df_r[(df_r["label"] == "B") & (df_r["period"] == "combined")
                  & (df_r["n_signals"] >= 3)]
    for col in ["ext_k", "sl_atr", "tp1_mult"]:
        g = b_comb.groupby(col)[["win_rate", "expectancy", "total_pnl",
                                  "pct_full_sl", "pct_tp1"]].mean().round(2)
        print(f"\n  {col}:\n{g.to_string()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
