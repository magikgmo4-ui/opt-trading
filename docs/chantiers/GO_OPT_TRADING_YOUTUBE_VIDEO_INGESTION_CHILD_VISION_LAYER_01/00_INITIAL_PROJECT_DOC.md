---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_LAYER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_LAYER_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
pf_id: PF_YOUTUBE_VIDEO_INGESTION
status: open
lifecycle_stage: implementation
surface: youtube_video_ingestion
source_kind: canonical
created_at: 2026-06-11
updated_at: 2026-06-11
---

# GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_LAYER_01

## Objectif

Créer une couche vision V1 indépendante pour transformer les textes OCR de frames
en indices trading structurés.

Le pilote `TRADEMACHINEOFF` a prouvé que la collecte fonctionne, mais aussi que
metadata + sous-titres restent insuffisants pour des Shorts où la valeur est
principalement visuelle.

## 1_MASTER_TARGET

```text
frames/OCR text
  -> screen_text normalise
  -> symbols_detected
  -> prices_detected
  -> indicators_detected
  -> chart_detected
  -> confidence
  -> parser youtube_trading_short_v1 enrichi
```

## 4_MASTER_PROJECT_PLAN

1. Ajouter un module `vision.py` déterministe, sans modèle externe.
2. Normaliser le texte OCR en `screen_text`.
3. Détecter symboles, prix typés, timeframes, indicateurs et indices chart.
4. Persister l'objet `vision` dans `parser_input`.
5. Permettre au parser de consommer `vision` sans inventer de prix.
6. Couvrir le flux par tests fixture-first.

## 12_INVARIANTS

- Aucun ordre réel.
- Aucun modèle vision obligatoire en V1.
- Aucun output brut YouTube committé.
- Aucun élargissement de chaînes.
- Les prix ne sont extraits que s'ils sont explicitement visibles dans OCR/screen text.

## 17_RESUME_POINT

Reprendre ici : valider Vision Layer V1 sur les frames `@trademachineoff`, puis
annoter des fixtures réduites avant tout passage V2 modèle vision.
