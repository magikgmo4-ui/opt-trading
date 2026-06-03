from __future__ import annotations

import re
from typing import Any

from modules.telegram_ingestion.parser.message_schema import RawMessage


_COINGLASS_ALERT_RE = re.compile(
    r"Hyperliquid巨鲸\*\*\((?P<wallet>0x[0-9a-f]+)\)\*\*\s+以\s+\*\*(?P<leverage>[0-9]+)x\*\*\s+杠杆做(?P<side>多|空)\*\*(?P<asset>[A-Z0-9]+)\*\*,开仓价格\s+\*\*\$(?P<entry>[0-9.]+)\*\*,仓位价值\*\*(?P<notional>[0-9.]+)万\*\*美元",
    re.IGNORECASE,
)


def parse_coinglass_alert(raw: RawMessage) -> dict[str, Any] | None:
    match = _COINGLASS_ALERT_RE.search(raw.raw_text)
    if not match:
        return None

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
