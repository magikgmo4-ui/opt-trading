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
    price_data = data.get("price", {})
    volume_data = data.get("volume", {})
    structure_data = data.get("structure", {})
    news_data = data.get("news", {})
    sources = data.get("sources", {})

    price = price_data.get("last", price_data.get("close", 0))
    price_status = price_data.get("status", "missing")
    vwap = price_data.get("vwap")
    spread_pct = price_data.get("spread_pct", 0)
    volume = volume_data.get("total", volume_data.get("shares", 0))
    dollar_volume = volume_data.get("dollar_volume", volume_data.get("dollar", 0))

    bars_count = len(data.get("bars", []))
    source_count = len(sources) if isinstance(sources, dict) else (sources if isinstance(sources, int) else 0)
    if source_count == 0:
        source_count = 1

    price_trust = price_data.get("trust", 0)
    if price_trust == 0 and price_status == "live":
        price_trust = 80
    elif price_trust == 0:
        price_trust = 30

    halt_active = data.get("halt", {}).get("active", False)

    nasdaq_contradiction = False
    yahoo_contradiction = False
    tv_source = (sources.get("tradingview", {}) if isinstance(sources, dict) else {})
    yahoo_source = (sources.get("yahoo", {}) if isinstance(sources, dict) else {})
    if isinstance(tv_source, dict) and isinstance(yahoo_source, dict):
        tv_price = tv_source.get("price", 0)
        yahoo_price = yahoo_source.get("price", 0)
        if tv_price and yahoo_price and abs(tv_price - yahoo_price) / max(tv_price, 1) > 0.05:
            nasdaq_contradiction = True

    smc_structures = []
    fvg = structure_data.get("fvg", [])
    if isinstance(fvg, list):
        for f in fvg:
            f_type = f.get("type", f.get("direction", ""))
            if f_type.lower() in ("bullish", "up", "long"):
                smc_structures.append({"type": "FVG_BULLISH"})
            elif f_type.lower() in ("bearish", "down", "short"):
                smc_structures.append({"type": "FVG_BEARISH"})
    bos = structure_data.get("bos", False)
    choch = structure_data.get("choch", False)
    ob = structure_data.get("order_blocks", [])
    if bos:
        smc_structures.append({"type": "BOS"})
    if choch:
        smc_structures.append({"type": "CHOCH"})
    if ob:
        smc_structures.append({"type": "ORDER_BLOCK"})

    liquidity_sweeps = structure_data.get("liquidity_sweeps", {})
    if isinstance(liquidity_sweeps, dict):
        if liquidity_sweeps.get("low"):
            smc_structures.append({"type": "LIQUIDITY_SWEEP_LOW"})
        if liquidity_sweeps.get("high"):
            smc_structures.append({"type": "LIQUIDITY_SWEEP_HIGH"})

    news_headline = news_data.get("headline")
    news_sentiment = news_data.get("sentiment")

    symbol = data.get("symbol", "SPCX")
    timestamp = data.get("ts", data.get("timestamp", ""))

    return MarketSnapshot(
        symbol=symbol,
        timestamp=timestamp,
        price=float(price) if price else 0.0,
        price_status=price_status if price_status in ("live", "delayed", "stale", "missing") else "missing",
        bars_count=bars_count,
        volume=int(volume) if volume else 0,
        price_trust=int(price_trust) if price_trust else 0,
        source_count=source_count,
        spread_pct=float(spread_pct) if spread_pct else 0.0,
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
