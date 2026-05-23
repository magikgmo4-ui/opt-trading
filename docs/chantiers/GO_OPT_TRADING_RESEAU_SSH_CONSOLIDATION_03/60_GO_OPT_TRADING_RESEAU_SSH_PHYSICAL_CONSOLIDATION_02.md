---
doc_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02
doc_type: go_preparation
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02
status: ready_for_execution
mode: doc-only
surface: modules
source_kind: child_go_preparation
machine_owner: db-layer
---

# 60_GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02

## Goal

Prepare the minimal physical consolidation lot that improves repo clarity around the SSH family without breaking the current runtime contract.

## Preconditions already satisfied

- `GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 = PASS`
- top-level canonical module is established as `modules/reseau_ssh`
- nested `reseau_ssh_step2` is established as active internal implementation
- `modules/reseau_ssh_step1b` is established as transitional prerequisite
- `scripts/reseau_ssh` is established as bounded rollback path

## Strict scope

Allowed in the physical GO:

1. remove duplicate publisher ambiguity around `*_step2` installers
2. clarify README and status files so they all point to the same canon
3. reduce path confusion between canonical facade and nested implementation
4. preserve current short aliases and current command contract

Forbidden in the physical GO:

1. deleting `modules/reseau_ssh_step1b`
2. archiving `scripts/reseau_ssh`
3. changing `registry/modules_registry.yaml`
4. changing the public short aliases away from `modules/reseau_ssh/scripts/*`
5. removing `baseline-*` while they still route to `step1b`
6. flattening nested `reseau_ssh_step2` into a new top-level module in one shot

## Minimal physical edits expected

| Area | Minimal target | Why |
| --- | --- | --- |
| `modules/reseau_ssh/scripts/install_shortcuts.sh` and nested `step2` installer | keep one clear compat publisher for `*_step2` aliases | remove duplicate installer ambiguity |
| README/status docs in `modules/reseau_ssh`, `modules/reseau_ssh_step1b`, `scripts/reseau_ssh` | align wording with current canonical split | remove contradictory operator guidance |
| optional comments / notes in shell installers | make intended ownership explicit | reduce future re-confusion |

## Verification gate for the physical GO

The physical GO must prove after edits:

1. `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` still resolve to `modules/reseau_ssh/scripts/*`
2. `baseline-*` commands still route successfully to `step1b`
3. `wg-*` and `fw-*` commands still route successfully to nested `step2`
4. `scripts/reseau_ssh/install_reseau_ssh.sh` remains a safe delegating compat entrypoint if kept
5. no registry diff is introduced

## Expected output of the physical GO

- clearer single-owner publication model
- fewer duplicate installers
- unchanged operator contract
- unchanged registry
- unchanged historical baseline references

## Execution prompt

```text
GO_OPT_TRADING_RESEAU_SSH_PHYSICAL_CONSOLIDATION_02

Role: repo consolidator.
Repo: opt-trading.
Base: sot/mainline.
Mode: minimal physical change.

Mission:
Apply the smallest safe physical cleanup for the SSH family after unified-module framing PASS.

Read first:
- docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01.md
- docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/10_CALLERS_AUDIT.md
- docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/20_WRAPPERS_AUDIT.md
- docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/30_TARGET_STRUCTURE.md
- docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/40_COMPATIBILITY_DECISION.md

Allowed changes:
- deduplicate step2 wrapper publishers
- clarify README/status/installers ownership
- small shell-script comments or path clarifications

Forbidden changes:
- no deletion of step1b
- no archive move of scripts/reseau_ssh
- no registry changes
- no runtime contract break on short aliases
- no removal of baseline-* commands

Verification:
- prove short alias target stability
- prove baseline-* still delegates to step1b
- prove wg/fw commands still delegate to nested step2
```

## Verdict

`READY_FOR_EXECUTION`
