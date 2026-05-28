---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: CURRENT_STATE_AUDIT
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 10_CURRENT_STATE_AUDIT

## Registry facts

1. `registry/machines_registry.yaml` defines a small stable machine catalog:
- `admin_trading`
- `msi_db_layer`
- `dell_cursor_ai`
- `student`
- `debian_network_future`

2. `registry/modules_registry.yaml` still uses `machine_target: any` in many entries as a coarse placeholder.

3. `registry/ui_surfaces_registry.yaml` remains single-target only.

## Reader/UI facts

1. `modules_registry_reader` prints one `machine_target` column only.
2. `ui_registry_msi` groups surfaces by one `machine_target` key only.
3. No current central reader models cross-machine placement explicitly.

## Meaning problem

The current field mixes at least four distinct ideas:

1. where the main runtime lives
2. where the operator enters
3. where a facade or router is exposed
4. whether the surface is portable or multi-machine

## Why `any` became overloaded

`any` is currently used for several different situations:

- truly machine-agnostic helper or governance tools
- modules whose runtime can be launched from multiple machines
- modules whose target was not modeled precisely enough
- facade or bridge modules spanning several locations

These are not the same thing and should no longer be collapsed into one bucket.
