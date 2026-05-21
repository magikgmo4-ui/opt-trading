"""simulator.py — Phase-based capital DCA with extreme fear bonus + CFD recycling.

Capital structure:
  total_capital   = $10,000 (default)
  n_phases        = 4 (Wyckoff cycle)
  phase_budget    = total_capital / n_phases = $2,500
  weekly_buy      = phase_budget / n_weeks_in_phase  (varies per phase)

Extreme fear rule:
  When FNG ≤ extreme_fear_thresh (default 25):
    - Trigger once per extreme-fear episode (min 10 bars between triggers)
    - Buy extra = total_capital × extreme_fear_pct (default 10% = $1,000)
    - Deducted from remaining phase budget (capped at remaining budget)

CFD recycling:
  cfd_profit (pre-computed from Signal B simulation) is added to DCA pool
  at start of each new phase proportionally.

Strategies compared:
  1. plain_dca        — $10,000 / 260 weeks flat (benchmark)
  2. phase_dca        — $2,500/phase, weekly amount varies
  3. phase_dca_efear  — phase_dca + extreme fear bonus
  4. phase_dca_cfd    — phase_dca + CFD profits recycled
  5. full_combo       — phase_dca + extreme fear + CFD recycled
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd


@dataclass
class BuyEvent:
    date: pd.Timestamp
    price: float
    amount_usd: float      # $ deployed
    qty_oz: float          # oz of gold bought
    trigger: str           # "weekly" | "extreme_fear" | "cfd_recycle"
    phase: str


@dataclass
class PortfolioResult:
    label: str
    buy_events: List[BuyEvent] = field(default_factory=list)
    total_deployed_usd: float = 0.0
    cfd_profit_recycled: float = 0.0

    def total_oz(self) -> float:
        return sum(e.qty_oz for e in self.buy_events)

    def avg_cost(self) -> float:
        tot_qty = self.total_oz()
        if tot_qty == 0:
            return float("nan")
        return self.total_deployed_usd / tot_qty

    def portfolio_value(self, last_price: float) -> float:
        return self.total_oz() * last_price

    def total_profit(self, last_price: float) -> float:
        return self.portfolio_value(last_price) - self.total_deployed_usd + self.cfd_profit_recycled

    def return_pct(self, last_price: float) -> float:
        if self.total_deployed_usd == 0:
            return 0.0
        return self.total_profit(last_price) / self.total_deployed_usd * 100

    def summary(self, last_price: float) -> dict:
        buys_by_phase = {}
        for e in self.buy_events:
            buys_by_phase.setdefault(e.phase, []).append(e)

        ef_buys = [e for e in self.buy_events if e.trigger == "extreme_fear"]
        return {
            "label":              self.label,
            "n_buys":             len(self.buy_events),
            "n_extreme_fear":     len(ef_buys),
            "total_deployed_usd": round(self.total_deployed_usd, 2),
            "total_oz":           round(self.total_oz(), 4),
            "avg_cost_usd":       round(self.avg_cost(), 2),
            "last_price":         round(last_price, 2),
            "portfolio_value":    round(self.portfolio_value(last_price), 2),
            "cfd_recycled_usd":   round(self.cfd_profit_recycled, 2),
            "total_profit_usd":   round(self.total_profit(last_price), 2),
            "return_pct":         round(self.return_pct(last_price), 2),
            "buys_per_phase":     {p: len(v) for p, v in buys_by_phase.items()},
            "deployed_per_phase": {p: round(sum(e.amount_usd for e in v), 2)
                                   for p, v in buys_by_phase.items()},
        }


def simulate_plain_dca(
    df: pd.DataFrame,
    phases: pd.Series,
    total_capital: float = 10_000.0,
) -> PortfolioResult:
    """Flat weekly DCA: total_capital / n_weeks, every week, ignore phases."""
    result = PortfolioResult(label="plain_dca")
    weeks_seen = set()
    iso_df     = df.index.isocalendar()
    total_weeks = len({f"{iso_df['year'].iloc[i]}_{iso_df['week'].iloc[i]}"
                       for i in range(len(iso_df))})
    weekly_usd  = total_capital / total_weeks

    for i, (ts, row) in enumerate(df.iterrows()):
        wk_key = f"{iso_df['year'].iloc[i]}_{iso_df['week'].iloc[i]}"
        if wk_key in weeks_seen:
            continue
        weeks_seen.add(wk_key)
        price = float(row["close"])
        qty   = weekly_usd / price
        result.buy_events.append(BuyEvent(ts, price, weekly_usd, qty, "weekly", phases.iloc[i]))
        result.total_deployed_usd += weekly_usd
    return result


PHASE_TYPES = ["accumulation", "markup", "distribution", "markdown"]


def simulate_phase_dca(
    df: pd.DataFrame,
    phases: pd.Series,
    fng: pd.DataFrame,
    phase_segments: pd.DataFrame,
    total_capital: float = 10_000.0,
    extreme_fear_thresh: int = 25,
    extreme_fear_pct: float = 0.10,
    extreme_fear_cooldown_bars: int = 10,
    use_extreme_fear: bool = False,
    cfd_profit: float = 0.0,
    use_cfd_recycle: bool = False,
) -> PortfolioResult:
    """Phase-budget DCA: $2,500 per phase TYPE (not per occurrence).

    Capital allocation:
      $2,500 per phase type × 4 types = $10,000 total
      Weekly buy = $2,500 / total_weeks_of_that_type_in_period

    Extreme fear: $1,000 extra per episode (from same type pool), 10-bar cooldown.
    CFD profit: distributed equally across all 4 type pools.
    """
    label_parts = ["phase_dca"]
    if use_extreme_fear:
        label_parts.append("efear")
    if use_cfd_recycle:
        label_parts.append("cfd")
    result = PortfolioResult(label="+".join(label_parts))

    phase_budget  = total_capital / len(PHASE_TYPES)   # $2,500 per type
    ef_bonus_usd  = total_capital * extreme_fear_pct    # $1,000 per episode
    cfd_per_type  = (cfd_profit / len(PHASE_TYPES)) if use_cfd_recycle else 0.0

    if use_cfd_recycle:
        result.cfd_profit_recycled = cfd_profit

    iso = df.index.isocalendar()

    # Count total UNIQUE weeks per phase type across the whole period
    weeks_by_type: dict[str, set] = {t: set() for t in PHASE_TYPES}
    for i in range(len(df)):
        wk = f"{iso['year'].iloc[i]}_{iso['week'].iloc[i]}"
        weeks_by_type[phases.iloc[i]].add(wk)

    # Weekly buy amount per type = type_budget / total_weeks_of_that_type
    weekly_by_type: dict[str, float] = {
        t: (phase_budget + cfd_per_type) / max(1, len(wks))
        for t, wks in weeks_by_type.items()
    }

    # Remaining budget per type (to cap extreme fear draws)
    remaining_by_type: dict[str, float] = {
        t: phase_budget + cfd_per_type for t in PHASE_TYPES
    }

    weeks_seen: set[str] = set()
    last_ef_bar = -extreme_fear_cooldown_bars

    for i in range(len(df)):
        ts          = df.index[i]
        price       = float(df.iloc[i]["close"])
        phase_label = phases.iloc[i]
        wk          = f"{iso['year'].iloc[i]}_{iso['week'].iloc[i]}"

        # ── Weekly DCA ───────────────────────────────────────────────────
        if wk not in weeks_seen:
            weeks_seen.add(wk)
            w_usd = min(weekly_by_type[phase_label],
                        remaining_by_type[phase_label])
            if w_usd > 1e-2:
                qty = w_usd / price
                result.buy_events.append(
                    BuyEvent(ts, price, w_usd, qty, "weekly", phase_label))
                result.total_deployed_usd     += w_usd
                remaining_by_type[phase_label] -= w_usd

        # ── Extreme fear bonus ───────────────────────────────────────────
        if use_extreme_fear:
            fng_val = int(fng["fng"].iloc[i]) if not pd.isna(fng["fng"].iloc[i]) else 50
            if (fng_val <= extreme_fear_thresh
                    and i - last_ef_bar >= extreme_fear_cooldown_bars):
                bonus = min(ef_bonus_usd, remaining_by_type[phase_label])
                if bonus > 1e-2:
                    qty = bonus / price
                    result.buy_events.append(
                        BuyEvent(ts, price, bonus, qty, "extreme_fear", phase_label))
                    result.total_deployed_usd     += bonus
                    remaining_by_type[phase_label] -= bonus
                    last_ef_bar = i

    return result
