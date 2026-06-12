from __future__ import annotations

import json
from pathlib import Path

from modules.youtube_video_ingestion import (
    SeedJsonClient,
    YtDlpPilotClient,
    analyze_vision_layer_v1,
    ensure_trademachineoff_source,
    load_youtube_sources,
    parse_youtube_trading_short,
    run_trademachineoff_pilot,
)
from modules.youtube_video_ingestion.cli import _normalize_source, _parsed_jsonl_path
from modules.youtube_video_ingestion.ocr import FfmpegFrameOcrRunner, FrameSamplingContract, OcrResult
from modules.youtube_video_ingestion.yt_dlp_runner import CommandResult
from modules.youtube_video_ingestion.yt_dlp_runner import discover_urls_for_source


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "youtube_video_ingestion" / "trademachineoff_seed.json"


def test_ensure_trademachineoff_source_is_idempotent(tmp_path: Path) -> None:
    registry_path = tmp_path / "registry" / "youtube_sources.jsonl"

    first = ensure_trademachineoff_source(registry_path)
    second = ensure_trademachineoff_source(registry_path)
    sources = load_youtube_sources(registry_path)

    assert first["handle"] == "@trademachineoff"
    assert second["priority"] == "P0_PILOT"
    assert len(sources) == 1
    assert sources[0]["parser_profile"] == "youtube_trading_short_v1"
    assert sources[0]["max_videos_per_run"] == 20


def test_run_trademachineoff_pilot_writes_canonical_artifacts(tmp_path: Path) -> None:
    result = run_trademachineoff_pilot(
        tmp_path,
        client=SeedJsonClient(FIXTURE),
        limit=20,
        collected_at="2026-06-11T00:00:00Z",
    )

    assert result["source_handle"] == "@trademachineoff"
    assert result["videos_collected"] == 2

    raw = _read_json(tmp_path / "outputs" / "youtube" / "raw_metadata" / "tm_xau_001.json")
    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "tm_xau_001.json")
    parsed = _read_json(tmp_path / "outputs" / "youtube" / "parsed" / "tm_xau_001.json")
    parsed_jsonl = (tmp_path / "outputs" / "youtube" / "parsed" / "trademachineoff_pilot.jsonl").read_text(encoding="utf-8").splitlines()
    ocr_lines = (tmp_path / "outputs" / "youtube" / "ocr" / "tm_xau_001.jsonl").read_text(encoding="utf-8").splitlines()

    assert raw["channel_handle"] == "@trademachineoff"
    assert raw["raw_collected_at"] == "2026-06-11T00:00:00Z"
    assert parser_input["parser_profile"] == "youtube_trading_short_v1"
    assert parser_input["subtitle_source"] == "manual"
    assert parser_input["subtitle_status"] == "unknown"
    assert parser_input["ocr_status"] == "not_run"
    assert parser_input["vision"]["symbols_detected"][0]["symbol"] == "XAUUSD"
    assert len(ocr_lines) == 2
    assert len(parsed_jsonl) == 2
    assert result["parsed_jsonl"] == "outputs/youtube/parsed/trademachineoff_pilot.jsonl"
    assert parsed["asset"] == "XAUUSD"
    assert parsed["direction"] == "long"
    assert parsed["entry"] == 2345.0
    assert parsed["stop_loss"] == 2335.0
    assert parsed["take_profits"] == [2360.0, 2375.0]
    assert parsed["classification"] == "candidate_complete"


def test_parser_does_not_invent_critical_trade_fields() -> None:
    parsed = parse_youtube_trading_short(
        {
            "video_id": "context_only",
            "title": "BTC liquidity lesson",
            "description": "",
            "spoken_transcript": "Do not long BTC here; this is a historical example.",
            "screen_text": "BTC liquidity lesson, no entry shown",
            "ocr_segments": [],
            "parser_profile": "youtube_trading_short_v1",
        }
    )

    assert parsed["asset"] == "BTCUSDT"
    assert parsed["direction"] == "unknown"
    assert parsed["entry"] is None
    assert parsed["stop_loss"] is None
    assert parsed["take_profits"] == []
    assert "entry" in parsed["missing_fields"]
    assert parsed["classification"] == "context_only"


def test_parser_marks_audio_ocr_direction_conflict() -> None:
    parsed = parse_youtube_trading_short(
        {
            "video_id": "conflict",
            "title": "Gold setup",
            "description": "",
            "spoken_transcript": "I want to buy gold from this zone.",
            "screen_text": "XAUUSD SELL BELOW 2330 SL 2340 TP 2310",
            "ocr_segments": [],
            "parser_profile": "youtube_trading_short_v1",
        }
    )

    assert parsed["asset"] == "XAUUSD"
    assert parsed["direction"] == "unknown"
    assert parsed["conflict_detected"] is True
    assert parsed["entry"] == 2330.0
    assert parsed["stop_loss"] == 2340.0
    assert parsed["take_profits"] == [2310.0]


