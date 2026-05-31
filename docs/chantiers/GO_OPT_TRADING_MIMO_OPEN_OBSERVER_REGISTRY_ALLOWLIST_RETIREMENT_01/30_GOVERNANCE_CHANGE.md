---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: GOVERNANCE_CHANGE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 30_GOVERNANCE_CHANGE

## Test tightening

`tests/governance/test_machine_target_model_impl.py` removes `mimo_open_observer` from the deferred allowlist.

## New steady state

- no residual allowlist entry remains for `machine_target:any`
- unqualified `any` is now fully eliminated from the previous P3 residual set
