#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from modules.derivatives_collector.app.derivatives_collector import DerivativesCollector, load_config

logger = logging.getLogger(__name__)

CONTRACT_VERSION = "v1"
MODULE_ID = "derivatives_collector"
FRESHNESS_MAX_AGE_SECONDS = 3600
MODULE_DIR = Path(__file__).resolve().parent.parent


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def now_z() -> str:
    return iso_z(now_utc())


def parse_z(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def build_run_id() -> str:
    return f"{now_utc().strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"


def load_json(path: Path):
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def append_jsonl(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload))
        handle.write("\n")


def ensure_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def relref(path: Path) -> str:
    return path.relative_to(MODULE_DIR).as_posix()


def provider_id_from_config(config: dict) -> str | None:
    value = config.get("DATA_SOURCE")
    if not value:
        return None
    return str(value).lower()


def freshness_state(previous_status: dict | None, reference_at: str) -> str:
    if not previous_status:
        return "unknown"
    last_success_at = previous_status.get("last_success_at")
    if not isinstance(last_success_at, str) or not last_success_at:
        return "unknown"
    age = parse_z(reference_at) - parse_z(last_success_at)
    if age <= timedelta(seconds=FRESHNESS_MAX_AGE_SECONDS):
        return "fresh"
    return "stale"


def status_value(status: dict | None, key: str):
    if not status:
        return None
    return status.get(key)


