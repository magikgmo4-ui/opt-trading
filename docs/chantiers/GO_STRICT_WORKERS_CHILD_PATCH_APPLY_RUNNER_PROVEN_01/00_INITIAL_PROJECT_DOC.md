---
doc_id: GO_STRICT_WORKERS_CHILD_PATCH_APPLY_RUNNER_PROVEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_CHILD_PATCH_APPLY_RUNNER_PROVEN_01
parent_go: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: closed
lifecycle_stage: impl
created_at: 2026-05-31
task_type: PATCH_APPLY
autonomy_max: A2
---

# 00_INITIAL_PROJECT_DOC — Child : PATCH_APPLY runner prouvé

## 1_MASTER_TARGET

Appliquer le patch DRAFT_ONLY produit par `GO_STRICT_WORKERS_CHILD_PATCH_DRAFT_RUNNER_PROVEN_01`
sur `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md`.

Gate humain APPROVE reçu : "go appliquer le patch" (2026-05-31).

## 2_PRECONDITIONS

```text
source patch    : reports/ai/workers/GO_STRICT_WORKERS_PATCH_DRAFT_RUNNER_PROVEN_01.md
gate humain     : APPROVE — "go appliquer le patch"
patch validé    : DRAFT_ONLY PASS (PR #1021)
```

## 3_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| Section `## Runner validé` présente dans le fichier | oui |
| Contenu conforme au diff proposé | oui |
| Reste du fichier intact | oui |
| git diff minimal | oui |

## 12_INVARIANTS

```text
- Patch minimal — aucune autre modification du fichier
- Gate humain documenté avant application
```
