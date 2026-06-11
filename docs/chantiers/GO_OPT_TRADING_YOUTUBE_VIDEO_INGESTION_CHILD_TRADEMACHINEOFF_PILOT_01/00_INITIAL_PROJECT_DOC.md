---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
pf_id: PF_YOUTUBE_VIDEO_INGESTION
status: open
lifecycle_stage: pilot_definition
surface: youtube_video_ingestion
source_kind: canonical
created_at: 2026-06-11
updated_at: 2026-06-11
TRANSPORT_MODE: patch_only
links:
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/01_SOURCE_REGISTRY_MODEL.md
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/02_RAW_OUTPUT_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/03_TRANSCRIPT_OCR_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1.md
  - docs/chantiers/GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01/05_FIXTURES_AND_VALIDATION.md
---

# GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01

## Objet

Ouvrir le child pilote `@trademachineoff` pour valider la chaine YouTube video
ingestion sur une seule source avant toute extension.

Ce GO transforme le cadrage parent en pilote borne :

```text
source registry -> raw output -> transcript/OCR -> parser_input -> parser -> fixtures -> decision
```

Le patch de ce child reste documentaire. Il ne collecte pas de videos, ne lance pas
`yt-dlp`, ne genere pas de frames et ne modifie pas les index globaux.

## 1_MASTER_TARGET

```text
@trademachineoff Shorts
  -> source P0_PILOT documentee
  -> 10 a 20 videos candidates
  -> raw evidence conservable
  -> parser_input conforme youtube_trading_short_v1
  -> 5 fixtures annotees minimum
  -> decision pilote PASS / PARTIAL / FAIL
```

## 4_MASTER_PROJECT_PLAN

1. Declarer le scope source unique `@trademachineoff`.
2. Collecter ou lister 10 a 20 Shorts candidats sans etendre la discovery.
3. Conserver les metadonnees brutes par video.
4. Extraire sous-titres, transcription ou fallback audio quand disponible.
5. Extraire frames et OCR selon la methode parent.
6. Consolider `parser_input/<video_id>.json`.
7. Executer ou simuler le parser `youtube_trading_short_v1`.
8. Annoter 5 fixtures minimum.
9. Produire une decision pilote : `PASS`, `PARTIAL` ou `FAIL`.

## 6_FINAL_TARGET

Le child est ferme seulement si les preuves suivantes existent dans le scope du GO :

```text
registry/youtube_sources.jsonl                         source @trademachineoff candidate
outputs/youtube/raw_metadata/*.json                    metadonnees brutes
outputs/youtube/parser_input/*.json                    inputs consolides
outputs/youtube/parsed/*.json                          sorties derivees
tests/fixtures/youtube_video_ingestion/*.json          fixtures annotees
docs/chantiers/.../90_CLOSEOUT.md                      decision pilote
```

## 12_INVARIANTS

- Aucun ordre reel.
- Aucune execution live trading.
- Aucune recommandation de trading produite par le parser.
- Une video YouTube reste une source d'observation, pas une source d'autorite.
- Raw output prioritaire sur parsed output.
- Pas d'extension a d'autres chaines avant decision pilote.
- Pas de modification des index globaux dans ce patch d'ouverture.
- Pas de suppression ou reecriture de fichiers hors `FILE_SCOPE.txt`.

## 13_ESTABLISHED

- Le parent `GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01` est materialise.
- Le parent etablit la source pilote `@trademachineoff`.
- Le parser cible est `youtube_trading_short_v1`.
- Le volume pilote attendu est 10 a 20 Shorts.
- Les fixtures manuelles minimales sont au nombre de 5.

## 14_HYPOTHESIS

- Les Shorts contiennent probablement plus de signal dans le texte ecran que dans l'audio.
- Les sous-titres YouTube peuvent etre absents ou incomplets.
- Les chiffres entry, SL et TP peuvent etre ambigus apres OCR.
- Le premier run doit favoriser la conservation raw et l'annotation humaine.

## 15_REMAINING_GAP

- Aucun collecteur YouTube runtime n'est encore valide.
- Aucune URL pilote n'est encore figee.
- Aucun raw output n'est encore produit.
- Aucune fixture `@trademachineoff` n'est encore annotee.
- Aucun seuil de confiance n'est encore prouve sur video reelle.

## 16_TODO

1. Appliquer ce patch child sur une branche dediee.
2. Verifier que le parent est present dans le repo local.
3. Ajouter la source `@trademachineoff` en `P0_PILOT`.
4. Collecter ou lister 10 a 20 Shorts candidats.
5. Produire raw metadata, transcript/OCR et parser inputs.
6. Annoter 5 fixtures minimum.
7. Produire le closeout pilote avec decision.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
source: @trademachineoff
pipeline: registry -> raw -> transcript/OCR -> parser -> fixtures
mode: pilot only, no source expansion
```

