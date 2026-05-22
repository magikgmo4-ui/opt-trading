#!/usr/bin/env python3
"""run_comparison.py — Exhaustive $ comparison of all strategies on $10,000 capital.

Strategies evaluated:
  1. plain_dca          : $10k / n_weeks flat, every Monday
  2. phase_dca          : $2,500/Wyckoff phase, weekly amount varies
  3. phase_dca+efear    : phase_dca + $1,000 on each Extreme Fear episode
  4. phase_dca+cfd      : phase_dca + CFD Signal B profits recycled
  5. full_combo         : phase_dca + extreme fear + CFD recycled
  --- Reference strategies (expressed in $ on $10k) ---
  6. daily_scalping     : NON CONCLUANT — reference only
  7. weekly_dca_optimized: $10k baseline, exp=+0.95R
  8. cfd_short_b_only   : $10k at 20% reserve → CFD only (~3 trades/yr × $8.63 exp)

Usage:
    python tools/strategy/dca_capital/run_comparison.py \
        --d1-2020 data/market/xauusd_d1_2020_2023.csv \
        --m5-2024 data/market/xauusd_m5_canonical.csv \
        --out artifacts/results
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_capital.fetch_fng import load_fng
from tools.strategy.dca_capital.cycle_detector import detect_phases, phase_summary
from tools.strategy.dca_capital.simulator import (
    simulate_plain_dca, simulate_phase_dca
)
from tools.strategy.dca_cfd_short.indicators import add_indicators as add_cfd_indicators
from tools.strategy.dca_spot.load_data import load_d1_canonical, load_m5_canonical, resample_to_d1

TOTAL_CAPITAL = 10_000.0
CFD_RESERVE_PCT = 0.20         # 20% of total for CFD
CFD_PROFIT_6Y = 138.14        # Signal B ext2 sl1 tp1×0.5 — 6 years, 1 oz
# Scale CFD to actual reserve: $2,000 reserve / $2,000 margin-equivalent
# At ~$25 max SL/trade on 1 oz, $2,000 reserve ≈ 80 oz capacity
# But realistic: 1 oz per signal, 16 signals × $8.63 exp = $138
# Scale to $2,000 reserve deployment: $138 × (2000/25) = $11,040... unrealistic
# Realistic lot: 2,000 / (avg_entry ~2000 / 500) = 2000/4 = 500 lots potential
# But we cap at 1 oz per trade for conservatism → $138 total CFD profit
CFD_PROFIT_REALISTIC = CFD_PROFIT_6Y   # conservative: 1 oz per trade


def load_combined_d1(d1_path: str | None, m5_path: str | None) -> pd.DataFrame:
    frames = []
    if d1_path:
        df = load_d1_canonical(d1_path)[["open", "high", "low", "close", "volume"]]
        frames.append(df)
    if m5_path:
        df_m5 = load_m5_canonical(m5_path)
        df = resample_to_d1(df_m5)[["open", "high", "low", "close", "volume"]]
        frames.append(df)
    combined = pd.concat(frames).sort_index()
    return combined[~combined.index.duplicated(keep="first")]


def print_phase_table(seg_df: pd.DataFrame) -> None:
    print("\n── WYCKOFF PHASES DETECTED ──────────────────────────────────────────")
    print(seg_df[["phase", "start", "end", "n_weeks", "price_start",
                  "price_end", "pct_chg", "avg_fng"]].to_string(index=False))
    print(f"\n  Phase counts: {seg_df['phase'].value_counts().to_dict()}")


def print_strategy_table(results: list[dict], last_price: float) -> None:
    cols = ["label", "total_deployed_usd", "total_oz", "avg_cost_usd",
            "portfolio_value", "cfd_recycled_usd",
            "total_profit_usd", "return_pct",
            "n_buys", "n_extreme_fear"]
    df = pd.DataFrame(results)[cols]
    df = df.sort_values("total_profit_usd", ascending=False).reset_index(drop=True)
    print(f"\n── STRATEGY COMPARISON  (last_price={last_price:.0f}, capital=${TOTAL_CAPITAL:,.0f}) ─")
    print(df.to_string(index=False))


def print_phase_breakdown(result, last_price: float) -> None:
    from tools.strategy.dca_capital.simulator import PortfolioResult
    if not isinstance(result, PortfolioResult):
        return
    print(f"\n  [{result.label}] buys per phase: {result.summary(last_price)['buys_per_phase']}")
    print(f"    deployed per phase: {result.summary(last_price)['deployed_per_phase']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--d1-2020", required=True)
    parser.add_argument("--m5-2024", required=True)
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load D1]")
    df = load_combined_d1(args.d1_2020, args.m5_2024)
    df = add_cfd_indicators(df)
    print(f"  {len(df)} bars  {df.index[0].date()} → {df.index[-1].date()}")
    last_price = float(df["close"].iloc[-1])
    print(f"  last_price: {last_price:.2f}")

    print("[fetch F&G]")
    fng = load_fng(df)
    print(f"  {fng['source'].value_counts().to_dict()}")
    print(f"  FNG range: {fng['fng'].min()} – {fng['fng'].max()}")
    print(f"  Extreme Fear days (≤25): {(fng['fng'] <= 25).sum()}")
    print(f"  Extreme Greed days (≥76): {(fng['fng'] >= 76).sum()}")

    print("[detect cycle phases]")
    phases = detect_phases(df, fng)
    seg_df = phase_summary(phases, df, fng)
    print_phase_table(seg_df)

    print("\n[simulate all strategies]")

    # 1. Plain DCA (benchmark)
    r1 = simulate_plain_dca(df, phases, total_capital=TOTAL_CAPITAL)

    # 2. Phase DCA
    r2 = simulate_phase_dca(df, phases, fng, seg_df, total_capital=TOTAL_CAPITAL)

    # 3. Phase DCA + extreme fear
    r3 = simulate_phase_dca(df, phases, fng, seg_df, total_capital=TOTAL_CAPITAL,
                             use_extreme_fear=True)

    # 4. Phase DCA + CFD recycled
    r4 = simulate_phase_dca(df, phases, fng, seg_df, total_capital=TOTAL_CAPITAL,
                             cfd_profit=CFD_PROFIT_REALISTIC, use_cfd_recycle=True)

    # 5. Full combo
    r5 = simulate_phase_dca(df, phases, fng, seg_df, total_capital=TOTAL_CAPITAL,
                             use_extreme_fear=True,
                             cfd_profit=CFD_PROFIT_REALISTIC, use_cfd_recycle=True)

    all_results = []
    for r in [r1, r2, r3, r4, r5]:
        all_results.append(r.summary(last_price))
        print_phase_breakdown(r, last_price)

    print_strategy_table(all_results, last_price)

    # Save
    df_out = pd.DataFrame(all_results)
    csv_path = out_dir / "strategy_comparison_10k.csv"
    df_out.to_csv(csv_path, index=False)

    # Per-strategy buy log
    for r in [r1, r2, r3, r4, r5]:
        rows = [{"date": e.date.date(), "price": e.price, "amount_usd": e.amount_usd,
                 "qty_oz": round(e.qty_oz, 6), "trigger": e.trigger, "phase": e.phase}
                for e in r.buy_events]
        pd.DataFrame(rows).to_csv(
            out_dir / f"buys_{r.label.replace('+','_')}.csv", index=False)

    # Phase breakdown table
    seg_df.to_csv(out_dir / "cycle_phases.csv", index=False)
    print(f"\n[out] {out_dir}")

    # F&G stats per phase
    print("\n── F&G STATS PER PHASE ──────────────────────────────────────────────")
    fng_phase = fng.copy()
    fng_phase["phase"] = phases.values
    g = fng_phase.groupby("phase")["fng"].agg(["mean", "min", "max", "count"]).round(1)
    print(g.to_string())

    # Extreme fear episodes
    ef = fng[fng["fng"] <= 25].copy()
    ef["phase"] = phases[fng["fng"] <= 25].values
    print(f"\n── EXTREME FEAR EPISODES (FNG ≤ 25): {len(ef)} days ────────────────")
    if not ef.empty:
        print(ef[["fng", "fng_label", "source", "phase"]].head(30).to_string())

    return 0


if __name__ == "__main__":
    sys.exit(main())
