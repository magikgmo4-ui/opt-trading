#!/usr/bin/env python3
"""BTC COIN-M parameter sweep simulation engine (PAPER_LOCKED formulas)."""
from __future__ import annotations

import hashlib
import json
import math
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE.parents[1]
STATE_DIR = REPO_ROOT / "state" / "trading_lab_v1"
RUNS_SUMMARY_JSONL = STATE_DIR / "param_sweep_runs_summary.jsonl"
CAMPAIGNS_JSONL = STATE_DIR / "param_sweep_campaigns.jsonl"


# ── risk tier table (PAPER_LOCKED, from BACKTEST_DATA_PREP_01) ──────────

RISK_TIERS = [
    {"tier": 1, "notional_max_usd": 50000, "mmr": 0.005, "max_lever": 125},
    {"tier": 2, "notional_max_usd": 250000, "mmr": 0.010, "max_lever": 100},
    {"tier": 3, "notional_max_usd": 1000000, "mmr": 0.015, "max_lever": 50},
    {"tier": 4, "notional_max_usd": 5000000, "mmr": 0.025, "max_lever": 25},
    {"tier": 5, "notional_max_usd": 10000000, "mmr": 0.050, "max_lever": 10},
    {"tier": 6, "notional_max_usd": 20000000, "mmr": 0.100, "max_lever": 5},
    {"tier": 7, "notional_max_usd": 50000000, "mmr": 0.150, "max_lever": 2},
    {"tier": 8, "notional_max_usd": 100000000, "mmr": 0.250, "max_lever": 1},
]


def _mmr_for_notional(notional_usd: float) -> float:
    for tier in RISK_TIERS:
        if notional_usd <= tier["notional_max_usd"]:
            return tier["mmr"]
    return RISK_TIERS[-1]["mmr"]


# ── PAPER_LOCKED formulas (FORMULAS_SOURCE_LOCK_01) ──────────────────────

def qty_to_notional(Q_native: float, contract_size: float = 1.0) -> float:
    """U1 PAPER_LOCKED: N_usd = Q_native * contractSize."""
    return Q_native * contract_size


def pnl_inverse_short(Q_native: float, P: float, E: float) -> float:
    """U3 PAPER_LOCKED: PnL_btc = Q_native * (1/P - 1/E)."""
    if Q_native <= 0 or P <= 0 or E <= 0:
        return 0.0
    return Q_native * (1.0 / P - 1.0 / E)


def funding_increment(Q_native: float, mark_price: float, funding_rate: float) -> float:
    """U4+U5 PAPER_LOCKED: funding = (Q_native / MarkPrice) * fundingRate."""
    if Q_native <= 0 or mark_price <= 0:
        return 0.0
    return (Q_native / mark_price) * funding_rate


def maintenance_margin_btc(Q_native: float, mark_price: float) -> float:
    """U7 PAPER_LOCKED: MM_btc = (Q_native / MarkPrice) * MMR_tier."""
    if Q_native <= 0 or mark_price <= 0:
        return 0.0
    notional_usd = qty_to_notional(Q_native)
    mmr = _mmr_for_notional(notional_usd)
    return (Q_native / mark_price) * mmr


def margin_ratio(Q_native: float, E: float, mark_price: float, wallet_btc: float) -> float | None:
    """U8 PAPER_LOCKED: MR = equity / MM_btc."""
    if Q_native <= 0 or mark_price <= 0:
        return None
    mm_btc = maintenance_margin_btc(Q_native, mark_price)
    if mm_btc <= 0:
        return None
    equity = wallet_btc + pnl_inverse_short(Q_native, mark_price, E)
    return equity / mm_btc


def liquidation_price_short(Q_native: float, E: float, wallet_btc: float) -> float | None:
    """U6 PAPER_LOCKED: LiqPrice for cross short.

    LiqPrice = Q * (1 - MMR) / (Q/E - WB)

    Returns None if position cannot be liquidated (wallet covers position).
    """
    if Q_native <= 0 or E <= 0:
        return None
    notional_usd = qty_to_notional(Q_native)
    mmr = _mmr_for_notional(notional_usd)
    denom = Q_native / E - wallet_btc
    if denom <= 0:
        return None
    return Q_native * (1.0 - mmr) / denom


