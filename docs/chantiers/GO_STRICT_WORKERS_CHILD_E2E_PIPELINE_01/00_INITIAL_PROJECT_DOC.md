---
doc_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_01
parent_go: GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01
status: closed
lifecycle_stage: impl
created_at: 2026-05-31
task_type: E2E_PIPELINE
---

# 00_INITIAL_PROJECT_DOC — Child : Pipeline E2E 2 workers

## 1_MASTER_TARGET

Exécuter un pipeline E2E à deux workers distincts avec chaînage sortie→entrée :

```text
Step 1 : big-pickle (READ_INVENTORY)  → rapport Step 1
Step 2 : glm-5.1   (REVIEW_DRAFT)    → lit rapport Step 1 + source → rapport Step 2
```

## 2_PIPELINE

| Étape | Runner | Worker | Task type | Inputs | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | runner_readonly.py | big-pickle | READ_INVENTORY | STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | E2E_STEP1_READ_INVENTORY_01.md |
| 2 | runner_readonly.py | glm-5.1 | REVIEW_DRAFT | source + Step1 output | E2E_STEP2_REVIEW_DRAFT_01.md |

## 3_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| Step 1 runner PASS, 1 read, 0 writes | oui |
| Step 2 runner PASS, 2 reads (source + Step1), 0 writes | oui |
| Step 2 `read_operations` inclut Step1 output | oui — preuve chaînage |
| Deux workers distincts | big-pickle ≠ glm-5.1 |
| Deux task types distincts | READ_INVENTORY ≠ REVIEW_DRAFT |
