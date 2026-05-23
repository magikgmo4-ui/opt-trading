---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: child_go_preparation
machine_owner: db-layer
---

# 85_GO_OPT_TRADING_RESEAU_SSH_LEGACY_BACKEND_EXIT_01

## Goal

Determine whether `scripts/reseau_ssh` can exit the active family flow, and if so under which proof gates.

## Established

- short aliases are already canonically published from `modules/reseau_ssh/scripts/*`
- low-risk baseline capabilities were absorbed into `modules/reseau_ssh`
- `scripts/reseau_ssh` is no longer the canonical family surface

## Blocking fact

`scripts/reseau_ssh` still remains the only repo-side implementation for explicit legacy commands:

- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`

It also still contains the legacy delegating installer:

- `scripts/reseau_ssh/install_reseau_ssh.sh`

## Decision

This GO cannot safely perform a physical backend exit yet.

## Needed next lot

`GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01`

## Verdict

`BLOCKED_WITH_REASON`