def liquidation_distance(liq_price: float | None, mark_price: float) -> float | None:
    """Distance to liquidation: (LiqPrice - MarkPrice) / MarkPrice."""
    if liq_price is None or mark_price <= 0:
        return None
    return (liq_price - mark_price) / mark_price


# ── state machine ────────────────────────────────────────────────────────

_INITIAL_STATE_TEMPLATE: dict[str, Any] = {
    "P_k": 0.0,
    "S_k_btc": 0.0,
    "U_k_usdt": 0.0,
    "M_k_btc": 0.0,
    "Q_k_native": 0.0,
    "E_k": None,
    "PnL_r_cumul_btc": 0.0,
    "Funding_paid_btc": 0.0,
    "Funding_received_btc": 0.0,
    "Fee_cumul_btc": 0.0,
    "NAV_peak_btc": 0.0,
    "last_dca_ts": None,
    "last_dca_price": 0.0,
    "last_short_ts": None,
    "last_short_price": 0.0,
    "last_pivot_price": 0.0,
    "liquidated": False,
    "liquidation_count": 0,
    "margin_breach_count": 0,
    "d_min_breach_count": 0,
    "capital_exhaustion_count": 0,
    "dca_count": 0,
    "short_add_count": 0,
    "tp_count": 0,
    "funding_event_count": 0,
    "fee_event_count": 0,
    "exchange_impossible_event_count": 0,
    "max_drawdown_btc": 0.0,
    "min_distance_to_liq": None,
    "max_position_native": 0.0,
    "max_notional_usd": 0.0,
    "max_leverage_realized": 0.0,
    "event_log": [],
}


def _init_state(initial: dict[str, Any]) -> dict[str, Any]:
    state = dict(_INITIAL_STATE_TEMPLATE)
    state["P_k"] = initial.get("P_0", 100000.0)
    state["S_k_btc"] = initial.get("S_0_btc", 0.1)
    state["U_k_usdt"] = initial.get("U_0_usdt", 10000.0)
    state["M_k_btc"] = initial.get("M_0_btc", 0.02)
    state["Q_k_native"] = initial.get("Q_0_native", 0.0)
    state["E_k"] = initial.get("E_0", None)
    state["PnL_r_cumul_btc"] = initial.get("PnL_r_0_btc", 0.0)
    state["Funding_paid_btc"] = 0.0
    state["Funding_received_btc"] = 0.0
    state["Fee_cumul_btc"] = initial.get("Fee_0_btc", 0.0)
    state["last_pivot_price"] = state["P_k"]
    nav0 = _compute_nav(state, state["P_k"])
    state["NAV_peak_btc"] = nav0
    state["event_log"] = []
    return state


def _compute_nav(state: dict[str, Any], P: float) -> float:
    equity = state["M_k_btc"]
    if state["Q_k_native"] > 0 and state["E_k"] is not None and state["E_k"] > 0:
        equity += pnl_inverse_short(state["Q_k_native"], P, state["E_k"])
    return state["S_k_btc"] + equity + state["U_k_usdt"] / P if P > 0 else state["S_k_btc"] + equity


def _compute_drawdown(state: dict[str, Any], P: float) -> float:
    nav = _compute_nav(state, P)
    if state["NAV_peak_btc"] <= 0:
        return 0.0
    return max(0.0, 1.0 - nav / state["NAV_peak_btc"])


# ── simulation steps ─────────────────────────────────────────────────────

def resolve_price(candle: dict[str, Any]) -> tuple[float, bool]:
    """Return (price, used_mark_proxy)."""
    mark = candle.get("mark_price")
    if mark is not None and isinstance(mark, (int, float)) and mark > 0:
        return float(mark), False
    idx = candle.get("index_price")
    if idx is not None and isinstance(idx, (int, float)) and idx > 0:
        return float(idx), True
    close = candle.get("close", 0.0)
    return float(close), True


