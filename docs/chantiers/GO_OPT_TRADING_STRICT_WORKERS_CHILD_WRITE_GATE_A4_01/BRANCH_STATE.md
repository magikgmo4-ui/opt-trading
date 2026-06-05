---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - branch_state
  - strict_workers
  - child
  - write_gate
  - A4
surface: docs/chantiers
updated_at: 2026-05-14
---

# BRANCH_STATE — GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01

## Branche

```text
go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
```

## Base

```text
sot/mainline @ 1a5dd9f (merge PR #364 pool smoke)
```

## Statut

```text
WRITE_GATE_CADRAGE — policy + tests negatifs puis positif
```

## Parent

```text
GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_SMOKE_01 (PASS, merge #364)
```

## Objet

Promouvoir le runner vers A4 (WRITE_GATED) sans jamais autoriser le write libre.

## Surfaces prevues

```text
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01/
scripts/ai/workers/tasks.index.json (modifie : +WRITE_GATED)
scripts/ai/workers/_validate_job.py (modifie : +gates A4)
scripts/ai/workers/job_packets/ (packets test A4)
reports/ai/workers/ (sorties test A4)
```

## Invariants Git

```text
- branche dediee
- doc/scripts/reports uniquement
- denied_commands conserves
- stash branch_arbitration preserve
```

## RISKS

- À qualifier.
