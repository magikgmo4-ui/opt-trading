---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: APPLIED_REGISTRY_CHANGE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 20_APPLIED_REGISTRY_CHANGE

## Applied change

For `mimo_open_observer`:

- change `machine_target` from `any` to `student`
- add `placement_mode: single_host`

## Why `single_host`

The residual runnable assets, archival override flow, and historical strategic classification all point to one dominant machine anchor: `student`.

The module is not a portable tool, not a cross-host facade, and not a compatibility shim.

## What this GO does not change

- `status` remains unchanged
- no wrapper registry mutation
- no UI surface registry mutation
- no new status vocabulary introduced