def apply_funding(state: dict[str, Any], candle: dict[str, Any]) -> None:
    if not candle.get("funding_settled", False):
        return
    Q = state["Q_k_native"]
    if Q <= 0:
        return
    rate = candle.get("funding_rate")
    if rate is None:
        return
    P_mark, _ = resolve_price(candle)
    if P_mark <= 0:
        return
    inc = funding_increment(Q, P_mark, float(rate))
    state["M_k_btc"] += inc
    if inc >= 0:
        state["Funding_received_btc"] += inc
    else:
        state["Funding_paid_btc"] += abs(inc)
    state["funding_event_count"] += 1
    state["event_log"].append({
        "type": "funding", "ts": candle.get("ts"),
        "rate": float(rate), "inc_btc": inc,
    })


def apply_dca(state: dict[str, Any], P: float, config: dict[str, Any], candle_ts: str) -> None:
    if P <= 0:
        return
    z_dca = config.get("z_dca", 0.005)
    y_dca_usdt = config.get("y_dca_usdt", 200.0)
    r_transfer = config.get("r_transfer", 0.30)
    cooldown_h = config.get("cooldown_dca_h", 8)

    if state["U_k_usdt"] < y_dca_usdt:
        return

    if state["last_dca_price"] > 0:
        drop_ratio = (P - state["last_dca_price"]) / state["last_dca_price"]
        if drop_ratio > -z_dca:
            return

    if cooldown_h > 0 and state["last_dca_ts"] is not None and candle_ts is not None:
        try:
            last_dt = datetime.fromisoformat(str(state["last_dca_ts"]).replace("Z", "+00:00"))
            curr_dt = datetime.fromisoformat(str(candle_ts).replace("Z", "+00:00"))
            if (curr_dt - last_dt).total_seconds() < cooldown_h * 3600:
                return
        except (ValueError, TypeError):
            pass

    btc_bought = y_dca_usdt / P
    btc_to_margin = btc_bought * r_transfer
    btc_to_spot = btc_bought - btc_to_margin

    state["S_k_btc"] += btc_to_spot
    state["M_k_btc"] += btc_to_margin
    state["U_k_usdt"] -= y_dca_usdt
    state["last_dca_ts"] = candle_ts
    state["last_dca_price"] = P
    state["dca_count"] += 1
    state["event_log"].append({
        "type": "dca", "ts": candle_ts, "P": P,
        "btc_bought": btc_bought, "btc_to_margin": btc_to_margin,
    })


def apply_short_add(state: dict[str, Any], P: float, config: dict[str, Any],
                    candle_ts: str) -> None:
    if P <= 0:
        return
    g_up = config.get("g_up", 0.015)
    q_add = config.get("q_add_native", 0.001)
    z_short = config.get("z_short", 0.015)
    cooldown_h = config.get("cooldown_short_h", 8)
    taker_fee = 0.0006

    pivot = state["last_pivot_price"]
    if pivot <= 0:
        return
    if P < pivot * (1.0 + g_up):
        return

    if z_short > 0 and state["last_short_price"] > 0:
        gap = (P - state["last_short_price"]) / state["last_short_price"]
        if abs(gap) < z_short:
            return

    if cooldown_h > 0 and state["last_short_ts"] is not None and candle_ts is not None:
        try:
            last_dt = datetime.fromisoformat(str(state["last_short_ts"]).replace("Z", "+00:00"))
            curr_dt = datetime.fromisoformat(str(candle_ts).replace("Z", "+00:00"))
            if (curr_dt - last_dt).total_seconds() < cooldown_h * 3600:
                return
        except (ValueError, TypeError):
            pass

    q_actual = q_add
    fee_btc = q_actual * taker_fee

    old_Q = state["Q_k_native"]
    old_E = state["E_k"] if state["E_k"] is not None and state["E_k"] > 0 else P
    if old_Q > 0 and old_E > 0:
        new_E = (old_E * old_Q + P * q_actual) / (old_Q + q_actual)
    else:
        new_E = P

    state["E_k"] = new_E
    state["Q_k_native"] += q_actual
    state["Fee_cumul_btc"] += fee_btc
    state["M_k_btc"] -= fee_btc
    state["last_short_ts"] = candle_ts
    state["last_short_price"] = P
    state["short_add_count"] += 1
    state["fee_event_count"] += 1

    state["max_position_native"] = max(state["max_position_native"], state["Q_k_native"])
    state["max_notional_usd"] = max(state["max_notional_usd"], qty_to_notional(state["Q_k_native"]))

    state["event_log"].append({
        "type": "short_add", "ts": candle_ts, "P": P,
        "q_add": q_actual, "new_Q": state["Q_k_native"], "new_E": new_E,
        "fee_btc": fee_btc,
    })

    # track exchange-impossible events in free-search mode
    _check_exchange_constraints(state, q_actual, P, config)


