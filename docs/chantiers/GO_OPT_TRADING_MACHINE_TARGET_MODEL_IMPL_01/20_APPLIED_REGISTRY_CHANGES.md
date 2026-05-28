---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: APPLIED_REGISTRY_CHANGES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 20_APPLIED_REGISTRY_CHANGES

## Registry mutation scope

Only `registry/modules_registry.yaml` is changed in this GO.

## Applied rule

- keep existing `machine_target`
- add optional `placement_mode` only for the selected first batch
- do not touch unrelated entries

## Expected interpretation after this GO

- `machine_target` remains the primary anchor field
- `placement_mode` clarifies whether a current `any` means portable tool or cross-host facade
- untouched `any` entries remain explicitly underspecified and should be audited later
