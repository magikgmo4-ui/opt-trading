"""simulator_v2.py — Dynamic-capital DCA with tiered fear buying, greed selling, CFD long.

Capital dynamics:
  - $2,000 initial DCA pool + $2,000/year injection at each new calendar year
  - $1,000 separate CFD pool (not mixed with DCA)
  - Sell proceeds go back into DCA pool

Buy rules (weekly, first bar of each ISO week):
  - Base: 0.2% of current DCA capital
  - Moderate fear (FNG ≤ moderate_fear_thresh, above extreme): extra moderate_fear_extra_pct
  - Extreme fear (FNG ≤ extreme_fear_thresh): extra extreme_fear_extra_pct
  - Fear extras are ADDITIVE to the 0.2% base (not replacements)

Sell rule (weekly check):
  - FNG ≥ 76 (extreme greed): sell 5% of gold oz holdings, proceeds → DCA pool
  - Weekly cadence (once per ISO week per sell event)

CFD long:
  - Entry: prev FNG ≤ extreme_fear_thresh AND current FNG ≥ cfd_entry_thresh
  - Size: cfd_lot_oz (default 3 oz = 0.03 lots at 0.01 lot = 1 oz)
  - SL: entry - sl_atr × ATR14
  - TP: entry + tp_atr × ATR14
  - Also exit at extreme greed (FNG ≥ 76) if no TP/SL
  - No pyramiding; one position at a time
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd


@dataclass
class V2Params:
    # ── Capital ───────────────────────────────────────────────────
    initial_capital: float = 2_000.0
    annual_injection: float = 2_000.0

    # ── Weekly base DCA ───────────────────────────────────────────
    base_weekly_pct: float = 0.002        # 0.2% of DCA capital per week

    # ── Moderate fear extra buy ───────────────────────────────────
    moderate_fear_thresh: int = 40        # FNG ≤ this (and > extreme thresh)
    moderate_fear_extra_pct: float = 0.0125  # 1.25% extra (0.5% × 2.5)

    # ── Extreme fear extra buy ────────────────────────────────────
    extreme_fear_thresh: int = 25         # FNG ≤ this
    extreme_fear_extra_pct: float = 0.15  # 15% extra (0.5% × 30)

    # ── Extreme greed sell ────────────────────────────────────────
    extreme_greed_thresh: int = 76        # FNG ≥ this → sell
    sell_pct: float = 0.05               # sell 5% of oz held

    # ── CFD long ─────────────────────────────────────────────────
    use_cfd: bool = True
    cfd_initial_capital: float = 1_000.0
    cfd_lot_oz: float = 3.0              # 0.03 lots = 3 oz (0.01 lot = 1 oz)
    cfd_entry_thresh: int = 40           # FNG recovery level for entry
    cfd_sl_atr: float = 1.0
    cfd_tp_atr: float = 2.0


@dataclass
class BuyEventV2:
    date: pd.Timestamp
    price: float
    amount_usd: float
    qty_oz: float
    trigger: str          # "weekly" | "moderate_fear" | "extreme_fear"
    fng: int


@dataclass
class SellEventV2:
    date: pd.Timestamp
    price: float
    qty_oz: float
    proceeds_usd: float
    fng: int


@dataclass
class CFDTradeV2:
    entry_date: pd.Timestamp
    entry_price: float
    exit_date: pd.Timestamp
    exit_price: float
    lot_oz: float
    pnl: float
    exit_type: str        # "tp" | "sl" | "greed_exit" | "end_of_period"


@dataclass
class V2Result:
    label: str
    params: V2Params
    buy_events: List[BuyEventV2] = field(default_factory=list)
    sell_events: List[SellEventV2] = field(default_factory=list)
    cfd_trades: List[CFDTradeV2] = field(default_factory=list)

    final_oz: float = 0.0
    final_dca_capital: float = 0.0
    final_cfd_capital: float = 0.0
    total_injected: float = 0.0         # all cash ever put in (DCA + CFD pools)
    total_gold_deployed: float = 0.0    # USD spent buying gold
    total_sell_proceeds: float = 0.0
    total_cfd_pnl: float = 0.0

    def total_assets(self, last_price: float) -> float:
        return (self.final_oz * last_price
                + self.final_dca_capital
                + self.final_cfd_capital)

    def total_return(self, last_price: float) -> float:
        return self.total_assets(last_price) - self.total_injected

    def return_pct(self, last_price: float) -> float:
        if self.total_injected == 0:
            return 0.0
        return self.total_return(last_price) / self.total_injected * 100

    def avg_cost(self) -> float:
        total_oz = sum(e.qty_oz for e in self.buy_events)
        if total_oz == 0:
            return float("nan")
        return self.total_gold_deployed / total_oz

    def summary(self, last_price: float) -> dict:
        n_cfd = len(self.cfd_trades)
        n_tp  = sum(1 for t in self.cfd_trades if t.exit_type == "tp")
        n_sl  = sum(1 for t in self.cfd_trades if t.exit_type == "sl")
        p     = self.params
        return {
            "label":                self.label,
            "mf_thresh":            p.moderate_fear_thresh,
            "ef_thresh":            p.extreme_fear_thresh,
            "mf_extra_pct":         round(p.moderate_fear_extra_pct * 100, 3),
            "ef_extra_pct":         round(p.extreme_fear_extra_pct * 100, 1),
            "cfd_entry_thresh":     p.cfd_entry_thresh,
            "total_injected_usd":   round(self.total_injected, 2),
            "total_gold_deployed":  round(self.total_gold_deployed, 2),
            "final_oz":             round(self.final_oz, 4),
            "avg_cost_usd":         round(self.avg_cost(), 2),
            "last_price":           round(last_price, 2),
            "gold_value_usd":       round(self.final_oz * last_price, 2),
            "dca_cash_usd":         round(self.final_dca_capital, 2),
            "cfd_capital_usd":      round(self.final_cfd_capital, 2),
            "total_assets_usd":     round(self.total_assets(last_price), 2),
            "total_return_usd":     round(self.total_return(last_price), 2),
            "return_pct":           round(self.return_pct(last_price), 2),
            "n_buys":               len(self.buy_events),
            "n_weekly_buys":        sum(1 for e in self.buy_events if e.trigger == "weekly"),
            "n_mod_fear_buys":      sum(1 for e in self.buy_events if e.trigger == "moderate_fear"),
            "n_ext_fear_buys":      sum(1 for e in self.buy_events if e.trigger == "extreme_fear"),
            "n_sells":              len(self.sell_events),
            "total_sell_proceeds":  round(self.total_sell_proceeds, 2),
            "cfd_n_trades":         n_cfd,
            "cfd_n_tp":             n_tp,
            "cfd_n_sl":             n_sl,
            "cfd_win_rate_pct":     round(n_tp / n_cfd * 100, 1) if n_cfd > 0 else None,
            "cfd_pnl_usd":          round(self.total_cfd_pnl, 2),
        }


def _label(p: V2Params) -> str:
    return (f"mf{p.moderate_fear_thresh}_ef{p.extreme_fear_thresh}"
            f"_mp{p.moderate_fear_extra_pct*100:.2f}"
            f"_ep{p.extreme_fear_extra_pct*100:.1f}"
            f"_cfd{p.cfd_entry_thresh}")


def simulate_v2(
    df: pd.DataFrame,
    fng: pd.DataFrame,
    params: V2Params,
    label: str = "",
) -> V2Result:
    result = V2Result(label=label or _label(params), params=params)

    dca_capital = params.initial_capital
    cfd_capital = params.cfd_initial_capital if params.use_cfd else 0.0
    oz_held = 0.0
    total_injected = params.initial_capital + (params.cfd_initial_capital if params.use_cfd else 0.0)
    total_gold_deployed = 0.0

    iso = df.index.isocalendar()
    current_year = df.index[0].year
    weeks_seen: set[str] = set()
    greed_weeks_seen: set[str] = set()

    prev_fng_val: int = 50
    cfd_open: Optional[dict] = None

    for i in range(len(df)):
        ts    = df.index[i]
        price = float(df.iloc[i]["close"])
        atr   = float(df.iloc[i]["atr14"]) if "atr14" in df.columns else price * 0.005
        low_p = float(df.iloc[i]["low"])
        high_p = float(df.iloc[i]["high"])
        fng_val = int(fng["fng"].iloc[i]) if not pd.isna(fng["fng"].iloc[i]) else 50
        wk = f"{iso['year'].iloc[i]}_{iso['week'].iloc[i]}"

        # ── Annual injection ─────────────────────────────────────
        if ts.year > current_year:
            dca_capital += params.annual_injection
            total_injected += params.annual_injection
            current_year = ts.year

        # ── Weekly buy ───────────────────────────────────────────
        if wk not in weeks_seen:
            weeks_seen.add(wk)

            buy_pct = params.base_weekly_pct
            trigger = "weekly"

            if fng_val <= params.extreme_fear_thresh:
                buy_pct += params.extreme_fear_extra_pct
                trigger = "extreme_fear"
            elif fng_val <= params.moderate_fear_thresh:
                buy_pct += params.moderate_fear_extra_pct
                trigger = "moderate_fear"

            buy_usd = min(dca_capital * buy_pct, dca_capital)
            if buy_usd > 0.01:
                qty = buy_usd / price
                oz_held += qty
                dca_capital -= buy_usd
                total_gold_deployed += buy_usd
                result.buy_events.append(
                    BuyEventV2(ts, price, buy_usd, qty, trigger, fng_val))

            # ── Extreme greed sell (same weekly slot) ────────────
            if (fng_val >= params.extreme_greed_thresh
                    and wk not in greed_weeks_seen
                    and oz_held > 1e-6):
                greed_weeks_seen.add(wk)
                sell_oz = oz_held * params.sell_pct
                if sell_oz > 1e-6:
                    proceeds = sell_oz * price
                    oz_held -= sell_oz
                    dca_capital += proceeds
                    result.total_sell_proceeds += proceeds
                    result.sell_events.append(
                        SellEventV2(ts, price, sell_oz, proceeds, fng_val))

        # ── CFD long ─────────────────────────────────────────────
        if params.use_cfd:
            # Exit check
            if cfd_open is not None:
                sl_p = cfd_open["entry"] - params.cfd_sl_atr * cfd_open["atr"]
                tp_p = cfd_open["entry"] + params.cfd_tp_atr * cfd_open["atr"]

                exit_type  = None
                exit_price = None

                if low_p <= sl_p:
                    exit_type, exit_price = "sl", sl_p
                elif high_p >= tp_p:
                    exit_type, exit_price = "tp", tp_p
                elif fng_val >= params.extreme_greed_thresh:
                    exit_type, exit_price = "greed_exit", price

                if exit_type:
                    pnl = (exit_price - cfd_open["entry"]) * cfd_open["lot_oz"]
                    cfd_capital += pnl
                    result.total_cfd_pnl += pnl
                    result.cfd_trades.append(CFDTradeV2(
                        cfd_open["entry_date"], cfd_open["entry"],
                        ts, exit_price, cfd_open["lot_oz"], pnl, exit_type,
                    ))
                    cfd_open = None

            # Entry check: FNG recovered from extreme fear
            if (cfd_open is None
                    and prev_fng_val <= params.extreme_fear_thresh
                    and fng_val >= params.cfd_entry_thresh
                    and cfd_capital > 0):
                cfd_open = {
                    "entry":      price,
                    "entry_date": ts,
                    "atr":        atr,
                    "lot_oz":     params.cfd_lot_oz,
                }

        prev_fng_val = fng_val

    # Close open CFD at end
    if cfd_open is not None and params.use_cfd:
        last_p = float(df.iloc[-1]["close"])
        pnl = (last_p - cfd_open["entry"]) * cfd_open["lot_oz"]
        cfd_capital += pnl
        result.total_cfd_pnl += pnl
        result.cfd_trades.append(CFDTradeV2(
            cfd_open["entry_date"], cfd_open["entry"],
            df.index[-1], last_p, cfd_open["lot_oz"], pnl, "end_of_period",
        ))

    result.final_oz          = oz_held
    result.final_dca_capital = dca_capital
    result.final_cfd_capital = cfd_capital
    result.total_injected    = total_injected
    result.total_gold_deployed = total_gold_deployed
    return result
