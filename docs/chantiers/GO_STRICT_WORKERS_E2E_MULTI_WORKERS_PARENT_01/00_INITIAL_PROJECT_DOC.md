---
doc_id: GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01
parent_go: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: open
lifecycle_stage: impl
created_at: 2026-05-31
task_type: PARENT
---

# 00_INITIAL_PROJECT_DOC — GO_STRICT_WORKERS_E2E_MULTI_WORKERS_PARENT_01

## 1_MASTER_TARGET

Prouver le chaînage E2E de deux strict workers distincts :

```text
Worker A (READ_INVENTORY) → rapport A
rapport A utilisé comme entrée de →
Worker B (REVIEW_DRAFT)   → rapport B
```

Deux workers différents, deux task types différents, sortie de A = input de B.
Aucun write durable — pipeline read-only.

## 2_PRECONDITIONS

```text
runner_readonly.py  = PASS (PR #995)
runner_writegated.py= PASS (PR #1024)
tasks.index.json    = READ_INVENTORY + REVIEW_DRAFT définis
models.registry.json= big-pickle, qwen3.5-plus, glm-5.1 VERIFIED
```

## 3_PIPELINE CIBLE

| Étape | Task type | Worker | Inputs | Output |
| --- | --- | --- | --- | --- |
| Step 1 | READ_INVENTORY | big-pickle | STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | E2E_STEP1_READ_INVENTORY.md |
| Step 2 | REVIEW_DRAFT | glm-5.1 | STRICT_WORKERS_AUTONOMIE_ETROITE_01.md + Step1 output | E2E_STEP2_REVIEW_DRAFT.md |

## 4_GAPS

| Gap | GO dédié | Statut |
| --- | --- | --- |
| Pipeline 2 workers + chaînage prouvé | GO_STRICT_WORKERS_CHILD_E2E_PIPELINE_01 | open |

## 5_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| Step 1 runner PASS | oui |
| Step 2 runner PASS avec Step1 output en input | oui |
| Step 2 lit effectivement le rapport Step 1 | oui (read_operations inclut le fichier) |
| 0 writes sur les deux steps | oui |
| Deux workers distincts utilisés | oui |

## 12_INVARIANTS

```text
- Pipeline read-only (DRAFT_ONLY sur les deux steps)
- Chaque step sur son propre job packet
- Chaînage via allowed_inputs du Step 2
```
