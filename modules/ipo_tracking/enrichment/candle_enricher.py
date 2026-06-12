from __future__ import annotations
from typing import Any

from .indicators import compute_all_indicators
from .smart_money import compute_smart_money
from .source_consensus import compute_consensus
from ..io import utc_now


def enrich_candles(
    bars: list[dict[str, Any]],
    events: list[dict[str, Any]],
    snapshot: dict[str, Any],
    *,
    timeframe: str = "M1",
    symbol: str = "SPCX",
    ipo_price: float = 135.0,
) -> dict[str, Any]:
    indicators = compute_all_indicators(bars, ipo_price=ipo_price)
    smc = compute_smart_money(bars)
    consensus = compute_consensus(events, snapshot)

    price_status = consensus.get("price_status", "missing")
    market_phase = consensus.get("market_phase", "unknown")
    has_real_bars = len(bars) > 0 and any(
        b.get("close") is not None and isinstance(b.get("volume"), (int, float)) and b.get("volume", 0) > 0
        for b in bars
    )
    is_live = price_status == "live" or has_real_bars

    scores = snapshot.get("scores", {})
    mega_scores = {
        "momentum_score": scores.get("momentum", 0),
        "volatility_score": _atr_volatility(smc, indicators) if is_live else 0.0,
        "liquidity_score": _liquidity_score(indicators) if is_live else 0.0,
        "news_score": scores.get("news_velocity", 0),
        "catalyst_score": _catalyst_score(events),
        "smart_money_score": smc.get("smc_score", 0) if is_live else 0.0,
        "trend_score": _trend_score(indicators, smc) if is_live else 0.0,
        "risk_score": scores.get("risk", 0),
        "trade_ready_score": scores.get("trade_ready", 0) if is_live else 0.0,
        "accumulation_score": scores.get("accumulation", 0),
    }

    sec_events = [e for e in events if e.get("source") == "sec_edgar"]
    news_events = [e for e in events if e.get("source") == "yahoo_news_rss"]
    bot_vision_events = [e for e in events if e.get("source") == "bot_vision_adapter"]
    bv_capture_map = {}
    bv_comp_map = {}
    bv_spcx_count = 0
    bv_visual_price = None
    for bv in bot_vision_events:
        if bv.get("ok"):
            bv_spcx_count = max(bv_spcx_count, bv.get("spcx_capture_count", 0))
            bv_capture_map = bv.get("spcx_capture_map", {}) or bv_capture_map
            bv_comp_map = bv.get("comparable_map", {}) or bv_comp_map
            vp = bv.get("visual_price")
            if vp is not None:
                bv_visual_price = float(vp) if not isinstance(vp, (int, float)) else vp
    tv_events = [e for e in events if e.get("source") == "tradingview_webhook"]

    last_timestamp = bars[-1].get("ts") if bars else None

    enriched = {
        "schema": "spacex_enriched_candle.v1",
        "enriched_at": utc_now(),
        "candle": {
            "timestamp": last_timestamp,
            "symbol": symbol,
            "timeframe": timeframe,
            "open": indicators.get("open"),
            "high": indicators.get("high"),
            "low": indicators.get("low"),
            "close": indicators.get("close"),
            "volume": indicators.get("volume"),
            "vwap": indicators.get("vwap"),
            "source": "yahoo_chart",
            "source_confidence": consensus.get("weighted_trust_score", 0.8),
            "session": _session_classify(),
        },
        "indicators": {
            "ema_9": indicators.get("ema_9"),
            "ema_20": indicators.get("ema_20"),
            "ema_50": indicators.get("ema_50"),
            "ema_200": indicators.get("ema_200"),
            "sma_20": indicators.get("sma_20"),
            "sma_50": indicators.get("sma_50"),
            "sma_200": indicators.get("sma_200"),
            "rsi_14": indicators.get("rsi_14"),
            "macd_line": indicators.get("macd_line"),
            "macd_signal": indicators.get("macd_signal"),
            "macd_histogram": indicators.get("macd_histogram"),
            "atr_14": indicators.get("atr_14"),
            "bb_upper": indicators.get("bb_upper"),
            "bb_middle": indicators.get("bb_middle"),
            "bb_lower": indicators.get("bb_lower"),
            "relative_volume": indicators.get("relative_volume"),
            "volume_zscore": indicators.get("volume_zscore"),
            "opening_range_5m": indicators.get("opening_range_5m"),
            "opening_range_15m": indicators.get("opening_range_15m"),
            "opening_range_30m": indicators.get("opening_range_30m"),
            "prev_gap_pct": indicators.get("prev_gap_pct"),
            "ipo_gap_pct": indicators.get("ipo_gap_pct"),
            "vwap_distance_pct": indicators.get("vwap_distance_pct"),
        },
        "smart_money": {
            "fvg_bullish": smc.get("fvg", {}).get("bullish"),
            "fvg_bearish": smc.get("fvg", {}).get("bearish"),
            "fvg_active_count": smc.get("fvg", {}).get("active_count"),
            "order_block_bullish": smc.get("order_blocks", {}).get("bullish_ob"),
            "order_block_bearish": smc.get("order_blocks", {}).get("bearish_ob"),
            "liquidity_sweep_high": smc.get("liquidity_sweeps", {}).get("high_sweep"),
            "liquidity_sweep_low": smc.get("liquidity_sweeps", {}).get("low_sweep"),
            "bos": smc.get("bos_choch", {}).get("bos"),
            "choch": smc.get("bos_choch", {}).get("choch"),
            "equal_highs": smc.get("equal_highs_lows", {}).get("equal_highs"),
            "equal_lows": smc.get("equal_highs_lows", {}).get("equal_lows"),
            "premium_discount_regime": smc.get("premium_discount", {}).get("regime"),
            "premium_discount_position_pct": smc.get("premium_discount", {}).get("position_pct"),
            "smc_score": smc.get("smc_score"),
            "smc_bias": smc.get("smc_bias"),
        },
        "consensus": {
            "consensus_price": consensus.get("consensus_price"),
            "consensus_volume": consensus.get("consensus_volume"),
            "source_count": consensus.get("source_count"),
            "trusted_source_count": consensus.get("trusted_source_count"),
            "source_disagreement_score": consensus.get("source_disagreement_score"),
            "weighted_trust_score": consensus.get("weighted_trust_score"),
            "price_trust": consensus.get("price_trust"),
            "info_trust": consensus.get("info_trust"),
            "stale_sources": consensus.get("stale_source_flags"),
            "missing_sources": consensus.get("missing_source_flags"),
            "market_phase": market_phase,
            "price_status": price_status,
        },
        "scores": mega_scores,
        "pipeline_state": {
            "market_phase": market_phase,
            "price_status": price_status,
            "scores_blocked": not is_live,
            "blocked_score_keys": [
                "momentum_score", "volatility_score", "liquidity_score",
                "smart_money_score", "trend_score", "trade_ready_score"
            ] if not is_live else [],
            "active_score_keys": [
                "catalyst_score", "news_score", "risk_score", "accumulation_score"
            ],
        },
        "context": {
            "news_count": sum(e.get("count", len(e.get("articles", []))) for e in news_events if e.get("ok")),
            "sec_filings_count": sum(len(e.get("filings", [])) for e in sec_events if e.get("ok")),
            "bot_vision_available": any(e.get("ok") for e in bot_vision_events),
            "bot_vision_capture_count": bv_spcx_count,
            "bot_vision_capture_map": bv_capture_map,
            "bot_vision_comparable_map": bv_comp_map,
            "bot_vision_visual_price": bv_visual_price,
            "tv_alert_active": any(e.get("ok") for e in tv_events),
        },
    }

    return enriched


