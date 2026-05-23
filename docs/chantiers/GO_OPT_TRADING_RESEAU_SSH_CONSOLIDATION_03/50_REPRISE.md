---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 50_REPRISE

## Resume point

```text
CURRENT_BASELINE: 98
HISTORICAL_BASELINE_REFERENCE: 87
GO courant: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
Mode: doc-only
Machine: db-layer
Verdict: PASS
```

## Established for next lot

- `modules/reseau_ssh` is the unique canonical top-level family module
- nested `reseau_ssh_step2` is the active internal implementation
- `modules/reseau_ssh_step1b` is still a transitional prerequisite
- `scripts/reseau_ssh` is a bounded rollback and transition backend
- short aliases remain canonical on `modules/reseau_ssh/scripts/*`
- step2 suffixed aliases remain tolerated as compatibility wrappers

## Next GO

```text
GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02
```

## Allowed scope for next GO

- wrapper publisher cleanup
- duplicate step2 installer cleanup
- path and README clarification
- compatibility-preserving physical adjustments

## Forbidden scope for next GO unless re-opened explicitly

- registry rewrite
- deletion of `modules/reseau_ssh_step1b`
- archive move of `scripts/reseau_ssh`
- broad runtime refactor outside the SSH family
- reopening the global modules baseline audit

## Memory candidates

- `CURRENT_MODULE_BASELINE_2026_05_20 = 98`
- `RESEAU_SSH_NEXT_ACTIVE = GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02`
- `RESEAU_SSH_CANONICAL_TOP_LEVEL = modules/reseau_ssh`
- `RESEAU_SSH_ACTIVE_IMPLEMENTATION = modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- `RESEAU_SSH_STEP1B_STATUS = transitional_prerequisite`

## Verdict

`PASS`
