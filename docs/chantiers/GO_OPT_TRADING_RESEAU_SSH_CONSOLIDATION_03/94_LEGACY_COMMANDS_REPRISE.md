---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
status: pass
mode: doc-only
surface: modules
source_kind: continuity
machine_owner: db-layer
---

# 94_LEGACY_COMMANDS_REPRISE

## Resume point

```text
Current sub-go: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
Mode: doc-only
Verdict: PASS
```

## Established

- `wg-server-init` = retire
- `wg-client-init` = retire
- `wg-add-peer` = retire
- no rehome into canonical module

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_PHYSICAL_RETIREMENT_01`

## Goal of next GO

Physically cut the last supported legacy command path from `scripts/reseau_ssh` and downgrade that backend to archival-candidate status.

## Verdict

`PASS`
