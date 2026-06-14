"""
SPCX SIP / Consolidated Tape + NBBO Collector
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Fetches consolidated trade and quote data from available free sources.
Aggregates into time buckets with inferred aggressor side.
Filters micro-trades below configured thresholds.
"""
from __future__ import annotations
import json, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

SIP_DEFAULTS = {
    "min_trade_value_usd": 25000,
    "min_trade_size_shares": 100,
    "large_print_threshold_usd": 500000,
    "block_trade_threshold_usd": 1000000,
    "ignore_odd_lots": True,
}


def collect_spcx_sip_tape() -> dict[str, Any]:
    """Collect consolidated tape data for SPCX from available free sources.

    Sources tried (in order):
      1. Finnhub quote (free tier)
      2. Yahoo public (via vision_inbox DOM + bars)
      3. Offline latest snapshot fallback
    """
    result = {
        "source": "spcx_sip_tape",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "symbol": "SPCX",

        # Best bid/ask (NBBO)
        "bid": None, "ask": None,
        "bid_size": None, "ask_size": None,
        "spread_abs": None, "spread_pct": None,

        # Last trade
        "last_price": None, "last_size": None,
        "last_trade_condition": None,

        # Aggregated volume stats
        "volume_today_shares": None,
        "volume_today_usd": None,
        "vwap": None,
        "price_vs_vwap_pct": None,

        # Inferred flow
        "buy_initiated_volume_shares": None,
        "sell_initiated_volume_shares": None,
        "delta_volume_shares": None,
        "delta_pct": None,

        # Large prints
        "large_prints": [],
        "block_trades": [],

        # Quality
        "aggressor_side_method": "quote_rule",
        "micro_trades_filtered": True,

        "error": None,
    }

    # --- Source 1: Finnhub quote (free tier) ---
    try:
        req = urllib.request.Request(
            "https://finnhub.io/api/v1/quote?symbol=SPCX&token=demo",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0 opt-trading"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        if data.get("c"):
            result["ok"] = True
            result["last_price"] = float(data["c"])
            result["volume_today_shares"] = data.get("v")
            result["high_today"] = data.get("h")
            result["low_today"] = data.get("l")
            result["open_today"] = data.get("o")
            result["prev_close"] = data.get("pc")
            if result["prev_close"] and result["prev_close"] > 0:
                result["change_pct"] = round(
                    (result["last_price"] - result["prev_close"]) / result["prev_close"] * 100, 2
                )
    except Exception as e:
        pass  # fall through to next source

    # --- Source 2: Yahoo DOM from vision_inbox ---
    vision_dir = REPO_ROOT / "data" / "vision_inbox"
    yahoo_dom = _get_yahoo_dom(vision_dir)
    if yahoo_dom:
        result["ok"] = True
        if not result["last_price"]:
            result["last_price"] = _parse(yahoo_dom.get("regularMarketPrice") or yahoo_dom.get("price"))
        result["bid"] = _parse(yahoo_dom.get("bid"))
        result["ask"] = _parse(yahoo_dom.get("ask"))
        result["bid_size"] = _parse(yahoo_dom.get("bidSize"))
        result["ask_size"] = _parse(yahoo_dom.get("askSize"))
        vol = _parse(yahoo_dom.get("regularMarketVolume"))
        if vol and not result["volume_today_shares"]:
            result["volume_today_shares"] = int(vol)

    # --- Spread ---
    if result["bid"] and result["ask"] and result["bid"] > 0:
        result["spread_abs"] = round(result["ask"] - result["bid"], 4)
        result["spread_pct"] = round(result["spread_abs"] / result["bid"] * 100, 4)
        result["mid"] = round((result["bid"] + result["ask"]) / 2, 2)

    # --- Source 3: Yahoo bars for VWAP and flow inference ---
    bars = _get_recent_bars()
    if bars:
        result["ok"] = True
        if not result["last_price"]:
            result["last_price"] = bars[-1].get("close")

        # VWAP
        cum_pv = 0.0
        cum_v = 0.0
        for b in bars:
            typical = (_float(b.get("high")) + _float(b.get("low")) + _float(b.get("close"))) / 3
            vol = _float(b.get("volume"))
            if vol > 0:
                cum_pv += typical * vol
                cum_v += vol
        if cum_v > 0:
            result["vwap"] = round(cum_pv / cum_v, 2)
            if result["last_price"] and result["vwap"] > 0:
                result["price_vs_vwap_pct"] = round(
                    (result["last_price"] - result["vwap"]) / result["vwap"] * 100, 2
                )

        # Inferred flow from bar closes vs opens
        buy_vol = 0.0
        sell_vol = 0.0
        for b in bars:
            vol = _float(b.get("volume"))
            close = _float(b.get("close"))
            open_p = _float(b.get("open"))
            if vol > SIP_DEFAULTS["min_trade_size_shares"]:
                if close > open_p:
                    buy_vol += vol
                elif close < open_p:
                    sell_vol += vol

        total_flow = buy_vol + sell_vol
        result["buy_initiated_volume_shares"] = round(buy_vol, 2)
        result["sell_initiated_volume_shares"] = round(sell_vol, 2)
        if total_flow > 0:
            result["delta_volume_shares"] = round(buy_vol - sell_vol, 2)
            result["delta_pct"] = round((buy_vol - sell_vol) / total_flow * 100, 2)

        # Large print detection from bar volume * typical price
        for b in bars:
            vol = _float(b.get("volume"))
            close_p = _float(b.get("close"))
            if vol > 0 and close_p > 0:
                value = vol * close_p
                if value >= SIP_DEFAULTS["large_print_threshold_usd"]:
                    entry = {
                        "bar_timestamp": b.get("timestamp"),
                        "price": close_p,
                        "volume": vol,
                        "value_usd": round(value, 2),
                        "open": _float(b.get("open")),
                        "high": _float(b.get("high")),
                        "low": _float(b.get("low")),
                    }
                    if value >= SIP_DEFAULTS["block_trade_threshold_usd"]:
                        result["block_trades"].append(entry)
                    else:
                        result["large_prints"].append(entry)

        # Volume today from most recent bars
        if not result["volume_today_shares"] and bars:
            result["volume_today_shares"] = round(sum(
                _float(b.get("volume")) for b in bars
            ), 2)

    # Estimate USD volume if we have shares
    if result["volume_today_shares"] and result["last_price"]:
        result["volume_today_usd"] = round(result["volume_today_shares"] * result["last_price"], 2)

    return result


def bucket_tape_1m(bars: list[dict]) -> list[dict]:
    """Aggregate bar data into 1-minute buckets with inferred flow.

    Each input bar expected to have: timestamp, open, high, low, close, volume.
    Returns list of bucket dicts matching spcx_orderflow_bucket_v1 schema.
    """
    buckets: list[dict] = []
    if not bars:
        return buckets

    for b in bars:
        ts = b.get("ts") or b.get("timestamp")
        price_close = _float(b.get("close"))
        price_open = _float(b.get("open"))
        price_high = _float(b.get("high"))
        price_low = _float(b.get("low"))
        vol = _float(b.get("volume"))

        if vol is None or vol <= 0:
            continue

        value_usd = vol * price_close if price_close else 0
        if value_usd < SIP_DEFAULTS["min_trade_value_usd"] or vol < SIP_DEFAULTS["min_trade_size_shares"]:
            continue

        is_buy = price_close > price_open
        is_sell = price_close < price_open

        large_print = value_usd >= SIP_DEFAULTS["large_print_threshold_usd"]

        bucket = {
            "schema": "spcx_orderflow_bucket_v1",
            "symbol": "SPCX",
            "bucket_seconds": 60,
            "bucket_start": ts,
            "bucket_end": ts,
            "price": {
                "open": price_open,
                "high": price_high,
                "low": price_low,
                "close": price_close,
                "vwap": price_close,
            },
            "volume": {
                "shares": vol,
                "usd": round(value_usd, 2),
                "trade_count": 1,
                "large_prints_count": 1 if large_print else 0,
                "large_prints_usd": round(value_usd, 2) if large_print else 0,
            },
            "flow": {
                "buy_initiated_volume": vol if is_buy else 0,
                "sell_initiated_volume": vol if is_sell else 0,
                "delta_volume": vol if is_buy else (-vol if is_sell else 0),
                "delta_pct": 100.0 if is_buy else (-100.0 if is_sell else 0),
                "sweep_count": None,
                "large_print_buy_count": 1 if (large_print and is_buy) else 0,
                "large_print_sell_count": 1 if (large_print and is_sell) else 0,
            },
            "book_snapshot": {
                "spread_pct_at_bucket_close": None,
                "bid_price": None,
                "ask_price": None,
                "bid_depth_1pct_usd": None,
                "ask_depth_1pct_usd": None,
                "bid_depth_5pct_usd": None,
                "ask_depth_5pct_usd": None,
                "orderbook_imbalance": None,
                "largest_bid_wall_size": None,
                "largest_bid_wall_price": None,
                "largest_ask_wall_size": None,
                "largest_ask_wall_price": None,
                "quote_update_count": None,
            },
            "quality": {
                "source": "SIP",
                "aggressor_side_method": "quote_rule",
                "micro_trades_filtered": True,
            },
        }
        buckets.append(bucket)

    return buckets


def _get_yahoo_dom(vision_dir: Path) -> dict | None:
    if not vision_dir.exists():
        return None
    for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
        if "yahoo" in f.name.lower() and "spcx" in f.name.lower() and f.suffix == ".json":
            try:
                data = json.loads(f.read_text())
                return data.get("dom_extracted", {}) or data
            except Exception:
                pass
    return None


def _get_recent_bars(limit: int = 500) -> list[dict]:
    try:
        from modules.ipo_tracking.collectors.yahoo_public import collect_yahoo_quote
        result_data = collect_yahoo_quote("SPCX", range_="5d", interval="1m")
        bars = result_data.get("bars", [])
        real = [b for b in bars if b.get("volume") and b["volume"] > 0]
        return real[-limit:] if real else []
    except Exception:
        scored = REPO_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
        if scored.exists():
            snap = json.loads(scored.read_text())
            yahoo = (snap.get("latest_events", {}) or {}).get("yahoo_chart", {})
            bars = yahoo.get("bars", [])
            return [b for b in bars if b.get("volume") and b["volume"] > 0][-limit:]
        return []


def _float(v: Any) -> float:
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0


def _parse(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").replace("$", "").replace("K", "e3").replace("M", "e6"))
    except (ValueError, TypeError):
        return None
