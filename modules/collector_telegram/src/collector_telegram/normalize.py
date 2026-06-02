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
_FREE_SIGNAL_RE = re.compile(
    r"(?P<side>BUY|SELL) GOLD NOW.*?Entry Point:\s*(?P<entry>[^\n]+).*?Stop Loss:\s*(?P<sl>[0-9.]+).*?TP1:\s*(?P<tp1>[0-9.]+).*?TP2:\s*(?P<tp2>[0-9.]+)",
    re.IGNORECASE | re.DOTALL,
)
_XAUHQ_SIGNAL_RE = re.compile(
    r"DIRECTION:\s*\*\*(?:↗️|↘️)?\s*(?P<side>BUY|SELL)\*\*.*?ENTRY:\s*(?P<entry>[^\n]+).*?STOP LOSS:\*\*\s*(?P<sl>[0-9.]+)\*\*.*?TAKE PROFIT:(?P<tp_block>.*?)(?:RISK:|$)",
    re.IGNORECASE | re.DOTALL,
)
_TP_VALUE_RE = re.compile(r"TP\d+\s*[→:]+\s*(?P<value>[0-9./]+)")
_BINANCE_KILLERS_RE = re.compile(
    r"COIN:\s*\*+\$(?P<symbol>[A-Z0-9]+)\*+/USDT.*?Direction:\s*(?P<side>LONG|SHORT).*?(?P<targets>(?:Target\s+\d+:\s*[0-9.]+✅?\s*)+)",
    re.IGNORECASE | re.DOTALL,
)
_BK_TARGET_RE = re.compile(r"Target\s+\d+:\s*(?P<value>[0-9.]+)")
_WSQ_SIGNAL_RE = re.compile(
    r"COIN:\s*\*+[#$]?(?P<symbol>[A-Z0-9]+)\*+.*?Direction:\*+\s*(?P<side>Long|Short).*?Entry:\s*(?P<entry>[^\n]+).*?Targets:\s*(?P<targets>[^\n]+).*?Stoploss:\s*(?P<sl>[0-9.]+)",
    re.IGNORECASE | re.DOTALL,
)
_FATPIG_HEADER_RE = re.compile(r"TP(?P<tp_level>[123]) HIT\s+[—-]\s+(?P<symbol>[A-Z0-9\u4e00-\u9fff]+)/USDT", re.IGNORECASE)
_FATPIG_SOLD_RE = re.compile(r"Sold\s+(?P<sold_pct>[0-9]+)%\s+at\s+\$(?P<hit_price>[0-9.]+)", re.IGNORECASE)
_FATPIG_SL_RE = re.compile(r"SL moved\s*[→:]\s*(?P<sl_label>[^\n(]+?)(?:\s*\(\$?(?P<sl_price>[0-9.]+)\))?(?:\n|$)", re.IGNORECASE)
_GOLDTRADING_ZONE_RE = re.compile(
    r"STNBY ZONE BUY RANGE.*?@\s*(?P<zone1>[0-9\s\-]+).*?ZONE BUY.*?@\s*(?P<zone2>[0-9\s\-]+)",
    re.IGNORECASE | re.DOTALL,
)
_GOLDTRADING_TP_RE = re.compile(
    r"HIT\s+(?P<pips>[0-9]+)\s+PIPS.*?(?:TP\s+(?P<tp_kind>PARSIAL|TAMAK))?.*?(?P<tp_price>[0-9]{4,5}(?:\.[0-9]+)?)?",
    re.IGNORECASE,
)
_CRYPTOQUANT_RE = re.compile(
    r"(?P<title>[^\n]+)\n\n[“\"]?(?P<thesis>.+?)[”\"]?\s*[–-]\s*\[Read More\]",
    re.IGNORECASE | re.DOTALL,
)
_ASSET_RE = re.compile(r"\b(BTC|BITCOIN|ETH|ETHEREUM|AAVE|XRP|XLM|USDT|ALTCOIN|ALTCOINS)\b", re.IGNORECASE)


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

    free_signal = _parse_free_gold_signal(raw.raw_text)
    if free_signal is not None:
        return _parsed_payload(raw, "TRADE_SIGNAL", "parsed", 0.9, free_signal)

    xuahq_signal = _parse_xauhq_signal(raw.raw_text)
    if xuahq_signal is not None:
        return _parsed_payload(raw, "TRADE_SIGNAL", "parsed", 0.92, xuahq_signal)

    bk_signal = _parse_binance_killers_signal(raw.raw_text)
    if bk_signal is not None:
        return _parsed_payload(raw, "TRADE_SIGNAL", "partial", 0.8, bk_signal)

    wsq_signal = _parse_wsq_signal(raw.raw_text)
    if wsq_signal is not None:
        return _parsed_payload(raw, "TRADE_SIGNAL", "parsed", 0.88, wsq_signal)

    fatpig_update = _parse_fatpig_update(raw.raw_text)
    if fatpig_update is not None:
        return _parsed_payload(raw, "MARKET_STRUCTURE", "partial", 0.7, fatpig_update)

    goldtrading_signal = _parse_goldtrading_signal(raw.raw_text)
    if goldtrading_signal is not None:
        return _parsed_payload(raw, goldtrading_signal.pop("message_type"), goldtrading_signal.pop("parser_status"), goldtrading_signal.pop("parser_score"), goldtrading_signal)

    cryptoquant_context = _parse_cryptoquant_context(raw.raw_text)
    if cryptoquant_context is not None:
        return _parsed_payload(raw, "NEWS_CATALYST", "partial", 0.5, cryptoquant_context)

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


