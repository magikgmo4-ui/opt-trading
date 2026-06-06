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
TRANSPORT_MODE: bundle_patch_zip
CLOSE_GATE_MASTER_TARGET: pending
---

# 00_INITIAL_PROJECT_DOC — YouTube Video Ingestion Parent

## 1_MASTER_TARGET

Construire une bibliothèque documentaire et technique autonome pour transformer des vidéos YouTube courtes et ciblées en données exploitables par `opt-trading`.

La cible n'est pas de faire un discovery massif comme Telegram. La cible est un pipeline restreint, contrôlé et validable :

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

Ce fichier est le document transporteur initial du chantier. Il doit rester la référence figée du plan initial validé, sauf changement explicite ou implicite majeur du projet.

Il permet de reprendre le chantier indépendamment de la session conversationnelle.

## 3_INITIAL_NEED

Automatiser l'analyse de vidéos courtes YouTube issues de chaînes trading ciblées, sans entrer manuellement chaque URL, afin de capturer :

- ce qui est dit dans la vidéo ;
- ce qui est écrit à l'écran ;
- les actifs mentionnés ;
- les directions long / short / neutral ;
- les entrées, stop-loss et take-profits éventuels ;
- les timeframes ;
- les indicateurs ;
- les règles de stratégie ;
- les formats de signal réutilisables comme fixtures ou données de backtest.

Chaîne pilote initiale :

```text
https://youtube.com/@trademachineoff
```

## 4_MASTER_PROJECT_PLAN

### Axe A — Registre de chaînes

Créer un registre déclaratif des chaînes YouTube et des profils de collecte.

Champs minimaux :

```json
{
  "source_type": "youtube_channel",
  "handle": "@trademachineoff",
  "url": "https://youtube.com/@trademachineoff",
  "theme": "trading_short_form",
  "language_hint": "auto",
  "priority": "P0_PILOT",
  "video_scope": "shorts_first",
  "collection_mode": "latest_or_keyword",
  "parser_profile": "youtube_trading_short_v1",
  "status": "candidate"
}
```

### Axe B — Discovery contrôlé

Ne pas faire de scraping large au départ. Le discovery doit rester limité :

- chaînes explicitement choisies ;
- vidéos récentes ;
- Shorts priorisés ;
- mots-clés ciblés : `gold`, `xau`, `btc`, `nasdaq`, `forex`, `entry`, `scalping`, `strategy`, `long`, `short`, `tp`, `sl` ;
- limite par chaîne configurable.

### Axe C — Raw output complet

Chaque vidéo doit conserver ses artefacts bruts avant parsing :

```text
raw_metadata.json
subtitles.vtt / subtitles.srt si disponibles
transcript.txt
ocr_frames.jsonl
sampled_frames/
parser_input.json
parser_output.json
```

Le raw prime sur le parser. Le parser est dérivé, donc révisable.

### Axe D — Transcription audio

Ordre de préférence :

1. sous-titres manuels YouTube si disponibles ;
2. sous-titres automatiques YouTube ;
3. transcription locale Whisper / faster-whisper ;
4. fallback manuel sur échantillon si audio inexploitable.

### Axe E — OCR texte écran

Les Shorts trading contiennent souvent plus d'information dans l'image que dans l'audio. Il faut donc extraire des frames.

Méthode proposée :

```text
ffmpeg → frame sampling → OCR → déduplication texte → consolidation temporelle
```

OCR possible :

- Tesseract pour version simple ;
- PaddleOCR si besoin de robustesse supérieure ;
- filtrage des doublons par similarité.

### Axe F — Parser trading spécialisé

Le parser `youtube_trading_short_v1` doit extraire :

```text
asset
market_type
direction
entry
stop_loss
take_profits
timeframe
indicators
pattern
strategy_rules
risk_rules
confidence
missing_fields
raw_evidence
```

Approche recommandée :

```text
règles déterministes / regex
→ normalisation symboles
→ heuristiques trading
→ LLM contrôlé optionnel
→ validation fixture
```

### Axe G — Fixtures et validation

Créer des fixtures manuelles sur un petit échantillon avant batch massif.

Échantillon initial :

```text
10 à 20 Shorts de @trademachineoff
```

Validation attendue :

- transcription présente ;
- texte écran extrait ou raison d'absence documentée ;
- parser output valide JSON ;
- champs inconnus explicitement `null` ou `unknown` ;
- confidence score ;
- preuve raw conservée.

## 5_GO_PLAN

1. Créer le dossier chantier parent.
2. Documenter le modèle registre.
3. Documenter le contrat raw output.
4. Documenter la méthode transcript/OCR.
5. Documenter le parser profile `youtube_trading_short_v1`.
6. Documenter fixtures et validation.
7. Préparer le premier child GO pilote pour `@trademachineoff`.
8. Ne pas fermer le parent après le pilote ; produire `NEXT_GO`.

## 6_FINAL_TARGET

