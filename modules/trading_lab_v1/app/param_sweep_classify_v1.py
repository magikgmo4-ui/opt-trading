#!/usr/bin/env python3
"""BTC COIN-M sweep reality classifier (post-simulation)."""
from __future__ import annotations

from typing import Any


def classify_run(run: dict[str, Any]) -> dict[str, Any]:
    """Apply classification rules and return the updated run dict."""
    tags: list[str] = []
    reasons: list[str] = []
    notes: list[str] = []

    primary = _classify_primary(run, tags, reasons, notes)

    run["classification_primary"] = primary
    run["classification_tags"] = tags
    run["reject_reasons"] = reasons
    run["notes"] = notes
    return run


def _classify_primary(run: dict[str, Any],
                      tags: list[str],
                      reasons: list[str],
                      notes: list[str]) -> str:

    # 1. MATH_INVALID
    math_valid = bool(run.get("math_valid", True))
    stop = run.get("simulation_stop_reason", "")
    if not math_valid or stop == "math_invalid":
        reasons.append("ERR_NAN_STATE" if not math_valid else "ERR_MATH_INVALID")
        return "MATH_INVALID"

    config = run.get("config", {})
    if (run.get("candle_count", 0) > 0 and
            (run.get("net_btc_initial") is None or run.get("net_btc_final") is None)):
        reasons.append("ERR_MATH_INVALID")
        return "MATH_INVALID"

    tp1 = config.get("tp1", 0)
    tp2 = config.get("tp2", 0)
    runner = config.get("runner", 0)
    if abs(tp1 + tp2 + runner - 1.0) > 0.001:
        reasons.append("ERR_TP_SIMPLEX_INVALID")
        return "MATH_INVALID"

    # 2. DATA_INVALID
    if not run.get("data_valid", True):
        reasons.append("ERR_DATA_INVALID")
        return "DATA_INVALID"

    # 3. LIQUIDATED
    if run.get("liquidation_count", 0) > 0:
        reasons.append("ERR_LIQUIDATION_TRIGGERED")
        return "LIQUIDATED"

    # 4. EXCHANGE_IMPOSSIBLE
    if _is_exchange_impossible(run, reasons):
        return "EXCHANGE_IMPOSSIBLE"

    # 5. PAPER_ONLY
    if run.get("used_paper_locked_formula", True):
        tags.append("WARN_PAPER_LOCKED_FORMULA")
    if run.get("used_mark_proxy", False):
        tags.append("WARN_MARK_PROXY_USED")
    gw_mode = config.get("weekly_structure_gate_mode", "off")
    if gw_mode != "off":
        tags.append("WARN_WEEKLY_GATE_SPEC_ONLY")

    if _has_paper_only_flags(tags):
        return "PAPER_ONLY"

    # 6. REALISTIC
    if run.get("liquidation_count", 0) == 0:
        return "REALISTIC"

    return "PAPER_ONLY"


def _is_exchange_impossible(run: dict[str, Any], reasons: list[str]) -> bool:
    if run.get("exchange_impossible_event_count", 0) > 0:
        reasons.append("ERR_QTY_OFF_GRID")
        return True

    config = run.get("config", {})
    q_add = config.get("q_add_native", 0.001)
    if q_add < 0.0001:
        reasons.append("ERR_QTY_BELOW_MIN")
        return True
    if q_add % 0.0001 != 0:
        reasons.append("ERR_QTY_OFF_GRID")
        return True

    lev = config.get("leverage_target", 2)
    if lev > 125 or lev < 1:
        reasons.append("ERR_LEVERAGE_ABOVE_MAX" if lev > 125 else "ERR_LEVERAGE_BELOW_MIN")
        return True

    marg = config.get("marginCoin", "BTC")
    if marg != "BTC":
        reasons.append("ERR_UNSUPPORTED_MARGIN_MODE")
        return True

    return False


def _has_paper_only_flags(tags: list[str]) -> bool:
    return any(t.startswith("WARN_") for t in tags)
