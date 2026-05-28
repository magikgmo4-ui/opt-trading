---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: READER_AND_TEST_CHANGES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_READER_AND_TEST_CHANGES

## Reader change

`modules_registry_reader` now displays `placement_mode` in its tabular list output.

This keeps compatibility:

- `machine_target` still exists and stays primary
- entries without `placement_mode` render with `N/A`

## Governance tests

The new tests validate that:

1. every module entry still has `machine_target`
2. `placement_mode` is optional
3. if present, `placement_mode` must belong to the approved vocabulary
4. `machine_target: any` must either be paired with an approved `placement_mode`, or belong to an explicit deferred allowlist for later audit
5. the reader prints the new column without breaking existing loading behavior
