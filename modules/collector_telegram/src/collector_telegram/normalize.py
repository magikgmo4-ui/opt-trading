from __future__ import annotations

import re
from collections import Counter
from typing import Any

from modules.telegram_ingestion.parser.message_schema import RawMessage
from modules.telegram_screener.parser import parse_alpha_signal, parse_news_alert, parse_trade_setup


_HYPERLIQUID_RE = re.compile(
    r"做(?P<side>多|空)\*\*(?P<symbol>[A-Z0-9]+)\*\*,开仓价格 \*\*\$(?P<entry>[0-9.]+)\*\*",
)
_OI_CHANGE_RE = re.compile(
    r"交易对 \*\*(?P<venue>[A-Za-z0-9_]+) (?P<symbol>[A-Z0-9]+/[A-Z0-9]+)\*\* ,\s+(?P<window>[0-9]+) 分钟内持仓变化:\*\*(?P<change>-?[0-9.]+)\*\*%",
)
_WHALE_TRANSFER_RE = re.compile(
    r"(?P<amount>[0-9,]+) \$(?P<asset>[A-Z0-9]+) \((?P<usd>[0-9,]+) USD\) (?P<action>transferred|minted|burned|locked)",
    re.IGNORECASE,
)


def parse_message(raw: RawMessage) -> dict[str, Any]:
    trade = parse_trade_setup(raw.raw_text, source_channel=raw.channel, timestamp=raw.timestamp)
    if trade is not None:
        normalized = {
            "symbol": trade.pair,
            "side": trade.direction.value if trade.direction else None,
            "entry": [trade.price] if trade.price is not None else [],
            "tp": [trade.tp] if trade.tp is not None else [],
            "sl": trade.sl,
            "size": trade.size,
        }
        return _parsed_payload(raw, "TRADE_SIGNAL", "parsed", 1.0, normalized)

    news = parse_news_alert(raw.raw_text, source_channel=raw.channel, timestamp=raw.timestamp)
    if news is not None:
        normalized = {"category": news.category, "headline": raw.raw_text}
        return _parsed_payload(raw, "NEWS_CATALYST", "parsed", 0.6, normalized)

    alpha = parse_alpha_signal(raw.raw_text, source_channel=raw.channel, timestamp=raw.timestamp)
    if alpha is not None:
        normalized = {"symbol": alpha.pair, "message": alpha.metadata.get("message")}
        return _parsed_payload(raw, "ALPHA_SIGNAL", "parsed", 0.55, normalized)

    hyperliquid = _parse_hyperliquid(raw.raw_text)
    if hyperliquid is not None:
        return _parsed_payload(raw, "MARKET_STRUCTURE", "partial", 0.78, hyperliquid)

    oi_change = _parse_oi_change(raw.raw_text)
    if oi_change is not None:
        return _parsed_payload(raw, "MARKET_STRUCTURE", "partial", 0.72, oi_change)

    whale = _parse_whale_transfer(raw.raw_text)
    if whale is not None:
        return _parsed_payload(raw, "MARKET_STRUCTURE", "partial", 0.86, whale)

    if "[Read Analysis]" in raw.raw_text:
        return _parsed_payload(raw, "NEWS_CATALYST", "partial", 0.45, {"headline": raw.raw_text.splitlines()[0]})

    return _parsed_payload(raw, "UNKNOWN_RAW", "unparsed", 0.0, None)


def summarize_channel(messages: list[dict[str, Any]], channel_alias: str) -> dict[str, Any]:
    total = len(messages)
    parsed_count = sum(1 for item in messages if item["parser_status"] != "unparsed")
    claims_count = sum(1 for item in messages if item["message_type"] == "TRADE_SIGNAL" and item["parser_status"] == "parsed")
    needs_review_count = sum(1 for item in messages if item["parser_status"] in {"parsed", "partial"})
    unknown_raw_count = sum(1 for item in messages if item["message_type"] == "UNKNOWN_RAW")
    counter = Counter(item["message_type"] for item in messages)
    scores = [float(item["parser_score"]) for item in messages if float(item["parser_score"]) > 0]
    return {
        "schema": "telegram_channel_result.v1",
        "source_kind": "live_capture",
        "channel_alias": channel_alias,
        "role": _channel_role(channel_alias),
        "messages_total": total,
        "parsed_count": parsed_count,
        "claims_count": claims_count,
        "needs_review_count": needs_review_count,
        "unknown_raw_count": unknown_raw_count,
        "noise_count": 0,
        "dominant_message_types": [name for name, _ in counter.most_common(3)],
        "avg_parser_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
        "supported_formats": sorted(counter.keys()),
        "rejected_patterns": [],
        "recommended_status": "KEEP_REVIEW_REQUIRED" if total else "NO_DATA",
    }


def _parsed_payload(raw: RawMessage, message_type: str, parser_status: str, parser_score: float, parsed: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "schema": "telegram_parsed_message.v1",
        "source_kind": "live_capture",
        "channel_alias": raw.channel,
        "message_id": raw.message_id,
        "raw_text": raw.raw_text,
        "sender": raw.sender,
        "timestamp_utc": raw.timestamp,
        "has_image": False,
        "message_type": message_type,
        "parser_status": parser_status,
        "parser_score": round(parser_score, 3),
        "parsed": parsed,
    }


def _parse_hyperliquid(raw_text: str) -> dict[str, Any] | None:
    match = _HYPERLIQUID_RE.search(raw_text)
    if not match:
        return None
    side = "LONG" if match.group("side") == "多" else "SHORT"
    return {
        "symbol": match.group("symbol"),
        "side": side,
        "entry": [float(match.group("entry"))],
        "tp": [],
        "sl": None,
    }


def _parse_oi_change(raw_text: str) -> dict[str, Any] | None:
    match = _OI_CHANGE_RE.search(raw_text)
    if not match:
        return None
    return {
        "symbol": match.group("symbol").replace("/", ""),
        "venue": match.group("venue"),
        "window_minutes": int(match.group("window")),
        "oi_change_pct": float(match.group("change")),
    }


def _parse_whale_transfer(raw_text: str) -> dict[str, Any] | None:
    match = _WHALE_TRANSFER_RE.search(raw_text)
    if not match:
        return None
    return {
        "asset": match.group("asset"),
        "amount": float(match.group("amount").replace(",", "")),
        "amount_usd": float(match.group("usd").replace(",", "")),
        "event": match.group("action").lower(),
    }


def _channel_role(channel_alias: str) -> str:
    mapping = {
        "coinglass_alerts": "LIQUIDITY_OI",
        "cryptoquant_official": "FUNDING_OI_ALERT",
        "glassnode": "ONCHAIN_STRUCTURE",
        "arkhamintelligence": "ENTITY_WALLET",
        "whale_alert_io": "WHALE_TRANSFER",
    }
    return mapping.get(channel_alias, "CANDIDATE_SIGNAL")
