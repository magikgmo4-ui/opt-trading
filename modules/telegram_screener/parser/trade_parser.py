from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from .signal_schema import Confidence, Direction, ScreenerSignal, SignalType


_TRADE_PATTERN = re.compile(
    r"^\s*(?P<pair>[A-Z0-9]{5,20})\s*:\s*"
    r"(?P<direction>LONG|SHORT|LONG_SHORT)\s*"
    r"@\s*(?P<price>[\d.,]+)"
    r"(?:\s+SL\s*(?P<sl>[\d.,]+))?"
    r"(?:\s+TP\s*(?P<tp>[\d.,]+))?"
    r"(?:\s+SIZE\s*(?P<size>\S+))?"
    r"\s*$",
    re.IGNORECASE,
)


def _parse_float(val: Optional[str]) -> Optional[float]:
    if val is None:
        return None
    cleaned = val.replace(",", "")
    return float(cleaned)


def _infer_confidence(sl: Optional[float], tp: Optional[float]) -> Confidence:
    if sl is not None and tp is not None:
        return Confidence.HIGH
    if sl is not None or tp is not None:
        return Confidence.MEDIUM
    return Confidence.LOW


def parse_trade_setup(
    raw_text: str,
    source_channel: str = "unknown",
    timestamp: Optional[str] = None,
) -> Optional[ScreenerSignal]:
    match = _TRADE_PATTERN.match(raw_text)
    if not match:
        return None

    g = match.groupdict()
    price = _parse_float(g["price"])
    sl = _parse_float(g["sl"])
    tp = _parse_float(g["tp"])

    direction_str = g["direction"].upper()
    if direction_str == "LONG_SHORT":
        direction = None
    else:
        direction = Direction(direction_str)

    now = datetime.now(timezone.utc).isoformat()
    ts = timestamp or now

    return ScreenerSignal(
        source_channel=source_channel,
        signal_type=SignalType.TRADE,
        timestamp=ts,
        parsed_at=now,
        raw_text=raw_text,
        pair=g["pair"].upper(),
        direction=direction,
        price=price,
        sl=sl,
        tp=tp,
        size=g.get("size"),
        confidence=_infer_confidence(sl, tp),
    )
