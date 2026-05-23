---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01_ARGUMENTS
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

# 92_RETIREMENT_ARGUMENTS

## Why not rehome

Rehoming would keep an old direct-write WireGuard path alive next to the current inventory-driven path.

That would preserve two incompatible operator doctrines:

1. direct imperative init/edit of `/etc/wireguard/wg0.conf`
2. canonical render/apply workflow centered on inventory and managed artifacts

The family should converge on one doctrine only.

## Why retirement is safe enough as a decision

- the commands are already cut from the canonical facade
- the canonical README for `step2` already teaches the replacement path
- the remaining dependence is only the explicit legacy escape hatch

## Retirement rule

Retire these commands from supported family flow.

If a historical recovery need exists later, it belongs in archive material, not in the active SSH family runtime surface.

## Verdict

`PASS`
