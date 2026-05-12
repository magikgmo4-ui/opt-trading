from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from collectors_core import (
    append_error_record,
    append_event_record,
    atomic_write_json,
    build_failure_status,
    build_latest_record,
    build_manifest_record,
    build_run_id,
    build_running_status,
    build_success_status,
    classify_collector_error,
    ensure_directory,
    ensure_file,
    ensure_writable_directories,
    module_relative_path,
    now_z,
    read_status_payload,
    safe_previous_status,
    status_payload_as_text,
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
    previous_status = safe_previous_status(config.paths.status_path)

    started_at = now_z()
    running_status = build_running_status(
        contract_version=config.contract_version,
        module_id=config.module_id,
        provider_id=config.provider_id,
        run_id=run_id,
        generated_at=started_at,
        previous_status=previous_status,
        max_age_seconds=config.freshness_max_age_seconds,
    )
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
        success_status = build_success_status(
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
            generated_at=finished_at,
            previous_status=previous_status,
        )
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
        failure_status = build_failure_status(
            contract_version=config.contract_version,
            module_id=config.module_id,
            provider_id=config.provider_id,
            run_id=run_id,
            generated_at=error_at,
            previous_status=previous_status,
            max_age_seconds=config.freshness_max_age_seconds,
            error_class=error_info.error_class,
            error_code=error_info.error_code,
            retryable=error_info.retryable,
            retry_after=error_info.retry_after,
            message=error_info.message,
        )
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
    return read_status_payload(config.paths.status_path)


def status_as_text(module_dir: Path) -> str:
    return status_payload_as_text(read_status(module_dir), "No status.json found yet. Run sanity or run first.")


def _ensure_runtime_directories(config: BinanceSpotRuntimeConfig) -> None:
    ensure_writable_directories(
        config.paths.runtime_dir,
        config.paths.logs_dir,
        config.paths.outputs_dir,
        config.paths.raw_dir,
        config.paths.normalized_dir,
        config.paths.snapshots_dir,
    )


def _ensure_errors_artifact(config: BinanceSpotRuntimeConfig) -> None:
    ensure_directory(config.paths.errors_path.parent)
    config.paths.errors_path.touch(exist_ok=True)


def _build_manifest(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    exchange_info_path: Path,
    ticker_path: Path,
    normalized_path: Path,
) -> dict[str, Any]:
    return build_manifest_record(
        contract_version=config.contract_version,
        module_id=config.module_id,
        provider_id=config.provider_id,
        run_id=run_id,
        generated_at=generated_at,
        artifacts={
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
        normalized_contract={
            "schema_version": config.schema_version,
            "entity_type": "pair_market_snapshot",
            "pair_symbols": list(config.collection_symbols),
        },
        compatibility_targets=["opt-trading", "localcms"],
        notes="Binance Spot oneshot pair market snapshot",
    )


def _build_latest(
    config: BinanceSpotRuntimeConfig,
    run_id: str,
    generated_at: str,
    normalized_path: Path,
    normalized_payload: dict[str, Any],
) -> dict[str, Any]:
    return build_latest_record(
        contract_version=config.contract_version,
        module_id=config.module_id,
        provider_id=config.provider_id,
        run_id=run_id,
        generated_at=generated_at,
        schema_version=config.schema_version,
        data_ref=module_relative_path(config.paths.module_dir, normalized_path),
        record_count=len(normalized_payload.get("records", [])),
        summary={
            "entity_type": normalized_payload.get("entity_type"),
            "pair_symbols": list(config.collection_symbols),
        },
    )


def _classify_error(exc: Exception) -> ErrorInfo:
    info = classify_collector_error(exc, extra_recoverable_codes={418})
    return ErrorInfo(info["error_code"], info["error_class"], info["retryable"], info["message"], info["stage"], info["http_status"], info["retry_after"])
