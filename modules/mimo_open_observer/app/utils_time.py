from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


ACTIVE_WEEKDAYS = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday")

MONTREAL_TZ = ZoneInfo("America/Montreal")


def is_active_weekday(dt_local: datetime) -> bool:
    return dt_local.strftime("%A") in ACTIVE_WEEKDAYS


def build_window_ts(
    date_value: datetime,
    tz_name: str = "America/Montreal",
    hour: int = 18,
    minute: int = 0,
) -> datetime:
    tz = ZoneInfo(tz_name)
    return date_value.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=tz)


def add_minutes(ts: datetime, minutes: int) -> datetime:
    return ts + timedelta(minutes=minutes)
