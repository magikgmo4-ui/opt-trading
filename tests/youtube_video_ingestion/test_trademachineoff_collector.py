from __future__ import annotations

import json
from pathlib import Path

from modules.youtube_video_ingestion import (
    SeedJsonClient,
    ensure_trademachineoff_source,
    load_youtube_sources,
    parse_youtube_trading_short,
    run_trademachineoff_pilot,
)


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
    ocr_lines = (tmp_path / "outputs" / "youtube" / "ocr" / "tm_xau_001.jsonl").read_text(encoding="utf-8").splitlines()

    assert raw["channel_handle"] == "@trademachineoff"
    assert raw["raw_collected_at"] == "2026-06-11T00:00:00Z"
    assert parser_input["parser_profile"] == "youtube_trading_short_v1"
    assert parser_input["subtitle_source"] == "manual"
    assert len(ocr_lines) == 2
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


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
