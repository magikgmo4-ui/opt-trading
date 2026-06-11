---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_RAW_OUTPUT_CONTRACT
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: raw_output_contract
status: draft_reference
created_at: 2026-06-06
---

# 02_RAW_OUTPUT_CONTRACT

## Objectif

Définir les artefacts bruts à conserver pour chaque vidéo avant parsing.

Le raw output doit permettre de refaire le parsing plus tard sans recollecter la vidéo.

## Structure cible

```text
outputs/youtube/
  raw_metadata/<video_id>.json
  subtitles/<video_id>.<lang>.vtt
  transcripts/<video_id>.txt
  frames/<video_id>/frame_000001.jpg
  ocr/<video_id>.jsonl
  parser_input/<video_id>.json
  parsed/<video_id>.json
```

## Métadonnées minimales

```json
{
  "source_type": "youtube_video",
  "channel_handle": "@trademachineoff",
  "video_id": "...",
  "url": "...",
  "title": "...",
  "description": "...",
  "duration_seconds": null,
  "published_at": null,
  "view_count": null,
  "like_count": null,
  "tags": [],
  "is_short": true,
  "raw_collected_at": "..."
}
```

## Parser input consolidé

```json
{
  "video_id": "...",
  "url": "...",
  "title": "...",
  "description": "...",
  "spoken_transcript": "...",
  "screen_text": "...",
  "ocr_segments": [],
  "subtitle_source": "manual|auto|whisper|none",
  "frame_sampling_rate": "1fps",
  "parser_profile": "youtube_trading_short_v1"
}
```

## Règles de conservation

- Ne jamais écraser le raw metadata original sans suffixe de version.
- Garder la source de la transcription.
- Garder les textes OCR par frame ou segment temporel.
- Ne pas inventer les champs absents.
- Le parser output est dérivé et peut être régénéré.
