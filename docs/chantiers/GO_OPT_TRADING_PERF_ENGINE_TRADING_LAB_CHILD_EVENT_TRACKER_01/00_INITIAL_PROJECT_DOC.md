---
doc_id: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01
pf_id: PF_PERF_ENGINE_TRADING_LAB
status: open
lifecycle_stage: implementation
surface: modules/perf_engine
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - adapters/webhook_to_perf.py
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01 — INITIAL_PROJECT_DOC

## Objectif

Formaliser le tracking des events de trading dans perf_db. Les events webhook
sont normalisés par `adapters/webhook_to_perf.py`, stockés dans perf_db (SQLite),
et suivis via le position tracker (`modules/perf_engine/`).

## 1_MASTER_TARGET

```text
webhook event -> webhook_to_perf -> perf event -> perf_db -> position tracker -> metrics
```

## 4_MASTER_PROJECT_PLAN

1. **Event schema** : formaliser le schéma des events perf.
2. **Event tracker** : tracker les events entry/exit/PnL dans perf_db.
3. **Position lifecycle** : gérer candidate → active → closed.
4. **Tests** : valider le tracking.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_PERF_ENGINE_TRADING_LAB_CHILD_EVENT_TRACKER_01
```
