from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from collectors_core import (
    ConfigurationError,
    HttpRequestError,
    ValidationError,
    append_error_record,
    append_event_record,
    atomic_write_json,
    build_run_id,
    ensure_directory,
    ensure_writable_directory,
    freshness_state,
    load_json,
    module_relative_path,
    now_z,
    retry_after_absolute,
    status_value,
)

from .client import CoinGeckoClient
from .config import CoinGeckoRuntimeConfig, load_runtime_config, validate_runtime_requirements
from .normalize import normalize_market_snapshot


@dataclass(frozen=True)
class ErrorInfo:
    error_code: str
    error_class: str
    retryable: bool
    message: str
    stage: str
    http_status: int | None = None
    retry_after: str | None = None


def run_sanity(module_dir: Path, client: CoinGeckoClient | Any | None = None) -> dict[str, Any]:
    config = load_runtime_config(module_dir)
    _ensure_runtime_directories(config)
    validate_runtime_requirements(config)

    live_client = client or CoinGeckoClient(config)
    ping_payload = live_client.ping()
    return {
        "module_id": config.module_id,
        "provider_id": config.provider_id,
        "status": "ok",
        "checked_at": now_z(),
        "ping": ping_payload,
    }


def run_collection(module_dir: Path, client: CoinGeckoClient | Any | None = None) -> dict[str, Any]:
    config = load_runtime_config(module_dir)
    _ensure_runtime_directories(config)

    run_id = build_run_id()
    run_log_path = config.paths.logs_dir / f"run_{run_id}.jsonl"
    previous_status = _safe_previous_status(config.paths.status_path)

    started_at = now_z()
    running_status = _build_running_status(config, run_id, started_at, previous_status)
    atomic_write_json(config.paths.status_path, running_status)
    append_event_record(
        events_path=config.paths.events_path,
        run_log_path=run_log_path,
        contract_version=config.contract_version,
        module_id=config.module_id,
        provider_id=config.provider_id,
        run_id=run_id,
        event_type="run_started",
        level="INFO",
        message="CoinGecko oneshot run started",
        state_after="running",
    )

    try:
        validate_runtime_requirements(config)
        live_client = client or CoinGeckoClient(config)
        raw_items = live_client.fetch_markets()

        raw_capture_path = config.paths.raw_dir / run_id / "coins_markets.json"
        ensure_directory(raw_capture_path.parent)
        atomic_write_json(
            raw_capture_path,
            {
                "contract_version": config.contract_version,
                "module_id": config.module_id,
                "provider_id": config.provider_id,
                "run_id": run_id,
                "generated_at": now_z(),
                "request": {
                    "path": "/coins/markets",
                    "params": {
                        "ids": list(config.collection_coin_ids),
                        "vs_currency": config.collection_vs_currency,
                        "sparkline": config.collection_sparkline,
                        "price_change_percentage": list(config.collection_price_change_percentage),
                        "locale": config.collection_locale,
                        "precision": config.collection_precision,
                    },
                },
                "response": raw_items,
            },
        )

        generated_at = now_z()
        normalized_payload = normalize_market_snapshot(
            config=config,
            run_id=run_id,
            generated_at=generated_at,
            raw_items=raw_items,
        )
        normalized_path = config.paths.normalized_dir / f"market_snapshot_{run_id}.json"
        atomic_write_json(normalized_path, normalized_payload)

        manifest = _build_manifest(config, run_id, generated_at, raw_capture_path, normalized_path)
        latest = _build_latest(config, run_id, generated_at, normalized_path, normalized_payload)

        atomic_write_json(config.paths.manifest_path, manifest)
        atomic_write_json(config.paths.latest_path, latest)

        append_event_record(
            events_path=config.paths.events_path,
            run_log_path=run_log_path,
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
            event_type="output_published",
            level="INFO",
            message="Canonical outputs published",
            details_ref=module_relative_path(config.paths.module_dir, normalized_path),
        )

        finished_at = now_z()
        success_status = _build_success_status(config, run_id, finished_at, previous_status)
        atomic_write_json(config.paths.status_path, success_status)
        append_event_record(
            events_path=config.paths.events_path,
            run_log_path=run_log_path,
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
            event_type="run_succeeded",
            level="INFO",
            message="CoinGecko oneshot run succeeded",
            state_after=success_status["state"],
        )

        return {
            "run_id": run_id,
            "status": success_status["state"],
            "raw_capture": module_relative_path(config.paths.module_dir, raw_capture_path),
            "normalized_output": module_relative_path(config.paths.module_dir, normalized_path),
            "status_artifact": module_relative_path(config.paths.module_dir, config.paths.status_path),
        }
    except Exception as exc:
        error_info = _classify_error(exc)
        error_at = now_z()
        append_error_record(
            errors_path=config.paths.errors_path,
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
            error_at=error_at,
            error_code=error_info.error_code,
            error_class=error_info.error_class,
            retryable=error_info.retryable,
            message=error_info.message,
            stage=error_info.stage,
            http_status=error_info.http_status,
            retry_after=error_info.retry_after,
        )
        failure_status = _build_failure_status(config, run_id, error_at, previous_status, error_info)
        atomic_write_json(config.paths.status_path, failure_status)
        append_event_record(
            events_path=config.paths.events_path,
            run_log_path=run_log_path,
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
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


def _ensure_runtime_directories(config: CoinGeckoRuntimeConfig) -> None:
    for path in (
        config.paths.runtime_dir,
        config.paths.logs_dir,
        config.paths.outputs_dir,
        config.paths.raw_dir,
        config.paths.normalized_dir,
        config.paths.snapshots_dir,
    ):
        ensure_writable_directory(path)


def _safe_previous_status(status_path: Path) -> dict[str, Any] | None:
    payload = load_json(status_path)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise ValidationError("Existing status.json must contain a JSON object")
    return payload


def _build_manifest(
    config: CoinGeckoRuntimeConfig,
    run_id: str,
    generated_at: str,
    raw_capture_path: Path,
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
            "raw_capture": module_relative_path(config.paths.module_dir, raw_capture_path),
            "normalized_output": module_relative_path(config.paths.module_dir, normalized_path),
            "snapshots_dir": module_relative_path(config.paths.module_dir, config.paths.snapshots_dir),
        },
        "normalized_contract": {
            "schema_version": config.schema_version,
            "entity_type": "market_snapshot",
            "quote_currency": config.collection_vs_currency,
        },
        "compatibility_targets": ["opt-trading", "localcms"],
        "notes": "Pilot CoinGecko oneshot market snapshot",
    }


