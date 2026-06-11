from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from .ocr import FrameSamplingContract, NoopOcrRunner, OcrRunner


@dataclass(frozen=True)
class CommandResult:
    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


class CommandRunner(Protocol):
    def run(self, args: list[str], cwd: Path | None = None) -> CommandResult:
        """Run an external command and return captured output."""


class SubprocessCommandRunner:
    def run(self, args: list[str], cwd: Path | None = None) -> CommandResult:
        completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
        return CommandResult(tuple(args), completed.returncode, completed.stdout, completed.stderr)


class YtDlpPilotClient:
    """Controlled yt-dlp adapter for the @trademachineoff pilot."""

    def __init__(
        self,
        *,
        urls: list[str],
        work_dir: Path,
        runner: CommandRunner | None = None,
        audio_fallback: bool = False,
        whisper_model: str = "small",
        subtitle_languages: tuple[str, ...] = ("en",),
        ocr_runner: OcrRunner | None = None,
        frame_sampling: FrameSamplingContract | None = None,
    ) -> None:
        if not urls:
            raise ValueError("urls must contain at least one URL")
        self.urls = urls
        self.work_dir = work_dir
        self.runner = runner or SubprocessCommandRunner()
        self.audio_fallback = audio_fallback
        self.whisper_model = whisper_model
        self.subtitle_languages = subtitle_languages
        self.ocr_runner = ocr_runner or NoopOcrRunner()
        self.frame_sampling = frame_sampling or FrameSamplingContract()

    def list_videos(self, source: dict[str, Any], limit: int) -> list[dict[str, Any]]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        self._ensure_dirs()
        videos: list[dict[str, Any]] = []
        for url in self.urls[:limit]:
            metadata = self._metadata(url)
            video_id = _safe_video_id(str(metadata.get("id") or ""))
            if not video_id:
                raise ValueError("yt-dlp metadata missing id")
            subtitle_text, subtitle_source, subtitle_status, subtitle_error = self._subtitles(url, video_id)
            if not subtitle_text and self.audio_fallback:
                subtitle_text, subtitle_source, subtitle_status, subtitle_error = self._audio_transcript(url, video_id)
            ocr = self.ocr_runner.extract(
                video_id=video_id,
                metadata=metadata,
                work_dir=self.work_dir,
                frame_sampling=self.frame_sampling,
            )
            videos.append(
                _video_from_metadata(
                    metadata,
                    url,
                    source,
                    subtitle_text,
                    subtitle_source,
                    subtitle_status,
                    subtitle_error,
                    ocr.text,
                    ocr.segments,
                    ocr.status,
                    ocr.error_summary,
                    self.frame_sampling.label,
                )
            )
        return videos

    def _metadata(self, url: str) -> dict[str, Any]:
        result = self._run_checked(["yt-dlp", "--dump-single-json", "--skip-download", url], stage="metadata")
        payload = json.loads(result.stdout)
        if not isinstance(payload, dict):
            raise ValueError("yt-dlp metadata output must be a JSON object")
        return payload

    def _subtitles(self, url: str, video_id: str) -> tuple[str, str, str, str | None]:
        result = self.runner.run(
            [
                "yt-dlp",
                "--write-subs",
                "--write-auto-subs",
                "--sub-lang",
                ",".join(self.subtitle_languages),
                "--sub-format",
                "vtt",
                "--skip-download",
                "-o",
                str(self.work_dir / "subtitles" / "%(id)s.%(ext)s"),
                url,
            ],
            cwd=self.work_dir,
        )
        subtitle_files = sorted((self.work_dir / "subtitles").glob(f"{video_id}*.vtt"))
        text = "\n".join(_vtt_to_text(path.read_text(encoding="utf-8")) for path in subtitle_files).strip()
        if result.returncode != 0:
            return text, "none", "failed", _summarize_error(result.stderr)
        return text, "manual|auto" if text else "none", "ok" if text else "missing", None

    def _audio_transcript(self, url: str, video_id: str) -> tuple[str, str, str, str | None]:
        audio_result = self.runner.run(
            [
                "yt-dlp",
                "--extract-audio",
                "--audio-format",
                "mp3",
                "-o",
                str(self.work_dir / "audio" / "%(id)s.%(ext)s"),
                url,
            ],
            cwd=self.work_dir,
        )
        if audio_result.returncode != 0:
            return "", "none", "failed", _summarize_error(audio_result.stderr)
        audio_files = sorted((self.work_dir / "audio").glob(f"{video_id}*.mp3"))
        if not audio_files:
            return "", "none", "missing", "audio file not produced"
        audio_path = audio_files[0]
        whisper_result = self.runner.run(
            [
                "whisper",
                str(audio_path),
                "--model",
                self.whisper_model,
                "--output_dir",
                str(self.work_dir / "transcripts"),
                "--output_format",
                "txt",
            ],
            cwd=self.work_dir,
        )
        if whisper_result.returncode != 0:
            return "", "none", "failed", _summarize_error(whisper_result.stderr)
        transcript_path = self.work_dir / "transcripts" / f"{audio_path.stem}.txt"
        if not transcript_path.exists():
            return "", "none", "missing", "whisper transcript file not produced"
        return transcript_path.read_text(encoding="utf-8").strip(), "whisper", "ok", None

    def _run_checked(self, args: list[str], *, stage: str) -> CommandResult:
        result = self.runner.run(args, cwd=self.work_dir)
        if result.returncode != 0:
            raise RuntimeError(f"{stage} command failed with code {result.returncode}: {_summarize_error(result.stderr)}")
        return result

    def _ensure_dirs(self) -> None:
        for name in ("subtitles", "audio", "transcripts", "frames"):
            (self.work_dir / name).mkdir(parents=True, exist_ok=True)


