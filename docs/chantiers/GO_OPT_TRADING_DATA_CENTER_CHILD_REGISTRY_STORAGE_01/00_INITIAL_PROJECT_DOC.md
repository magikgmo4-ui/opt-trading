---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
pf_id: PF_DATA_CENTER
status: open
lifecycle_stage: implementation
surface: data/data_center
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01 — INITIAL_PROJECT_DOC

## Objectif

Implémenter la structure `data/data_center/` avec raw/, normalized/, latest.json, manifest.json, status.json, events.jsonl, errors.jsonl, cache/by_symbol/.

## 1_MASTER_TARGET

```text
data/data_center/<producer>/raw/ -> normalized/ -> latest.json
data/data_center/_registry/producers.json
data/data_center/_registry/consumers.json
data/data_center/_registry/schema_versions.json
```

## 17_RESUME_POINT

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
```
