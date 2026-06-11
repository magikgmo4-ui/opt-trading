---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_COLLECTOR_IMPLEMENTATION
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: collector_implementation
status: patch_ready_not_applied
created_at: 2026-06-11
---

# 50_COLLECTOR_IMPLEMENTATION

## Scope

This implementation patch creates a fixture-first collector for the
`@trademachineoff` pilot.

It does not call YouTube directly. The collector receives an injected client and
writes canonical artifacts under `outputs/youtube/`.

## Runtime contract

```text
registry/youtube_sources.jsonl
modules/youtube_video_ingestion/**
tests/fixtures/youtube_video_ingestion/trademachineoff_seed.json
tests/youtube_video_ingestion/test_trademachineoff_collector.py
```

## Artifacts written by run_trademachineoff_pilot

```text
outputs/youtube/raw_metadata/<video_id>.json
outputs/youtube/ocr/<video_id>.jsonl
outputs/youtube/parser_input/<video_id>.json
outputs/youtube/parsed/<video_id>.json
```

## Safety

- The test client is JSON fixture backed.
- No network call is made by default.
- The parser preserves `unknown` and `null` instead of inventing values.
- Entry, stop loss and take profits are extracted only from explicit evidence.

