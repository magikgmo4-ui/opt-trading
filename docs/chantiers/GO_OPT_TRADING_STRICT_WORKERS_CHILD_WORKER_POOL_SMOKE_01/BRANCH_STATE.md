---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - branch_state
  - strict_workers
  - child
  - pool_smoke
surface: docs/chantiers
source_kind: canonical
point_de_reprise: "Smoke test READ_INVENTORY sur 3 nouveaux modeles VERIFIED_FREE"
updated_at: 2026-05-14
---

# BRANCH_STATE — GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01

## Branche

```text
go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01
```

## Base

```text
sot/mainline @ 3a6c2fe (merge PR #362 pool extension)
```

## Statut

```text
CADRAGE — smoke test 3 nouveaux modeles en cours
```

## Parent

```text
GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01 (PASS, merge #362)
```

## Objet

Valider par smoke READ_INVENTORY les 3 nouveaux modeles VERIFIED_FREE avant usage operationnel.

## Surfaces prevues

```text
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01/
scripts/ai/workers/job_packets/  (3 nouveaux)
reports/ai/workers/              (3 sorties smoke)
```
