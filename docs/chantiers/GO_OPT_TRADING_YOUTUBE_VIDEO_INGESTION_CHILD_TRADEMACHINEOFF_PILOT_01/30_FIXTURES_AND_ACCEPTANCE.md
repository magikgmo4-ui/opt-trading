---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_FIXTURES_AND_ACCEPTANCE
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: fixtures_acceptance
status: draft_reference
created_at: 2026-06-11
---

# 30_FIXTURES_AND_ACCEPTANCE

## Fixture minimale

```json
{
  "video_id": "sample_001",
  "source_handle": "@trademachineoff",
  "input": {
    "title": "...",
    "spoken_transcript": "...",
    "screen_text": "...",
    "ocr_segments": []
  },
  "expected": {
    "asset": "XAUUSD",
    "market_type": "forex",
    "direction": "long",
    "entry": null,
    "stop_loss": null,
    "take_profits": [],
    "timeframe": "M5",
    "indicators": ["EMA"],
    "classification": "candidate_partial",
    "must_not_invent": ["entry", "stop_loss", "take_profits"]
  }
}
```

## Champs obligatoires

```text
video_id
source_handle
input.title
input.spoken_transcript
input.screen_text
expected.asset
expected.direction
expected.classification
expected.must_not_invent
```

## Classification attendue

```text
candidate_complete   asset + direction + entry + SL + TP ou preuve equivalente
candidate_partial    signal exploitable mais incomplet
context_only         contexte marche ou strategie sans entree exploitable
reject_noise         contenu insuffisant ou hors scope
```

## Tests minimum

- JSON valide.
- `source_handle` vaut `@trademachineoff`.
- `parser_profile` vaut `youtube_trading_short_v1`.
- Les alias asset parent sont reconnus.
- `long` / `short` ne sont pas declenches par un contexte negatif.
- `entry`, `stop_loss` et `take_profits` ne sont jamais inventes.
- Un conflit audio/OCR devient un champ explicite ou une evidence contradictoire.
- La classification reste coherente avec les champs detectes.

## Acceptance gate pilote

```text
10 videos candidates minimum
5 fixtures annotees minimum
parser output valide sur 100 % de l'echantillon annote
0 invention critique entry/sl/tp
raw output conserve pour chaque video annotee
decision PASS/PARTIAL/FAIL documentee
```

## Decision

| Decision | Critere | Suite |
|---|---|---|
| PASS | Fixtures stables, aucune invention critique | Ouvrir extension source ou runtime regularise |
| PARTIAL | Parsing utile mais erreurs corrigeables | Corriger parser puis refaire fixtures |
| FAIL | Trop de bruit ou source non exploitable | Garder source en discovery ou rejeter |

