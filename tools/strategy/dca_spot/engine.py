"""engine.py — Event-driven DCA spot simulation (L0/L1/L2/L3 layers).

Processes D1 bars sequentially, maintaining capital allocation state.
All prices in points (XAUUSD). Capital in abstract units (1 unit = S per week).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pandas as pd


@dataclass
class Position:
    date: pd.Timestamp
    price: float
    qty_s: float        # qty in units of S (1.0 = 1 base unit)
    layer: str          # "L1" | "L2" | "L3"


@dataclass
class Event:
    date: pd.Timestamp
    event_type: str     # "BUY_L1" | "BUY_L2" | "BUY_L3" | "SELL_L1" | "INJECT"
    price: float
    qty_s: float
    trigger: str        # human-readable reason
    l0_after: float
    n_l1: int
    n_l2: int
    n_l3: int


@dataclass
class DCAConfig:
    # Reference for L1 buy/sell trigger
    ref_type: str = "w2_close"         # "w2_close" | "ma4w"
    # L2 / L3 correction thresholds (negative %, e.g. -8.0)
    corr_medium_pct: float = -8.0
    corr_large_pct: float = -20.0
    # Size multipliers vs base unit S
    mult_medium: float = 3.0
    mult_large: float = 10.0
    # Sell mode
    sell_mode: str = "price_or_spike"  # "price_only" | "price_or_spike"
    spike_k: float = 2.0               # spike = (close - open) > spike_k * ATR
    # Cooldown (in weeks) before another L2/L3 buy
    cooldown_l2_weeks: int = 2
    cooldown_l3_weeks: int = 4
    # Weekly injection (in S units, added to L0 each week)
    weekly_injection: float = 1.0
    # Fallback: buy at week-end close if L1 trigger never fired this week
    fallback_l1: bool = True


class DCAEngine:
    def __init__(self, config: DCAConfig, initial_l0: float = 0.0):
        self.cfg = config
        self.l0 = initial_l0
        self.positions: List[Position] = []
        self.events: List[Event] = []

        self._current_week: Optional[str] = None
        self._l1_bought_this_week = False
        self._l1_fallback_price: Optional[float] = None   # Monday open, used if no trigger
        self._l2_last_buy: Optional[pd.Timestamp] = None
        self._l3_last_buy: Optional[pd.Timestamp] = None
        self._total_injected: float = 0.0

    # ── Properties ──────────────────────────────────────────────────────────

    def _l1_positions(self) -> List[Position]:
        return [p for p in self.positions if p.layer == "L1"]

    def _ref_price(self, bar: pd.Series) -> Optional[float]:
        v = bar["ref_w2"] if self.cfg.ref_type == "w2_close" else bar["ma4w"]
        return float(v) if pd.notna(v) and v > 0 else None

    def _week_of(self, ts: pd.Timestamp) -> str:
        iso = ts.isocalendar()
        return f"{iso[0]}_{iso[1]:02d}"

    def _weeks_since(self, ts: Optional[pd.Timestamp], now: pd.Timestamp) -> float:
        if ts is None:
            return float("inf")
        return (now - ts).days / 7.0

    def _log(self, event_type: str, date: pd.Timestamp, price: float,
             qty_s: float, trigger: str) -> None:
        l1 = [p for p in self.positions if p.layer == "L1"]
        l2 = [p for p in self.positions if p.layer == "L2"]
        l3 = [p for p in self.positions if p.layer == "L3"]
        self.events.append(Event(
            date=date, event_type=event_type, price=price, qty_s=qty_s,
            trigger=trigger, l0_after=self.l0,
            n_l1=len(l1), n_l2=len(l2), n_l3=len(l3),
        ))

    # ── Main bar processor ──────────────────────────────────────────────────

    def process(self, ts: pd.Timestamp, bar: pd.Series) -> None:
        week = self._week_of(ts)

        # 1. New week: inject capital, reset L1 flag, record Monday open as fallback price
        if week != self._current_week:
            self._current_week = week
            self._l1_bought_this_week = False
            self._l1_fallback_price = bar["open"]   # Monday open = worst-case entry
            self.l0 += self.cfg.weekly_injection
            self._total_injected += self.cfg.weekly_injection
            self._log("INJECT", ts, bar["close"], self.cfg.weekly_injection, "weekly")

        ref = self._ref_price(bar)
        atr = bar.get("atr_d1", 0.0)
        corr_4w = bar.get("corr_4w_pct", 0.0)
        corr_4m = bar.get("corr_4m_pct", 0.0)

        # 2. L3 buy — monthly correction (highest priority)
        if (pd.notna(corr_4m) and corr_4m <= self.cfg.corr_large_pct
                and self._weeks_since(self._l3_last_buy, ts) >= self.cfg.cooldown_l3_weeks
                and self.l0 >= self.cfg.mult_large):
            qty = self.cfg.mult_large
            price = bar["close"]
            self.l0 -= qty
            self.positions.append(Position(ts, price, qty, "L3"))
            self._l3_last_buy = ts
            self._log("BUY_L3", ts, price, qty,
                      f"corr_4m={corr_4m:.1f}%")

        # 3. L2 buy — weekly correction
        elif (pd.notna(corr_4w) and corr_4w <= self.cfg.corr_medium_pct
              and self._weeks_since(self._l2_last_buy, ts) >= self.cfg.cooldown_l2_weeks
              and self.l0 >= self.cfg.mult_medium):
            qty = self.cfg.mult_medium
            price = bar["close"]
            self.l0 -= qty
            self.positions.append(Position(ts, price, qty, "L2"))
            self._l2_last_buy = ts
            self._log("BUY_L2", ts, price, qty,
                      f"corr_4w={corr_4w:.1f}%")

        # 4. L1 buy — weekly DCA (limit at ref_w2)
        if (not self._l1_bought_this_week and ref is not None
                and bar["low"] < ref and self.l0 >= 1.0):
            entry_price = ref           # limit order at the reference level
            self.l0 -= 1.0
            self.positions.append(Position(ts, entry_price, 1.0, "L1"))
            self._l1_bought_this_week = True
            self._log("BUY_L1", ts, entry_price, 1.0, f"low<ref={ref:.2f}")

        # 5. L1 sell — price trigger: close above ref
        # Sell at close (not at ref_w2) so P&L > 0 when close > entry (ref_w2)
        l1 = self._l1_positions()
        if ref is not None and l1 and bar["close"] > ref:
            sell_price = bar["close"]
            total_qty = sum(p.qty_s for p in l1)
            self.positions = [p for p in self.positions if p.layer != "L1"]
            self.l0 += total_qty            # recycle original S units to L0
            self._log("SELL_L1", ts, sell_price, total_qty, "close>ref")

        # 6. L1 sell — spike trigger (bullish spike = take quick profit)
        elif (self.cfg.sell_mode == "price_or_spike" and l1
              and atr > 0 and (bar["close"] - bar["open"]) > self.cfg.spike_k * atr):
            spike_price = bar["close"]
            total_qty = sum(p.qty_s for p in l1)
            self.positions = [p for p in self.positions if p.layer != "L1"]
            self.l0 += total_qty
            self._log("SELL_L1", ts, spike_price, total_qty,
                      f"spike {(bar['close']-bar['open']):.1f}>{self.cfg.spike_k}*ATR")

        # 7. L1 fallback — last bar of week, no trigger fired → buy at Monday open
        # Monday open recorded at week start; guarantees avg_price ≤ benchmark (same entry)
        if (self.cfg.fallback_l1 and not self._l1_bought_this_week
                and bar.get("is_week_end", False) and self.l0 >= 1.0
                and self._l1_fallback_price is not None):
            entry_price = self._l1_fallback_price
            self.l0 -= 1.0
            self.positions.append(Position(ts, entry_price, 1.0, "L1"))
            self._l1_bought_this_week = True
            self._log("BUY_L1", ts, entry_price, 1.0, "fallback_monday_open")

    # ── Results ─────────────────────────────────────────────────────────────

    def summary(self, last_price: float) -> dict:
        buys = [e for e in self.events if e.event_type.startswith("BUY")]
        sells = [e for e in self.events if e.event_type == "SELL_L1"]

        if not buys:
            return {"error": "no_trades"}

        buy_l1 = [e for e in buys if e.event_type == "BUY_L1"]
        buy_l2 = [e for e in buys if e.event_type == "BUY_L2"]
        buy_l3 = [e for e in buys if e.event_type == "BUY_L3"]

        def wavg(events):
            tot_qty = sum(e.qty_s for e in events)
            if tot_qty == 0:
                return float("nan")
            return sum(e.price * e.qty_s for e in events) / tot_qty

        total_bought_s = sum(e.qty_s for e in buys)
        total_sold_s = sum(e.qty_s for e in sells)
        held_s = sum(p.qty_s for p in self.positions)

        # P&L on deployed capital only (excluding idle L0)
        # sell_proceeds: realized cash from L1 sells (at sell price)
        # held_value: mark-to-market for still-held positions
        # total_cost: capital deployed into buys (in pts)
        sell_proceeds_pts = sum(e.price * e.qty_s for e in sells)
        buy_cost_pts = sum(e.price * e.qty_s for e in buys)
        held_cost_pts = sum(p.price * p.qty_s for p in self.positions)
        held_value_pts = held_s * last_price

        # Realized + unrealized P&L on deployed capital
        realized_profit_pts = sell_proceeds_pts - (buy_cost_pts - held_cost_pts)
        unrealized_profit_pts = held_value_pts - held_cost_pts
        total_profit_pts = realized_profit_pts + unrealized_profit_pts
        total_return_pct = (
            total_profit_pts / buy_cost_pts * 100 if buy_cost_pts > 0 else 0.0
        )

        # Units accumulated vs capital efficiency
        # avg cost across all held + sold positions
        avg_accumulation_price = buy_cost_pts / total_bought_s if total_bought_s > 0 else float("nan")

        portfolio_value_pts = held_value_pts

        return {
            "n_l1_buys":              len(buy_l1),
            "n_l2_buys":              len(buy_l2),
            "n_l3_buys":              len(buy_l3),
            "n_l1_sells":             len(sells),
            "avg_price_l1":           round(wavg(buy_l1), 2) if buy_l1 else float("nan"),
            "avg_price_l2":           round(wavg(buy_l2), 2) if buy_l2 else float("nan"),
            "avg_price_l3":           round(wavg(buy_l3), 2) if buy_l3 else float("nan"),
            "avg_price_all":          round(wavg(buys), 2),
            "total_bought_s":         round(total_bought_s, 2),
            "total_sold_s":           round(total_sold_s, 2),
            "held_s":                 round(held_s, 2),
            "total_injected_s":       round(self._total_injected, 2),
            "l0_remaining_s":         round(self.l0, 2),
            "total_return_pct":       round(total_return_pct, 2),
            "realized_profit_pts":    round(realized_profit_pts, 0),
            "unrealized_profit_pts":  round(unrealized_profit_pts, 0),
            "max_simultaneous_s":     _max_simultaneous(self.events),
        }


def _max_simultaneous(events: List[Event]) -> float:
    """Peak total units held simultaneously (L1+L2+L3)."""
    peak = 0.0
    held = 0.0
    for e in events:
        if e.event_type.startswith("BUY"):
            held += e.qty_s
            peak = max(peak, held)
        elif e.event_type == "SELL_L1":
            held -= e.qty_s
    return round(peak, 2)


def run_simulation(
    df: pd.DataFrame,
    config: DCAConfig,
    initial_l0: float = 0.0,
) -> Tuple[DCAEngine, dict]:
    engine = DCAEngine(config, initial_l0)
    for ts, bar in df.iterrows():
        engine.process(ts, bar)
    last_price = float(df["close"].iloc[-1])
    summary = engine.summary(last_price)
    return engine, summary
