---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_FIXTURES_AND_VALIDATION
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: fixtures_validation_method
status: draft_reference
created_at: 2026-06-06
---

# 05_FIXTURES_AND_VALIDATION

## Objectif

Définir comment valider le pipeline YouTube avant extension.

## Échantillon pilote

```text
source: @trademachineoff
volume: 10 à 20 Shorts
fixtures manuelles: minimum 5
```

## Fixture attendue

```json
{
  "video_id": "sample_001",
  "input": {
    "title": "...",
    "spoken_transcript": "...",
    "screen_text": "..."
  },
  "expected": {
    "asset": "XAUUSD",
    "direction": "long",
    "entry": null,
    "stop_loss": null,
    "take_profits": [],
    "timeframe": "M5",
    "indicators": ["EMA"],
    "classification": "candidate_partial"
  }
}
```

## Tests minimum

- JSON valide.
- Champs obligatoires présents.
- Champs inconnus `null` ou `unknown`.
- Pas de TP/SL inventé.
- Détection asset stable sur alias courants.
- Détection long/short non déclenchée par contexte négatif ou exemple historique.

## Critères de passage pilote

```text
10 vidéos collectées minimum
5 fixtures annotées minimum
parser output valide sur 100 % de l'échantillon
aucune invention critique entry/sl/tp
raw output conservé
```

## Décision après pilote

```text
PASS       ouvrir extension P1_ACTIVE
PARTIAL    corriger parser et refaire fixtures
FAIL       garder source en P2_DISCOVERY ou REJECTED
```
