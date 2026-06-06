---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_TARGETS
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: targets
status: active
created_at: 2026-06-06
surface: youtube_video_ingestion
---

# TARGETS — GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01

## FINAL_TARGET

Ouvrir un chantier parent autonome pour cadrer l'ingestion vidéo YouTube ciblée dans opt-trading.

## Livrables parent

- `00_INITIAL_PROJECT_DOC.md`
- `01_SOURCE_REGISTRY_MODEL.md`
- `02_RAW_OUTPUT_CONTRACT.md`
- `03_TRANSCRIPT_OCR_METHOD.md`
- `04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1.md`
- `05_FIXTURES_AND_VALIDATION.md`
- `TARGETS.md`
- `target_card.json`

## Hors scope parent

- Implémentation runtime complète.
- Batch massif multi-chaînes.
- Trading live.
- Fermeture du parent après le premier pilote.
- Modification des index globaux sans changement global prouvé.

## NEXT_GO

```text
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
```

Cible du child :

```text
@trademachineoff
→ registre source
→ collecte 10 à 20 Shorts
→ raw output
→ transcript/OCR
→ parser output
→ 5 fixtures annotées
→ décision extension ou correction parser
```

## CLOSE_GATE

Le parent reste ouvert tant que :

- aucun child pilote n'a validé les fixtures ;
- aucun collecteur minimal n'est prouvé ;
- aucun dataset JSONL pilote n'est produit ;
- les seuils de confiance parser ne sont pas validés.