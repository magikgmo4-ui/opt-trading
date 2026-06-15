"""
SPCX Source Quality Classifier
GO_SPACEX_OPS_READINESS_LIVE_01

Classifies each data source by quality tier:
  - direct: live, native market data (L2 vendor, SIP consolidated)
  - delayed: slightly stale but reliable (broker, TV DOM)
  - fallback: best-effort estimation (Yahoo, synthetic perp)
  - synthetic: derived from non-spot sources (perp, proxy)
  - estimated: human-curated or press-reported (ownership, private rounds)
  - unavailable: source not reachable

Produces a source_quality block for injection into latest_snapshot.json.
"""
from __future__ import annotations
from typing import Any


def classify_source_quality(
    tape_data: dict | None = None,
    depth_data: dict | None = None,
    auction_data: dict | None = None,
    ownership_data: dict | None = None,
    price_status: str = "missing",
) -> dict[str, Any]:
    """Classify the quality of each data source feeding the SPCX pipeline.

    Returns a dict with per-source tier + confidence and flags that
    downstream consumers can use to cap trade_ready or trigger warnings.
    """
    result = {
        "spot_price": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "orderbook": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "tape": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "auction": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "perp": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "ownership": {"tier": "unavailable", "confidence": 0.0, "source": None},
        "overall_tier": "unavailable",
        "can_affect_trade_ready": False,
        "degraded_reasons": [],
    }

    # --- Spot price ---
    if price_status == "live":
        result["spot_price"] = {"tier": "direct", "confidence": 0.9, "source": "sip_consolidated"}
    elif price_status == "delayed":
        result["spot_price"] = {"tier": "delayed", "confidence": 0.6, "source": "broker_delayed"}
    elif price_status == "stale":
        result["spot_price"] = {"tier": "fallback", "confidence": 0.3, "source": "offline_snapshot"}
    else:
        result["spot_price"] = {"tier": "unavailable", "confidence": 0.0, "source": None}

    # --- Orderbook / L2 ---
    if depth_data and depth_data.get("ok"):
        src = depth_data.get("depth_source", "")
        if src in ("tradingview_dom",):
            result["orderbook"] = {"tier": "delayed", "confidence": 0.7, "source": src}
        elif src in ("spot_orderbook", "yahoo_dom"):
            result["orderbook"] = {"tier": "fallback", "confidence": 0.5, "source": src}
        elif src in ("perp_synthetic",):
            result["orderbook"] = {"tier": "synthetic", "confidence": 0.3, "source": src}
        elif src:
            result["orderbook"] = {"tier": "direct", "confidence": 0.8, "source": src}
        else:
            result["orderbook"] = {"tier": "fallback", "confidence": 0.4, "source": "inferred"}
    else:
        result["orderbook"] = {"tier": "unavailable", "confidence": 0.0, "source": None}
        result["degraded_reasons"].append("l2_depth_unavailable")

    # --- Tape ---
    if tape_data and tape_data.get("ok"):
        source = tape_data.get("source", "")
        if "sip" in source.lower():
            result["tape"] = {"tier": "direct", "confidence": 0.8, "source": source}
        elif source:
            result["tape"] = {"tier": "fallback", "confidence": 0.5, "source": source}
    else:
        result["tape"] = {"tier": "fallback", "confidence": 0.4, "source": "yahoo_bars_inferred"}
        result["degraded_reasons"].append("tape_no_sip")

    # --- Auction ---
    if auction_data and auction_data.get("ok"):
        src = auction_data.get("opening", {}).get("source", "")
        if src == "bar_inferred":
            result["auction"] = {"tier": "fallback", "confidence": 0.4, "source": "bar_inferred"}
        else:
            result["auction"] = {"tier": "direct", "confidence": 0.7, "source": src}
    else:
        result["auction"] = {"tier": "unavailable", "confidence": 0.0, "source": None}

    # --- Perp (always synthetic for spot validation) ---
    result["perp"] = {"tier": "synthetic", "confidence": 0.3, "source": "spcxusdt_perp"}
    result["degraded_reasons"].append("perp_is_synthetic_never_validates_spot_liquidity")

    # --- Ownership ---
    if ownership_data and ownership_data.get("ok"):
        result["ownership"] = {"tier": "estimated", "confidence": 0.6, "source": "sec_reported"}
    else:
        result["ownership"] = {"tier": "estimated", "confidence": 0.3, "source": "press_only"}

    # --- Overall tier ---
    tiers = [result[k]["tier"] for k in ("spot_price", "orderbook", "tape")]
    if "direct" in tiers:
        result["overall_tier"] = "direct"
    elif "delayed" in tiers:
        result["overall_tier"] = "delayed"
    elif "fallback" in tiers:
        result["overall_tier"] = "fallback"
    elif "synthetic" in tiers:
        result["overall_tier"] = "synthetic"
    else:
        result["overall_tier"] = "unavailable"

    # --- Can trade_ready be affected? ---
    result["can_affect_trade_ready"] = result["overall_tier"] in ("direct", "delayed")

    return result


def cap_trade_ready_from_quality(
    trade_ready: float,
    source_quality: dict,
    max_degraded: float = 40.0,
) -> float:
    """Cap trade_ready based on source quality.

    If overall_tier is not direct or delayed, cap trade_ready to max_degraded.
    This prevents false A/A+ signals on fallback/synthetic data.
    """
    tier = source_quality.get("overall_tier", "unavailable")
    if tier in ("direct", "delayed"):
        return trade_ready
    return min(trade_ready, max_degraded)
