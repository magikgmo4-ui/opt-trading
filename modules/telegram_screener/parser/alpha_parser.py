from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from .signal_schema import Confidence, ScreenerSignal, SignalType


_ALPHA_PATTERN = re.compile(
    r"^\s*(?P<ticker>[A-Za-z0-9]{1,10})\s*:\s*(?P<message>.+)$"
)


def parse_alpha_signal(
    raw_text: str,
    source_channel: str = "unknown",
    timestamp: Optional[str] = None,
) -> Optional[ScreenerSignal]:
    match = _ALPHA_PATTERN.match(raw_text)
    if not match:
        return None

    ticker = match.group("ticker").strip().upper()
    message = match.group("message").strip()

    now = datetime.now(timezone.utc).isoformat()
    ts = timestamp or now

    return ScreenerSignal(
        source_channel=source_channel,
        signal_type=SignalType.ALPHA,
        timestamp=ts,
        parsed_at=now,
        raw_text=raw_text,
        pair=ticker,
        confidence=Confidence.LOW,
        metadata={"message": message},
    )
