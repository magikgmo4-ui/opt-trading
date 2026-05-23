---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01_NEXT_GO
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 98_ONE_MODULE_NEXT_GO

## Resume point

```text
Current sub-go: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
Mode: doc-only
Verdict: BLOCKED_WITH_REASON
```

## Proven current state

- canonical top-level owner: `modules/reseau_ssh`
- nested implementation owner: `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- residual top-level dependency: `modules/reseau_ssh_step1b` via `baseline-hostname`
- residual legacy runtime path: `scripts/reseau_ssh`

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_FINAL_RESIDUALS_RESOLUTION_01`

## Goal of next GO

Resolve the last residuals blocking true one-module canonization:

1. `baseline-hostname`
2. legacy transition helpers
3. legacy delegating installer

## Verdict

`BLOCKED_WITH_REASON`
