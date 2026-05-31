---
doc_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_3W_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_3W_01
parent_go: GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01
status: closed
lifecycle_stage: closed
created_at: 2026-05-31
closed_at: 2026-05-31
task_type: E2E_PIPELINE_3W
---

# 00_INITIAL_PROJECT_DOC — Pipeline E2E 3 workers

## 1_MASTER_TARGET

Pipeline 3 workers avec double chaînage :

```text
Step 1 : big-pickle    (READ_INVENTORY)  → inventaire + 2 GAPs identifiés
Step 2 : kimi-k2.6    (PATCH_DRAFT)     → lit Step1, propose patch sur 2 GAPs
Step 3 : qwen3.6-plus (REVIEW_DRAFT)    → lit Step1+Step2, approuve le patch
```

## 2_PIPELINE

| Étape | Worker | Task type | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1 | big-pickle | READ_INVENTORY | 1 | 0 |
| 2 | kimi-k2.6 | PATCH_DRAFT | 2 (source + Step1) | 0 |
| 3 | qwen3.6-plus | REVIEW_DRAFT | 3 (source + Step1 + Step2) | 0 |
