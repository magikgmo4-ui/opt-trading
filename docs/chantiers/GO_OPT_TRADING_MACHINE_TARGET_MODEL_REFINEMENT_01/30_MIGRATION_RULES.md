---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: MIGRATION_RULES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_MIGRATION_RULES

## Backward-compatible migration policy

1. do not remove `machine_target`
2. do not replace existing readers in one step
3. add `placement_mode` first as optional
4. migrate current `any` entries in small audited batches

## Interpretation policy during transition

### Case A - `machine_target != any` and no `placement_mode`

Interpret as legacy-compatible `single_host` unless docs say otherwise.

### Case B - `machine_target = any` and no `placement_mode`

Interpret as underspecified, not as automatically correct.

It should trigger later audit or refinement.

### Case C - `machine_target` present with `placement_mode`

Use the pair as the canonical semantic read.

## Reader implications

1. `modules_registry_reader` should later display both `machine_target` and `placement_mode`
2. `ui_registry_msi` may later group by target, by placement mode, or both
3. governance tests should later reject new ambiguous `any` entries unless explicitly allowed

## Decision on cross-machine modeling

This GO does not recommend `machine_targets` as the first refinement.

Reason:

- it is heavier to adopt
- it risks looking more precise than current governance can truly support
- one dominant anchor plus one mode is enough for the next iteration
