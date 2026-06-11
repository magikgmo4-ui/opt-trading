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
        return f"{self.fps:g}fps"


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


class OcrCommandRunner(Protocol):
    def run(self, args: list[str], cwd: Path | None = None) -> Any:
        """Run an external command and return an object with returncode/stdout/stderr."""


class FfmpegFrameOcrRunner:
    """Sample video frames with yt-dlp + ffmpeg, with optional OCR command support."""

    def __init__(
        self,
        *,
        runner: OcrCommandRunner | None = None,
        ocr_command: str | None = None,
    ) -> None:
        if runner is None:
            from .yt_dlp_runner import SubprocessCommandRunner

            runner = SubprocessCommandRunner()
        self.runner = runner
        self.ocr_command = ocr_command

    def extract(
        self,
        *,
        video_id: str,
        metadata: dict[str, Any],
        work_dir: Path,
        frame_sampling: FrameSamplingContract,
    ) -> OcrResult:
        url = str(metadata.get("webpage_url") or "").strip()
        if not url:
            return OcrResult(status="failed", error_summary="metadata missing webpage_url for OCR")
        frames_dir = work_dir / "frames" / video_id
        frames_dir.mkdir(parents=True, exist_ok=True)
        video_path = work_dir / "video" / f"{video_id}.mp4"
        video_path.parent.mkdir(parents=True, exist_ok=True)

        download = self.runner.run(
            [
                "yt-dlp",
                "-f",
                "mp4/best[height<=720]/best",
                "--merge-output-format",
                "mp4",
                "-o",
                str(video_path),
                url,
            ],
            cwd=work_dir,
        )
        if getattr(download, "returncode", 1) != 0:
            return OcrResult(status="failed", error_summary=f"video download failed: {_summarize_error(getattr(download, 'stderr', ''))}")

        frame_pattern = frames_dir / f"frame_%06d.{frame_sampling.image_format}"
        ffmpeg = self.runner.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video_path),
                "-vf",
                f"fps={frame_sampling.fps:g}",
                "-frames:v",
                str(frame_sampling.max_frames),
                str(frame_pattern),
            ],
            cwd=work_dir,
        )
        if getattr(ffmpeg, "returncode", 1) != 0:
            return OcrResult(status="failed", error_summary=f"ffmpeg frame sampling failed: {_summarize_error(getattr(ffmpeg, 'stderr', ''))}")

        frames = sorted(frames_dir.glob(f"*.{frame_sampling.image_format}"))
        if not frames:
            return OcrResult(status="failed", error_summary="ffmpeg produced no frames")

        segments = []
        texts = []
        for index, frame in enumerate(frames, start=1):
            text, status, error = self._ocr_frame(frame)
            if status == "failed":
                return OcrResult(status="failed", error_summary=error)
            if text:
                texts.append(text)
            segments.append(
                {
                    "video_id": video_id,
                    "frame": frame.name,
                    "timestamp_sec": round((index - 1) / frame_sampling.fps, 3) if frame_sampling.fps else index - 1,
                    "text": text,
                    "confidence": None,
                }
            )

        if self.ocr_command is None:
            return OcrResult(
                text="",
                segments=segments,
                status="frames_sampled",
                error_summary="OCR command not configured",
            )
        return OcrResult(text="\n".join(texts).strip(), segments=segments, status="ok")

    def _ocr_frame(self, frame: Path) -> tuple[str, str, str | None]:
        if self.ocr_command is None:
            return "", "skipped", None
        result = self.runner.run([self.ocr_command, str(frame), "stdout"], cwd=frame.parent)
        if getattr(result, "returncode", 1) != 0:
            return "", "failed", _summarize_error(getattr(result, "stderr", ""))
        return str(getattr(result, "stdout", "")).strip(), "ok", None


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


def _summarize_error(stderr: str) -> str:
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    if not lines:
        return "unknown command error"
    for line in reversed(lines):
        if "ERROR:" in line or "Error" in line:
            return line[-300:]
    return lines[-1][-300:]
