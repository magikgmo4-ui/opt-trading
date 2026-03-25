from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

from collectors_core import (
    ConfigurationError,
    HttpRequestError,
    ValidationError,
    append_jsonl,
    atomic_write_json,
    build_run_id,
    ensure_directory,
    ensure_writable_directory,
    load_json,
    module_relative_path,
    now_z,
    parse_z,
)

from .client import BinanceSpotClient
from .config import BinanceSpotRuntimeConfig, load_runtime_config, validate_runtime_requirements
from .normalize import normalize_pair_market_snapshot


@dataclass(frozen=True)
class ErrorInfo:
    error_code: str
    error_class: str
    retryable: bool
    message: str
    stage: str
    http_status: int | None = None
    retry_after: str | None = None


def run_sanity(module_dir: Path, client: BinanceSpotClient | Any | None = None) -> dict[str, Any]:
    config = load_runtime_config(module_dir)
    _ensure_runtime_directories(config)
    validate_runtime_requirements(config)

    live_client = client or BinanceSpotClient(config)
    ping_payload = live_client.ping()
    return {
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "status": "ok",
        "checked_at": now_z(),
        "ping": ping_payload,
    }


def run_collection(module_dir: Path, client: BinanceSpotClient | Any | None = None) -> dict[str, Any]:
    config = load_runtime_config(module_dir)
    _ensure_runtime_directories(config)
    _ensure_errors_artifact(config)

    run_id = build_run_id()
    run_log_path = config.paths.logs_dir / f"run_{run_id}.jsonl"
    previous_status = _safe_previous_status(config.paths.status_path)

    started_at = now_z()
    running_status = _build_running_status(config, run_id, started_at, previous_status)
    atomic_write_json(config.paths.status_path, running_status)
    _append_event(
        config=config,
        run_id=run_id,
        run_log_path=run_log_path,
        event_type="run_started",
        level="INFO",
        message="Binance Spot oneshot run started",
        state_after="running",
    )

    try:
        validate_runtime_requirements(config)
        live_client = client or BinanceSpotClient(config)
        exchange_info = live_client.fetch_exchange_info()
        ticker_items = live_client.fetch_ticker_24hr()

        raw_run_dir = config.paths.raw_dir / run_id
        ensure_directory(raw_run_dir)
        exchange_info_path = raw_run_dir / "exchange_info.json"
        ticker_path = raw_run_dir / "ticker_24hr.json"

        atomic_write_json(
            exchange_info_path,
            {
                "contract_version": config.contract_version,
                "module_id": config.module_id,
                "provider_id": config.provider_id,
                "run_id": run_id,
                "generated_at": now_z(),
                "request": {
                    "path": "/api/v3/exchangeInfo",
                    "params": {"symbols": list(config.collection_symbols)},
                },
                "response": exchange_info,
            },
        )
        atomic_write_json(
            ticker_path,
            {
                "contract_version": config.contract_version,
                "module_id": config.module_id,
                "provider_id": config.provider_id,
                "run_id": run_id,
                "generated_at": now_z(),
                "request": {
                    "path": "/api/v3/ticker/24hr",
                    "params": {
                        "symbols": list(config.collection_symbols),
                        "type": config.collection_ticker_type,
                    },
                },
                "response": ticker_items,
            },
        )

        generated_at = now_z()
        normalized_payload = normalize_pair_market_snapshot(
            config=config,
            run_id=run_id,
            generated_at=generated_at,
            exchange_info=exchange_info,
            ticker_items=ticker_items,
        )
        normalized_path = config.paths.normalized_dir / f"pair_market_snapshot_{run_id}.json"
        atomic_write_json(normalized_path, normalized_payload)

        manifest = _build_manifest(config, run_id, generated_at, exchange_info_path, ticker_path, normalized_path)
        latest = _build_latest(config, run_id, generated_at, normalized_path, normalized_payload)
        atomic_write_json(config.paths.manifest_path, manifest)
        atomic_write_json(config.paths.latest_path, latest)

        _append_event(
            config=config,
            run_id=run_id,
            run_log_path=run_log_path,
            event_type="output_published",
            level="INFO",
            message="Canonical outputs published",
            details_ref=module_relative_path(config.paths.module_dir, normalized_path),
        )

        finished_at = now_z()
        success_status = _build_success_status(config, run_id, finished_at, previous_status)
        atomic_write_json(config.paths.status_path, success_status)
        _append_event(
            config=config,
            run_id=run_id,
            run_log_path=run_log_path,
            event_type="run_succeeded",
            level="INFO",
            message="Binance Spot oneshot run succeeded",
            state_after=success_status["state"],
        )

        return {
            "run_id": run_id,
            "status": success_status["state"],
            "raw_exchange_info": module_relative_path(config.paths.module_dir, exchange_info_path),
            "raw_ticker_24hr": module_relative_path(config.paths.module_dir, ticker_path),
            "normalized_output": module_relative_path(config.paths.module_dir, normalized_path),
            "status_artifact": module_relative_path(config.paths.module_dir, config.paths.status_path),
        }
    except Exception as exc:
        error_info = _classify_error(exc)
        error_at = now_z()
        _append_error(config=config, run_id=run_id, error_info=error_info, error_at=error_at)
        failure_status = _build_failure_status(config, run_id, error_at, previous_status, error_info)
        atomic_write_json(config.paths.status_path, failure_status)
        _append_event(
            config=config,
            run_id=run_id,
            run_log_path=run_log_path,
            event_type="run_failed",
            level="ERROR",
            message=error_info.message,
            state_after=failure_status["state"],
        )
        raise


