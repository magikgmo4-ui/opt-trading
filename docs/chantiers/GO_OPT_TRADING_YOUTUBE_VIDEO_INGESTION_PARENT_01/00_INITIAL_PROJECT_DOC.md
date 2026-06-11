---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: initial_project_doc
status: reference
lifecycle_stage: opening
created_at: 2026-06-06
updated_at: 2026-06-06
surface: youtube_video_ingestion
source_kind: canonical
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_OPT_TRADING_DATA_INGESTION
MASTER_TARGET_ID: MASTER_TARGET_OPT_TRADING_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_OPT_TRADING_DATA_INGESTION_AND_SIGNAL_DISCOVERY
PARENT_GO_ID: null
NEXT_ATTACH_TARGET: null
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: pending
---

# 00_INITIAL_PROJECT_DOC — YouTube Video Ingestion Parent

## 1_MASTER_TARGET

Construire une bibliothèque documentaire et technique autonome pour transformer des vidéos YouTube courtes et ciblées en données exploitables par `opt-trading`.

Chaîne logique :

```text
chaînes YouTube ciblées
→ registre de sources
→ collecte métadonnées / raw output
→ transcription audio
→ OCR texte écran
→ parser spécialisé trading
→ fixtures validées
→ dataset JSONL exploitable
```

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document transporteur initial du chantier. Il reste la référence figée du plan initial validé, sauf changement explicite ou implicite majeur du projet.

Le chantier doit être reprenable sans historique conversationnel.

## 3_INITIAL_NEED

Automatiser l'analyse de vidéos courtes YouTube issues de chaînes trading ciblées, sans saisir chaque URL manuellement.

Données à extraire :

- audio/transcription ;
- texte visible écran ;
- actif ;
- direction ;
- entrée ;
- stop-loss ;
- take-profits ;
- timeframe ;
- indicateurs ;
- règles de stratégie ;
- format de signal réutilisable.

Chaîne pilote initiale :

```text
https://youtube.com/@trademachineoff
```

## 4_MASTER_PROJECT_PLAN

### Axe A — Registre de chaînes

Créer un registre déclaratif des chaînes YouTube et profils de collecte.

### Axe B — Discovery contrôlé

Ne pas faire de scraping large. Le discovery doit rester limité aux chaînes choisies, aux Shorts récents et à des mots-clés ciblés.

### Axe C — Raw output complet

Conserver les artefacts bruts avant toute normalisation.

### Axe D — Transcription audio

Ordre de préférence : sous-titres manuels, sous-titres auto, Whisper/faster-whisper, fallback manuel échantillonné.

### Axe E — OCR texte écran

Extraire des frames, passer OCR, dédupliquer, puis consolider le texte temporel.

### Axe F — Parser trading spécialisé

Parser hybride : règles déterministes, regex, normalisation symboles, heuristiques trading, LLM contrôlé optionnel, validation par fixtures.

### Axe G — Fixtures et validation

Valider d'abord 10 à 20 Shorts sur une chaîne pilote avant extension.

## 5_GO_PLAN

1. Documenter le modèle registre.
2. Documenter le contrat raw output.
3. Documenter la méthode transcript/OCR.
4. Documenter le parser profile `youtube_trading_short_v1`.
5. Documenter fixtures et validation.
6. Préparer le child pilote `@trademachineoff`.

## 6_FINAL_TARGET

Documentation parent complète et autonome pour permettre l'implémentation ultérieure du pipeline YouTube ciblé.

## 7_CANONICAL_STATE

```yaml
GO_ID: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_OPT_TRADING_DATA_INGESTION
MASTER_TARGET_ID: MASTER_TARGET_OPT_TRADING_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_OPT_TRADING_DATA_INGESTION_AND_SIGNAL_DISCOVERY
PARENT_GO_ID: null
6_FINAL_TARGET: documentation parent complète et autonome
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: pending
status: PATCH_READY_NOT_APPLIED
```

## 8_VALIDATED_PLAN

Plan validé : documenter méthodes YouTube, screener, AI, registre, parser ; définir modèles robustes ; appliquer le schéma channels/discovery → raw output → data types → parser model ; même logique que Telegram mais plus ciblée.

## 9_SELECTED_SOLUTION

```text
yt-dlp → metadata / subtitles / URLs
ffmpeg → audio / frames
Whisper ou faster-whisper → transcription
Tesseract/PaddleOCR → OCR
parser déterministe + LLM contrôlé optionnel
fixtures JSONL → validation
```

## 10_SELECTED_SETUP

```text
registry/youtube_sources.jsonl
outputs/youtube/raw_metadata/
outputs/youtube/subtitles/
outputs/youtube/transcripts/
outputs/youtube/frames/
outputs/youtube/ocr/
outputs/youtube/parsed/
tests/fixtures/youtube_parser/
```

## 11_KEY_DECISIONS

- Discovery limité, pas massif.
- Chaîne pilote : `@trademachineoff`.
- Raw output conservé avant parser.
- Transcription et OCR séparés.
- Parser validé par fixtures.
- Champs inconnus explicitement `null` ou `unknown`.
- Le parent ne se ferme pas avec le premier pilote.

## 12_INVARIANTS

- Aucun ordre réel.
- Aucune exécution live.
- Données vidéo = observation / recherche / signaux candidats.
- Raw prioritaire sur parser.
- Parser révisable.
- Pas d'extension discovery avant validation pilote.

## 13_ESTABLISHED

- Besoin validé : automatiser sans entrer les URLs manuellement.
- Besoin validé : documenter méthodes YouTube/screener/AI/registre/parser.
- Besoin validé : chantier indépendant de la session.

## 14_HYPOTHESIS

- Sous-titres souvent absents ou incomplets.
- OCR critique pour Shorts trading.
- Formats de signal partiellement implicites.
- Parser hybride nécessaire.

## 15_REMAINING_GAP

- Pas de script collecteur.
- Pas de registre réel.
- Pas de fixtures.
- Pas de dataset JSONL.
- Pas de seuils de confiance validés.

## 16_TODO

1. Appliquer le patch sur branche dédiée.
2. Ouvrir child pilote `GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01`.
3. Collecter 10 à 20 Shorts.
4. Générer raw output.
5. Annoter 5 fixtures.
6. Ajuster parser profile.

## 17_RESUME_POINT

Reprendre ici : appliquer ce patch, puis ouvrir le child pilote `@trademachineoff` avec pipeline `registry → raw → transcript/OCR → parser → fixtures`.

## 18_TO_DOCUMENT

- `01_SOURCE_REGISTRY_MODEL.md`
- `02_RAW_OUTPUT_CONTRACT.md`
- `03_TRANSCRIPT_OCR_METHOD.md`
- `04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1.md`
- `05_FIXTURES_AND_VALIDATION.md`

## 19_TO_REMEMBER

### MEM_CANDIDATE

Pour ingestion vidéo YouTube opt-trading : registre de chaînes → raw output complet → transcription audio → OCR écran → parser spécialisé → fixtures validées → dataset JSONL.

### SAVE_MEMORY

Non demandé explicitement.
