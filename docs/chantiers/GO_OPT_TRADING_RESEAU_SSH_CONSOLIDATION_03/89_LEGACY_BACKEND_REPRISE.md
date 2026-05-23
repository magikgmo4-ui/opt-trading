---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 89_LEGACY_BACKEND_REPRISE

## Resume point

```text
Current sub-go: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
Mode: doc-only
Verdict: BLOCKED_WITH_REASON
```

## Established

- canonical family flow no longer depends on `scripts/reseau_ssh` for normal operations
- legacy backend still owns the last unresolved explicit commands
- backend exit must follow command retirement or rehome proof

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01`

## Goal of next GO

Decide the fate of:

- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

## Verdict

`BLOCKED_WITH_REASON`