def read_status(module_dir: Path) -> dict[str, Any] | None:
    config = load_runtime_config(module_dir)
    status_payload = load_json(config.paths.status_path)
    if status_payload is None:
        return None
    if not isinstance(status_payload, dict):
        raise ValidationError("status.json must contain a JSON object")
    return status_payload


def status_as_text(module_dir: Path) -> str:
    status_payload = read_status(module_dir)
    if status_payload is None:
        return "No status.json found yet. Run sanity or run first."
    return json.dumps(status_payload, indent=2)


def _ensure_runtime_directories(config: BinanceSpotRuntimeConfig) -> None:
    for path in (
        config.paths.runtime_dir,
        config.paths.logs_dir,
        config.paths.outputs_dir,
        config.paths.raw_dir,
        config.paths.normalized_dir,
        config.paths.snapshots_dir,
    ):
        ensure_writable_directory(path)


def _ensure_errors_artifact(config: BinanceSpotRuntimeConfig) -> None:
    ensure_directory(config.paths.errors_path.parent)
    config.paths.errors_path.touch(exist_ok=True)


def _safe_previous_status(status_path: Path) -> dict[str, Any] | None:
    payload = load_json(status_path)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValidationError("Existing status.json must contain a JSON object")
    return payload


def _build_manifest(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    exchange_info_path: Path,
    ticker_path: Path,
    normalized_path: Path,
) -> dict[str, Any]:
    return {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "artifacts": {
            "manifest": module_relative_path(config.paths.module_dir, config.paths.manifest_path),
            "status": module_relative_path(config.paths.module_dir, config.paths.status_path),
            "latest": module_relative_path(config.paths.module_dir, config.paths.latest_path),
            "events": module_relative_path(config.paths.module_dir, config.paths.events_path),
            "errors": module_relative_path(config.paths.module_dir, config.paths.errors_path),
            "raw_exchange_info": module_relative_path(config.paths.module_dir, exchange_info_path),
            "raw_ticker_24hr": module_relative_path(config.paths.module_dir, ticker_path),
            "normalized_output": module_relative_path(config.paths.module_dir, normalized_path),
            "snapshots_dir": module_relative_path(config.paths.module_dir, config.paths.snapshots_dir),
        },
        "normalized_contract": {
            "schema_version": config.schema_version,
            "entity_type": "pair_market_snapshot",
            "pair_symbols": list(config.collection_symbols),
        },
        "compatibility_targets": ["opt-trading", "localcms"],
        "notes": "Binance Spot oneshot pair market snapshot",
    }


def _build_latest(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    normalized_path: Path,
    normalized_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "schema_version": config.schema_version,
        "data_ref": module_relative_path(config.paths.module_dir, normalized_path),
        "record_count": len(normalized_payload.get("records", [])),
        "summary": {
            "entity_type": normalized_payload.get("entity_type"),
            "pair_symbols": list(config.collection_symbols),
        },
    }


def _build_running_status(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    previous_status: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": "running",
        "freshness_state": _freshness_state(previous_status, config.freshness_max_age_seconds, generated_at),
        "last_event_at": generated_at,
        "last_success_run_id": _status_value(previous_status, "last_success_run_id"),
        "last_success_at": _status_value(previous_status, "last_success_at"),
        "last_failure_run_id": _status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": _status_value(previous_status, "last_failure_at"),
        "active_run_id": run_id,
        "last_error_code": _status_value(previous_status, "last_error_code"),
        "retryable": None,
        "retry_after": None,
        "message": "run started",
    }


