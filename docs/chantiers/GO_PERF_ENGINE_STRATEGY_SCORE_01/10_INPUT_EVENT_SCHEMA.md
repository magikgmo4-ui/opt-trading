---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_INPUT_EVENT_SCHEMA
doc_type: schema
repo: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 10_INPUT_EVENT_SCHEMA - Observation Event (minimal)

## Objectif

Supporter un input flexible (fixtures-first) qui peut venir de différentes surfaces, sans dépendre d’une classe Python.

## Format supporté

- JSONL: une ligne = un event JSON object
- JSON list: un fichier = liste d’events

## Champs attendus (extraction best-effort)

Le scorer cherche les champs dans les chemins suivants:

| Champ canonique | Chemins acceptés |
| --- | --- |
| `strategy_id` | `strategy_id` ; `strategy.strategy_id` |
| `strategy_version` | `strategy_version` ; `strategy.strategy_version` |
| `produced_at` | `produced_at` ; `timestamp` ; `_ts` |
| `run_id` | `run_id` ; `source_run_id` |
| `verdict` | `verdict` ; `pipeline_verdict` ; `validation_verdict` |
| `outcome` | `outcome` ; `pnl_paper.outcome` |
| `pnl_net` | `pnl_net` ; `pnl_paper.net_pnl` |

## Notes

- les events sans `strategy_id` sont ignorés
- la date d’observation est dérivée de `produced_at` si présent, sinon de `run_id` (YYYYMMDD prefix)
