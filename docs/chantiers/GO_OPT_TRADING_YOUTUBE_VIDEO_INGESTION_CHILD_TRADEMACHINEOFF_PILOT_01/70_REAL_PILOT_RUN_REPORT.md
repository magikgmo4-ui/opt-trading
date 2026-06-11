---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_REAL_PILOT_RUN_REPORT
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: real_pilot_run_report
status: draft
created_at: 2026-06-11
---

# 70_REAL_PILOT_RUN_REPORT

## Local run summary

The first controlled local run collected 5 Shorts from `@trademachineoff`.

```text
videos_requested: 5
videos_collected: 5
setup_complete: 0
context_only: 2
reject_noise: 3
confidence_range: 0.1-0.3
```

## Findings

- Metadata and subtitle collection work in a bounded local pilot.
- The first CLI surface was incomplete for operator use.
- Default subtitles should use `en`; adding `fr` triggered HTTP 429 in local testing.
- Subtitle failures must not fail the whole batch.
- Audio/subtitles are insufficient for visual trading Shorts.
- OCR integration is required before source expansion.

## Hardening target

```text
CLI source/output flags
subtitle-lang default en
non-fatal subtitle errors
OCR adapter contract
parsed JSONL preserved
outputs/youtube not committed
```

## Operator note

PowerShell treats `@name` as syntax unless quoted. Use:

```bash
python -m modules.youtube_video_ingestion.cli --source '@trademachineoff' --limit 5 --output outputs/youtube/pilots/trademachineoff --subtitle-lang en
```

## Gate

Do not expand beyond `@trademachineoff` until a follow-up run shows at least
5 manually reviewable fixtures with raw evidence and no invented entry/SL/TP.
