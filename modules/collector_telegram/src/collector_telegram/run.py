from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modules.telegram_ingestion.parser.message_schema import RawMessage

from .client import CollectorTelegramClient
from .config import CollectorConfig, ChannelConfig, enabled_channels, load_config
from .normalize import parse_message, summarize_channel


def run_sanity(module_dir: Path) -> dict[str, Any]:
    config = load_config(module_dir)
    return {
        "module_id": "collector_telegram",
        "python_ok": True,
        "config_path": str(config.paths.module_dir / "config" / "channels.json"),
        "channels_total": len(config.channels),
        "channels_enabled": len(enabled_channels(config)),
        "telegram_api_id_present": config.api_id is not None,
        "telegram_api_hash_present": bool(config.api_hash),
        "session_path": str(config.paths.session_path),
    }


def run_collection(
    module_dir: Path,
    *,
    channel_alias: str | None = None,
    limit: int = 100,
    client: CollectorTelegramClient | None = None,
) -> dict[str, Any]:
    config = load_config(module_dir)
    selected_channels = _select_channels(config, channel_alias)
    run_id = _run_id()
    paths = config.paths
    _ensure_dirs(paths)
    _append_event(paths.events_path, _event(run_id, "run_started", "INFO", "Telegram batch collection started", state_after="running"))

    owned_client = client is None
    if client is None:
        if config.api_id is None or not config.api_hash:
            raise RuntimeError("TELEGRAM_API_ID and TELEGRAM_API_HASH are required for live collection")
        client = CollectorTelegramClient(paths.session_path, config.api_id, config.api_hash)
    if owned_client:
        client.start()

    channel_results: list[dict[str, Any]] = []
    total_messages = 0
    failed_channels: list[str] = []
    per_channel_limit = min(limit, 30)  # cap to avoid memory pressure segfaults

    for i, channel in enumerate(selected_channels):
        try:
            raw_messages = _dedupe_messages(client.fetch_messages(channel.source_ref, limit=per_channel_limit))
            parsed_messages = [parse_message(_retag_channel(msg, channel.alias)) for msg in raw_messages]
            total_messages += len(parsed_messages)
            _write_jsonl(paths.raw_dir / f"{channel.alias}.jsonl", [_raw_message_dict(_retag_channel(msg, channel.alias)) for msg in raw_messages])
            channel_results.append(summarize_channel(parsed_messages, channel.alias))
        except Exception as e:
            err_msg = str(e)[:200]
            failed_channels.append(f"{channel.alias}: {err_msg}")
            _append_event(paths.events_path, _event(run_id, "channel_failed", "WARN", f"Channel {channel.alias} failed: {err_msg}"))
        # Refresh connection every 30 channels to release native memory
        if (i + 1) % 30 == 0 and i + 1 < len(selected_channels):
            try:
                client.start()
            except Exception:
                client = CollectorTelegramClient(paths.session_path, config.api_id, config.api_hash)
                client.start()

    details_name = f"channel_results_{run_id}.json"
    details_path = paths.channel_results_dir / details_name
    _write_json(details_path, channel_results)
    _write_json(paths.manifest_path, _manifest(run_id, details_name))
    _write_json(paths.latest_path, _latest(run_id, details_name, channel_results, total_messages))
    _write_json(paths.status_path, _status(run_id))
    _append_event(paths.events_path, _event(run_id, "output_published", "INFO", f"Captured {total_messages} messages across {len(channel_results)} channels", details_ref=f"outputs/channel_results/{details_name}"))
    if failed_channels:
        _append_event(paths.events_path, _event(run_id, "channels_failed", "WARN", f"{len(failed_channels)} channels failed: {', '.join(failed_channels[:10])}"))
    _append_event(paths.events_path, _event(run_id, "run_succeeded", "INFO", "Telegram batch collection succeeded", state_after="healthy"))

    return {
        "module_id": "collector_telegram",
        "run_id": run_id,
        "channels": [channel.alias for channel in selected_channels],
        "messages_total": total_messages,
        "channels_succeeded": len(channel_results),
        "channels_failed": len(failed_channels),
        "failed_list": failed_channels[:20],
        "channel_results_path": str(details_path),
        "status_path": str(paths.status_path),
    }