def _parse_free_gold_signal(raw_text: str) -> dict[str, Any] | None:
    match = _FREE_SIGNAL_RE.search(raw_text)
    if not match:
        return None
    side = "LONG" if match.group("side").upper() == "BUY" else "SHORT"
    entry = _parse_price_series(match.group("entry"))
    return {
        "symbol": "XAUUSD",
        "side": side,
        "entry": entry,
        "tp": [float(match.group("tp1")), float(match.group("tp2"))],
        "sl": float(match.group("sl")),
    }


def _parse_xauhq_signal(raw_text: str) -> dict[str, Any] | None:
    match = _XAUHQ_SIGNAL_RE.search(raw_text)
    if not match:
        return None
    side = "LONG" if match.group("side").upper() == "BUY" else "SHORT"
    targets = []
    for tp_match in _TP_VALUE_RE.finditer(match.group("tp_block")):
        targets.extend(_parse_price_series(tp_match.group("value")))
    return {
        "symbol": "XAUUSD",
        "side": side,
        "entry": _parse_price_series(match.group("entry")),
        "tp": targets,
        "sl": float(match.group("sl")),
    }


def _parse_binance_killers_signal(raw_text: str) -> dict[str, Any] | None:
    match = _BINANCE_KILLERS_RE.search(raw_text)
    if not match:
        return None
    return {
        "symbol": f"{match.group('symbol').upper()}USDT",
        "side": match.group("side").upper(),
        "entry": [],
        "tp": [float(tp.group("value")) for tp in _BK_TARGET_RE.finditer(match.group("targets"))],
        "sl": None,
    }


def _parse_wsq_signal(raw_text: str) -> dict[str, Any] | None:
    match = _WSQ_SIGNAL_RE.search(raw_text)
    if not match:
        return None
    return {
        "symbol": match.group("symbol").upper(),
        "side": "LONG" if match.group("side").upper() == "LONG" else "SHORT",
        "entry": [] if match.group("entry").strip().lower() == "market price" else _parse_price_series(match.group("entry")),
        "tp": [float(value.strip().replace("$+", "")) for value in match.group("targets").split("-") if value.strip()],
        "sl": float(match.group("sl")),
    }


def _parse_fatpig_update(raw_text: str) -> dict[str, Any] | None:
    header = _FATPIG_HEADER_RE.search(raw_text)
    sold = _FATPIG_SOLD_RE.search(raw_text)
    stop = _FATPIG_SL_RE.search(raw_text)
    if not header or not sold or not stop:
        return None
    sl_price = stop.group("sl_price")
    return {
        "symbol": f"{header.group('symbol').upper()}USDT",
        "event": f"TP{header.group('tp_level')}_HIT",
        "sold_pct": int(sold.group("sold_pct")),
        "hit_price": float(sold.group("hit_price")),
        "sl_state": stop.group("sl_label").strip(),
        "sl": float(sl_price) if sl_price else None,
    }


