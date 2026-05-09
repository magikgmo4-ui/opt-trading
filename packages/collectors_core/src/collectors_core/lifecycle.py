from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping
from uuid import uuid4

from .files import append_jsonl
from .timeutil import now_z, parse_z


def status_value(status: Mapping[str, Any] | None, key: str) -> Any:
    if not status:
        return None
    return status.get(key)


def freshness_state(previous_status: Mapping[str, Any] | None, max_age_seconds: int, reference_at: str) -> str:
    if not previous_status:
        return "unknown"
    last_success_at = previous_status.get("last_success_at")
    if not isinstance(last_success_at, str) or not last_success_at:
        return "unknown"
    age = parse_z(reference_at) - parse_z(last_success_at)
    if age <= timedelta(seconds=max_age_seconds):
        return "fresh"
    return "stale"


def retry_after_absolute(headers: Mapping[str, str]) -> str | None:
    raw_value = headers.get("Retry-After") or headers.get("retry-after")
    if raw_value is None:
        return None
    raw_value = raw_value.strip()
    if raw_value.isdigit():
        retry_at = parse_z(now_z()) + timedelta(seconds=int(raw_value))
        return retry_at.isoformat(timespec="seconds").replace("+00:00", "Z")
    return None


def append_event_record(
    *,
    events_path,
    run_log_path,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    event_type: str,
    level: str,
    message: str,
    state_after: str | None = None,
    details_ref: str | None = None,
) -> None:
    event_at = now_z()
    payload = {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": event_at,
        "event_id": uuid4().hex,
        "event_at": event_at,
        "event_type": event_type,
        "level": level,
        "message": message,
    }
    if state_after is not None:
        payload["state_after"] = state_after
    if details_ref is not None:
        payload["details_ref"] = details_ref

    append_jsonl(events_path, payload)
    append_jsonl(run_log_path, payload)


def append_error_record(
    *,
    errors_path,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    error_at: str,
    error_code: str,
    error_class: str,
    retryable: bool,
    message: str,
    stage: str,
    http_status: int | None = None,
    retry_after: str | None = None,
) -> None:
    payload = {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": error_at,
        "error_id": uuid4().hex,
        "error_at": error_at,
        "error_code": error_code,
        "error_class": error_class,
        "retryable": retryable,
        "message": message,
        "stage": stage,
    }
    if http_status is not None:
        payload["http_status"] = http_status
    if retry_after is not None:
        payload["retry_after"] = retry_after

    append_jsonl(errors_path, payload)
