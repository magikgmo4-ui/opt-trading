"""
SPCX Orderflow Scoring Engine
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Scores orderflow quality from bucket data produced by spcx_sip_tape + spcx_l2_depth.
Produces a unified orderflow quality score (0-100) with component breakdown.
"""
from __future__ import annotations
from typing import Any


def score_orderflow(
    tape_data: dict | None = None,
    depth_data: dict | None = None,
    auction_data: dict | None = None,
) -> dict[str, Any]:
    """Score SPCX orderflow quality from composite market microstructure data.

    Args:
        tape_data: Output from collect_spcx_sip_tape()
        depth_data: Output from collect_spcx_l2_depth()
        auction_data: Output from collect_spcx_auction_imbalance()
    """
    result = {
        "score": 50.0,
        "component_scores": {},
        "signals": [],
        "reasons": [],
        "warnings": [],
    }

    # --- 1. Liquidity score (from depth data) ---
    liquidity = _score_liquidity(depth_data)
    result["component_scores"]["liquidity"] = liquidity

    # --- 2. Tape flow score (from tape data) ---
    tape_flow = _score_tape_flow(tape_data)
    result["component_scores"]["tape_flow"] = tape_flow

    # --- 3. Auction score (from auction data) ---
    auction = _score_auction(auction_data)
    result["component_scores"]["auction"] = auction

    # --- 4. Volume quality score ---
    volume_quality = _score_volume_quality(tape_data)
    result["component_scores"]["volume_quality"] = volume_quality

    # --- 5. Price vs VWAP context ---
    price_context = _score_price_context(tape_data)
    result["component_scores"]["price_context"] = price_context

    # --- Composite score ---
    weights = {
        "liquidity": 0.25,
        "tape_flow": 0.35,
        "auction": 0.15,
        "volume_quality": 0.15,
        "price_context": 0.10,
    }

    composite = 0.0
    total_weight = 0.0
    for key, weight in weights.items():
        val = result["component_scores"].get(key, {})
        if isinstance(val, dict):
            comp_score = val.get("score", 50)
        else:
            comp_score = 50
        composite += comp_score * weight
        total_weight += weight

    result["score"] = round(composite / total_weight, 1) if total_weight > 0 else 50.0

    # --- Signals ---
    if result["score"] >= 80:
        result["signals"].append("SPCX_ORDERFLOW_BULLISH")
        result["signals"].append("STRONG_BUY_FLOW")
    elif result["score"] >= 65:
        result["signals"].append("SPCX_ORDERFLOW_NEUTRAL_POSITIVE")
    elif result["score"] >= 50:
        result["signals"].append("SPCX_ORDERFLOW_NEUTRAL")
    elif result["score"] >= 35:
        result["signals"].append("SPCX_ORDERFLOW_NEUTRAL_NEGATIVE")
    else:
        result["signals"].append("SPCX_ORDERFLOW_BEARISH")

    if result["component_scores"]["tape_flow"].get("delta_pct", 0) > 30:
        result["signals"].append("AGGRESSIVE_BUYING_DETECTED")
    if result["component_scores"]["tape_flow"].get("delta_pct", 0) < -30:
        result["signals"].append("AGGRESSIVE_SELLING_DETECTED")

    large_count = result["component_scores"]["tape_flow"].get("large_print_count", 0)
    if large_count >= 5:
        result["signals"].append(f"INSTITUTIONAL_FLOW_{large_count}_LARGE_PRINTS")

    return result


def _score_liquidity(depth_data: dict | None) -> dict:
    """Score liquidity from L2 depth data. Returns 0-100."""
    if not depth_data or not depth_data.get("ok"):
        return {"score": 50, "label": "no_data", "reasons": ["no_depth_data"]}

    score = 50
    reasons = []

    spread_pct = _num(depth_data.get("spread_pct"))
    if spread_pct is not None:
        if spread_pct < 0.05:
            score += 25
            reasons.append("ultra_tight_spread")
        elif spread_pct < 0.15:
            score += 15
            reasons.append("tight_spread")
        elif spread_pct < 0.3:
            score += 5
        elif spread_pct > 1.0:
            score -= 20
            reasons.append("wide_spread")
        elif spread_pct > 0.5:
            score -= 10
            reasons.append("moderate_spread")

    imbalance = _num(depth_data.get("orderbook_imbalance"))
    if imbalance is not None:
        if imbalance > 0.3:
            score += 15
            reasons.append("strong_bid_imbalance")
        elif imbalance > 0.1:
            score += 5
            reasons.append("mild_bid_imbalance")
        elif imbalance < -0.3:
            score -= 10
            reasons.append("strong_ask_imbalance")

    bid_depth = _num(depth_data.get("bid_depth_1pct_usd"))
    ask_depth = _num(depth_data.get("ask_depth_1pct_usd"))
    if bid_depth is not None and ask_depth is not None:
        depth_usd = bid_depth + ask_depth
        if depth_usd > 10000000:
            score += 10
            reasons.append("deep_book")
        elif depth_usd > 1000000:
            score += 5
        elif depth_usd < 100000:
            score -= 10
            reasons.append("thin_book")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "spread_pct": spread_pct,
        "imbalance": imbalance,
        "bid_depth_1pct_usd": bid_depth,
        "ask_depth_1pct_usd": ask_depth,
        "reasons": reasons,
    }


