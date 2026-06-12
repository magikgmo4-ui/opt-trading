---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_LAYER_01_VISION_LAYER_V1
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_LAYER_01
doc_type: implementation_spec
status: draft_reference
created_at: 2026-06-11
---

# 10_VISION_LAYER_V1

## Input

```json
{
  "video_id": "...",
  "screen_text": "...",
  "ocr_segments": []
}
```

## Output

```json
{
  "video_id": "...",
  "screen_text": "...",
  "symbols_detected": [],
  "directions_detected": [],
  "prices_detected": [],
  "timeframes_detected": [],
  "indicators_detected": [],
  "chart_detected": false,
  "chart_evidence": [],
  "confidence": 0.0
}
```

## V1 rules

- OCR text is deduplicated line by line.
- Symbol aliases follow the parent parser profile.
- Price roles are limited to explicit labels: `entry`, `buy above`, `sell below`, `SL`, `stop loss`, `TP`, `target`.
- Chart detection is heuristic only: chart terms, symbol+price overlay, or indicator overlay.
- V1 does not infer missing entry/SL/TP.

## V2 candidates

```text
vision model
chart understanding
bounding boxes
overlay layout confidence
```
