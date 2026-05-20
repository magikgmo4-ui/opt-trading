---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - perf_engine
  - strategy_score
  - evidence_pack
  - gates
  - signal_chain
links:
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/10_INPUT_EVENT_SCHEMA.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/20_METRICS_AND_GATES.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/30_EVIDENCE_PACK_SCHEMA.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/90_REPRISE_POINT.md
---

# INBOX - GO_PERF_ENGINE_STRATEGY_SCORE_01

## Objet

Définir et implémenter un “strategy score” (Perf Engine) calculé à partir d’Observation Events (fixtures-first), produisant un evidence pack + verdict de gates (promotion/retirement), sans décision live.

## Résultat

État établi :

- surfaces Perf Engine relues et reconfirmees pour `modules/perf_engine/app/perf_engine.py`, `tests/e2e/test_perf_engine_strategy_score.py` et `60_PERF_ENGINE_STRATEGY_EVALUATION.md`
- le subcommand `strategy-score` existe et produit un evidence pack JSON stable a partir d'events JSONL ou JSON list
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_perf_engine_strategy_score.py -q` -> `1 passed`
- aucune mutation runtime introduite ; le chantier reste fixtures-first et offline-first

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via le scoring strategie Perf Engine
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01`
- `Gaps encore ouverts` : producer officiel absent, consumer registry/lab absent, export Sheets `strategy_perf` hors scope

## Point de reprise

```text
docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/20_METRICS_AND_GATES.md
docs/chantiers/GO_PERF_ENGINE_STRATEGY_SCORE_01/30_EVIDENCE_PACK_SCHEMA.md
```