def _score_tape_flow(tape_data: dict | None) -> dict:
    """Score tape flow from tape data. Returns 0-100."""
    if not tape_data or not tape_data.get("ok"):
        return {"score": 50, "label": "no_data", "reasons": ["no_tape_data"]}

    score = 50
    reasons = []
    delta_pct = _num(tape_data.get("delta_pct"))
    price_vs_vwap = _num(tape_data.get("price_vs_vwap_pct"))
    large_prints = tape_data.get("large_prints", [])
    block_trades = tape_data.get("block_trades", [])

    if delta_pct is not None:
        if delta_pct > 50:
            score += 25
            reasons.append("very_bullish_delta")
        elif delta_pct > 20:
            score += 15
            reasons.append("bullish_delta")
        elif delta_pct > 5:
            score += 5
        elif delta_pct < -50:
            score -= 25
            reasons.append("very_bearish_delta")
        elif delta_pct < -20:
            score -= 15
            reasons.append("bearish_delta")
        elif delta_pct < -5:
            score -= 5

    if price_vs_vwap is not None:
        if price_vs_vwap > 2:
            score += 10
            reasons.append("above_vwap")
        elif price_vs_vwap < -2:
            score -= 10
            reasons.append("below_vwap")

    total_large = len(large_prints) + len(block_trades)
    if total_large >= 10:
        score += 10
        reasons.append(f"{total_large}_large_prints")
    elif total_large >= 3:
        score += 5
        reasons.append(f"{total_large}_large_prints")

    volume_usd = _num(tape_data.get("volume_today_usd"))
    if volume_usd is not None:
        if volume_usd > 10000000000:  # $10B+
            score += 10
            reasons.append("massive_volume")
        elif volume_usd > 1000000000:  # $1B+
            score += 5
            reasons.append("high_volume")

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "delta_pct": delta_pct,
        "price_vs_vwap_pct": price_vs_vwap,
        "large_print_count": total_large,
        "block_trade_count": len(block_trades),
        "volume_today_usd": volume_usd,
        "reasons": reasons,
    }


def _score_auction(auction_data: dict | None) -> dict:
    """Score auction imbalance data. Returns 0-100."""
    if not auction_data or not auction_data.get("ok"):
        return {"score": 50, "label": "no_data", "reasons": ["no_auction_data"]}

    score = 50
    reasons = []
    day_side = auction_data.get("day_imbalance_side")
    strength = auction_data.get("day_imbalance_strength")
    opening = auction_data.get("opening", {})
    closing = auction_data.get("closing", {})

    open_side = opening.get("imbalance_side")
    close_side = closing.get("imbalance_side")
    open_sig = opening.get("significant")
    close_sig = closing.get("significant")

    if open_side == "BUY" and open_sig:
        score += 10
        reasons.append("bullish_opening_auction")
    elif open_side == "SELL" and open_sig:
        score -= 10
        reasons.append("bearish_opening_auction")

    if close_side == "BUY" and close_sig:
        score += 15
        reasons.append("bullish_closing_auction")
    elif close_side == "SELL" and close_sig:
        score -= 15
        reasons.append("bearish_closing_auction")

    if strength == "STRONG":
        if "BUY" in str(day_side):
            score += 15
            reasons.append("strong_bullish_auction_day")
        else:
            score -= 15
            reasons.append("strong_bearish_auction_day")
    elif strength == "DIVERGENT":
        reasons.append("divergent_auction_flow")
    elif strength == "MODERATE":
        if "BUY" in str(day_side):
            score += 5
        else:
            score -= 5

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "day_imbalance_side": day_side,
        "day_imbalance_strength": strength,
        "opening_significant": open_sig,
        "closing_significant": close_sig,
        "reasons": reasons,
    }


def _score_volume_quality(tape_data: dict | None) -> dict:
    """Score volume quality / reliability. Returns 0-100."""
    if not tape_data or not tape_data.get("ok"):
        return {"score": 50, "label": "no_data"}

    score = 50
    reasons = []
    lps = tape_data.get("large_prints", [])
    blocks = tape_data.get("block_trades", [])

    lp_count = len(lps)
    block_count = len(blocks)
    total_special = lp_count + block_count

    if block_count >= 3:
        score += 20
        reasons.append(f"{block_count}_block_trades_institutional")
    elif block_count >= 1:
        score += 10
        reasons.append("block_trade_present")

    if lp_count >= 5:
        score += 10
        reasons.append(f"{lp_count}_large_prints_active")
    elif lp_count >= 2:
        score += 5
        reasons.append("large_prints_present")

    if total_special == 0:
        reasons.append("no_institutional_prints")
        score -= 5

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "large_print_count": lp_count,
        "block_trade_count": block_count,
        "reasons": reasons,
    }


def _score_price_context(tape_data: dict | None) -> dict:
    """Score price context relative to VWAP and spread. Returns 0-100."""
    if not tape_data or not tape_data.get("ok"):
        return {"score": 50, "label": "no_data"}

    score = 50
    reasons = []
    spread_pct = _num(tape_data.get("spread_pct"))
    price_vs_vwap = _num(tape_data.get("price_vs_vwap_pct"))

    if spread_pct is not None:
        if spread_pct < 0.05:
            score += 15
            reasons.append("efficient_market")
        elif spread_pct < 0.15:
            score += 5
        elif spread_pct > 1.0:
            score -= 15
            reasons.append("inefficient_market")

    if price_vs_vwap is not None:
        if abs(price_vs_vwap) < 0.5:
            score += 10
            reasons.append("equilibrium")
        elif abs(price_vs_vwap) < 2:
            score += 5

    return {
        "score": round(_clamp(score, 0, 100), 1),
        "spread_pct": spread_pct,
        "price_vs_vwap_pct": price_vs_vwap,
        "reasons": reasons,
    }


def _num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))
