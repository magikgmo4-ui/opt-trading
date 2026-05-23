---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01_GATES
doc_type: compatibility_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
status: pass
mode: doc-only
surface: modules
source_kind: canonical_decision
machine_owner: db-layer
---

# 93_LEGACY_BACKEND_PHYSICAL_RETIREMENT_GATES

## Physical retirement gates

Before physically retiring the active legacy backend role of `scripts/reseau_ssh`, the next GO must:

1. remove `wg-server-init`, `wg-client-init`, `wg-add-peer` from the legacy menu and command help
2. remove the canonical facade message that points operators to `bash "$RESEAU_SSH_COMPAT_CMD" "$cmd" ...`
3. update legacy README files to state these commands are retired in favor of the canonical workflow
4. preserve short alias publication through `modules/reseau_ssh/scripts/*`
5. avoid deleting the whole backend directory in the same lot unless archival handling is explicit and safe

## Minimal physical target

- retire commands as supported behavior
- cut explicit runtime references
- downgrade `scripts/reseau_ssh` from active rollback backend to archival candidate

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_PHYSICAL_RETIREMENT_01`

## Verdict

`PASS`
