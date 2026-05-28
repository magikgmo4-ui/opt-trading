---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: NEXT_IMPL_GO
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 40_NEXT_IMPL_GO

## Recommended next implementation GO

- `GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01`

## Expected scope of that GO

1. extend central registry schema and docs with optional `placement_mode`
2. audit current `machine_target: any` entries and classify them
3. update readers and governance tests to expose the refined pair
4. leave `machine_target` in place for compatibility

## First migration candidates

Good first candidates are entries currently using `any` in `registry/modules_registry.yaml`, especially:

- registry readers
- OpenClaw facades/bridges
- operator tools that are truly portable vs merely cross-host

## Non-goal for the next GO

- no full multi-target matrix yet
- no forced rewrite of every registry entry in one batch
- no coupling with `legacy/transitional` rollout unless a concrete entry requires both at once
