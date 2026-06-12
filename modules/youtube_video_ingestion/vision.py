from __future__ import annotations

import re
from typing import Any


_SYMBOL_ALIASES: tuple[tuple[str, str, str], ...] = (
    ("XAUUSD", "forex", r"\b(?:xauusd|xau|gold)\b"),
    ("BTCUSDT", "crypto", r"\b(?:btcusdt|btc(?:usdt)?|bitcoin)\b"),
    ("ETHUSDT", "crypto", r"\b(?:ethusdt|eth(?:usdt)?|ethereum)\b"),
    ("NASDAQ/US100", "index", r"\b(?:nasdaq|us100|nq)\b"),
    ("SPX/US500", "index", r"\b(?:spx|s&p|us500)\b"),
)
_PRICE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("entry", re.compile(r"\b(?:entry|buy\s+above|sell\s+below)\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE)),
    ("stop_loss", re.compile(r"\b(?:sl|stop\s*loss)\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE)),
    ("take_profit", re.compile(r"\b(?:tp\d*|target)\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE)),
)
_DIRECTION_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("long", re.compile(r"\b(?:buy|long|bullish|upside|breakout)\b", re.IGNORECASE)),
    ("short", re.compile(r"\b(?:sell|short(?![-\s]*(?:form|video|videos|content)s?\b)|bearish|downside|breakdown)\b", re.IGNORECASE)),
)
_TIMEFRAME_RE = re.compile(r"\b(?P<tf>M1|M5|M15|M30|H1|H4|D1|W1|1m|5m|15m|30m|1h|4h|daily|weekly)\b", re.IGNORECASE)
_INDICATORS = (
    "EMA",
    "SMA",
    "RSI",
    "MACD",
    "VWAP",
    "Bollinger",
    "Fibonacci",
    "liquidity",
    "order block",
    "FVG",
    "support",
    "resistance",
    "trendline",
)
_CHART_TERMS = re.compile(r"\b(?:chart|candle|candles|breakout|support|resistance|trendline|order block|fvg|liquidity|ema|rsi|macd)\b", re.IGNORECASE)


def analyze_vision_layer_v1(
    *,
    video_id: str,
    screen_text: str = "",
    ocr_segments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Extract structured trading hints from OCR/screen text.

    V1 is intentionally deterministic: OCR text in, normalized trading fields out.
    It does not call a vision model and does not infer missing prices.
    """

    segments = ocr_segments or []
    normalized_screen_text = _normalized_text(screen_text, segments)
    symbols = _detect_symbols(normalized_screen_text)
    directions = _detect_directions(normalized_screen_text)
    prices = _detect_prices(normalized_screen_text)
    timeframes = _detect_timeframes(normalized_screen_text)
    indicators = _detect_indicators(normalized_screen_text)
    chart_evidence = _chart_evidence(normalized_screen_text, symbols, prices, indicators)
    confidence = _confidence(normalized_screen_text, symbols, prices, timeframes, indicators, chart_evidence)
    return {
        "video_id": video_id,
        "screen_text": normalized_screen_text,
        "symbols_detected": symbols,
        "directions_detected": directions,
        "prices_detected": prices,
        "timeframes_detected": timeframes,
        "indicators_detected": indicators,
        "chart_detected": bool(chart_evidence),
        "chart_evidence": chart_evidence,
        "confidence": confidence,
    }


def _normalized_text(screen_text: str, ocr_segments: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for raw in [screen_text, *[str(segment.get("text") or "") for segment in ocr_segments if isinstance(segment, dict)]]:
        for line in raw.splitlines():
            cleaned = re.sub(r"\s+", " ", line).strip()
            if cleaned and cleaned not in lines:
                lines.append(cleaned)
    return "\n".join(lines)


def _detect_symbols(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for symbol, market_type, pattern in _SYMBOL_ALIASES:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and symbol not in seen:
            seen.add(symbol)
            found.append({"symbol": symbol, "market_type": market_type, "evidence": match.group(0)})
    return found


def _detect_directions(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for direction, pattern in _DIRECTION_PATTERNS:
        match = pattern.search(text)
        if match and direction not in seen:
            seen.add(direction)
            found.append({"direction": direction, "evidence": match.group(0)})
    return found


def _detect_prices(text: str) -> list[dict[str, Any]]:
    prices: list[dict[str, Any]] = []
    seen: set[tuple[str, float]] = set()
    for role, pattern in _PRICE_PATTERNS:
        for match in pattern.finditer(text):
            value = _parse_price(match.group("price"))
            key = (role, value)
            if key in seen:
                continue
            seen.add(key)
            prices.append({"role": role, "value": value, "evidence": match.group(0)})
    return prices


def _detect_timeframes(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for match in _TIMEFRAME_RE.finditer(text):
        timeframe = _normalize_timeframe(match.group("tf"))
        if timeframe not in seen:
            seen.add(timeframe)
            found.append({"timeframe": timeframe, "evidence": match.group(0)})
    return found


def _detect_indicators(text: str) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for indicator in _INDICATORS:
        match = re.search(rf"\b{re.escape(indicator)}\b", text, re.IGNORECASE)
        if not match:
            continue
        canonical = indicator.upper() if indicator in {"EMA", "SMA", "RSI", "MACD", "VWAP", "FVG"} else indicator
        if canonical not in seen:
            seen.add(canonical)
            found.append({"indicator": canonical, "evidence": match.group(0)})
    return found


def _chart_evidence(
    text: str,
    symbols: list[dict[str, str]],
    prices: list[dict[str, Any]],
    indicators: list[dict[str, str]],
) -> list[str]:
    evidence = []
    match = _CHART_TERMS.search(text)
    if match:
        evidence.append(match.group(0))
    if symbols and prices:
        evidence.append("symbol+price_overlay")
    if indicators:
        evidence.append("indicator_overlay")
    return evidence


def _confidence(
    text: str,
    symbols: list[dict[str, str]],
    prices: list[dict[str, Any]],
    timeframes: list[dict[str, str]],
    indicators: list[dict[str, str]],
    chart_evidence: list[str],
) -> float:
    score = 0.0
    if text:
        score += 0.15
    if symbols:
        score += 0.20
    if prices:
        score += min(0.30, 0.10 * len(prices))
    if timeframes:
        score += 0.10
    if indicators:
        score += 0.10
    if chart_evidence:
        score += 0.15
    return round(min(score, 1.0), 2)


def _parse_price(value: str) -> float:
    return float(value.replace(",", ""))


def _normalize_timeframe(value: str) -> str:
    mapping = {
        "1m": "M1",
        "5m": "M5",
        "15m": "M15",
        "30m": "M30",
        "1h": "H1",
        "4h": "H4",
        "daily": "D1",
        "weekly": "W1",
    }
    return mapping.get(value.lower(), value.upper())
