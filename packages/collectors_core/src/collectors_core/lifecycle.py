from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Mapping
from uuid import uuid4

from .files import append_jsonl
from .errors import ConfigurationError, HttpRequestError, ValidationError
from .timeutil import now_z, parse_z


@dataclass(frozen=True)
class ErrorInfo:
    error_code: str
    error_class: str
    retryable: bool
    message: str
    stage: str
    http_status: int | None = None
    retry_after: str | None = None


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


def safe_previous_status(status_path) -> dict[str, Any] | None:
    from .files import load_json

    payload = load_json(status_path)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValidationError("Existing status.json must contain a JSON object")
    return payload


def read_status_payload(status_path) -> dict[str, Any] | None:
    return safe_previous_status(status_path)


def status_payload_as_text(status_payload: Mapping[str, Any] | None, empty_message: str) -> str:
    if status_payload is None:
        return empty_message
    import json

    return json.dumps(status_payload, indent=2)


def build_running_status(
    *,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    generated_at: str,
    previous_status: Mapping[str, Any] | None,
    max_age_seconds: int,
) -> dict[str, Any]:
    return {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": "running",
        "freshness_state": freshness_state(previous_status, max_age_seconds, generated_at),
        "last_event_at": generated_at,
        "last_success_run_id": status_value(previous_status, "last_success_run_id"),
        "last_success_at": status_value(previous_status, "last_success_at"),
        "last_failure_run_id": status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": status_value(previous_status, "last_failure_at"),
        "active_run_id": run_id,
        "last_error_code": status_value(previous_status, "last_error_code"),
        "retryable": None,
        "retry_after": None,
        "message": "run started",
    }


def build_success_status(
    *,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    generated_at: str,
    previous_status: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": "healthy",
        "freshness_state": "fresh",
        "last_event_at": generated_at,
        "last_success_run_id": run_id,
        "last_success_at": generated_at,
        "last_failure_run_id": status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": status_value(previous_status, "last_failure_at"),
        "active_run_id": None,
        "last_error_code": None,
        "retryable": None,
        "retry_after": None,
        "message": "run succeeded",
    }


def build_failure_status(
    *,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    generated_at: str,
    previous_status: Mapping[str, Any] | None,
    max_age_seconds: int,
    error_class: str,
    error_code: str,
    retryable: bool,
    retry_after: str | None,
    message: str,
) -> dict[str, Any]:
    fresh_state = freshness_state(previous_status, max_age_seconds, generated_at)
    has_previous_success = bool(status_value(previous_status, "last_success_run_id"))

    if error_class == "non_recoverable" or not has_previous_success:
        state = "failed"
    elif fresh_state == "stale":
        state = "stale"
    else:
        state = "degraded"

    return {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state,
        "freshness_state": fresh_state,
        "last_event_at": generated_at,
        "last_success_run_id": status_value(previous_status, "last_success_run_id"),
        "last_success_at": status_value(previous_status, "last_success_at"),
        "last_failure_run_id": run_id,
        "last_failure_at": generated_at,
        "active_run_id": None,
        "last_error_code": error_code,
        "retryable": retryable,
        "retry_after": retry_after,
        "message": message,
    }


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


def build_manifest_record(
    *,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    generated_at: str,
    artifacts: Mapping[str, Any],
    normalized_contract: Mapping[str, Any],
    compatibility_targets: list[str] | tuple[str, ...],
    notes: str,
) -> dict[str, Any]:
    return {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "artifacts": dict(artifacts),
        "normalized_contract": dict(normalized_contract),
        "compatibility_targets": list(compatibility_targets),
        "notes": notes,
    }


def build_latest_record(
    *,
    contract_version: str,
    module_id: str,
    provider_id: str | None,
    run_id: str,
    generated_at: str,
    schema_version: str | int,
    data_ref: str,
    record_count: int,
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "contract_version": contract_version,
        "module_id": module_id,
        "provider_id": provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "schema_version": schema_version,
        "data_ref": data_ref,
        "record_count": record_count,
        "summary": dict(summary),
    }


_HTTP_RECOVERABLE_BASE: set[int] = {408, 429, 500, 502, 503, 504}


def classify_collector_error(
    exc: Exception,
    extra_recoverable_codes: set[int] | frozenset[int] | None = None,
) -> ErrorInfo:
    if isinstance(exc, ConfigurationError):
        return ErrorInfo(
            error_code="configuration_error",
            error_class="non_recoverable",
            retryable=False,
            message=str(exc),
            stage="configuration",
            http_status=None,
            retry_after=None,
        )
    if isinstance(exc, ValidationError):
        return ErrorInfo(
            error_code="validation_error",
            error_class="non_recoverable",
            retryable=False,
            message=str(exc),
            stage="validation",
            http_status=None,
            retry_after=None,
        )
    if isinstance(exc, HttpRequestError):
        http_err: Any = exc
        status_code = http_err.status_code
        retry_after = retry_after_absolute(http_err.headers)
        recoverable = _HTTP_RECOVERABLE_BASE.copy()
        if extra_recoverable_codes:
            recoverable.update(extra_recoverable_codes)
        if status_code in recoverable or status_code is None:
            error_class = "recoverable"
            retryable = True
        else:
            error_class = "non_recoverable"
            retryable = False
        code_suffix = "unknown" if status_code is None else str(status_code)
        return ErrorInfo(
            error_code=f"http_{code_suffix}",
            error_class=error_class,
            retryable=retryable,
            message=str(http_err),
            stage="http",
            http_status=status_code,
            retry_after=retry_after,
        )
    return ErrorInfo(
        error_code="unexpected_error",
        error_class="non_recoverable",
        retryable=False,
        message=str(exc),
        stage="runtime",
        http_status=None,
        retry_after=None,
    )
