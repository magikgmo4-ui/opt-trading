---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - child
  - pool_smoke
  - read_inventory
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/90_CLOSEOUT.md
point_de_reprise: "Smoke test READ_INVENTORY pour les 3 nouveaux modeles VERIFIED_FREE"
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/90_CLOSEOUT.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Exécuter un smoke test READ_INVENTORY sur chacun des 3 nouveaux modèles VERIFIED_FREE issus du pool extension, pour valider leur comportement read-only avant usage opérationnel.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| Pool etendu | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01` (PASS, merge #362) |
| Registry a jour | `scripts/ai/workers/models.registry.json` (15 VERIFIED/VERIFIED_FREE) |
| Task index a jour | `scripts/ai/workers/tasks.index.json` (7 task types) |
| Runner operationnel | `scripts/ai/workers/run_task.sh` |

## 3_MODELES_A_TESTER

| Modele | Statut | Tache | Scope |
|--------|--------|-------|-------|
| deepseek-v4-flash-free | VERIFIED_FREE | READ_INVENTORY | docs/agents/strict_workers/ + registry |
| ring-2.6-1t-free | VERIFIED_FREE | READ_INVENTORY | docs/agents/strict_workers/ + registry |
| trinity-large-preview-free | VERIFIED_FREE | READ_INVENTORY | docs/agents/strict_workers/ + registry |

## 4_CRITERES_PASS

```text
Pour chaque modele teste :
- La sortie est DRAFT_ONLY
- Toutes les sections obligatoires READ_INVENTORY sont presentes
- Aucun write runtime
- Aucun secret expose
- Sortie ≤ 500 lignes
- Garde-fous Phase A/B actifs (runner_lock, patch_draft_guard)
```

## 5_VERDICT

```text
PASS si les 3 modeles passent tous les criteres individuellement.
BLOCKED si un modele echoue.
REMAINING_GAP si un modele est limite mais non bloquant.
```

## 6_INVARIANTS

```text
- Runner intact (run_task.sh 0 diff)
- Aucun write runtime
- Aucun secret
- Aucun index global modifie
- Stash branch_arbitration preserve
```
