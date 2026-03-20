from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


def now_utc() -> datetime:
    return datetime.now(UTC)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def now_z() -> str:
    return iso_z(now_utc())


def parse_z(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).astimezone(UTC)


def build_run_id() -> str:
    return f"{now_utc().strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
