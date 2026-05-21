#!/usr/bin/env python3
"""run_dca_adaptive.py — Adaptive DCA: buy ×mult_down if price < last buy,
sell ×sell_frac if price > first buy.

Grid: frequencies × buy_mult × sell_frac.
Benchmark: fixed DCA (1S every F bars, no sell).

Usage:
    python tools/strategy/dca_spot/run_dca_adaptive.py \
        --input data/market/xauusd_m5_canonical.csv \
        --out artifacts/backtests/dca_spot
"""
from __future__ import annotations

import itertools
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.strategy.dca_spot.load_data import load_m5_canonical, resample_to_d1


# ── Grid ──────────────────────────────────────────────────────────────────────
FREQUENCIES = [1, 5, 10, 21]       # D1 bars between buy events
FREQ_LABELS = {1: "daily", 5: "weekly", 10: "biweekly", 21: "monthly"}
BUY_MULTS = [1.1, 1.2, 1.5, 2.0]  # multiply base unit when price < last_buy
SELL_FRACS = [0.5, 0.8, 1.0]       # fraction of base unit to sell when price > first_buy
BASE_UNIT = 1.0                     # S units per standard buy


# ── Simulation ────────────────────────────────────────────────────────────────

@dataclass
class Position:
    date: pd.Timestamp
    price: float
    qty: float


def _sell_fifo(positions: List[Position], qty_to_sell: float, sell_price: float) -> float:
    """Remove qty_to_sell from oldest positions (FIFO). Returns cash proceeds."""
    proceeds = 0.0
    remaining = qty_to_sell
    while remaining > 1e-9 and positions:
        pos = positions[0]
        if pos.qty <= remaining + 1e-9:
            proceeds += pos.qty * sell_price
            remaining -= pos.qty
            positions.pop(0)
        else:
            proceeds += remaining * sell_price
            pos.qty -= remaining
            remaining = 0.0
    return proceeds


def simulate(
    bars: pd.DataFrame,
    freq: int,
    buy_mult: float,
    sell_frac: float,
) -> dict:
    """
    bars: D1 bars sorted by date.
    At each scheduled bar (index % freq == 0):
      - Buy: base_unit × buy_mult if close < last_buy_price, else base_unit
      - Sell: base_unit × sell_frac if close > first_buy_price (and positions exist)
    Returns metrics dict.
    """
    positions: List[Position] = []
    first_buy_price: Optional[float] = None
    last_buy_price: Optional[float] = None
    total_cost = 0.0
    total_sold_qty = 0.0
    total_sell_proceeds = 0.0
    buy_log: List[dict] = []
    sell_log: List[dict] = []

    scheduled_indices = range(0, len(bars), freq)

    for i in scheduled_indices:
        row = bars.iloc[i]
        price = row["close"]
        ts = bars.index[i]

        # ── BUY ──────────────────────────────────────────────────────────────
        if last_buy_price is not None and price < last_buy_price:
            qty_buy = BASE_UNIT * buy_mult
            trigger = "down"
        else:
            qty_buy = BASE_UNIT
            trigger = "flat_or_up"

        positions.append(Position(ts, price, qty_buy))
        total_cost += qty_buy * price
        last_buy_price = price
        if first_buy_price is None:
            first_buy_price = price
        buy_log.append({"date": ts, "price": price, "qty": qty_buy, "trigger": trigger})

        # ── SELL ─────────────────────────────────────────────────────────────
        if first_buy_price is not None and price > first_buy_price and positions:
            qty_sell = BASE_UNIT * sell_frac
            # Don't sell more than we hold
            held = sum(p.qty for p in positions)
            qty_sell = min(qty_sell, held)
            if qty_sell > 1e-9:
                proceeds = _sell_fifo(positions, qty_sell, price)
                total_sold_qty += qty_sell
                total_sell_proceeds += proceeds
                sell_log.append({"date": ts, "price": price, "qty": qty_sell})

    # ── End-of-period metrics ─────────────────────────────────────────────────
    last_price = float(bars["close"].iloc[-1])
    held_qty = sum(p.qty for p in positions)
    held_cost = sum(p.price * p.qty for p in positions)
    held_value = held_qty * last_price

    total_bought_qty = sum(e["qty"] for e in buy_log)
    avg_buy_price = total_cost / total_bought_qty if total_bought_qty > 0 else float("nan")

    # P&L: realized (sells - cost of sold positions) + unrealized (held mark-to-market)
    # Cost of sold positions = total_cost - held_cost
    sold_cost = total_cost - held_cost
    realized_profit = total_sell_proceeds - sold_cost
    unrealized_profit = held_value - held_cost
    total_profit = realized_profit + unrealized_profit
    total_return_pct = total_profit / total_cost * 100 if total_cost > 0 else 0.0

    # Portfolio value = cash from sells + held mark-to-market
    portfolio_value = total_sell_proceeds + held_value
    # Total invested = total_cost (cost of all buys)
    portfolio_return_pct = (portfolio_value - total_cost) / total_cost * 100 if total_cost > 0 else 0.0

    n_buy_events = len(buy_log)
    n_buy_down = sum(1 for e in buy_log if e["trigger"] == "down")
    n_sell_events = len(sell_log)

    return {
        "n_buy_events":        n_buy_events,
        "n_buy_down":          n_buy_down,
        "n_buy_up_flat":       n_buy_events - n_buy_down,
        "n_sell_events":       n_sell_events,
        "total_bought_qty":    round(total_bought_qty, 3),
        "total_sold_qty":      round(total_sold_qty, 3),
        "held_qty":            round(held_qty, 3),
        "avg_buy_price":       round(avg_buy_price, 2),
        "first_buy_price":     round(first_buy_price, 2) if first_buy_price else float("nan"),
        "last_price":          round(last_price, 2),
        "realized_profit":     round(realized_profit, 1),
        "unrealized_profit":   round(unrealized_profit, 1),
        "portfolio_return_pct": round(portfolio_return_pct, 2),
        "total_return_pct":    round(total_return_pct, 2),
    }


