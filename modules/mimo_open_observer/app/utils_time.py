from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo


ACTIVE_WEEKDAYS = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday")

WEEKDAY_MAP = {
    "sun": 6, "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5,
}

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


def is_market_open_day(dt_local: datetime) -> bool:
    return dt_local.weekday() in (6, 0, 1, 2, 3)


def get_enabled_windows(config: dict) -> list[dict]:
    tz_name = config.get("timezone", "America/Montreal")
    tz = ZoneInfo(tz_name)
    windows_cfg = config.get("windows", {})
    enabled = []
    for name, wcfg in windows_cfg.items():
        if not wcfg.get("enabled", False):
            continue
        weekdays_raw = wcfg.get("weekdays", [])
        weekdays = set()
        for d in weekdays_raw:
            d_lower = d.lower()[:3]
            if d_lower in WEEKDAY_MAP:
                weekdays.add(WEEKDAY_MAP[d_lower])
        enabled.append({
            "name": name,
            "hour": wcfg.get("hour", 0),
            "minute": wcfg.get("minute", 0),
            "weekdays": weekdays,
            "tz": tz,
            "tz_name": tz_name,
        })
    return enabled


def is_market_window(dt_local: datetime, config: dict) -> bool:
    windows = get_enabled_windows(config)
    for w in windows:
        if (
            dt_local.weekday() in w["weekdays"]
            and dt_local.hour == w["hour"]
            and dt_local.minute == w["minute"]
        ):
            return True
    return False


def next_market_window(after_dt: datetime, config: dict) -> Optional[datetime]:
    windows = get_enabled_windows(config)
    if not windows:
        return None

    tz_name = config.get("timezone", "America/Montreal")
    tz = ZoneInfo(tz_name)

    after_local = after_dt.astimezone(tz)
    best = None

    for w in windows:
        for day_offset in range(8):
            candidate_date = after_local.date() + timedelta(days=day_offset)
            candidate = datetime(
                candidate_date.year, candidate_date.month, candidate_date.day,
                w["hour"], w["minute"], tzinfo=tz,
            )
            if candidate <= after_local:
                continue
            if candidate.weekday() not in w["weekdays"]:
                continue
            if best is None or candidate < best:
                best = candidate

    return best