def _build_success_status(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    previous_status: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": "healthy",
        "freshness_state": "fresh",
        "last_event_at": generated_at,
        "last_success_run_id": run_id,
        "last_success_at": generated_at,
        "last_failure_run_id": _status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": _status_value(previous_status, "last_failure_at"),
        "active_run_id": None,
        "last_error_code": None,
        "retryable": None,
        "retry_after": None,
        "message": "run succeeded",
    }


def _build_failure_status(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    previous_status: dict[str, Any] | None,
    error_info: ErrorInfo,
) -> dict[str, Any]:
    freshness_state = _freshness_state(previous_status, config.freshness_max_age_seconds, generated_at)
    has_previous_success = bool(_status_value(previous_status, "last_success_run_id"))

    if error_info.error_class == "non_recoverable" or not has_previous_success:
        state = "failed"
    elif freshness_state == "stale":
        state = "stale"
    else:
        state = "degraded"

    return {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state,
        "freshness_state": freshness_state,
        "last_event_at": generated_at,
        "last_success_run_id": _status_value(previous_status, "last_success_run_id"),
        "last_success_at": _status_value(previous_status, "last_success_at"),
        "last_failure_run_id": run_id,
        "last_failure_at": generated_at,
        "active_run_id": None,
        "last_error_code": error_info.error_code,
        "retryable": error_info.retryable,
        "retry_after": error_info.retry_after,
        "message": error_info.message,
    }


def _freshness_state(previous_status: dict[str, Any] | None, max_age_seconds: int, reference_at: str) -> str:
    if not previous_status:
        return "unknown"
    last_success_at = previous_status.get("last_success_at")
    if not isinstance(last_success_at, str) or not last_success_at:
        return "unknown"
    age = parse_z(reference_at) - parse_z(last_success_at)
    if age <= timedelta(seconds=max_age_seconds):
        return "fresh"
    return "stale"


def _append_event(
    *,
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    run_log_path: Path,
    event_type: str,
    level: str,
    message: str,
    state_after: str | None = None,
    details_ref: str | None = None,
) -> None:
    event_at = now_z()
    payload = {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
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

    append_jsonl(config.paths.events_path, payload)
    append_jsonl(run_log_path, payload)


def _append_error(*, config: BinanceSpotRuntimeConfig, run_id: str, error_info: ErrorInfo, error_at: str) -> None:
    payload = {
        "contract_version": config.contract_version,
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "run_id": run_id,
        "generated_at": error_at,
        "error_id": uuid4().hex,
        "error_at": error_at,
        "error_code": error_info.error_code,
        "error_class": error_info.error_class,
        "retryable": error_info.retryable,
        "message": error_info.message,
        "stage": error_info.stage,
    }
    if error_info.http_status is not None:
        payload["http_status"] = error_info.http_status
    if error_info.retry_after is not None:
        payload["retry_after"] = error_info.retry_after

    append_jsonl(config.paths.errors_path, payload)


def _classify_error(exc: Exception) -> ErrorInfo:
    if isinstance(exc, ConfigurationError):
        return ErrorInfo("configuration_error", "non_recoverable", False, str(exc), "configuration")
    if isinstance(exc, ValidationError):
        return ErrorInfo("validation_error", "non_recoverable", False, str(exc), "validation")
    if isinstance(exc, HttpRequestError):
        http_error: Any = exc
        status_code = http_error.status_code
        retry_after = _retry_after_absolute(http_error.headers)
        if status_code in {408, 418, 429, 500, 502, 503, 504} or status_code is None:
            error_class = "recoverable"
            retryable = True
        else:
            error_class = "non_recoverable"
            retryable = False
        code_suffix = "unknown" if status_code is None else str(status_code)
        return ErrorInfo(f"http_{code_suffix}", error_class, retryable, str(http_error), "http", status_code, retry_after)
    return ErrorInfo("unexpected_error", "non_recoverable", False, str(exc), "runtime")


def _retry_after_absolute(headers: dict[str, str]) -> str | None:
    raw_value = headers.get("Retry-After") or headers.get("retry-after")
    if raw_value is None:
        return None
    raw_value = raw_value.strip()
    if raw_value.isdigit():
        retry_at = parse_z(now_z()) + timedelta(seconds=int(raw_value))
        return retry_at.isoformat(timespec="seconds").replace("+00:00", "Z")
    return None


def _status_value(status: dict[str, Any] | None, key: str) -> Any:
    if not status:
        return None
    return status.get(key)