def simulate_benchmark(bars: pd.DataFrame, freq: int) -> dict:
    """Fixed DCA: buy 1S every freq bars, never sell."""
    indices = range(0, len(bars), freq)
    prices = [bars["close"].iloc[i] for i in indices]
    last_price = float(bars["close"].iloc[-1])
    n = len(prices)
    avg = sum(prices) / n if n else float("nan")
    held_qty = float(n) * BASE_UNIT
    total_cost = sum(p * BASE_UNIT for p in prices)
    portfolio_value = held_qty * last_price
    return {
        "n_buy_events": n,
        "avg_buy_price": round(avg, 2),
        "held_qty": round(held_qty, 3),
        "portfolio_return_pct": round((portfolio_value - total_cost) / total_cost * 100, 2),
    }


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[load + resample]", flush=True)
    df_m5 = load_m5_canonical(args.input)
    df_d1 = resample_to_d1(df_m5)
    print(f"  → {len(df_d1)} D1 bars  "
          f"{df_d1.index[0].date()} → {df_d1.index[-1].date()}", flush=True)

    rows = []
    bench_rows = []

    for freq in FREQUENCIES:
        bench = simulate_benchmark(df_d1, freq)
        bench_rows.append({
            "freq": freq,
            "freq_label": FREQ_LABELS[freq],
            **bench,
        })

        for buy_mult, sell_frac in itertools.product(BUY_MULTS, SELL_FRACS):
            m = simulate(df_d1, freq, buy_mult, sell_frac)
            rows.append({
                "freq": freq,
                "freq_label": FREQ_LABELS[freq],
                "buy_mult": buy_mult,
                "sell_frac": sell_frac,
                "price_delta_vs_bench": round(m["avg_buy_price"] - bench["avg_buy_price"], 2),
                "return_delta_vs_bench": round(m["portfolio_return_pct"] - bench["portfolio_return_pct"], 2),
                **m,
            })

    df_r = pd.DataFrame(rows).sort_values(
        ["freq", "portfolio_return_pct"], ascending=[True, False]
    ).reset_index(drop=True)
    df_bench = pd.DataFrame(bench_rows)

    csv_path = out_dir / "dca_adaptive_grid.csv"
    df_r.to_csv(csv_path, index=False)
    print(f"[out] {csv_path}", flush=True)

    # ── Benchmark summary ─────────────────────────────────────────────────────
    print("\n── BENCHMARK (fixed DCA, no sell) ───────────────────────────────────")
    print(df_bench[["freq_label", "n_buy_events", "avg_buy_price",
                     "held_qty", "portfolio_return_pct"]].to_string(index=False))

    # ── Best per frequency ────────────────────────────────────────────────────
    print("\n── BEST ADAPTIVE DCA PER FREQUENCY (portfolio_return_pct) ───────────")
    key_cols = ["freq_label", "buy_mult", "sell_frac",
                "n_buy_events", "n_buy_down", "n_sell_events",
                "avg_buy_price", "held_qty",
                "portfolio_return_pct", "return_delta_vs_bench", "price_delta_vs_bench"]
    best = df_r.groupby("freq").apply(lambda g: g.nlargest(1, "portfolio_return_pct")).reset_index(drop=True)
    print(best[key_cols].to_string(index=False))

    # ── Full results per frequency ────────────────────────────────────────────
    for freq in FREQUENCIES:
        sub = df_r[df_r["freq"] == freq].copy()
        bench_row = df_bench[df_bench["freq"] == freq].iloc[0]
        print(f"\n── freq={freq} ({FREQ_LABELS[freq]})  "
              f"bench: avg={bench_row['avg_buy_price']}  "
              f"return={bench_row['portfolio_return_pct']}%  "
              f"held={bench_row['held_qty']} ─────────────────────────────")
        print(sub[key_cols].to_string(index=False))

    # ── Overall best (all frequencies combined) ───────────────────────────────
    print("\n── TOP 10 OVERALL (portfolio_return_pct) ────────────────────────────")
    print(df_r.nlargest(10, "portfolio_return_pct")[key_cols].to_string(index=False))

    # ── Best beating benchmark on avg_price ───────────────────────────────────
    cheaper = df_r[df_r["price_delta_vs_bench"] < 0].nsmallest(10, "price_delta_vs_bench")
    print(f"\n── CHEAPEST AVG PRICE vs BENCHMARK ({len(cheaper)} configs) ─────────")
    if not cheaper.empty:
        print(cheaper[key_cols].to_string(index=False))
    else:
        print("  none beat benchmark on avg_price")

    return 0


if __name__ == "__main__":
    sys.exit(main())
