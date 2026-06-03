from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from .parser.signal_schema import Confidence, Direction, ScreenerSignal, SignalType
from .schema import SignalCandidate


def coinglass_dict_to_candidate(raw: dict[str, Any]) -> SignalCandidate:
    tps = [raw.get(k) for k in ("tp1", "tp2", "tp3") if raw.get(k) is not None]

    entry = raw.get("entry")
    raw_text = ""
    message_ref = raw.get("raw_text_ref", "")
    if message_ref:
        parts = message_ref.split(":", 1)
        if len(parts) == 2:
            raw_text = f"<ref:{parts[0]}:{parts[1]}>"

    return SignalCandidate(
        raw_message=raw_text,
        source_channel=raw.get("source_channel", ""),
        asset=raw.get("asset"),
        symbol=raw.get("symbol"),
        direction=raw.get("direction"),
        entry_min=entry,
        entry_max=entry,
        tp=tps,
        sl=raw.get("stop_loss"),
        leverage=raw.get("leverage"),
        timeframe=raw.get("timeframe"),
        parse_status=raw.get("parse_status", "PARTIAL"),
        parse_confidence=raw.get("confidence", "LOW"),
        parse_errors=list(raw.get("parse_errors", [])),
        message_ref=message_ref,
        created_at=raw.get("message_timestamp", ""),
    )


def screener_signal_to_candidate(signal: ScreenerSignal) -> SignalCandidate:
    tps = []
    if signal.tp is not None:
        tps.append(signal.tp)

    asset = None
    if signal.pair:
        asset = signal.pair

    return SignalCandidate(
        raw_message=signal.raw_text,
        source_channel=signal.source_channel,
        asset=asset,
        symbol=signal.pair,
        direction=signal.direction.value if signal.direction else None,
        entry_min=signal.price,
        entry_max=signal.price,
        tp=tps,
        sl=signal.sl,
        leverage=signal.metadata.get("leverage"),
        timeframe=signal.metadata.get("timeframe"),
        parse_status=signal.metadata.get("parse_status", "PARSED"),
        parse_confidence=signal.confidence.value if signal.confidence else "LOW",
        parse_errors=list(signal.metadata.get("parse_errors", [])),
        message_ref=signal.metadata.get("message_ref", ""),
        created_at=signal.timestamp,
    )


def _direction_from_str(val: Optional[str]) -> Optional[Direction]:
    if val is None:
        return None
    try:
        return Direction(val.upper())
    except ValueError:
        return None


def _confidence_from_str(val: Optional[str]) -> Optional[Confidence]:
    if val is None:
        return None
    try:
        return Confidence(val.upper())
    except ValueError:
        return Confidence.LOW


def candidate_to_screener_signal(
    candidate: SignalCandidate,
    signal_type: SignalType = SignalType.TRADE,
) -> ScreenerSignal:
    now = datetime.now(timezone.utc).isoformat()

    metadata: dict[str, Any] = {}
    if candidate.parse_errors:
        metadata["parse_errors"] = list(candidate.parse_errors)
    if candidate.leverage is not None:
        metadata["leverage"] = candidate.leverage
    if candidate.timeframe is not None:
        metadata["timeframe"] = candidate.timeframe
    if candidate.message_ref:
        metadata["message_ref"] = candidate.message_ref
    metadata["parse_status"] = candidate.parse_status

    return ScreenerSignal(
        source_channel=candidate.source_channel,
        signal_type=signal_type,
        timestamp=candidate.created_at or now,
        parsed_at=now,
        raw_text=candidate.raw_message,
        pair=candidate.symbol,
        direction=_direction_from_str(candidate.direction),
        price=candidate.entry_min,
        sl=candidate.sl,
        tp=candidate.tp[0] if candidate.tp else None,
        confidence=_confidence_from_str(candidate.parse_confidence),
        metadata=metadata,
    )


def normalize_coinglass_dict(raw: dict[str, Any]) -> ScreenerSignal:
    candidate = coinglass_dict_to_candidate(raw)
    return candidate_to_screener_signal(candidate)