def _check_exchange_constraints(state: dict[str, Any], q: float, P: float,
                                config: dict[str, Any]) -> None:
    size_multiplier = 0.0001
    min_trade_num = 0.0001
    max_lever = 125
    impossible = False
    if q % size_multiplier != 0:
        impossible = True
    if q < min_trade_num:
        impossible = True
    lev = config.get("leverage_target", 2)
    if lev > max_lever or lev < 1:
        impossible = True
    if impossible:
        state["exchange_impossible_event_count"] += 1


def apply_tp(state: dict[str, Any], P: float, config: dict[str, Any],
             candle_ts: str) -> None:
    Q = state["Q_k_native"]
    if Q <= 0 or P <= 0:
        return
    E = state["E_k"]
    if E is None or E <= 0:
        return

    g_down = config.get("g_down", 0.010)
    pivot = state["last_pivot_price"]
    if pivot <= 0 or P > pivot * (1.0 - g_down):
        return

    tp1 = config.get("tp1", 0.50)
    tp2 = config.get("tp2", 0.25)
    q_add_ref = config.get("q_add_native", 0.001)

    q_close_1 = min(Q, q_add_ref * tp1)
    remaining = Q - q_close_1
    q_close_2 = min(remaining, q_add_ref * tp2)
    pnl_1 = pnl_inverse_short(q_close_1, P, E)
    pnl_2 = pnl_inverse_short(q_close_2, P, E)

    state["Q_k_native"] = Q - q_close_1 - q_close_2
    state["PnL_r_cumul_btc"] += pnl_1 + pnl_2
    state["M_k_btc"] += pnl_1 + pnl_2
    state["last_pivot_price"] = P
    state["tp_count"] += 1

    if state["Q_k_native"] <= 0:
        state["Q_k_native"] = 0.0
        state["E_k"] = None

    state["event_log"].append({
        "type": "tp", "ts": candle_ts, "P": P,
        "q_close_1": q_close_1, "q_close_2": q_close_2,
        "pnl_btc": pnl_1 + pnl_2, "remaining_Q": state["Q_k_native"],
    })


def _record_breaches(state: dict[str, Any], P: float, config: dict[str, Any]) -> None:
    Q = state["Q_k_native"]
    E = state["E_k"]
    if Q <= 0 or E is None or E <= 0:
        return

    liq = liquidation_price_short(Q, E, state["M_k_btc"])
    dist = liquidation_distance(liq, P)

    D_min = config.get("D_min", 0.20)
    MR_max = config.get("MR_max", 0.60)
    Q_max = config.get("Q_max_native", 0.02)
    funding_limit = config.get("funding_limit", 0.001)
    fee_limit = config.get("fee_limit", 0.0005)

    if dist is not None and dist < D_min:
        state["d_min_breach_count"] += 1
    if state["min_distance_to_liq"] is None or (dist is not None and dist < state["min_distance_to_liq"]):
        state["min_distance_to_liq"] = dist

    mr = margin_ratio(Q, E, P, state["M_k_btc"])
    if mr is not None and mr > MR_max:
        state["margin_breach_count"] += 1
    if Q > Q_max:
        state["margin_breach_count"] += 1
    if state["Funding_paid_btc"] > funding_limit:
        pass  # diagnostic only, counted as cumulative
    if state["Fee_cumul_btc"] > fee_limit:
        pass

    if state["S_k_btc"] <= 0 and state["U_k_usdt"] <= 0 and state["M_k_btc"] <= 0:
        state["capital_exhaustion_count"] += 1