def test_yt_dlp_client_reads_metadata_and_subtitles(tmp_path: Path) -> None:
    runner = FakeCommandRunner(tmp_path)
    client = YtDlpPilotClient(
        urls=["https://youtube.com/shorts/live_xau_001"],
        work_dir=tmp_path / "outputs" / "youtube",
        runner=runner,
    )

    result = run_trademachineoff_pilot(tmp_path, client=client, limit=1, collected_at="2026-06-11T00:00:00Z")

    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "live_xau_001.json")
    parsed = _read_json(tmp_path / "outputs" / "youtube" / "parsed" / "live_xau_001.json")

    assert result["videos_collected"] == 1
    assert parser_input["subtitle_source"] == "manual|auto"
    assert parser_input["subtitle_status"] == "ok"
    assert "XAUUSD BUY ABOVE 2345" in parser_input["spoken_transcript"]
    assert parsed["classification"] == "candidate_complete"
    assert any("--dump-single-json" in command for command in runner.commands)
    assert any("--write-subs" in command for command in runner.commands)
    assert not any("whisper" in command for command in runner.commands)


def test_yt_dlp_client_audio_fallback_uses_whisper_when_subtitles_absent(tmp_path: Path) -> None:
    runner = FakeCommandRunner(tmp_path, write_subtitles=False)
    client = YtDlpPilotClient(
        urls=["https://youtube.com/shorts/live_xau_001"],
        work_dir=tmp_path / "outputs" / "youtube",
        runner=runner,
        audio_fallback=True,
    )

    run_trademachineoff_pilot(tmp_path, client=client, limit=1, collected_at="2026-06-11T00:00:00Z")

    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "live_xau_001.json")
    parsed = _read_json(tmp_path / "outputs" / "youtube" / "parsed" / "live_xau_001.json")

    assert parser_input["subtitle_source"] == "whisper"
    assert parser_input["subtitle_status"] == "ok"
    assert "SELL BELOW 2330" in parser_input["spoken_transcript"]
    assert parsed["direction"] == "short"
    assert any("--extract-audio" in command for command in runner.commands)
    assert any(command.startswith("whisper ") for command in runner.commands)


def test_subtitle_failure_is_non_fatal_and_recorded(tmp_path: Path) -> None:
    runner = FakeCommandRunner(tmp_path, fail_subtitles=True)
    client = YtDlpPilotClient(
        urls=["https://youtube.com/shorts/live_xau_001"],
        work_dir=tmp_path / "outputs" / "youtube",
        runner=runner,
    )

    run_trademachineoff_pilot(tmp_path, client=client, limit=1, collected_at="2026-06-11T00:00:00Z")

    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "live_xau_001.json")
    parsed_jsonl = (tmp_path / "outputs" / "youtube" / "parsed" / "trademachineoff_pilot.jsonl").read_text(encoding="utf-8")

    assert parser_input["subtitle_status"] == "failed"
    assert "HTTP Error 429" in parser_input["subtitle_error_summary"]
    assert "live_xau_001" in parsed_jsonl


def test_fake_ocr_runner_populates_screen_text_and_segments(tmp_path: Path) -> None:
    runner = FakeCommandRunner(tmp_path, write_subtitles=False)
    client = YtDlpPilotClient(
        urls=["https://youtube.com/shorts/live_xau_001"],
        work_dir=tmp_path / "outputs" / "youtube",
        runner=runner,
        ocr_runner=FakeOcrRunner(),
        frame_sampling=FrameSamplingContract(fps=1, max_frames=2),
    )

    run_trademachineoff_pilot(tmp_path, client=client, limit=1, collected_at="2026-06-11T00:00:00Z")

    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "live_xau_001.json")
    parsed = _read_json(tmp_path / "outputs" / "youtube" / "parsed" / "live_xau_001.json")

    assert parser_input["subtitle_status"] == "missing"
    assert parser_input["ocr_status"] == "ok"
    assert parser_input["screen_text"] == "XAUUSD BUY ABOVE 2345 SL 2335 TP 2360"
    assert parser_input["frame_sampling_rate"] == "1fps"
    assert len(parser_input["ocr_segments"]) == 1
    assert parser_input["vision"]["chart_detected"] is True
    assert parser_input["vision"]["prices_detected"][0]["role"] == "entry"
    assert parsed["classification"] == "candidate_complete"


def test_discover_urls_for_source_uses_flat_playlist(tmp_path: Path) -> None:
    runner = FakeDiscoveryRunner()

    urls = discover_urls_for_source("@trademachineoff", 2, tmp_path, runner=runner)

    assert urls == [
        "https://www.youtube.com/shorts/a",
        "https://www.youtube.com/shorts/b",
    ]
    assert "--flat-playlist" in runner.commands[0]
    assert "--playlist-end 2" in runner.commands[0]


