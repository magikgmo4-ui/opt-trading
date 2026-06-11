from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class FrameSamplingContract:
    fps: int = 1
    max_frames: int = 60
    image_format: str = "jpg"

    @property
    def label(self) -> str:
        return f"{self.fps}fps"


@dataclass(frozen=True)
class OcrResult:
    text: str = ""
    segments: list[dict[str, Any]] = field(default_factory=list)
    status: str = "not_run"
    error_summary: str | None = None


class OcrRunner(Protocol):
    def extract(
        self,
        *,
        video_id: str,
        metadata: dict[str, Any],
        work_dir: Path,
        frame_sampling: FrameSamplingContract,
    ) -> OcrResult:
        """Return OCR text and segments for a video without requiring a hard dependency."""


class NoopOcrRunner:
    def extract(
        self,
        *,
        video_id: str,
        metadata: dict[str, Any],
        work_dir: Path,
        frame_sampling: FrameSamplingContract,
    ) -> OcrResult:
        return OcrResult(status="skipped", error_summary="OCR runner not configured")
