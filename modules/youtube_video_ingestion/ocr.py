from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


DEFAULT_OCR_TIMEOUT_SECONDS = 10.0


@dataclass(frozen=True)
class FrameSamplingContract:
    fps: float = 1
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
    command: str | None = None


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
    def run(self, args: list[str], cwd: Path | None = None, timeout_seconds: float | None = None) -> Any:
        """Run an external command and return an object with returncode/stdout/stderr."""


@dataclass(frozen=True)
class OcrCommandResult:
    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


class SubprocessOcrCommandRunner:
    def run(self, args: list[str], cwd: Path | None = None, timeout_seconds: float | None = None) -> OcrCommandResult:
        try:
            completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            summary = stderr or f"command timed out after {timeout_seconds:g}s"
            return OcrCommandResult(tuple(args), 124, stdout, summary)
        return OcrCommandResult(tuple(args), completed.returncode, completed.stdout, completed.stderr)


class FfmpegFrameOcrRunner:
    """Sample video frames with yt-dlp + ffmpeg, with optional OCR command support."""

    def __init__(
        self,
        *,
        runner: OcrCommandRunner | None = None,
        ocr_command: str | None = None,
        ocr_timeout_seconds: float = DEFAULT_OCR_TIMEOUT_SECONDS,
    ) -> None:
        if runner is None:
            runner = SubprocessOcrCommandRunner()
        self.runner = runner
        self.ocr_command = ocr_command.strip() if ocr_command else None
        if self.ocr_command and "{image}" not in self.ocr_command:
            raise ValueError("ocr_command must include the {image} placeholder")
        self.ocr_timeout_seconds = ocr_timeout_seconds

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
            if status == "failed":
                return OcrResult(
                    text="\n".join(texts).strip(),
                    segments=segments,
                    status="failed",
                    error_summary=f"OCR command failed for {frame.name}: {error}",
                    command=self.ocr_command,
                )

        if self.ocr_command is None:
            return OcrResult(
                text="",
                segments=segments,
                status="frames_sampled",
                error_summary="OCR command not configured",
            )
        return OcrResult(text="\n".join(texts).strip(), segments=segments, status="ok", command=self.ocr_command)

    def _ocr_frame(self, frame: Path) -> tuple[str, str, str | None]:
        if self.ocr_command is None:
            return "", "skipped", None
        try:
            args = self._ocr_command_args(frame)
        except ValueError as exc:
            return "", "failed", str(exc)
        result = _run_with_timeout(self.runner, args, frame.parent, self.ocr_timeout_seconds)
        if getattr(result, "returncode", 1) != 0:
            return "", "failed", _summarize_error(getattr(result, "stderr", ""))
        return str(getattr(result, "stdout", "")).strip(), "ok", None

    def _ocr_command_args(self, frame: Path) -> list[str]:
        if self.ocr_command is None:
            return []
        try:
            args = shlex.split(self.ocr_command)
        except ValueError as exc:
            raise ValueError(f"invalid OCR command template: {exc}") from exc
        rendered = [arg.replace("{image}", str(frame)) for arg in args]
        if not rendered:
            raise ValueError("OCR command template produced no command")
        return rendered


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


def _run_with_timeout(
    runner: OcrCommandRunner,
    args: list[str],
    cwd: Path,
    timeout_seconds: float,
) -> Any:
    try:
        return runner.run(args, cwd=cwd, timeout_seconds=timeout_seconds)
    except TypeError:
        return runner.run(args, cwd=cwd)
