---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01_TARGET_MAP
doc_type: target_structure
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
status: pass
mode: doc-only
surface: modules
source_kind: forward_plan
machine_owner: db-layer
---

# 82_STEP1B_TARGET_ABSORPTION_MAP

## Target principle

Absorb baseline ownership into `modules/reseau_ssh` without forcing an all-at-once rewrite.

## Proposed target map

```text
modules/
  reseau_ssh/
    scripts/
      cmd.sh
      menu.sh
      baseline_apply.sh           <- absorbed from step1b/apply_linux.sh
      baseline_sanity.sh          <- absorbed from step1b/sanity_check.sh
      baseline_hostname.sh        <- optional later, only if retained
    templates/
      hosts.block                 <- absorbed from step1b
      ssh_config.linux            <- absorbed from step1b
    data/
      baseline_inventory.yaml     <- optional if inventory still needed
```

## Mapping detail

| Current step1b path | Canonical target path | Decision |
| --- | --- | --- |
| `.../scripts/apply_linux.sh` | `modules/reseau_ssh/scripts/baseline_apply.sh` | move/absorb |
| `.../scripts/sanity_check.sh` | `modules/reseau_ssh/scripts/baseline_sanity.sh` | move/absorb |
| `.../templates/hosts.block` | `modules/reseau_ssh/templates/hosts.block` | move/absorb |
| `.../templates/ssh_config.linux` | `modules/reseau_ssh/templates/ssh_config.linux` | move/absorb |
| `.../inventory.yaml` | `modules/reseau_ssh/data/baseline_inventory.yaml` | optional keep |
| `.../scripts/apply_hostname_linux.sh` | `modules/reseau_ssh/scripts/baseline_hostname.sh` | keep separate decision |

## Design rule

- the canonical facade `cmd.sh` should keep the public `baseline-*` command names
- only the implementation target should move from `step1b` to `modules/reseau_ssh`
- public behavior should stay stable during absorption

## Explicit non-goals

- no rename of public `baseline-*` commands in the same lot
- no deletion of `step1b` wrappers until delegation has been removed
- no Windows-side baseline expansion in this lot

## Verdict

`PASS`