def test_parsed_jsonl_relative_path_resolves_from_cwd(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    parsed_path = _parsed_jsonl_path("outputs/youtube/parsed/custom.jsonl")

    assert parsed_path == tmp_path / "outputs" / "youtube" / "parsed" / "custom.jsonl"


def test_parsed_jsonl_absolute_path_is_used_as_is(tmp_path: Path) -> None:
    absolute = tmp_path / "custom" / "parsed.jsonl"

    parsed_path = _parsed_jsonl_path(str(absolute))

    assert parsed_path == absolute


def test_source_handle_keeps_at_prefix() -> None:
    assert _normalize_source("@trademachineoff") == "@trademachineoff"
    assert _normalize_source("trademachineoff") == "@trademachineoff"


def test_ocr_disabled_by_default_uses_noop(tmp_path: Path) -> None:
    runner = FakeCommandRunner(tmp_path, write_subtitles=False)
    client = YtDlpPilotClient(
        urls=["https://youtube.com/shorts/live_xau_001"],
        work_dir=tmp_path / "outputs" / "youtube",
        runner=runner,
    )

    run_trademachineoff_pilot(tmp_path, client=client, limit=1, collected_at="2026-06-11T00:00:00Z")

    parser_input = _read_json(tmp_path / "outputs" / "youtube" / "parser_input" / "live_xau_001.json")
    assert parser_input["ocr_status"] == "skipped"
    assert not any(command.startswith("ffmpeg ") for command in runner.commands)


def test_ffmpeg_ocr_runner_samples_frames_without_ocr_command(tmp_path: Path) -> None:
    runner = FakeOcrCommandRunner(tmp_path)
    ocr = FfmpegFrameOcrRunner(runner=runner)

    result = ocr.extract(
        video_id="live_xau_001",
        metadata=_metadata_payload(),
        work_dir=tmp_path / "outputs" / "youtube",
        frame_sampling=FrameSamplingContract(fps=1, max_frames=2),
    )

    assert result.status == "frames_sampled"
    assert result.error_summary == "OCR command not configured"
    assert len(result.segments) == 2
    assert any(command.startswith("yt-dlp -f") for command in runner.commands)
    assert any(command.startswith("ffmpeg -y") for command in runner.commands)


def test_ffmpeg_ocr_runner_failure_is_non_fatal_result(tmp_path: Path) -> None:
    runner = FakeOcrCommandRunner(tmp_path, fail_ffmpeg=True)
    ocr = FfmpegFrameOcrRunner(runner=runner)

    result = ocr.extract(
        video_id="live_xau_001",
        metadata=_metadata_payload(),
        work_dir=tmp_path / "outputs" / "youtube",
        frame_sampling=FrameSamplingContract(fps=1),
    )

    assert result.status == "failed"
    assert "ffmpeg frame sampling failed" in result.error_summary


def test_vision_layer_v1_extracts_trading_overlay_fields() -> None:
    vision = analyze_vision_layer_v1(
        video_id="overlay",
        screen_text="XAUUSD BUY ABOVE 2345\nSL 2335 TP1 2360 TP2 2375\nM5 EMA liquidity",
        ocr_segments=[],
    )

    assert vision["screen_text"].startswith("XAUUSD BUY ABOVE 2345")
    assert vision["symbols_detected"] == [{"symbol": "XAUUSD", "market_type": "forex", "evidence": "XAUUSD"}]
    assert [item["role"] for item in vision["prices_detected"]] == ["entry", "stop_loss", "take_profit", "take_profit"]
    assert vision["timeframes_detected"][0]["timeframe"] == "M5"
    assert {item["indicator"] for item in vision["indicators_detected"]} >= {"EMA", "liquidity"}
    assert vision["chart_detected"] is True
    assert vision["confidence"] >= 0.8


def test_parser_consumes_structured_vision_when_screen_text_is_not_flattened() -> None:
    vision = analyze_vision_layer_v1(
        video_id="vision_only",
        screen_text="BTCUSDT SELL BELOW 64000 SL 65000 TP 62000 H1 RSI",
        ocr_segments=[],
    )
    parsed = parse_youtube_trading_short(
        {
            "video_id": "vision_only",
            "title": "Short setup",
            "description": "",
            "spoken_transcript": "",
            "screen_text": "",
            "ocr_segments": [],
            "vision": vision,
            "parser_profile": "youtube_trading_short_v1",
        }
    )

    assert parsed["asset"] == "BTCUSDT"
    assert parsed["direction"] == "short"
    assert parsed["entry"] == 64000.0
    assert parsed["stop_loss"] == 65000.0
    assert parsed["take_profits"] == [62000.0]
    assert parsed["timeframe"] == "H1"
    assert parsed["indicators"] == ["RSI"]
    assert parsed["classification"] == "candidate_complete"
    assert parsed["chart_detected"] is True
    assert parsed["vision_confidence"] >= 0.8


class FakeCommandRunner:
    def __init__(self, root: Path, *, write_subtitles: bool = True, fail_subtitles: bool = False) -> None:
        self.root = root
        self.write_subtitles = write_subtitles
        self.fail_subtitles = fail_subtitles
        self.commands: list[str] = []

    def run(self, args: list[str], cwd: Path | None = None) -> CommandResult:
        self.commands.append(" ".join(args))
        work_dir = cwd or self.root
        if "--dump-single-json" in args:
            return CommandResult(tuple(args), 0, json.dumps(_metadata_payload()), "")
        if "--write-subs" in args:
            if self.fail_subtitles:
                return CommandResult(tuple(args), 1, "", "ERROR: Unable to download video subtitles for 'fr': HTTP Error 429: Too Many Requests")
            if self.write_subtitles:
                subtitle_path = work_dir / "subtitles" / "live_xau_001.en.vtt"
                subtitle_path.parent.mkdir(parents=True, exist_ok=True)
                subtitle_path.write_text(
                    "WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nXAUUSD BUY ABOVE 2345\n"
                    "00:00:01.000 --> 00:00:02.000\nSL 2335 TP1 2360 TP2 2375\n",
                    encoding="utf-8",
                )
            return CommandResult(tuple(args), 0, "", "")
        if "--extract-audio" in args:
            audio_path = work_dir / "audio" / "live_xau_001.mp3"
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            audio_path.write_bytes(b"fake audio")
            return CommandResult(tuple(args), 0, "", "")
        if args and args[0] == "whisper":
            transcript_path = work_dir / "transcripts" / "live_xau_001.txt"
            transcript_path.parent.mkdir(parents=True, exist_ok=True)
            transcript_path.write_text("XAUUSD SELL BELOW 2330 SL 2340 TP 2310", encoding="utf-8")
            return CommandResult(tuple(args), 0, "", "")
        return CommandResult(tuple(args), 1, "", "unexpected command")


class FakeOcrCommandRunner:
    def __init__(self, root: Path, *, fail_ffmpeg: bool = False) -> None:
        self.root = root
        self.fail_ffmpeg = fail_ffmpeg
        self.commands: list[str] = []

    def run(self, args: list[str], cwd: Path | None = None) -> CommandResult:
        self.commands.append(" ".join(args))
        work_dir = cwd or self.root
        if args and args[0] == "yt-dlp":
            video_path = Path(args[args.index("-o") + 1])
            video_path.parent.mkdir(parents=True, exist_ok=True)
            video_path.write_bytes(b"fake video")
            return CommandResult(tuple(args), 0, "", "")
        if args and args[0] == "ffmpeg":
            if self.fail_ffmpeg:
                return CommandResult(tuple(args), 1, "", "ffmpeg Error: cannot decode input")
            pattern = Path(args[-1])
            pattern.parent.mkdir(parents=True, exist_ok=True)
            for index in range(1, 3):
                (pattern.parent / f"frame_{index:06d}.jpg").write_bytes(b"fake frame")
            return CommandResult(tuple(args), 0, "", "")
        return CommandResult(tuple(args), 1, "", "unexpected command")


class FakeOcrRunner:
    def extract(self, *, video_id, metadata, work_dir, frame_sampling) -> OcrResult:
        return OcrResult(
            text="XAUUSD BUY ABOVE 2345 SL 2335 TP 2360",
            segments=[
                {
                    "video_id": video_id,
                    "frame": "frame_000001.jpg",
                    "timestamp_sec": 1,
                    "text": "XAUUSD BUY ABOVE 2345 SL 2335 TP 2360",
                    "confidence": 0.9,
                }
            ],
            status="ok",
        )


class FakeDiscoveryRunner:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def run(self, args: list[str], cwd: Path | None = None) -> CommandResult:
        self.commands.append(" ".join(args))
        return CommandResult(
            tuple(args),
            0,
            "https://www.youtube.com/shorts/a\nhttps://www.youtube.com/shorts/b\nhttps://www.youtube.com/shorts/c\n",
            "",
        )


def _metadata_payload() -> dict:
    return {
        "id": "live_xau_001",
        "webpage_url": "https://youtube.com/shorts/live_xau_001",
        "title": "Gold setup",
        "description": "XAUUSD scalping setup",
        "duration": 34,
        "upload_date": "20260610",
        "view_count": 100,
        "like_count": 12,
        "tags": ["xauusd", "scalping"],
    }


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
