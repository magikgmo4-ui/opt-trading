from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from ..parser import ScreenerSignal, SignalType
from .signal_schema import ScreenerProducedSignal


def _build_summary(signal: ScreenerSignal) -> str:
    if signal.signal_type == SignalType.TRADE:
        dir_str = signal.direction.value if signal.direction else "BIDIRECTIONAL"
        price_str = f" @ {signal.price}" if signal.price is not None else ""
        return f"{signal.pair} {dir_str}{price_str}"
    if signal.signal_type == SignalType.NEWS:
        return f"[{signal.category}]" if signal.category else "news alert"
    if signal.signal_type == SignalType.ALPHA:
        msg = signal.metadata.get("message", "")
        return f"{signal.pair}: {msg}" if signal.pair else msg
    return signal.raw_text


def produce_screener_signal(
    signal: ScreenerSignal,
    source: str = "telegram_screener",
) -> ScreenerProducedSignal:
    now = datetime.now(timezone.utc).isoformat()
    entries = _build_entries(signal)
    direction_val = signal.direction.value if signal.direction else None

    return ScreenerProducedSignal(
        id=str(uuid.uuid4()),
        source=source,
        signal_type=signal.signal_type.value,
        channel=signal.source_channel,
        parsed_at=signal.parsed_at,
        produced_at=now,
        pair=entries["pair"],
        direction=direction_val,
        entry_price=entries["price"],
        sl=signal.sl,
        tp=signal.tp,
        size=signal.size,
        category=signal.category,
        confidence=signal.confidence.value if signal.confidence else None,
        raw_text=signal.raw_text,
        summary=_build_summary(signal),
    )


def _build_entries(signal: ScreenerSignal) -> dict:
    if signal.signal_type == SignalType.TRADE:
        return {"pair": signal.pair, "price": signal.price}
    if signal.signal_type == SignalType.ALPHA:
        return {"pair": signal.pair, "price": None}
    return {"pair": None, "price": None}


def produce_batch(
    signals: list[ScreenerSignal],
    source: str = "telegram_screener",
) -> list[ScreenerProducedSignal]:
    return [produce_screener_signal(s, source=source) for s in signals]
