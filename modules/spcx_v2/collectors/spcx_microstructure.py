"""
SPCX Spot Microstructure Collector
GO_SPACEX_DIRECT_MARKET_DATA_AND_SENTIMENT_FIX_01

Extracts bid/ask/spread/depth from Yahoo Finance DOM captures.
When Nasdaq/broker feed unavailable, falls back to DOM extraction.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]


def collect_spcx_microstructure() -> dict[str, Any]:
    """Collect SPCX bid/ask/spread from latest DOM captures."""
    vision_dir = REPO_ROOT / "data" / "vision_inbox"
    result = {
        "source": "spcx_spot_microstructure",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "bid": None,
        "ask": None,
        "bid_size": None,
        "ask_size": None,
        "spread_abs": None,
        "spread_pct": None,
        "last_price": None,
        "volume": None,
        "vwap": None,
        "source_method": "yahoo_dom",
        "error": None,
    }

    if not vision_dir.exists():
        result["error"] = "vision_inbox not found"
        return result

    # Try Yahoo DOM first (has structured fin-streamer data)
    for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if "yahoo" in f.name.lower() and "spcx" in f.name.lower() and f.suffix == ".json":
            try:
                data = json.loads(f.read_text())
                dom = data.get("dom_extracted", {})
                if dom and isinstance(dom, dict):
                    result["ok"] = True
                    result["last_price"] = _parse_num(dom.get("regularMarketPrice") or dom.get("price"))
                    result["bid"] = _parse_num(dom.get("bid"))
                    result["ask"] = _parse_num(dom.get("ask"))
                    result["bid_size"] = _parse_num(dom.get("bidSize"))
                    result["ask_size"] = _parse_num(dom.get("askSize"))
                    result["volume"] = _parse_num(dom.get("regularMarketVolume") or dom.get("volume"))
                    result["source_method"] = "yahoo_dom_fin_streamer"
                    break
            except Exception:
                pass

    # Fallback: TradingView DOM (has O/H/L/C)
    if not result["ok"]:
        for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if "tradingview" in f.name.lower() and "spcx" in f.name.lower() and f.suffix == ".json":
                try:
                    data = json.loads(f.read_text())
                    dom = data.get("dom_extracted", {})
                    if dom and isinstance(dom, dict):
                        result["ok"] = True
                        result["last_price"] = _parse_num(dom.get("close"))
                        result["volume"] = _parse_num(dom.get("volume"))
                        result["source_method"] = "tv_dom_bodytext"
                        # TV DOM may have bid/ask in body text
                        bid_ask = dom.get("bidAsk", "")
                        if bid_ask:
                            parts = bid_ask.replace("SELL", "").replace("BUY", "").split()
                            if len(parts) >= 2:
                                result["bid"] = _parse_num(parts[0])
                                result["ask"] = _parse_num(parts[1])
                        break
                except Exception:
                    pass

    # Compute spread if both bid and ask present
    if result["bid"] and result["ask"]:
        result["spread_abs"] = round(result["ask"] - result["bid"], 4)
        if result["bid"] > 0:
            result["spread_pct"] = round((result["ask"] - result["bid"]) / result["bid"] * 100, 4)

    # Fallback spread estimate from volatility if no direct bid/ask
    if result["spread_pct"] is None and result["last_price"]:
        result["spread_pct"] = 0.15  # default estimate for liquid IPO
        result["source_method"] += "_estimated"

    return result


def compute_liquidity_depth_score(micro: dict) -> dict[str, Any]:
    """Score SPCX spot liquidity from microstructure data."""
    score = 0.5  # neutral baseline
    reasons = []

    spread = micro.get("spread_pct")
    if spread is not None:
        if spread < 0.1:
            score += 0.25
            reasons.append("tight_spread")
        elif spread < 0.3:
            score += 0.15
        elif spread > 1.0:
            score -= 0.2
            reasons.append("wide_spread")

    vol = micro.get("volume")
    if vol:
        if vol > 1_000_000:
            score += 0.15
        elif vol > 100_000:
            score += 0.05

    if micro.get("source_method", "").endswith("_estimated"):
        score -= 0.1
        reasons.append("estimated_spread")

    return {
        "liquidity_depth_score": round(max(0, min(1, score)), 2),
        "reasons": reasons,
        "spread_pct": spread,
        "bid": micro.get("bid"),
        "ask": micro.get("ask"),
        "source": micro.get("source_method"),
    }


def _parse_num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("K", "e3").replace("M", "e6").replace("B", "e9"))
    except (ValueError, TypeError):
        return None