À la fin de ce chantier parent, le repo doit contenir une documentation complète permettant à une autre session, un IDE ou un agent local de construire le pipeline sans dépendre de l'historique conversationnel.

Livrables documentaires du parent :

```text
00_INITIAL_PROJECT_DOC.md
01_SOURCE_REGISTRY_MODEL.md
02_RAW_OUTPUT_CONTRACT.md
03_TRANSCRIPT_OCR_METHOD.md
04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1.md
05_FIXTURES_AND_VALIDATION.md
TARGETS.md
target_card.json
```

## 7_CANONICAL_STATE

```yaml
GO_ID: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_OPT_TRADING_DATA_INGESTION
MASTER_TARGET_ID: MASTER_TARGET_OPT_TRADING_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_OPT_TRADING_DATA_INGESTION_AND_SIGNAL_DISCOVERY
PARENT_GO_ID: null
6_FINAL_TARGET: documentation parent complète et autonome pour ingestion YouTube vidéo ciblée
TRANSPORT_MODE: bundle_patch_zip
CLOSE_GATE_MASTER_TARGET: pending
status: OPENING
```

## 8_VALIDATED_PLAN

Plan validé par l'utilisateur :

```text
Mieux documenter les méthodes YouTube, screener, AI, registre, parser.
Définir des modèles robustes de base.
Appliquer ensuite le même schéma : channels choisis ou discovery, raw output, type of data, parser model.
Même logique que Telegram, mais sur vidéos, moins large, pour sujets ciblés.
```

## 9_SELECTED_SOLUTION

Solution retenue : pipeline multimodal YouTube ciblé.

```text
yt-dlp pour discovery / metadata / sous-titres
ffmpeg pour audio / frames
Whisper ou faster-whisper pour transcription
OCR pour texte écran
parser déterministe + LLM contrôlé optionnel
fixtures JSONL pour validation
```

## 10_SELECTED_SETUP

Setup logique :

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

- Ne pas traiter YouTube comme Telegram discovery massif au départ.
- Commencer par un pilote ciblé `@trademachineoff`.
- Garder le raw output complet.
- Séparer transcript audio et OCR écran.
- Ne pas faire confiance au parser sans fixtures.
- Produire des champs structurés exploitables par Data Center / backtest.
- Ne pas fermer le parent avec le premier pilote.

## 12_INVARIANTS

- Aucun ordre réel de trading.
- Aucune exécution live.
- Données vidéo = observations / signaux candidats / matière de recherche.
- Raw output conservé avant toute normalisation.
- Parser révisable.
- Champs inconnus documentés, pas inventés.
- Discovery limité tant que les fixtures ne sont pas validées.

## 13_ESTABLISHED

- Besoin validé : automatiser le processus pour ne pas entrer les URLs manuellement.
- Besoin validé : documenter méthodes YouTube / screener / AI / registre / parser.
- Besoin validé : appliquer un schéma comparable à Telegram, mais plus ciblé.
- Chaîne pilote proposée : `@trademachineoff`.

## 14_HYPOTHESIS

À valider lors du child pilote :

- La chaîne pilote contient suffisamment de Shorts trading exploitables.
- Les sous-titres YouTube seront insuffisants ou absents pour une partie des vidéos.
- L'OCR sera critique pour capturer les signaux affichés.
- Les formats de signal seront partiellement implicites, donc parser hybride requis.

## 15_REMAINING_GAP

- Pas encore de script collecteur.
- Pas encore de registre réel commité.
- Pas encore de fixtures.
- Pas encore de dataset JSONL.
- Pas encore de seuils de confiance validés.
- Pas encore de child GO pilote ouvert.

## 16_TODO

1. Finaliser les documents parent.
2. Créer le child GO pilote : `GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01`.
3. Implémenter un collecteur minimal ou fournir un patch opérateur.
4. Collecter 10 à 20 vidéos courtes.
5. Générer raw output.
6. Produire 5 fixtures annotées manuellement.
7. Ajuster parser profile.
8. Décider si extension à d'autres chaînes.

## 17_RESUME_POINT

Reprendre ici : lire ce fichier, puis ouvrir le child pilote `@trademachineoff` avec pipeline `registry → raw → transcript/OCR → parser → fixtures`.

## 18_TO_DOCUMENT

- `01_SOURCE_REGISTRY_MODEL.md`
- `02_RAW_OUTPUT_CONTRACT.md`
- `03_TRANSCRIPT_OCR_METHOD.md`
- `04_PARSER_PROFILE_YOUTUBE_TRADING_SHORT_V1.md`
- `05_FIXTURES_AND_VALIDATION.md`

## 19_TO_REMEMBER

### MEM_CANDIDATE

Pour les chantiers d'ingestion vidéo YouTube opt-trading, utiliser un pipeline ciblé : registre de chaînes → raw output complet → transcription audio → OCR écran → parser spécialisé → fixtures validées → dataset JSONL.

### SAVE_MEMORY

Non demandé explicitement.