def discover_urls_for_source(
    source: str,
    limit: int,
    work_dir: Path,
    runner: CommandRunner | None = None,
) -> list[str]:
    normalized = source if source.startswith("@") else f"@{source}"
    if normalized != "@trademachineoff":
        raise ValueError(f"Unsupported source for this pilot: {source}")
    if limit <= 0:
        raise ValueError("limit must be positive")
    runner = runner or SubprocessCommandRunner()
    work_dir.mkdir(parents=True, exist_ok=True)
    result = runner.run(
        [
            "yt-dlp",
            "--flat-playlist",
            "--playlist-end",
            str(limit),
            "--print",
            "%(webpage_url)s",
            "https://www.youtube.com/@trademachineoff/shorts",
        ],
        cwd=work_dir,
    )
    if result.returncode != 0:
        raise RuntimeError(f"source discovery failed: {_summarize_error(result.stderr)}")
    urls = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not urls:
        raise RuntimeError("source discovery returned no URLs")
    return urls[:limit]


def _video_from_metadata(
    metadata: dict[str, Any],
    fallback_url: str,
    source: dict[str, Any],
    spoken_transcript: str,
    subtitle_source: str,
    subtitle_status: str,
    subtitle_error_summary: str | None,
    screen_text: str,
    ocr_segments: list[dict[str, Any]],
    ocr_status: str,
    ocr_error_summary: str | None,
    frame_sampling_rate: str,
) -> dict[str, Any]:
    video_id = _safe_video_id(str(metadata.get("id") or ""))
    return {
        "video_id": video_id,
        "url": _text(metadata.get("webpage_url")) or fallback_url,
        "title": _text(metadata.get("title")),
        "description": _text(metadata.get("description")),
        "duration_seconds": _optional_int(metadata.get("duration")),
        "published_at": _published_at(metadata),
        "view_count": _optional_int(metadata.get("view_count")),
        "like_count": _optional_int(metadata.get("like_count")),
        "tags": [str(tag) for tag in metadata.get("tags") or []],
        "is_short": _is_short(metadata),
        "selection_reason": f"controlled yt-dlp run for {source.get('handle', '@trademachineoff')}",
        "spoken_transcript": spoken_transcript,
        "screen_text": screen_text,
        "subtitle_source": subtitle_source,
        "subtitle_status": subtitle_status,
        "subtitle_error_summary": subtitle_error_summary,
        "ocr_segments": ocr_segments,
        "ocr_status": ocr_status,
        "ocr_error_summary": ocr_error_summary,
        "frame_sampling_rate": frame_sampling_rate,
    }


def _published_at(metadata: dict[str, Any]) -> str | None:
    timestamp = metadata.get("timestamp")
    if isinstance(timestamp, int):
        from datetime import UTC, datetime

        return datetime.fromtimestamp(timestamp, tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    upload_date = _text(metadata.get("upload_date"))
    if re.fullmatch(r"\d{8}", upload_date):
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}T00:00:00Z"
    return None


def _is_short(metadata: dict[str, Any]) -> bool:
    url = _text(metadata.get("webpage_url"))
    duration = _optional_int(metadata.get("duration"))
    if "/shorts/" in url:
        return True
    return duration is not None and duration <= 60


def _vtt_to_text(raw: str) -> str:
    lines = []
    seen: set[str] = set()
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "WEBVTT" or "-->" in stripped:
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        cleaned = re.sub(r"<[^>]+>", "", stripped).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            lines.append(cleaned)
    return "\n".join(lines)


def _summarize_error(stderr: str) -> str:
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    if not lines:
        return "unknown command error"
    for line in reversed(lines):
        if "ERROR:" in line or "HTTP Error" in line:
            return line[-300:]
    return lines[-1][-300:]


def _safe_video_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