def enrich_from_snapshot(snapshot: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    yahoo = (snapshot.get("latest_events") or {}).get("yahoo_chart", {})
    bars = yahoo.get("bars", [])
    symbol = snapshot.get("symbol", "SPCX")
    ipo_price = snapshot.get("ipo_price", 135)

    return enrich_candles(
        bars=bars,
        events=events,
        snapshot=snapshot,
        timeframe="M1",
        symbol=symbol,
        ipo_price=float(ipo_price),
    )


def _session_classify() -> str:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    h = now.hour
    if h < 13 or h >= 20:
        return "after_hours"
    if h < 14:
        return "pre_market"
    return "regular_hours"


def _atr_volatility(smc: dict, indicators: dict) -> float:
    atr = indicators.get("atr_14")
    price = indicators.get("close")
    if atr and price and price > 0:
        return round(min(1.0, (atr / price * 100) / 5), 3)
    return 0.0


def _liquidity_score(indicators: dict) -> float:
    rel_vol = indicators.get("relative_volume") or 1.0
    vol_z = indicators.get("volume_zscore") or 0.0
    return round(max(0, min(1, (rel_vol * 0.3 + (vol_z / 2) * 0.7))), 3)


def _catalyst_score(events: list[dict]) -> float:
    news_count = sum(e.get("count", len(e.get("articles", []))) for e in events if e.get("source") == "yahoo_news_rss" and e.get("ok"))
    filing_count = sum(len(e.get("filings", [])) for e in events if e.get("source") == "sec_edgar" and e.get("ok"))
    tv_count = sum(1 for e in events if e.get("source") == "tradingview_webhook" and e.get("ok"))
    score = min(1.0, (news_count * 0.05 + filing_count * 0.025 + tv_count * 0.3))
    return round(score, 3)


def _trend_score(indicators: dict, smc: dict) -> float:
    score = 0.0
    close = indicators.get("close")
    ema20 = indicators.get("ema_20")
    ema50 = indicators.get("ema_50")
    rsi = indicators.get("rsi_14") or 50

    if close and ema20 and close > ema20:
        score += 0.25
    if close and ema50 and close > ema50:
        score += 0.25
    if ema20 and ema50 and ema20 > ema50:
        score += 0.25
    if rsi > 50:
        score += 0.15
    if smc.get("smc_bias") == "bullish":
        score += 0.10

    return round(min(1.0, score), 3)
