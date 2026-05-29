from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from .signal_schema import ScreenerProducedSignal


def adapt_to_telegram_claim(
    signal: ScreenerProducedSignal,
    channel_id: Optional[str] = None,
    message_id: Optional[str] = None,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    claim_id = f"tg_claim_{now[:19].replace(':', '')}_{signal.pair or 'UNKNOWN'}"

    entities = _build_entities(signal)

    return {
        "input_class": "telegram_claim.v1",
        "claim_id": claim_id,
        "source": signal.source,
        "channel_id": channel_id or signal.channel,
        "message_id": message_id or str(uuid.uuid4())[:8],
        "symbol": signal.pair or "",
        "timeframe": "H1",
        "claim_ts": signal.produced_at,
        "claim_type": _claim_type(signal.signal_type),
        "text": signal.raw_text,
        "entities": entities,
        "refs": {
            "telegram_message_ref": (
                f"telegram://{channel_id or signal.channel}/{message_id or 'unknown'}"
            ),
        },
    }


_DESK_PRO_SIGNAL_TYPE_MAP = {
    "trade": "trade_context",
    "news": "news_alert",
    "alpha": "alpha_signal",
}


def _claim_type(signal_type: str) -> str:
    return _DESK_PRO_SIGNAL_TYPE_MAP.get(signal_type, "trade_context")


def _build_entities(signal: ScreenerProducedSignal) -> dict:
    entities: dict = {}

    if signal.direction:
        entities["direction"] = signal.direction.lower()

    levels = []
    if signal.entry_price is not None:
        levels.append(signal.entry_price)
    if signal.sl is not None:
        levels.append(signal.sl)
    if signal.tp is not None:
        levels.append(signal.tp)
    if levels:
        entities["levels"] = levels
    else:
        entities["levels"] = []

    if signal.confidence:
        conf_map = {"HIGH": 0.85, "MEDIUM": 0.60, "LOW": 0.35}
        entities["confidence"] = conf_map.get(signal.confidence, 0.5)

    if signal.category:
        entities["category"] = signal.category

    if signal.summary:
        entities["summary"] = signal.summary

    return entities


def adapt_batch(
    signals: list[ScreenerProducedSignal],
    channel_id: Optional[str] = None,
) -> list[dict]:
    return [adapt_to_telegram_claim(s, channel_id=channel_id) for s in signals]
