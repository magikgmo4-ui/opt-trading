from __future__ import annotations

import re
from typing import Any

from modules.telegram_ingestion.parser.message_schema import RawMessage


_COINGLASS_ALERT_RE = re.compile(
    r"Hyperliquid巨鲸\*\*\((?P<wallet>0x[0-9a-f]+)\)\*\*\s+以\s+\*\*(?P<leverage>[0-9]+)x\*\*\s+杠杆做(?P<side>多|空)\*\*(?P<asset>[A-Z0-9]+)\*\*,开仓价格\s+\*\*\$(?P<entry>[0-9.]+)\*\*,仓位价值\*\*(?P<notional>[0-9.]+)万\*\*美元",
    re.IGNORECASE,
)

_COINGLASS_TRANSFER_RE = re.compile(
    r"\*\*大额转账\*\* : \*\*(?P<amount_asset>[\d,]+)\*\* #(?P<asset>[A-Z0-9]+) \(\*\*(?P<amount_usd>[\d,]+)\*\* USD\)\s*(?:\n|\\n) 从 (?P<from_entity>[^ ]+) 钱包 转移到 (?P<to_entity>[^ ]+) 钱包",
)


def _parse_amount(raw: str) -> float:
    return float(raw.replace(",", ""))


def parse_coinglass_transfer(raw: RawMessage) -> dict[str, Any] | None:
    match = _COINGLASS_TRANSFER_RE.search(raw.raw_text)
    if not match:
        return None

    from_entity = match.group("from_entity")
    to_entity = match.group("to_entity")
    is_unknown_from = from_entity == "未知"
    is_unknown_to = to_entity == "未知"

    confidence = "MEDIUM" if (not is_unknown_from and not is_unknown_to) else "LOW"
    parse_status = "PARSED" if (not is_unknown_from and not is_unknown_to) else "PARTIAL"

    return {
        "schema": "telegram_transfer_candidate.v1",
        "source_channel": raw.channel,
        "message_timestamp": raw.timestamp,
        "raw_text_ref": f"{raw.channel}:{raw.message_id}",
        "asset": match.group("asset").upper(),
        "amount_asset": _parse_amount(match.group("amount_asset")),
        "amount_usd": _parse_amount(match.group("amount_usd")),
        "from_entity": from_entity,
        "to_entity": to_entity,
        "from_identified": not is_unknown_from,
        "to_identified": not is_unknown_to,
        "transaction_type": "TRANSFER",
        "confidence": confidence,
        "parse_status": parse_status,
        "parse_errors": [],
    }


def parse_coinglass_alert(raw: RawMessage) -> dict[str, Any] | None:
    match = _COINGLASS_ALERT_RE.search(raw.raw_text)
    if not match:
        return parse_coinglass_transfer(raw)

    side = "LONG" if match.group("side") == "多" else "SHORT"
    return {
        "schema": "telegram_trade_signal_candidate.v1",
        "source_channel": raw.channel,
        "message_timestamp": raw.timestamp,
        "raw_text_ref": f"{raw.channel}:{raw.message_id}",
        "asset": match.group("asset").upper(),
        "symbol": match.group("asset").upper(),
        "direction": side,
        "entry": float(match.group("entry")),
        "tp1": None,
        "tp2": None,
        "tp3": None,
        "stop_loss": None,
        "leverage": int(match.group("leverage")),
        "timeframe": None,
        "exchange_source": "Hyperliquid",
        "confidence": "MEDIUM",
        "parse_status": "PARTIAL",
        "parse_errors": [],
        "notional_usd": float(match.group("notional")) * 10000,
    }
