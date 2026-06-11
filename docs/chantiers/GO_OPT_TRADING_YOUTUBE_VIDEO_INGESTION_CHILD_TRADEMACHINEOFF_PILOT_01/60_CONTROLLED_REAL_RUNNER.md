---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_CONTROLLED_REAL_RUNNER
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: controlled_real_runner
status: patch_ready_not_applied
created_at: 2026-06-11
---

# 60_CONTROLLED_REAL_RUNNER

## Scope

This patch adds a controlled real runner for the `@trademachineoff` pilot.

The runner is explicit and bounded:

```text
yt-dlp metadata
-> yt-dlp subtitles
-> optional yt-dlp audio + whisper fallback
-> collector raw artifacts
-> parser input
-> parsed JSON + parsed JSONL
```

## Safety

- No command runs at import time.
- The real runner is only used when a caller instantiates `YtDlpPilotClient`.
- Tests inject a fake command runner; no network calls are made in tests.
- Audio fallback is opt-in with `--audio-fallback`.
- OCR remains out of this patch; `ocr_segments` stays empty for real runner output.

## Manual command

```bash
python -m modules.youtube_video_ingestion.cli \
  --root . \
  run-trademachineoff \
  --urls-file outputs/youtube/trademachineoff_urls.txt \
  --limit 20
```

With audio fallback:

```bash
python -m modules.youtube_video_ingestion.cli \
  --root . \
  run-trademachineoff \
  --urls-file outputs/youtube/trademachineoff_urls.txt \
  --limit 20 \
  --audio-fallback
```
