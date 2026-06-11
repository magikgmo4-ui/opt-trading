from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .collector import run_trademachineoff_pilot
from .yt_dlp_runner import YtDlpPilotClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="youtube_video_ingestion")
    parser.add_argument("--root", default=".", help="Repository root where registry/ and outputs/ live")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run-trademachineoff", help="Run controlled @trademachineoff yt-dlp pilot")
    run_parser.add_argument("--urls-file", required=True, help="Text file with one YouTube URL per line")
    run_parser.add_argument("--limit", type=int, default=20)
    run_parser.add_argument("--audio-fallback", action="store_true", help="Use yt-dlp audio extraction and whisper if subtitles are absent")
    run_parser.add_argument("--whisper-model", default="small")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    try:
        if args.command == "run-trademachineoff":
            urls = _read_urls(Path(args.urls_file))
            client = YtDlpPilotClient(
                urls=urls,
                work_dir=root / "outputs" / "youtube",
                audio_fallback=args.audio_fallback,
                whisper_model=args.whisper_model,
            )
            result = run_trademachineoff_pilot(root, client=client, limit=args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    parser.print_help()
    return 1


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
