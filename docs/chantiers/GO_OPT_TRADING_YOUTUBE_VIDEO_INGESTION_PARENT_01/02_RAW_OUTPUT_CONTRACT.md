---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_RAW_OUTPUT_CONTRACT
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: raw_output_contract
status: reference
created_at: 2026-06-06
surface: youtube_video_ingestion
---

# 02_RAW_OUTPUT_CONTRACT

## Objectif

Définir ce qui doit être conservé avant toute interprétation ou parsing.

Le raw output est la source de vérité du chantier. Le parser est seulement une vue dérivée.

## Arborescence cible

```text
outputs/youtube/
  raw_metadata/
  subtitles/
  audio/
  transcripts/
  frames/
  ocr/
  parser_inputs/
  parsed/
  audit/
```

## Artefacts par vidéo

```text
<video_id>.metadata.json
<video_id>.subtitles.vtt | .srt
<video_id>.audio.mp3 | .wav
<video_id>.transcript.txt
<video_id>.frames/*.jpg
<video_id>.ocr.jsonl
<video_id>.parser_input.json
<video_id>.parsed.json
<video_id>.audit.json
```

## Contrat metadata

```json
{
  "source_type": "youtube_video",
  "channel_handle": "@trademachineoff",
  "video_id": "string",
  "url": "string",
  "title": "string",
  "description": "string|null",
  "published_at": "string|null",
  "duration_seconds": 0,
  "is_short": true,
  "tags": [],
  "view_count": null,
  "like_count": null,
  "collector": "yt-dlp",
  "collected_at": "ISO-8601"
}
```

## Contrat parser input

```json
{
  "video_id": "string",
  "url": "string",
  "title": "string",
  "description": "string|null",
  "spoken_transcript": "string|null",
  "screen_text": "string|null",
  "metadata": {},
  "raw_artifact_paths": {}
}
```

## Contrat parser output

```json
{
  "video_id": "string",
  "source_id": "youtube_trademachineoff",
  "parser_profile": "youtube_trading_short_v1",
  "assets": [],
  "market_type": "unknown",
  "direction": "unknown",
  "entry": null,
  "stop_loss": null,
  "take_profits": [],
  "timeframe": null,
  "indicators": [],
  "pattern": null,
  "strategy_rules": [],
  "risk_rules": [],
  "confidence": 0.0,
  "missing_fields": [],
  "raw_evidence": []
}
```

## Règles de qualité

- Ne jamais écraser un raw artifact sans versionner ou journaliser.
- Ne jamais remplir un champ par hypothèse non prouvée.
- Utiliser `null` si absent et `unknown` si ambigu.
- Ajouter `raw_evidence` pour chaque extraction importante.
- Garder transcript et OCR séparés.

## Critère de réussite

Une vidéo est exploitable si :

```text
metadata présente
+ transcript ou raison d'absence
+ OCR ou raison d'absence
+ parser_output JSON valide
+ audit JSON présent
```