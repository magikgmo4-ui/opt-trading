---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01
status: pass
mode: doc-only
surface: modules
source_kind: child_go_preparation
machine_owner: db-layer
---

# 80_GO_OPT_TRADING_RESEAU_SSH_STEP1B_ABSORPTION_OR_RETIREMENT_01

## Goal

Decide how each remaining `step1b` baseline capability should evolve so the SSH family can converge toward one top-level module without premature deletion.

## Established

- `modules/reseau_ssh` remains the canonical top-level SSH module
- `modules/reseau_ssh_step1b` is still live because `baseline-*` commands in `modules/reseau_ssh/scripts/cmd.sh` delegate to it
- nested `reseau_ssh_step2` remains the active WireGuard/firewall implementation
- no repo proof was found of non-doc direct callers requiring `*_step1b` public aliases

## Scope of this GO

- baseline command family only
- no WireGuard changes
- no legacy backend exit yet
- no registry changes

## Decision summary

| Capability | Current decision |
| --- | --- |
| `baseline-dry-run` | `ABSORB_INTO_CANONICAL` |
| `baseline-apply` | `ABSORB_INTO_CANONICAL` |
| `baseline-hostname` | `KEEP_TRANSITIONALLY_THEN_REVIEW` |
| `baseline-sanity` | `ABSORB_OR_INLINE` |
| `baseline-show-hosts` | `ABSORB_AS_READONLY_ASSET` |
| `baseline-show-ssh` | `ABSORB_AS_READONLY_ASSET` |
| `menu/cmd/sanity-reseau_ssh_step1b` wrappers | `RETIRE_AFTER_BASELINE_COMMAND_EXIT` |

## Why

- the baseline capabilities are family-adjacent and belong conceptually inside the canonical SSH module
- most of `step1b` is shell/templates and can be absorbed incrementally
- the hostname mutation path is the only sub-capability that still deserves special caution because it changes machine identity

## Required outputs

- capability matrix
- absorption target map
- retirement gates
- next physical GO prompt

## Next physical GO

`GO_OPT_TRADING_RESEAU_SSH_STEP1B_PHYSICAL_ABSORPTION_01`

## Verdict

`PASS`
