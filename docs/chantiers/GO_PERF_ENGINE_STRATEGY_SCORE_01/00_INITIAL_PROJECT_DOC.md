---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/60_PERF_ENGINE_STRATEGY_EVALUATION.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/10_INPUT_EVENT_SCHEMA.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/20_METRICS_AND_GATES.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/30_EVIDENCE_PACK_SCHEMA.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Perf Engine strategy score

## But

Produire un evidence pack “strategy score” à partir d’Observation Events enrichis:

- calcul métriques standard (sample, pass_rate, pnl, drawdown, etc.)
- verdicts de gates (promotion / retirement)
- output JSON stable, contrôlé, offline

## Contraintes

- fixtures-first (input JSONL offline)
- aucun ordre live, aucune écriture Sheets automatique
- les seuils sont paramétrables (pas codés en dur produit)

## Implémentation cible (safe)

- un subcommand `strategy-score` dans `modules/perf_engine/app/perf_engine.py`
- support JSONL et JSON list