def _parse_goldtrading_signal(raw_text: str) -> dict[str, Any] | None:
    zone = _GOLDTRADING_ZONE_RE.search(raw_text)
    if zone is not None:
        entries = _extract_int_levels(zone.group("zone1")) + _extract_int_levels(zone.group("zone2"))
        return {
            "message_type": "TRADE_SIGNAL",
            "parser_status": "partial",
            "parser_score": 0.62,
            "symbol": "XAUUSD",
            "side": "LONG",
            "entry": entries,
            "tp": [],
            "sl": None,
        }

    tp = _GOLDTRADING_TP_RE.search(raw_text)
    if tp is None or "HIT" not in raw_text.upper():
        return None
    tp_price = tp.group("tp_price")
    parsed: dict[str, Any] = {
        "message_type": "MARKET_STRUCTURE",
        "parser_status": "partial",
        "parser_score": 0.45,
        "symbol": "XAUUSD",
        "event": "TP_HIT",
        "pips": int(tp.group("pips")),
    }
    if tp.group("tp_kind"):
        parsed["tp_kind"] = tp.group("tp_kind").upper()
    if tp_price:
        parsed["tp_price"] = float(tp_price)
    return parsed


def _parse_cryptoquant_context(raw_text: str) -> dict[str, Any] | None:
    match = _CRYPTOQUANT_RE.search(raw_text)
    if not match:
        return None
    title = match.group("title").strip()
    thesis = match.group("thesis").strip()
    assets = []
    seen: set[str] = set()
    for asset in _ASSET_RE.findall(title + "\n" + thesis):
        normalized = asset.upper()
        if normalized == "BITCOIN":
            normalized = "BTC"
        elif normalized == "ETHEREUM":
            normalized = "ETH"
        elif normalized == "ALTCOINS":
            normalized = "ALTCOIN"
        if normalized not in seen:
            seen.add(normalized)
            assets.append(normalized)
    return {
        "headline": title,
        "summary": thesis,
        "assets": assets,
        "source_type": "research_note",
    }


def _extract_int_levels(raw_value: str) -> list[float]:
    return [float(match.group(0)) for match in re.finditer(r"[0-9]{4,5}(?:\.[0-9]+)?", raw_value)]


def _parse_price_series(raw_value: str) -> list[float]:
    values = [part.strip() for part in raw_value.replace("-", "/").split("/") if part.strip() and part.strip().upper() != "OPEN"]
    if not values:
        return []
    parsed = [float(values[0])]
    for value in values[1:]:
        parsed.append(_expand_shorthand(parsed[-1], value))
    return parsed


def _expand_shorthand(previous: float, raw_value: str) -> float:
    if re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", raw_value) and float(raw_value) >= 100:
        return float(raw_value)
    previous_text = f"{previous:.4f}".rstrip("0").rstrip(".")
    prev_int = previous_text.split(".")[0]
    if "." in raw_value:
        int_part, frac_part = raw_value.split(".", 1)
        if len(int_part) < len(prev_int):
            int_part = prev_int[: len(prev_int) - len(int_part)] + int_part
        return float(f"{int_part}.{frac_part}")
    if len(raw_value) < len(prev_int):
        raw_value = prev_int[: len(prev_int) - len(raw_value)] + raw_value
    return float(raw_value)


def _channel_role(channel_alias: str) -> str:
    mapping = {
        "coinglass_alerts": "LIQUIDITY_OI",
        "cryptoquant_official": "FUNDING_OI_ALERT",
        "glassnode": "ONCHAIN_STRUCTURE",
        "arkhamintelligence": "ENTITY_WALLET",
        "whale_alert_io": "WHALE_TRANSFER",
    }
    return mapping.get(channel_alias, "CANDIDATE_SIGNAL")