def build_running_status(config: dict, run_id: str, generated_at: str, previous_status: dict | None) -> dict:
    return {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": generated_at,
        "state": "running",
        "freshness_state": freshness_state(previous_status, generated_at),
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


def build_success_status(config: dict, run_id: str, generated_at: str, previous_status: dict | None, failed_rows: int) -> dict:
    state = "degraded" if failed_rows > 0 else "healthy"
    message = "run completed with row errors" if failed_rows > 0 else "run succeeded"
    return {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state,
        "freshness_state": "fresh",
        "last_event_at": generated_at,
        "last_success_run_id": run_id,
        "last_success_at": generated_at,
        "last_failure_run_id": status_value(previous_status, "last_failure_run_id"),
        "last_failure_at": status_value(previous_status, "last_failure_at"),
        "active_run_id": None,
        "last_error_code": "source_row_error" if failed_rows > 0 else None,
        "retryable": None,
        "retry_after": None,
        "message": message,
    }


def build_failure_status(config: dict, run_id: str, generated_at: str, previous_status: dict | None, error_info: dict) -> dict:
    fresh = freshness_state(previous_status, generated_at)
    has_previous_success = bool(status_value(previous_status, "last_success_run_id"))
    if error_info["error_class"] == "non_recoverable" or not has_previous_success:
        state = "failed"
    elif fresh == "stale":
        state = "stale"
    else:
        state = "degraded"
    return {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state,
        "freshness_state": fresh,
        "last_event_at": generated_at,
        "last_success_run_id": status_value(previous_status, "last_success_run_id"),
        "last_success_at": status_value(previous_status, "last_success_at"),
        "last_failure_run_id": run_id,
        "last_failure_at": generated_at,
        "active_run_id": None,
        "last_error_code": error_info["error_code"],
        "retryable": error_info["retryable"],
        "retry_after": error_info["retry_after"],
        "message": error_info["message"],
    }


def append_event(config: dict, events_path: Path, run_id: str, event_type: str, level: str, message: str, state_after: str | None = None) -> None:
    event_at = now_z()
    payload = {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
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
    append_jsonl(events_path, payload)


def append_error(config: dict, errors_path: Path, run_id: str, error_info: dict, error_at: str) -> None:
    payload = {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": error_at,
        "error_id": uuid4().hex,
        "error_at": error_at,
        "error_code": error_info["error_code"],
        "error_class": error_info["error_class"],
        "retryable": error_info["retryable"],
        "message": error_info["message"],
        "stage": error_info["stage"],
    }
    if error_info.get("retry_after") is not None:
        payload["retry_after"] = error_info["retry_after"]
    append_jsonl(errors_path, payload)


def classify_error(exc: Exception, stage: str) -> dict:
    code = {
        "configuration": "configuration_error",
        "source_fetch": "source_request_error",
        "publish": "output_write_error",
        "lifecycle": "unknown_error",
    }.get(stage, "unknown_error")
    return {
        "error_code": code,
        "error_class": "non_recoverable",
        "retryable": False,
        "retry_after": None,
        "message": str(exc),
        "stage": stage,
    }


def write_primary_outputs(config: dict, data: list[dict], duration_s: float) -> dict:
    output_dir = Path(config["OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    fmt = str(config["OUTPUT_FORMAT"]).lower()
    now = now_utc()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    primary_path = output_dir / f"derivatives_{timestamp_str}.{fmt}"
    meta_path = primary_path.with_suffix(".meta.json")

    stats = {
        "requested": len(data),
        "succeeded": len([row for row in data if row.get("error") is None]),
        "failed": len([row for row in data if row.get("error") is not None]),
    }
    meta = {
        "batch_timestamp": now.astimezone().isoformat(),
        "source": config["DATA_SOURCE"],
        "stats": stats,
        "duration_s": round(duration_s, 3),
        "meta_schema_version": 1,
    }

    print(json.dumps(data, indent=2))

    if fmt == "json":
        write_json(primary_path, data)
    elif fmt == "csv":
        with primary_path.open("w", newline="", encoding="utf-8") as handle:
            fieldnames = list(data[0].keys()) if data else [
                "symbol", "exchange", "timestamp", "open_interest", "funding_rate",
                "long_short_ratio", "liquidations_long", "liquidations_short",
                "volume_futures", "error"
            ]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else:
        raise ValueError(f"Unsupported OUTPUT_FORMAT: {fmt}")

    write_json(meta_path, meta)
    return {
        "primary_path": primary_path,
        "meta_path": meta_path,
        "stats": stats,
        "output_format": fmt,
    }


def build_manifest(config: dict, run_id: str, generated_at: str, primary_path: Path, meta_path: Path, output_dir: Path) -> dict:
    return {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": generated_at,
        "artifacts": {
            "manifest": relref(output_dir / "manifest.json"),
            "status": relref(output_dir / "status.json"),
            "latest": relref(output_dir / "latest.json"),
            "events": relref(output_dir / "events.jsonl"),
            "errors": relref(output_dir / "errors.jsonl"),
            "primary_output": relref(primary_path),
            "meta_output": relref(meta_path),
        },
        "derivatives_outputs": {
            "primary_output_format": primary_path.suffix.lstrip("."),
            "legacy_exports_preserved": True,
        },
        "compatibility_notes": [
            "Legacy derivatives JSON/CSV exports remain authoritative downstream outputs.",
            "Lifecycle artifacts are additive compatibility companions only.",
        ],
    }


def build_latest(config: dict, run_id: str, generated_at: str, primary_path: Path, meta_path: Path, stats: dict) -> dict:
    return {
        "contract_version": CONTRACT_VERSION,
        "module_id": MODULE_ID,
        "provider_id": provider_id_from_config(config),
        "run_id": run_id,
        "generated_at": generated_at,
        "outputs": {
            "primary_output": relref(primary_path),
            "meta_output": relref(meta_path),
        },
        "summary": {
            "data_source": config["DATA_SOURCE"],
            "symbols": list(config["SYMBOLS"]),
            "records_total": stats["requested"],
            "records_failed": stats["failed"],
        },
    }


def run_collection_with_lifecycle(config: dict) -> dict:
    collector = DerivativesCollector(config)
    output_dir = Path(config["OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)

    status_path = output_dir / "status.json"
    manifest_path = output_dir / "manifest.json"
    latest_path = output_dir / "latest.json"
    events_path = output_dir / "events.jsonl"
    errors_path = output_dir / "errors.jsonl"

    previous_status = load_json(status_path)
    run_id = build_run_id()
    started_at = now_z()
    write_json(status_path, build_running_status(config, run_id, started_at, previous_status))
    ensure_file(errors_path)
    append_event(config, events_path, run_id, "run_started", "INFO", "derivatives lifecycle compatibility run started", "running")
    append_event(config, events_path, run_id, "source_fetch_started", "INFO", f"collecting derivatives data from {config['DATA_SOURCE']}")

    stage = "source_fetch"
    try:
        started = time.perf_counter()
        data = collector.adapter.collect(config["SYMBOLS"])
        duration_s = time.perf_counter() - started
        append_event(config, events_path, run_id, "source_fetch_succeeded", "INFO", f"collected {len(data)} derivatives rows")

        stage = "publish"
        outputs = write_primary_outputs(config, data, duration_s)
        generated_at = now_z()
        manifest = build_manifest(config, run_id, generated_at, outputs["primary_path"], outputs["meta_path"], output_dir)
        latest = build_latest(config, run_id, generated_at, outputs["primary_path"], outputs["meta_path"], outputs["stats"])
        write_json(manifest_path, manifest)
        write_json(latest_path, latest)
        append_event(config, events_path, run_id, "outputs_published", "INFO", "lifecycle compatibility artifacts published")

        success_status = build_success_status(config, run_id, generated_at, previous_status, outputs["stats"]["failed"])
        write_json(status_path, success_status)
        append_event(config, events_path, run_id, "run_succeeded", "INFO", success_status["message"], success_status["state"])
        return {
            "run_id": run_id,
            "state": success_status["state"],
            "primary_output": relref(outputs["primary_path"]),
            "meta_output": relref(outputs["meta_path"]),
            "status_artifact": relref(status_path),
        }
    except Exception as exc:
        error_at = now_z()
        error_info = classify_error(exc, stage)
        append_error(config, errors_path, run_id, error_info, error_at)
        failure_status = build_failure_status(config, run_id, error_at, previous_status, error_info)
        write_json(status_path, failure_status)
        if stage == "source_fetch":
            append_event(config, events_path, run_id, "source_fetch_failed", "ERROR", error_info["message"], failure_status["state"])
        append_event(config, events_path, run_id, "run_failed", "ERROR", error_info["message"], failure_status["state"])
        raise


def status_as_text(config: dict) -> str:
    status_path = Path(config["OUTPUT_DIR"]) / "status.json"
    payload = load_json(status_path)
    if payload is None:
        return "No lifecycle compatibility status.json found yet. Run collect first."
    return json.dumps(payload, indent=2)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Derivatives Collector lifecycle compatibility runner")
    parser.add_argument("command", nargs="?", default="collect", choices=["collect", "sample", "export", "status"])
    args = parser.parse_args()

    config = load_config()
    if args.command == "sample":
        config["DATA_SOURCE"] = "mock"
        run_collection_with_lifecycle(config)
    elif args.command == "export":
        run_collection_with_lifecycle(config)
    elif args.command == "status":
        print(status_as_text(config))
    else:
        run_collection_with_lifecycle(config)


if __name__ == "__main__":
    main()
