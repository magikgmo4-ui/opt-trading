from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_TRADEMACHINEOFF_SOURCE: dict[str, Any] = {
    "source_type": "youtube_channel",
    "handle": "@trademachineoff",
    "url": "https://youtube.com/@trademachineoff",
    "channel_id": None,
    "theme": "trading_short_form",
    "language_hint": "auto",
    "priority": "P0_PILOT",
    "video_scope": "shorts_first",
    "collection_mode": "latest_or_keyword",
    "keywords": ["gold", "xau", "btc", "nasdaq", "entry", "scalping", "strategy", "long", "short", "tp", "sl"],
    "max_videos_per_run": 20,
    "parser_profile": "youtube_trading_short_v1",
    "status": "candidate",
    "notes": "Source pilote initiale pour validation YouTube video ingestion.",
}


def load_youtube_sources(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    sources: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}:{line_no} must contain a JSON object")
        _validate_source(payload)
        sources.append(payload)
    return sources


def ensure_trademachineoff_source(path: Path) -> dict[str, Any]:
    sources = load_youtube_sources(path)
    selected = None
    for index, source in enumerate(sources):
        if source.get("handle") == DEFAULT_TRADEMACHINEOFF_SOURCE["handle"]:
            merged = dict(DEFAULT_TRADEMACHINEOFF_SOURCE)
            merged.update(source)
            sources[index] = merged
            selected = merged
            break
    if selected is None:
        selected = dict(DEFAULT_TRADEMACHINEOFF_SOURCE)
        sources.append(selected)
    _write_jsonl(path, sources)
    return selected


def _validate_source(source: dict[str, Any]) -> None:
    required = {
        "source_type",
        "handle",
        "url",
        "priority",
        "video_scope",
        "collection_mode",
        "keywords",
        "max_videos_per_run",
        "parser_profile",
        "status",
    }
    missing = sorted(key for key in required if key not in source)
    if missing:
        raise ValueError(f"youtube source missing required fields: {', '.join(missing)}")
    if source["source_type"] != "youtube_channel":
        raise ValueError("youtube source source_type must be youtube_channel")
    if not str(source["handle"]).startswith("@"):
        raise ValueError("youtube source handle must start with @")
    if source["parser_profile"] != "youtube_trading_short_v1":
        raise ValueError("youtube source parser_profile must be youtube_trading_short_v1")
    if not isinstance(source["keywords"], list):
        raise ValueError("youtube source keywords must be a list")
    if int(source["max_videos_per_run"]) <= 0:
        raise ValueError("youtube source max_videos_per_run must be positive")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        temp_path = Path(handle.name)
        for row in rows:
            _validate_source(row)
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    os.replace(temp_path, path)
