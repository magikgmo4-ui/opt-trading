---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_ROUTING_CLASS_MATRIX
doc_type: matrix
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_ROUTING_CLASS_MATRIX - event → destination

## Mapping basé sur la taxonomie

Référence: familles/types définis dans `GO_EVENT_TAXONOMY_01`.

## Dispatcher actuel (PipelineEvent.event_type)

| Event type (actuel) | Family (cible) | Alias destination | Policy |
| --- | --- | --- | --- |
| `signal_received` | `SIGNAL` | `TG_PAPER` si `dry_run` ; sinon `TG_TRADING` | noise-control: regrouper |
| `proposition_generated` | `DECISION` | `TG_PAPER` si `dry_run` ; sinon `TG_TRADING` | inclure confidence |
| `approval_required` | `DECISION` | `TG_TRADING` | priorité haute |
| `trade_executed` | `EXECUTION` | `TG_TRADING` | priorité haute |
| `result_known` | `EXECUTION` | `TG_TRADING` | priorité haute |
| `pipeline_info` | `NOTIFY` | `TG_OPS` | éviter spam |
| `pipeline_error` | `NOTIFY` | `TG_ALERTS` | priorité critique |

## Règles minimales

- En dry-run, tout ce qui est routé trading doit basculer vers `TG_PAPER` ou être “skipped”.
- Les erreurs doivent pouvoir aller vers un canal dédié (`TG_ALERTS`) sans polluer `TG_TRADING`.
