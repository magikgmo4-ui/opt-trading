"""SPCX V2 — Pipeline adapter: converts enriched SpaceX events to MarketSnapshot."""

import json
from pathlib import Path
from typing import Optional

from modules.spcx_v2.config import MarketSnapshot, PROJECT_ROOT


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def enriched_to_snapshot(enriched: dict) -> MarketSnapshot:
    data = enriched.get("snapshot", enriched)

    # Handle enriched format: candle + consensus + smart_money
    candle = data.get("candle", {})
    consensus = data.get("consensus", {})
    smart_money = data.get("smart_money", {})
    indicators = data.get("indicators", {})
    scores = data.get("scores", {})
    context = data.get("context", {})

    # Price from candle (primary) or consensus (fallback)
    price_data = data.get("price", {})
    price = price_data.get("last", price_data.get("close",
        candle.get("close", consensus.get("consensus_price", 0))))

    # VWAP from candle or indicators
    vwap = price_data.get("vwap") or candle.get("vwap") or indicators.get("vwap")

    # Volume
    volume_data = data.get("volume", {})
    volume = volume_data.get("total", volume_data.get("shares",
        int(candle.get("volume", 0))))
    if volume == 0 and price and float(price) > 0:
        volume = 1

    dollar_volume = volume_data.get("dollar_volume", volume_data.get("dollar",
        volume * price if volume and price else 0))

    # Price status: determine from candle session + source_confidence
    session = candle.get("session", "")
    source_conf = candle.get("source_confidence", 0)
    if session == "regular_hours" and source_conf > 0:
        price_status = "live"
    elif session == "regular_hours":
        price_status = "delayed"
    elif session == "after_hours":
        price_status = "stale"
    else:
        price_status = price_data.get("status", "missing")

    # Bars count from consensus or inferred
    bars_count = len(data.get("bars", []))
    if bars_count == 0:
        bars_count = 1 if candle.get("close") else 0

    # Source count
    source_count = consensus.get("source_count", consensus.get("trusted_source_count", 0))
    if source_count == 0:
        source_count = 1 if candle.get("close") else 0

    # Price trust from consensus (scale 0-1 → 0-100)
    price_trust_raw = consensus.get("weighted_trust_score", 0)
    if 0 < price_trust_raw <= 1:
        price_trust = int(round(price_trust_raw * 100))
    else:
        price_trust = int(price_trust_raw)
    if price_trust == 0 and price_status == "live":
        price_trust = 80
    elif price_trust == 0:
        price_trust = int(source_conf * 100) if source_conf else 30

    # Spread estimate
    spread_pct = price_data.get("spread_pct", 0)
    if spread_pct == 0 and candle.get("high") and candle.get("low"):
        h, l = candle["high"], candle["low"]
        if (h + l) > 0:
            spread_pct = abs(h - l) / ((h + l) / 2) * 100

    # Halt detection
    halt_active = data.get("halt", {}).get("active", False)

    # Source contradictions
    nasdaq_contradiction = False
    yahoo_contradiction = False
    sources = data.get("sources", {})
    if not sources:
        stale_sources = consensus.get("stale_sources", [])
        if stale_sources:
            nasdaq_contradiction = True

    # SMC structures from smart_money
    smc_structures = []
    structure_data = data.get("structure", {})
    if smart_money.get("fvg_bullish"):
        smc_structures.append({"type": "FVG_BULLISH"})
    if smart_money.get("fvg_bearish"):
        smc_structures.append({"type": "FVG_BEARISH"})
    if smart_money.get("bos"):
        smc_structures.append({"type": "BOS"})
    if smart_money.get("choch"):
        smc_structures.append({"type": "CHOCH"})
    if smart_money.get("liquidity_sweep_low"):
        smc_structures.append({"type": "LIQUIDITY_SWEEP_LOW"})
    if smart_money.get("liquidity_sweep_high"):
        smc_structures.append({"type": "LIQUIDITY_SWEEP_HIGH"})
    if smart_money.get("order_block_bullish") or smart_money.get("order_block_bearish"):
        smc_structures.append({"type": "ORDER_BLOCK"})

    # Also check structure_data for backward compat
    if not smc_structures:
        fvg = structure_data.get("fvg", [])
        if isinstance(fvg, list):
            for f in fvg:
                f_type = f.get("type", f.get("direction", ""))
                if f_type.lower() in ("bullish", "up", "long"):
                    smc_structures.append({"type": "FVG_BULLISH"})
                elif f_type.lower() in ("bearish", "down", "short"):
                    smc_structures.append({"type": "FVG_BEARISH"})
        if structure_data.get("bos"):
            smc_structures.append({"type": "BOS"})
        if structure_data.get("choch"):
            smc_structures.append({"type": "CHOCH"})
        ob = structure_data.get("order_blocks", [])
        if ob:
            smc_structures.append({"type": "ORDER_BLOCK"})
        ls = structure_data.get("liquidity_sweeps", {})
        if isinstance(ls, dict):
            if ls.get("low"):
                smc_structures.append({"type": "LIQUIDITY_SWEEP_LOW"})
            if ls.get("high"):
                smc_structures.append({"type": "LIQUIDITY_SWEEP_HIGH"})

    # News
    news_data = data.get("news", {})
    news_headline = news_data.get("headline")
    news_sentiment = news_data.get("sentiment")

    symbol = data.get("symbol", candle.get("symbol", "SPCX"))
    timestamp = data.get("ts", data.get("timestamp", candle.get("timestamp", "")))

    return MarketSnapshot(
        symbol=symbol,
        timestamp=timestamp,
        price=float(price) if price else 0.0,
        price_status=price_status if price_status in ("live", "delayed", "stale", "missing") else "missing",
        bars_count=bars_count,
        volume=int(volume) if volume else 0,
        price_trust=int(price_trust) if price_trust else 0,
        source_count=source_count,
        spread_pct=round(float(spread_pct), 4) if spread_pct else 0.0,
        dollar_volume=float(dollar_volume) if dollar_volume else 0.0,
        vwap=float(vwap) if vwap is not None else None,
        halt_active=bool(halt_active),
        nasdaq_contradiction=nasdaq_contradiction,
        yahoo_contradiction=yahoo_contradiction,
        news_headline=news_headline,
        news_sentiment=news_sentiment,
        smc_structures=smc_structures,
    )


def load_enriched_snapshot(path: Optional[str] = None) -> MarketSnapshot:
    if path:
        p = Path(path)
    else:
        p = PROJECT_ROOT / "data" / "ipo" / "spacex" / "enriched" / "latest.json"

    enriched = _read_json(p)
    if not enriched:
        alt = PROJECT_ROOT / "data" / "ipo" / "spacex" / "scored" / "latest.json"
        enriched = _read_json(alt)

    return enriched_to_snapshot(enriched)
