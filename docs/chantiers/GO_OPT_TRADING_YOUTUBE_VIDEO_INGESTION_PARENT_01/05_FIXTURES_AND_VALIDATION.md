---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_FIXTURES_AND_VALIDATION
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: fixtures_validation
status: reference
created_at: 2026-06-06
surface: youtube_video_ingestion
---

# 05_FIXTURES_AND_VALIDATION

## Objectif

Définir comment valider le pipeline avant extension à plusieurs chaînes.

Aucun batch large ne doit être lancé avant validation d'un échantillon pilote.

## Échantillon pilote

```text
source: @trademachineoff
sample_size: 10 à 20 Shorts
manual_annotation: 5 vidéos minimum
```

## Fixtures attendues

```text
tests/fixtures/youtube_parser/trademachineoff/video_001.input.json
tests/fixtures/youtube_parser/trademachineoff/video_001.expected.json
tests/fixtures/youtube_parser/trademachineoff/video_001.audit.json
```

## Input fixture

```json
{
  "video_id": "fixture_video_001",
  "url": "https://youtube.com/shorts/...",
  "title": "Example trading short",
  "spoken_transcript": "...",
  "screen_text": "...",
  "metadata": {}
}
```

## Expected fixture

```json
{
  "assets": ["XAUUSD"],
  "direction": "long",
  "entry": null,
  "stop_loss": null,
  "take_profits": [],
  "timeframe": "M5",
  "indicators": ["EMA"],
  "confidence_min": 0.5,
  "must_have_missing_fields": ["entry", "stop_loss", "take_profits"]
}
```

## Tests minimaux

- JSON valide.
- Aucun champ obligatoire absent.
- `unknown` ou `null` utilisé quand incertain.
- `confidence` dans `[0.0, 1.0]`.
- `raw_evidence` présent pour chaque champ critique extrait.
- Le parser ne transforme pas une vidéo éducative en signal réel sans preuve.

## États de validation

```text
RAW_COLLECTED
TRANSCRIPT_READY
OCR_READY
PARSER_READY
MANUAL_REVIEWED
FIXTURE_LOCKED
REJECTED_NO_SIGNAL
REJECTED_LOW_QUALITY
```

## Gate avant extension

Extension à d'autres chaînes seulement si :

```text
5 fixtures manuelles verrouillées
+ parser JSON stable
+ erreurs connues documentées
+ raw output complet
+ au moins 70% des vidéos pilotes classées correctement comme signal / non-signal
```

## Prochain child GO

```text
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
```

Cible : collecter un échantillon, produire fixtures, ajuster parser profile.