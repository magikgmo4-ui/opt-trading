---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - branch_state
  - strict_workers
  - child
  - pool_extension
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/90_CLOSEOUT.md
point_de_reprise: "Revalider endpoint OpenCode Zen, mettre a jour le registry et le task index"
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/90_CLOSEOUT.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
---

# BRANCH_STATE — GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01

## Branche

```text
go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
```

## Base

```text
sot/mainline
```

## Base SHA

```text
1571af5 (merge PR #355 strict_workers child runtime lock + PATCH_DRAFT + E2E)
```

## Statut

```text
CADRAGE — revalidation endpoint en cours
```

## Parent

```text
GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01 (PASS, merge #355)
```

## Objet

Etendre le pool de workers stricts en reinterrogeant l'endpoint OpenCode Zen, en ajoutant les modeles nouvellement disponibles, et en retirant/remplacant ceux qui ont disparu.

## Surfaces prevues

```text
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/BRANCH_STATE.md
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/01_ENDPOINT_REVALIDATION_REPORT.md
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01/90_CLOSEOUT.md
scripts/ai/workers/models.registry.json (mis a jour)
scripts/ai/workers/tasks.index.json (mis a jour)
```

## Invariants Git

```text
- branche dediee pour extension pool strict_workers
- doc/scripts/reports uniquement
- pas de modification des index globaux
- runner run_task.sh intact
- stash branch_arbitration preserve
- aucun write runtime
```

## RISKS

- À qualifier.
