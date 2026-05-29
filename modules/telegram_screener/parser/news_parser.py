from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from .signal_schema import Confidence, ScreenerSignal, SignalType


_NEWS_PATTERN = re.compile(
    r"^\s*\[(?P<category>[A-Za-z_]+)\]\s*(?P<message>.+)$"
)


def parse_news_alert(
    raw_text: str,
    source_channel: str = "unknown",
    timestamp: Optional[str] = None,
) -> Optional[ScreenerSignal]:
    match = _NEWS_PATTERN.match(raw_text)
    if not match:
        return None

    category = match.group("category").strip()

    now = datetime.now(timezone.utc).isoformat()
    ts = timestamp or now

    return ScreenerSignal(
        source_channel=source_channel,
        signal_type=SignalType.NEWS,
        timestamp=ts,
        parsed_at=now,
        raw_text=raw_text,
        category=category,
        confidence=Confidence.MEDIUM,
    )