def check_liquidation(state: dict[str, Any], P: float) -> None:
    Q = state["Q_k_native"]
    if Q <= 0:
        return
    E = state["E_k"]
    if E is None or E <= 0:
        return

    if state["M_k_btc"] <= 0:
        state["liquidated"] = True
        state["liquidation_count"] += 1
        state["Q_k_native"] = 0.0
        state["E_k"] = None
        state["event_log"].append({
            "type": "liquidation", "P": P, "reason": "margin_depleted",
        })
        return

    liq = liquidation_price_short(Q, E, state["M_k_btc"])
    if liq is not None and P >= liq:
        pnl_liq = pnl_inverse_short(Q, liq, E)
        state["PnL_r_cumul_btc"] += pnl_liq
        state["M_k_btc"] += pnl_liq
        state["liquidated"] = True
        state["liquidation_count"] += 1
        state["Q_k_native"] = 0.0
        state["E_k"] = None
        state["event_log"].append({
            "type": "liquidation", "P": P, "liq_price": liq,
            "pnl_btc": pnl_liq,
        })


# ── main loop ────────────────────────────────────────────────────────────

def simulate_run(config: dict[str, Any],
                 candles: list[dict[str, Any]],
                 contract_spec: dict[str, Any] | None = None,
                 initial_state: dict[str, Any] | None = None,
                 apply_guards: bool = False) -> dict[str, Any]:
    """Run one simulation and return the canonical result dict."""
    if initial_state is None:
        initial_state = {}
    state = _init_state(initial_state)
    contract_spec = contract_spec or {}

    run_id = str(uuid.uuid4())[:12]
    config_hash_str = _sha(config)
    start_ts = candles[0].get("ts") if candles else None
    end_ts = candles[-1].get("ts") if candles else None
    nav_initial = _compute_nav(state, state["P_k"])
    stop_reason = "completed"

    for candle in candles:
        P, used_proxy = resolve_price(candle)
        if P <= 0 or math.isnan(P) or math.isinf(P):
            stop_reason = "math_invalid"
            break

        ts = candle.get("ts", "")

        apply_funding(state, candle)
        apply_dca(state, P, config, ts)
        apply_short_add(state, P, config, ts)
        apply_tp(state, P, config, ts)

        state["P_k"] = P
        _record_breaches(state, P, config)

        nav = _compute_nav(state, P)
        if nav > state["NAV_peak_btc"]:
            state["NAV_peak_btc"] = nav

        dd = _compute_drawdown(state, P)
        if dd > state["max_drawdown_btc"]:
            state["max_drawdown_btc"] = dd

        check_liquidation(state, P)
        if state["liquidated"]:
            stop_reason = "liquidated"
            break

        max_lev = 0.0
        if state["Q_k_native"] > 0 and state["M_k_btc"] > 0 and P > 0:
            pos_val = qty_to_notional(state["Q_k_native"]) / P
            max_lev = min(pos_val / state["M_k_btc"], 999.0) if state["M_k_btc"] > 0 else 0.0
        if max_lev > state["max_leverage_realized"]:
            state["max_leverage_realized"] = max_lev

    nav_final = _compute_nav(state, state["P_k"])
    return _build_output(state, config, run_id, config_hash_str, candles,
                         start_ts, end_ts, nav_initial, nav_final,
                         stop_reason, contract_spec)


