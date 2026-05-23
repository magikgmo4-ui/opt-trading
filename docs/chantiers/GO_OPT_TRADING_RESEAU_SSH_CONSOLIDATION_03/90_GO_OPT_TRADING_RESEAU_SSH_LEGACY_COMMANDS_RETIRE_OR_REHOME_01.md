---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
status: pass
mode: doc-only
surface: modules
source_kind: child_go_preparation
machine_owner: db-layer
---

# 90_GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01

## Goal

Decide the fate of the last three legacy WireGuard commands still living only in `scripts/reseau_ssh`.

## Commands in scope

- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

## Decision

All three commands are explicitly marked for retirement, not rehome.

## Why

- the active canonical workflow already exists in nested `step2`
- the active documentation already recommends the canonical workflow:
  - `wg-genkeys`
  - `wg-render`
  - `wg-apply`
  - `wg-up`
  - `wg-status`
- the legacy commands write directly to `/etc/wireguard/wg0.conf` and reflect an older operational model
- rehoming them would preserve parallel WireGuard workflows inside the same family, which conflicts with the one-module convergence goal

## Consequence

The next physical lot should remove these commands from the legacy backend and cut the remaining explicit escape-hatch references to that backend.

## Next GO

`GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_PHYSICAL_RETIREMENT_01`

## Verdict

`PASS`
