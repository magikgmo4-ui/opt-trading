---
doc_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01
status: blocked_with_reason
mode: doc-only
surface: modules
source_kind: final_canonization_gate
machine_owner: db-layer
---

# 95_GO_OPT_TRADING_RESEAU_SSH_ONE_MODULE_CANONIZATION_01

## Goal

Decide whether the SSH family can now be canonized as truly converged to one operational module.

## Result

It cannot be canonized as complete yet.

## Blocking facts

1. `modules/reseau_ssh/scripts/cmd.sh` still delegates `baseline-hostname` to `RESEAU_SSH_STEP1B_CMD`
2. `modules/reseau_ssh_step1b` is therefore still operationally relevant
3. `scripts/reseau_ssh` still keeps a bounded runtime role for:
   - `bootstrap`
   - `ssh-hardening-safe`
   - `ssh-lockdown`
   - `install_reseau_ssh.sh` legacy delegating installer

## Current truth

- `modules/reseau_ssh` is the canonical top-level SSH module
- most of the family has already converged to it
- but the family is not yet at the strict end state required for `ONE_MODULE_CANONIZATION`

## Next missing decisions

1. decide the fate of `baseline-hostname`
2. decide the final fate of legacy runtime transition helpers in `scripts/reseau_ssh`
3. decide whether the legacy installer is retired or archived

## Verdict

`BLOCKED_WITH_REASON`
