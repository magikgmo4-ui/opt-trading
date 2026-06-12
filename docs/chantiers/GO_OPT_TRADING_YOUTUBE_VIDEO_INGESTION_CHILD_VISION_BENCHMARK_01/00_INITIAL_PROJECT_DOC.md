---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_BENCHMARK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_BENCHMARK_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
pf_id: PF_YOUTUBE_VIDEO_INGESTION
status: open
lifecycle_stage: validation
surface: youtube_video_ingestion
source_kind: canonical
created_at: 2026-06-11
updated_at: 2026-06-11
---

# GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_VISION_BENCHMARK_01

## Objectif

Créer un benchmark empirique pour mesurer la Vision Layer V1 sur les artefacts
réels `@trademachineoff`, avant tout élargissement à d'autres chaînes.

Le pipeline sait désormais collecter, extraire des frames, produire OCR et
structurer des signaux visuels. La question suivante est la qualité : faux
positifs symboles, prix mal typés, contexte chart incomplet, TP/SL absents.

## 1_MASTER_TARGET

```text
parser_input/*.json reels
  -> annotation template
  -> annotation manuelle reduite
  -> benchmark_results.json
  -> benchmark_report.md
  -> fixtures_real_world selectionnees
```

## 4_MASTER_PROJECT_PLAN

1. Lire les `parser_input/*.json` produits par les runs réels.
2. Générer un template d'annotations pour 25 à 50 vidéos.
3. Comparer Vision Layer V1 à une annotation manuelle.
4. Mesurer precision, recall, F1 et exact match par champ.
5. Mesurer `chart_detected` par accuracy.
6. Ecrire les résultats dans `outputs/youtube/benchmark/`.
7. Ne committer que le code, les tests, la documentation et les fixtures réduites validées.

## 12_INVARIANTS

- Aucun output brut YouTube committé.
- Aucun `outputs/youtube/benchmark/` committé par défaut.
- Aucun runtime-contracts dans le scope.
- Le benchmark ne relance pas d'ordre réel et ne déclenche aucun trade.
- Le benchmark score uniquement les champs annotés explicitement.

## 17_RESUME_POINT

Reprendre ici : lancer un run réel limité `@trademachineoff`, générer le template
d'annotations, annoter un sous-ensemble, puis lancer `benchmark-vision`.
