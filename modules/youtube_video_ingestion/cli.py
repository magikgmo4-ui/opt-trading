from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .benchmark import run_vision_benchmark, write_vision_annotation_template
from .collector import run_trademachineoff_pilot
from .ocr import FfmpegFrameOcrRunner, FrameSamplingContract
from .yt_dlp_runner import YtDlpPilotClient, discover_urls_for_source


DEFAULT_SOURCE = "@trademachineoff"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="youtube_video_ingestion")
    parser.add_argument("--root", default=".", help="Repository root where registry/ lives")
    parser.add_argument("--source", default=None, help="Source handle to discover, currently @trademachineoff")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--output", default=None, help="Artifact output root. Defaults to <root>/outputs/youtube")
    parser.add_argument("--subtitle-lang", default="en", help="Comma-separated subtitle languages. Default: en")
    parser.add_argument("--parsed-jsonl", default=None, help="Parsed batch JSONL path or filename")
    parser.add_argument("--urls-file", default=None, help="Text file with one YouTube URL per line")
    parser.add_argument("--audio-fallback", action="store_true", help="Use yt-dlp audio extraction and whisper if subtitles are absent")
    parser.add_argument("--whisper-model", default="small")
    parser.add_argument("--enable-ocr", action="store_true", help="Download video and sample frames with ffmpeg for OCR")
    parser.add_argument("--frame-rate", type=float, default=1.0, help="Frame sampling rate in frames per second")

    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run-trademachineoff", help="Run controlled @trademachineoff yt-dlp pilot")
    run_parser.add_argument("--urls-file", required=True, help="Text file with one YouTube URL per line")
    run_parser.add_argument("--limit", type=int, default=None)
    run_parser.add_argument("--output", default=None)
    run_parser.add_argument("--subtitle-lang", default=None)
    run_parser.add_argument("--parsed-jsonl", default=None)
    run_parser.add_argument("--audio-fallback", action="store_true")
    run_parser.add_argument("--whisper-model", default=None)
    run_parser.add_argument("--enable-ocr", action="store_true")
    run_parser.add_argument("--frame-rate", type=float, default=None)

    template_parser = subparsers.add_parser("benchmark-vision-template", help="Write manual annotation template from parser_input artifacts")
    template_parser.add_argument("--parser-input-dir", required=True)
    template_parser.add_argument("--output", required=True)
    template_parser.add_argument("--limit", type=int, default=None)

    benchmark_parser = subparsers.add_parser("benchmark-vision", help="Score Vision Layer V1 against manual annotations")
    benchmark_parser.add_argument("--parser-input-dir", required=True)
    benchmark_parser.add_argument("--annotations", required=True)
    benchmark_parser.add_argument("--output", default="outputs/youtube/benchmark")
    benchmark_parser.add_argument("--fixtures-output", default=None)
    benchmark_parser.add_argument("--limit", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = _dispatch(args, parser)
        if result is None:
            return 1
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


def _dispatch(args: argparse.Namespace, parser: argparse.ArgumentParser) -> dict | None:
    root = Path(args.root).resolve()
    if args.command == "run-trademachineoff":
        urls_file = Path(args.urls_file)
        limit = args.limit if args.limit is not None else 20
        output = args.output
        subtitle_lang = args.subtitle_lang or "en"
        parsed_jsonl = args.parsed_jsonl
        audio_fallback = args.audio_fallback
        whisper_model = args.whisper_model or "small"
        enable_ocr = args.enable_ocr
        frame_rate = args.frame_rate if args.frame_rate is not None else 1.0
        urls = _read_urls(urls_file)
        return _run(root, urls, limit, output, subtitle_lang, parsed_jsonl, audio_fallback, whisper_model, enable_ocr, frame_rate)

    if args.command == "benchmark-vision-template":
        return write_vision_annotation_template(
            parser_input_dir=_resolve_root_path(root, args.parser_input_dir),
            output_path=_resolve_root_path(root, args.output),
            limit=args.limit,
        )

    if args.command == "benchmark-vision":
        return run_vision_benchmark(
            parser_input_dir=_resolve_root_path(root, args.parser_input_dir),
            annotations_path=_resolve_root_path(root, args.annotations),
            output_root=_resolve_root_path(root, args.output),
            limit=args.limit,
            fixtures_output_dir=_resolve_root_path(root, args.fixtures_output) if args.fixtures_output else None,
        )

    if args.source:
        source = _normalize_source(args.source)
        if source != DEFAULT_SOURCE:
            raise ValueError(f"Unsupported source for this pilot: {args.source}")
        output_root = _output_root(root, args.output)
        urls = discover_urls_for_source(source, args.limit, output_root)
        return _run(
            root,
            urls,
            args.limit,
            args.output,
            args.subtitle_lang,
            args.parsed_jsonl,
            args.audio_fallback,
            args.whisper_model,
            args.enable_ocr,
            args.frame_rate,
        )

    parser.print_help()
    return None


def _run(
    root: Path,
    urls: list[str],
    limit: int,
    output: str | None,
    subtitle_lang: str,
    parsed_jsonl: str | None,
    audio_fallback: bool,
    whisper_model: str,
    enable_ocr: bool,
    frame_rate: float,
) -> dict:
    output_root = _output_root(root, output)
    frame_sampling = FrameSamplingContract(fps=frame_rate)
    ocr_runner = FfmpegFrameOcrRunner() if enable_ocr else None
    client = YtDlpPilotClient(
        urls=urls,
        work_dir=output_root,
        audio_fallback=audio_fallback,
        whisper_model=whisper_model,
        subtitle_languages=_subtitle_languages(subtitle_lang),
        ocr_runner=ocr_runner,
        frame_sampling=frame_sampling,
    )
    return run_trademachineoff_pilot(
        root,
        client=client,
        limit=limit,
        output_root=output_root,
        parsed_jsonl_path=_parsed_jsonl_path(parsed_jsonl),
    )


def _output_root(root: Path, output: str | None) -> Path:
    if output:
        path = Path(output)
        return path if path.is_absolute() else (root / path)
    return root / "outputs" / "youtube"


def _resolve_root_path(root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (root / path)


def _subtitle_languages(raw: str) -> tuple[str, ...]:
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    if not values:
        raise ValueError("--subtitle-lang must include at least one language")
    return values


def _parsed_jsonl_path(raw: str | None) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else (Path.cwd() / path)


def _normalize_source(source: str) -> str:
    stripped = source.strip()
    return stripped if stripped.startswith("@") else f"@{stripped}"


def _read_urls(path: Path) -> list[str]:
    urls = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        urls.append(stripped)
    if not urls:
        raise ValueError(f"No URLs found in {path}")
    return urls


if __name__ == "__main__":
    raise SystemExit(main())