def _build_output(state: dict[str, Any], config: dict[str, Any],
                  run_id: str, config_hash_str: str,
                  candles: list[dict[str, Any]],
                  start_ts: str | None, end_ts: str | None,
                  nav_initial: float, nav_final: float,
                  stop_reason: str,
                  contract_spec: dict[str, Any] | None = None) -> dict[str, Any]:
    delta_btc = nav_final - nav_initial
    Q_final = state["Q_k_native"]
    E_final = state["E_k"]
    unrealized = 0.0
    if Q_final > 0 and E_final is not None and E_final > 0 and state["P_k"] > 0:
        unrealized = pnl_inverse_short(Q_final, state["P_k"], E_final)

    funding_count = 0
    for c in candles:
        if c.get("funding_settled"):
            funding_count += 1

    output: dict[str, Any] = {
        "run_id": run_id,
        "batch_id": "",
        "config_hash": config_hash_str,
        "seed": config.get("_seed", 0),
        "generator_method": config.get("_generator_method", "unknown"),
        "generator_stage": config.get("_generator_stage", ""),
        "engine_version": "param_sweep_engine_v1",
        "dataset_id": "",
        "dataset_start": start_ts,
        "dataset_end": end_ts,
        "timeframe_primary": "1h",
        "candle_count": len(candles),
        "funding_points": funding_count,
        "contract_snapshot_id": "",
        "config": config,
        "config_surface_version": "free_search_v1",
        "apply_strategic_guards": False,
        "net_btc_initial": round(nav_initial, 12),
        "net_btc_final": round(nav_final, 12),
        "delta_btc_net": round(delta_btc, 12),
        "delta_btc_pct": round(delta_btc / nav_initial * 100, 6) if nav_initial > 0 else 0.0,
        "spot_btc_final": round(state["S_k_btc"], 12),
        "margin_btc_final": round(state["M_k_btc"], 12),
        "reserve_usdt_final": round(state["U_k_usdt"], 6),
        "realized_pnl_btc": round(state["PnL_r_cumul_btc"], 12),
        "unrealized_pnl_btc": round(unrealized, 12),
        "funding_paid_btc": round(state["Funding_paid_btc"], 12),
        "funding_received_btc": round(state["Funding_received_btc"], 12),
        "fees_btc": round(state["Fee_cumul_btc"], 12),
        "max_drawdown_btc": round(state["max_drawdown_btc"], 12),
        "max_drawdown_pct": round(state["max_drawdown_btc"] * 100, 4),
        "liquidation_count": state["liquidation_count"],
        "margin_breach_count": state["margin_breach_count"],
        "d_min_breach_count": state["d_min_breach_count"],
        "capital_exhaustion_count": state["capital_exhaustion_count"],
        "worst_margin_ratio": None,
        "min_distance_to_liq": state["min_distance_to_liq"],
        "max_position_native": round(state["max_position_native"], 8),
        "max_notional_usd": round(state["max_notional_usd"], 2),
        "max_leverage_realized": round(state["max_leverage_realized"], 2),
        "dca_count": state["dca_count"],
        "short_add_count": state["short_add_count"],
        "tp_count": state["tp_count"],
        "funding_event_count": state["funding_event_count"],
        "fee_event_count": state["fee_event_count"],
        "exchange_impossible_event_count": state["exchange_impossible_event_count"],
        "simulation_stop_reason": stop_reason,
        "math_valid": stop_reason != "math_invalid",
        "data_valid": True,
        "exchange_feasible": True,
        "used_paper_locked_formula": True,
        "used_mark_proxy": False,
        "classification_primary": "",
        "classification_tags": [],
        "reject_reasons": [],
        "overfit_score": 0.0,
        "notes": [],
    }
    return output


# ── helpers ───────────────────────────────────────────────────────────────

def _sha(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def count_jsonl(path: Path) -> int:
    return len(load_jsonl(path))
