from __future__ import annotations

import re
from typing import Any


PARSER_PROFILE = "youtube_trading_short_v1"

_ASSET_ALIASES: tuple[tuple[str, str, str], ...] = (
    ("XAUUSD", "forex", r"\b(?:xauusd|xau|gold)\b"),
    ("BTCUSDT", "crypto", r"\b(?:btcusdt|btc|bitcoin)\b"),
    ("ETHUSDT", "crypto", r"\b(?:ethusdt|eth|ethereum)\b"),
    ("NASDAQ/US100", "index", r"\b(?:nasdaq|us100|nq)\b"),
    ("SPX/US500", "index", r"\b(?:spx|s&p|us500)\b"),
)
_LONG_RE = re.compile(r"\b(?:buy|long|bullish|pump|upside|breakout)\b", re.IGNORECASE)
_SHORT_RE = re.compile(r"\b(?:sell|short(?![-\s]*(?:form|video|videos|content)s?\b)|bearish|dump|downside|breakdown)\b", re.IGNORECASE)
_NEGATED_DIRECTION_RE = re.compile(r"\b(?:do not|dont|don't|avoid|no|never)\s+(?:buy|sell|long|short)\b", re.IGNORECASE)
_ENTRY_PATTERNS = (
    re.compile(r"\bentry\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE),
    re.compile(r"\bbuy\s+above\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE),
    re.compile(r"\bsell\s+below\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE),
    re.compile(r"\bzone\s*(?P<price>[0-9][0-9,.]*)\s*[-/]\s*[0-9][0-9,.]*\b", re.IGNORECASE),
)
_SL_RE = re.compile(r"\b(?:sl|stop\s*loss)\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE)
_TP_RE = re.compile(r"\b(?:tp\d*|target)\s*[:@]?\s*(?P<price>[0-9][0-9,.]*)\b", re.IGNORECASE)
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


def parse_youtube_trading_short(parser_input: dict[str, Any]) -> dict[str, Any]:
    if parser_input.get("parser_profile") not in {None, "", PARSER_PROFILE}:
        raise ValueError(f"Unsupported parser_profile: {parser_input.get('parser_profile')}")

    title = _text(parser_input.get("title"))
    description = _text(parser_input.get("description"))
    spoken = _text(parser_input.get("spoken_transcript"))
    screen = _text(parser_input.get("screen_text"))
    combined = "\n".join(part for part in (title, description, spoken, screen) if part)

    asset, market_type, asset_evidence = _detect_asset(combined)
    direction, direction_evidence = _detect_direction(combined)
    audio_direction, _ = _detect_direction(spoken)
    screen_direction, _ = _detect_direction(screen)
    conflict_detected = audio_direction in {"long", "short"} and screen_direction in {"long", "short"} and audio_direction != screen_direction
    if conflict_detected:
        direction = "unknown"

    entry, entry_evidence = _first_price_match(_ENTRY_PATTERNS, combined)
    stop_loss, sl_evidence = _single_price_match(_SL_RE, combined)
    take_profits, tp_evidence = _take_profit_matches(combined)
    timeframe, timeframe_evidence = _detect_timeframe(combined)
    indicators, indicator_evidence = _detect_indicators(combined)

    raw_evidence = []
    for field, evidence in (
        ("asset", asset_evidence),
        ("direction", direction_evidence),
        ("entry", entry_evidence),
        ("stop_loss", sl_evidence),
        ("take_profits", tp_evidence),
        ("timeframe", timeframe_evidence),
        ("indicators", indicator_evidence),
    ):
        if evidence:
            raw_evidence.append({"field": field, "text": evidence})

    confidence = _confidence(asset, direction, entry, stop_loss, take_profits, timeframe, indicators)
    missing_fields = _missing_fields(asset, direction, entry, stop_loss, take_profits)
    classification = _classification(confidence)

    return {
        "video_id": _text(parser_input.get("video_id")),
        "asset": asset,
        "market_type": market_type,
        "direction": direction,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profits": take_profits,
        "timeframe": timeframe,
        "indicators": indicators,
        "pattern": None,
        "strategy_rules": [],
        "risk_rules": [],
        "confidence": confidence,
        "classification": classification,
        "missing_fields": missing_fields,
        "raw_evidence": raw_evidence,
        "conflict_detected": conflict_detected,
    }


def _detect_asset(text: str) -> tuple[str, str, str | None]:
    for asset, market_type, pattern in _ASSET_ALIASES:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return asset, market_type, match.group(0)
    return "unknown", "unknown", None


def _detect_direction(text: str) -> tuple[str, str | None]:
    scrubbed = _NEGATED_DIRECTION_RE.sub("", text)
    long_match = _LONG_RE.search(scrubbed)
    short_match = _SHORT_RE.search(scrubbed)
    if long_match and short_match:
        return "unknown", f"{long_match.group(0)} / {short_match.group(0)}"
    if long_match:
        return "long", long_match.group(0)
    if short_match:
        return "short", short_match.group(0)
    return "unknown", None


def _first_price_match(patterns: tuple[re.Pattern[str], ...], text: str) -> tuple[float | None, str | None]:
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            return _parse_price(match.group("price")), match.group(0)
    return None, None


def _single_price_match(pattern: re.Pattern[str], text: str) -> tuple[float | None, str | None]:
    match = pattern.search(text)
    if not match:
        return None, None
    return _parse_price(match.group("price")), match.group(0)


def _take_profit_matches(text: str) -> tuple[list[float], str | None]:
    values: list[float] = []
    evidence: list[str] = []
    for match in _TP_RE.finditer(text):
        price = _parse_price(match.group("price"))
        if price not in values:
            values.append(price)
            evidence.append(match.group(0))
    return values, "; ".join(evidence) if evidence else None


def _detect_timeframe(text: str) -> tuple[str | None, str | None]:
    match = _TIMEFRAME_RE.search(text)
    if not match:
        return None, None
    return _normalize_timeframe(match.group("tf")), match.group(0)


def _detect_indicators(text: str) -> tuple[list[str], str | None]:
    found: list[str] = []
    evidence: list[str] = []
    for indicator in _INDICATORS:
        if re.search(rf"\b{re.escape(indicator)}\b", text, re.IGNORECASE):
            canonical = indicator.upper() if indicator in {"EMA", "SMA", "RSI", "MACD", "VWAP", "FVG"} else indicator
            found.append(canonical)
            evidence.append(indicator)
    return found, ", ".join(evidence) if evidence else None


def _confidence(
    asset: str,
    direction: str,
    entry: float | None,
    stop_loss: float | None,
    take_profits: list[float],
    timeframe: str | None,
    indicators: list[str],
) -> float:
    score = 0.0
    if asset != "unknown":
        score += 0.25
    if direction in {"long", "short"}:
        score += 0.20
    if entry is not None:
        score += 0.20
    if stop_loss is not None:
        score += 0.15
    if take_profits:
        score += 0.10
    if timeframe or indicators:
        score += 0.10
    return round(score, 2)


def _classification(confidence: float) -> str:
    if confidence >= 0.75:
        return "candidate_complete"
    if confidence >= 0.50:
        return "candidate_partial"
    if confidence >= 0.25:
        return "context_only"
    return "reject_noise"


def _missing_fields(
    asset: str,
    direction: str,
    entry: float | None,
    stop_loss: float | None,
    take_profits: list[float],
) -> list[str]:
    missing = []
    if asset == "unknown":
        missing.append("asset")
    if direction == "unknown":
        missing.append("direction")
    if entry is None:
        missing.append("entry")
    if stop_loss is None:
        missing.append("stop_loss")
    if not take_profits:
        missing.append("take_profits")
    return missing


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
    lowered = value.lower()
    return mapping.get(lowered, value.upper())


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)
