from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import parse_qs, urlparse

from .parser import PARSER_PROFILE, parse_youtube_trading_short
from .registry import DEFAULT_TRADEMACHINEOFF_SOURCE, ensure_trademachineoff_source


class YouTubePilotClient(Protocol):
    def list_videos(self, source: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        """Return raw candidate videos for the pilot source."""


class SeedJsonClient:
    """Fixture-backed client used for dry-run and tests."""

    def __init__(self, seed_path: Path) -> None:
        self.seed_path = seed_path

    def list_videos(self, source: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        payload = json.loads(self.seed_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Seed payload must be a JSON array")
        return [dict(item) for item in payload[:limit]]


def run_trademachineoff_pilot(
    root: Path,
    *,
    client: YouTubePilotClient,
    limit: int = 20,
    collected_at: str | None = None,
    output_root: Path | None = None,
    parsed_jsonl_path: Path | None = None,
) -> dict[str, Any]:
    """Collect a bounded @trademachineoff pilot batch into canonical artifacts.

    The function is network-neutral: callers must inject a client. Tests use
    SeedJsonClient; a future live adapter can wrap yt-dlp without changing this
    artifact-writing contract.
    """

    if limit <= 0:
        raise ValueError("limit must be positive")

    root = root.resolve()
    source_path = root / "registry" / "youtube_sources.jsonl"
    source = ensure_trademachineoff_source(source_path)
    max_videos = int(source.get("max_videos_per_run") or DEFAULT_TRADEMACHINEOFF_SOURCE["max_videos_per_run"])
    effective_limit = min(limit, max_videos)
    videos = client.list_videos(source, effective_limit)
    run_collected_at = collected_at or _now_z()

    output_root = (output_root or (root / "outputs" / "youtube")).resolve()
    raw_dir = output_root / "raw_metadata"
    ocr_dir = output_root / "ocr"
    parser_input_dir = output_root / "parser_input"
    parsed_dir = output_root / "parsed"
    for directory in (raw_dir, ocr_dir, parser_input_dir, parsed_dir):
        directory.mkdir(parents=True, exist_ok=True)

    written: list[dict[str, str]] = []
    parsed_rows: list[dict[str, Any]] = []
    for raw_video in videos:
        video = dict(raw_video)
        video_id = _coerce_video_id(video)
        video["video_id"] = video_id
        raw_metadata = _raw_metadata(video, source, run_collected_at)
        parser_input = _parser_input(video, source)
        parsed = parse_youtube_trading_short(parser_input)

        raw_path = raw_dir / f"{video_id}.json"
        ocr_path = ocr_dir / f"{video_id}.jsonl"
        parser_input_path = parser_input_dir / f"{video_id}.json"
        parsed_path = parsed_dir / f"{video_id}.json"

        _atomic_write_json(raw_path, raw_metadata)
        _write_ocr_jsonl(ocr_path, video_id, parser_input["ocr_segments"])
        _atomic_write_json(parser_input_path, parser_input)
        _atomic_write_json(parsed_path, parsed)
        parsed_rows.append(parsed)
        written.append(
            {
                "video_id": video_id,
                "raw_metadata": _repo_rel(root, raw_path),
                "ocr": _repo_rel(root, ocr_path),
                "parser_input": _repo_rel(root, parser_input_path),
                "parsed": _repo_rel(root, parsed_path),
            }
        )

    if parsed_jsonl_path is None:
        parsed_jsonl_path = parsed_dir / "trademachineoff_pilot.jsonl"
    elif not parsed_jsonl_path.is_absolute():
        parsed_jsonl_path = parsed_dir / parsed_jsonl_path
    _write_jsonl(parsed_jsonl_path, parsed_rows)

    return {
        "source_handle": source["handle"],
        "parser_profile": PARSER_PROFILE,
        "videos_requested": limit,
        "videos_collected": len(written),
        "max_videos_per_run": max_videos,
        "parsed_jsonl": _repo_rel(root, parsed_jsonl_path),
        "artifacts": written,
    }


def _raw_metadata(video: dict[str, Any], source: dict[str, Any], collected_at: str) -> dict[str, Any]:
    return {
        "source_type": "youtube_video",
        "channel_handle": source["handle"],
        "video_id": video["video_id"],
        "url": _string_or_none(video.get("url")),
        "title": _string_or_empty(video.get("title")),
        "description": _string_or_empty(video.get("description")),
        "duration_seconds": _optional_int(video.get("duration_seconds")),
        "published_at": _string_or_none(video.get("published_at")),
        "view_count": _optional_int(video.get("view_count")),
        "like_count": _optional_int(video.get("like_count")),
        "tags": _string_list(video.get("tags")),
        "is_short": _bool_or_default(video.get("is_short"), True),
        "raw_collected_at": collected_at,
        "selection_reason": _string_or_none(video.get("selection_reason")),
    }


def _parser_input(video: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    ocr_segments = _normalize_ocr_segments(video.get("ocr_segments"), video["video_id"])
    screen_text = _string_or_empty(video.get("screen_text"))
    if not screen_text and ocr_segments:
        screen_text = "\n".join(segment["text"] for segment in ocr_segments if segment["text"])
    return {
        "video_id": video["video_id"],
        "url": _string_or_none(video.get("url")),
        "title": _string_or_empty(video.get("title")),
        "description": _string_or_empty(video.get("description")),
        "spoken_transcript": _string_or_empty(video.get("spoken_transcript") or video.get("transcript")),
        "screen_text": screen_text,
        "ocr_segments": ocr_segments,
        "subtitle_source": _string_or_empty(video.get("subtitle_source") or "none"),
        "subtitle_status": _string_or_empty(video.get("subtitle_status") or "unknown"),
        "subtitle_error_summary": _string_or_none(video.get("subtitle_error_summary")),
        "frame_sampling_rate": _string_or_empty(video.get("frame_sampling_rate") or "1fps"),
        "ocr_status": _string_or_empty(video.get("ocr_status") or "not_run"),
        "ocr_error_summary": _string_or_none(video.get("ocr_error_summary")),
        "parser_profile": source.get("parser_profile") or PARSER_PROFILE,
    }


def _normalize_ocr_segments(value: Any, video_id: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("ocr_segments must be a list when present")
    segments: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ValueError("ocr_segments items must be JSON objects")
        frame = _string_or_empty(item.get("frame")) or f"frame_{index:06d}.jpg"
        segments.append(
            {
                "video_id": _string_or_empty(item.get("video_id")) or video_id,
                "frame": frame,
                "timestamp_sec": _optional_int(item.get("timestamp_sec")) if item.get("timestamp_sec") is not None else index,
                "text": _string_or_empty(item.get("text")),
                "confidence": _optional_float(item.get("confidence")),
            }
        )
    return segments


def _write_ocr_jsonl(path: Path, video_id: str, segments: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        temp_path = Path(handle.name)
        wrote = False
        for segment in segments:
            payload = dict(segment)
            payload.setdefault("video_id", video_id)
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=False) + "\n")
            wrote = True
        if not wrote:
            handle.write("")
    os.replace(temp_path, path)


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        temp_path = Path(handle.name)
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")
    os.replace(temp_path, path)


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _coerce_video_id(video: dict[str, Any]) -> str:
    explicit = _string_or_empty(video.get("video_id"))
    if explicit:
        return _safe_video_id(explicit)
    url = _string_or_empty(video.get("url"))
    parsed = urlparse(url)
    query_id = parse_qs(parsed.query).get("v", [""])[0]
    if query_id:
        return _safe_video_id(query_id)
    match = re.search(r"/(?:shorts|watch)/([A-Za-z0-9_-]{6,})", parsed.path)
    if match:
        return _safe_video_id(match.group(1))
    return f"yt_{hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]}"


def _safe_video_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    if not cleaned:
        raise ValueError("video_id cannot be empty")
    return cleaned


def _string_or_empty(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _string_or_none(value: Any) -> str | None:
    text = _string_or_empty(value)
    return text or None


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _optional_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _bool_or_default(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _repo_rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _now_z() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