def status_as_text(module_dir: Path) -> str:
    config = load_config(module_dir)
    if not config.paths.status_path.exists():
        return "status.json not found"
    return config.paths.status_path.read_text(encoding="utf-8")


def _select_channels(config: CollectorConfig, channel_alias: str | None) -> list[ChannelConfig]:
    if channel_alias:
        for channel in config.channels:
            if channel.alias == channel_alias:
                return [channel]
        raise ValueError(f"Unknown channel alias: {channel_alias}")
    channels = enabled_channels(config)
    if not channels:
        raise ValueError("No enabled channels configured")
    return channels


def _retag_channel(message: RawMessage, alias: str) -> RawMessage:
    return RawMessage(
        message_id=message.message_id,
        channel=alias,
        raw_text=message.raw_text,
        sender=message.sender,
        timestamp=message.timestamp,
    )


def _dedupe_messages(messages: list[RawMessage]) -> list[RawMessage]:
    deduped: list[RawMessage] = []
    seen: set[str] = set()
    for message in messages:
        key = f"{message.channel}:{message.message_id}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(message)
    return deduped


def _raw_message_dict(message: RawMessage) -> dict[str, Any]:
    return {
        "schema": "telegram_raw_message.v1",
        "source_kind": "live_capture",
        "message_id": message.message_id,
        "channel_alias": message.channel,
        "raw_text": message.raw_text,
        "sender": message.sender,
        "timestamp_utc": message.timestamp,
        "has_image": False,
    }


def _ensure_dirs(paths) -> None:
    for path in (paths.outputs_dir, paths.raw_dir, paths.channel_results_dir, paths.logs_dir, paths.runtime_dir):
        path.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    os.replace(tmp, path)


def _append_event(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _manifest(run_id: str, details_name: str) -> dict[str, Any]:
    return {
        "contract_version": "v1",
        "module_id": "collector_telegram",
        "provider_id": "telegram",
        "run_id": run_id,
        "generated_at": _utc_now_iso(),
        "artifacts": {
            "manifest": "outputs/manifest.json",
            "status": "outputs/status.json",
            "latest": "outputs/latest.json",
            "events": "outputs/events.jsonl",
            "errors": "outputs/errors.jsonl",
            "raw_messages_dir": "outputs/raw",
            "channel_results": f"outputs/channel_results/{details_name}",
        },
        "normalized_contract": {
            "schema_version": "v1.0",
            "entity_type": "telegram_channel_results",
        },
        "compatibility_targets": ["opt-trading", "localcms"],
        "notes": "Telegram read-only batch channel capture",
    }


def _latest(run_id: str, details_name: str, channel_results: list[dict[str, Any]], total_messages: int) -> dict[str, Any]:
    return {
        "contract_version": "v1",
        "module_id": "collector_telegram",
        "provider_id": "telegram",
        "run_id": run_id,
        "generated_at": _utc_now_iso(),
        "schema_version": "v1.0",
        "data_ref": f"outputs/channel_results/{details_name}",
        "record_count": len(channel_results),
        "summary": {
            "entity_type": "telegram_channel_results",
            "total_messages": total_messages,
            "channels": [item["channel_alias"] for item in channel_results],
        },
    }


def _status(run_id: str) -> dict[str, Any]:
    now = _utc_now_iso()
    return {
        "contract_version": "v1",
        "module_id": "collector_telegram",
        "provider_id": "telegram",
        "run_id": run_id,
        "generated_at": now,
        "state": "healthy",
        "freshness_state": "fresh",
        "last_event_at": now,
        "last_success_run_id": run_id,
        "last_success_at": now,
        "last_failure_run_id": None,
        "last_failure_at": None,
        "active_run_id": None,
        "last_error_code": None,
        "retryable": None,
        "retry_after": None,
        "message": "run succeeded",
    }


def _event(run_id: str, event_type: str, level: str, message: str, **extra: Any) -> dict[str, Any]:
    payload = {
        "contract_version": "v1",
        "module_id": "collector_telegram",
        "provider_id": "telegram",
        "run_id": run_id,
        "generated_at": _utc_now_iso(),
        "event_id": uuid.uuid4().hex,
        "event_at": _utc_now_iso(),
        "event_type": event_type,
        "level": level,
        "message": message,
    }
    payload.update(extra)
    return payload


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"-{uuid.uuid4().hex[:8]}"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
