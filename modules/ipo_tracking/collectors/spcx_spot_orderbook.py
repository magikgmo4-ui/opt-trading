"""
SPCX Spot Orderbook + Tape + Auction Collector
GO_SPACEX_SPOT_ORDERBOOK_L2_TAPE_AUCTIONS_01

Combines Yahoo DOM + TradingView DOM + Yahoo bars for best-effort
SPCX market microstructure: bid/ask, depth, tape, auctions.
Falls back gracefully when sources are unavailable.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]


def collect_spcx_orderbook() -> dict[str, Any]:
    """Collect SPCX order book data from available DOM sources + bars."""
    result = {
        "source": "spcx_spot_orderbook",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "available": False,
        "method": "dom_composite",

        # Top of book
        "bid": None, "ask": None,
        "bid_size": None, "ask_size": None,
        "spread_abs": None, "spread_pct": None,
        "mid_price": None,

        # Depth (estimated from available data)
        "bid_depth_estimate": None,
        "ask_depth_estimate": None,
        "orderbook_imbalance": None,

        # Tape (from Yahoo bars)
        "last_trade_price": None,
        "last_trade_size": None,
        "vwap": None,
        "price_vs_vwap_pct": None,
        "tape_imbalance": None,
        "large_prints": [],

        # Auction
        "opening_imbalance": None,
        "closing_imbalance": None,
    }

    vision_dir = REPO_ROOT / "data" / "vision_inbox"
    yahoo_dom = _get_yahoo_dom(vision_dir)
    tv_dom = _get_tv_dom(vision_dir)
    bars = _get_recent_bars()

    # --- TOP OF BOOK ---
    # Yahoo DOM via fin-streamer
    if yahoo_dom:
        result["ok"] = True
        result["available"] = True
        result["last_trade_price"] = _parse(yahoo_dom.get("regularMarketPrice") or yahoo_dom.get("price"))
        result["bid"] = _parse(yahoo_dom.get("bid"))
        result["ask"] = _parse(yahoo_dom.get("ask"))
        result["bid_size"] = _parse(yahoo_dom.get("bidSize"))
        result["ask_size"] = _parse(yahoo_dom.get("askSize"))

    # TV DOM fallback for OHLCV
    if tv_dom:
        result["ok"] = True
        result["available"] = True
        result["last_trade_price"] = result["last_trade_price"] or _parse(tv_dom.get("close"))

    # --- SPREAD ---
    if result["bid"] and result["ask"] and result["bid"] > 0:
        result["spread_abs"] = round(result["ask"] - result["bid"], 4)
        result["spread_pct"] = round(result["spread_abs"] / result["bid"] * 100, 4)
        result["mid_price"] = round((result["bid"] + result["ask"]) / 2, 2)
    elif result["last_trade_price"]:
        # Estimate spread from IPO day data
        result["spread_pct"] = 0.15

    # --- DEPTH ESTIMATE ---
    if result["bid"] and result["ask"] and result["bid_size"] and result["ask_size"]:
        result["bid_depth_estimate"] = result["bid"] * result["bid_size"]
        result["ask_depth_estimate"] = result["ask"] * result["ask_size"]
        total = result["bid_depth_estimate"] + result["ask_depth_estimate"]
        if total > 0:
            result["orderbook_imbalance"] = round(
                (result["bid_depth_estimate"] - result["ask_depth_estimate"]) / total, 3
            )

    # --- TAPE (from Yahoo bars) ---
    if bars:
        result["ok"] = True
        result["available"] = True
        if not result["last_trade_price"]:
            result["last_trade_price"] = bars[-1].get("close")

        # VWAP
        if bars:
            cum_pv = 0.0
            cum_v = 0.0
            for b in bars:
                typical = (b.get("high", 0) + b.get("low", 0) + b.get("close", 0)) / 3
                vol = b.get("volume", 0) or 0
                cum_pv += typical * vol
                cum_v += vol
            result["vwap"] = round(cum_pv / cum_v, 2) if cum_v > 0 else None

        if result["vwap"] and result["last_trade_price"] and result["vwap"] > 0:
            result["price_vs_vwap_pct"] = round(
                (result["last_trade_price"] - result["vwap"]) / result["vwap"] * 100, 2
            )

        # Tape: last 20 bars with volume
        for b in bars[-20:]:
            vol = b.get("volume", 0) or 0
            if vol > 500_000:
                result["large_prints"].append({
                    "price": b.get("close"),
                    "volume": vol,
                })

        # Buy/sell imbalance from last 10 bars
        buys = sum(1 for b in bars[-10:] if b.get("close", 0) > b.get("open", 0))
        sells = 10 - buys
        result["tape_imbalance"] = round((buys - sells) / 10, 2)

        # Last trade size
        if bars:
            result["last_trade_size"] = bars[-1].get("volume")

    return result


def compute_liquidity_depth_score(ob: dict) -> dict[str, Any]:
    """Score SPCX spot liquidity from orderbook data. 0-1 scale."""
    score = 0.5
    reasons = []

    spread = ob.get("spread_pct")
    if spread is not None:
        if spread < 0.1:
            score += 0.25; reasons.append("tight_spread")
        elif spread < 0.3:
            score += 0.15
        elif spread > 1.0:
            score -= 0.2; reasons.append("wide_spread")

    imbalance = ob.get("orderbook_imbalance")
    if imbalance is not None:
        if imbalance > 0.2:
            score += 0.1; reasons.append("bid_heavy")
        elif imbalance < -0.2:
            score -= 0.05; reasons.append("ask_heavy")

    tape_imb = ob.get("tape_imbalance")
    if tape_imb is not None and tape_imb > 0.3:
        score += 0.1; reasons.append("buy_tape")

    large = ob.get("large_prints", [])
    if large:
        score += 0.05; reasons.append(f"{len(large)}_large_prints")

    vwap_dist = ob.get("price_vs_vwap_pct")
    if vwap_dist is not None and vwap_dist > 2:
        score += 0.05; reasons.append("above_vwap")

    return {
        "liquidity_depth_score": round(max(0, min(1, score)), 3),
        "reasons": reasons,
        "spread_pct": spread,
        "imbalance": imbalance,
        "tape_bias": tape_imb,
    }


def _get_yahoo_dom(vision_dir: Path) -> dict | None:
    if not vision_dir.exists():
        return None
    for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if "yahoo" in f.name.lower() and "spcx" in f.name.lower() and f.suffix == ".json":
            try:
                data = json.loads(f.read_text())
                return data.get("dom_extracted", {})
            except Exception:
                pass
    return None


def _get_tv_dom(vision_dir: Path) -> dict | None:
    if not vision_dir.exists():
        return None
    for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if "tradingview" in f.name.lower() and "spcx" in f.name.lower() and f.suffix == ".json":
            try:
                data = json.loads(f.read_text())
                return data.get("dom_extracted", {})
            except Exception:
                pass
    return None


def _get_recent_bars(limit: int = 100) -> list[dict]:
    try:
        from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
        result = collect_yahoo_quote("SPCX")
        bars = result.get("bars", [])
        real = [b for b in bars if b.get("volume") and b["volume"] > 0]
        return real[-limit:] if real else []
    except Exception:
        # Offline fallback
        scored = REPO_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
        if scored.exists():
            snap = json.loads(scored.read_text())
            yahoo = (snap.get("latest_events", {}) or {}).get("yahoo_chart", {})
            bars = yahoo.get("bars", [])
            return [b for b in bars if b.get("volume") and b["volume"] > 0][-limit:]
        return []


def _parse(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("K", "e3").replace("M", "e6"))
    except (ValueError, TypeError):
        return None
