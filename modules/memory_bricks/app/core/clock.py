from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.constants import DEFAULT_TIMEZONE


def now_iso() -> str:
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).isoformat(timespec="seconds")