def _build_latest(
    config: CoinGeckoRuntimeConfig,
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
            "quote_currency": normalized_payload.get("quote_currency"),
            "coin_ids": list(config.collection_coin_ids),
        },
    }


def _build_running_status(
    config: CoinGeckoRuntimeConfig,
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
        "freshness_state": freshness_state(previous_status, config.freshness_max_age_seconds, generated_at),
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


def _build_success_status(
    config: CoinGeckoRuntimeConfig,
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
        "last_failure_run_id": status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": status_value(previous_status, "last_failure_at"),
        "active_run_id": None,
        "last_error_code": None,
        "retryable": None,
        "retry_after": None,
        "message": "run succeeded",
    }


def _build_failure_status(
    config: CoinGeckoRuntimeConfig,
    run_id: str,
    generated_at: str,
    previous_status: dict[str, Any] | None,
    error_info: ErrorInfo,
) -> dict[str, Any]:
    freshness_state_value = freshness_state(previous_status, config.freshness_max_age_seconds, generated_at)
    has_previous_success = bool(status_value(previous_status, "last_success_run_id"))

    if error_info.error_class == "non_recoverable" or not has_previous_success:
        state = "failed"
    elif freshness_state_value == "stale":
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
        "freshness_state": freshness_state_value,
        "last_event_at": generated_at,
        "last_success_run_id": status_value(previous_status, "last_success_run_id"),
        "last_success_at": status_value(previous_status, "last_success_at"),
        "last_failure_run_id": run_id,
        "last_failure_at": generated_at,
        "active_run_id": None,
        "last_error_code": error_info.error_code,
        "retryable": error_info.retryable,
        "retry_after": error_info.retry_after,
        "message": error_info.message,
    }


def _classify_error(exc: Exception) -> ErrorInfo:
    if isinstance(exc, ConfigurationError):
        return ErrorInfo(
            error_code="configuration_error",
            error_class="non_recoverable",
            retryable=False,
            message=str(exc),
            stage="configuration",
        )
    if isinstance(exc, ValidationError):
        return ErrorInfo(
            error_code="validation_error",
            error_class="non_recoverable",
            retryable=False,
            message=str(exc),
            stage="validation",
        )
    if isinstance(exc, HttpRequestError):
        status_code = exc.status_code
        retry_after = retry_after_absolute(exc.headers)
        if status_code in {408, 429, 500, 502, 503, 504} or status_code is None:
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
            message=str(exc),
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
    )
