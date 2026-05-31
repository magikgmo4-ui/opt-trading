---
doc_id: GO_STRICT_WORKERS_CHILD_PATCH_DRAFT_RUNNER_PROVEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRICT_WORKERS_CHILD_PATCH_DRAFT_RUNNER_PROVEN_01
parent_go: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: open
lifecycle_stage: impl
created_at: 2026-05-31
task_type: PATCH_DRAFT
autonomy_max: A2
---

# 00_INITIAL_PROJECT_DOC — Child : PATCH_DRAFT runner prouvé

## 1_MASTER_TARGET

Exécuter un PATCH_DRAFT réel via `runner_readonly.py` : produire un patch qui met à jour
`docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` pour référencer
le runner validé (`runner_readonly.py`, PASS 2026-05-31). Patch DRAFT_ONLY — non appliqué.

## 2_PRECONDITIONS

```text
runner_readonly.py      = PASS (GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01, PR #995)
tasks.index.json        = PATCH_DRAFT entry présente (A2, writes_code=false)
job packet              = à créer : GO_STRICT_WORKERS_PATCH_DRAFT_RUNNER_PROVEN_01.json
output autorisé         = reports/ai/workers/**
```

## 3_JOB_PACKET

`scripts/ai/workers/job_packets/GO_STRICT_WORKERS_PATCH_DRAFT_RUNNER_PROVEN_01.json`

## 4_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| runner_readonly exécute le packet | PASS |
| Sections requises présentes | OBJECTIF_PATCH, FICHIERS_TOUCHES, DIFF_ATTENDU, RISQUES, TESTS_A_EXECUTER, VERDICT_DRAFT_ONLY |
| Patch format unified diff | oui |
| Fichier cible non modifié | 0 writes |
| git status post-run | clean |

## 12_INVARIANTS

```text
- Patch DRAFT_ONLY — non appliqué
- 0 modification du fichier cible
- Output uniquement dans reports/ai/workers/
- writes_code=false respecté
```
