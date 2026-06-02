from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ChannelConfig:
    alias: str
    source_ref: str
    enabled: bool
    categories: list[str]
    notes: str = ""


@dataclass(frozen=True)
class PathsConfig:
    module_dir: Path
    outputs_dir: Path
    raw_dir: Path
    channel_results_dir: Path
    logs_dir: Path
    runtime_dir: Path
    session_path: Path
    manifest_path: Path
    latest_path: Path
    status_path: Path
    events_path: Path
    errors_path: Path


@dataclass(frozen=True)
class CollectorConfig:
    api_id: int | None
    api_hash: str
    channels: list[ChannelConfig]
    paths: PathsConfig


def load_config(module_dir: Path) -> CollectorConfig:
    module_dir = module_dir.resolve()
    outputs_dir = module_dir / "outputs"
    paths = PathsConfig(
        module_dir=module_dir,
        outputs_dir=outputs_dir,
        raw_dir=outputs_dir / "raw",
        channel_results_dir=outputs_dir / "channel_results",
        logs_dir=module_dir / "logs",
        runtime_dir=module_dir / "runtime",
        session_path=Path(os.getenv("TELEGRAM_SESSION_PATH", str(module_dir / "runtime" / "telegram_session.session"))),
        manifest_path=outputs_dir / "manifest.json",
        latest_path=outputs_dir / "latest.json",
        status_path=outputs_dir / "status.json",
        events_path=outputs_dir / "events.jsonl",
        errors_path=outputs_dir / "errors.jsonl",
    )

    channels_path = module_dir / "config" / "channels.json"
    raw = json.loads(channels_path.read_text(encoding="utf-8"))
    channels = [
        ChannelConfig(
            alias=item["alias"],
            source_ref=item.get("source_ref") or item["alias"],
            enabled=bool(item.get("enabled", False)),
            categories=list(item.get("categories", [])),
            notes=item.get("notes", ""),
        )
        for item in raw.get("channels", [])
    ]

    api_id_raw = os.getenv("TELEGRAM_API_ID", "").strip()
    return CollectorConfig(
        api_id=int(api_id_raw) if api_id_raw else None,
        api_hash=os.getenv("TELEGRAM_API_HASH", "").strip(),
        channels=channels,
        paths=paths,
    )


def enabled_channels(config: CollectorConfig) -> list[ChannelConfig]:
    return [channel for channel in config.channels if channel.enabled]
