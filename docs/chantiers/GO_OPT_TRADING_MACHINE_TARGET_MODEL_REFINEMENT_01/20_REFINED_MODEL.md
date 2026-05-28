---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_REFINEMENT_01
doc_type: REFINED_MODEL
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 20_REFINED_MODEL

## Keep

Keep `machine_target` as the primary required field in central registries.

Meaning:

- the dominant machine anchor for the object
- the simplest first answer to "where does this primarily belong?"

This preserves compatibility with existing readers, tables, and exports.

## Add in follow-up implementation

Introduce one complementary field for machine semantics.

Recommended name:

- `placement_mode`

## Proposed `placement_mode` vocabulary

### `single_host`

Object primarily belongs to one concrete machine and behaves there.

Examples:
- `deepseek_response` on `student`
- `desk_pro_runner` on `admin_trading`

### `operator_entry`

Object is exposed mainly as an operator-facing entrypoint on the declared machine, even if downstream runtime spans elsewhere.

Examples:
- `deepseek_hub` on `msi_db_layer`
- `ops_menu_hub` on `msi_db_layer`

### `cross_host_facade`

Object is a facade, bridge, or control surface whose value spans multiple machines, but still has one dominant machine anchor.

Examples:
- `gateway_openclaw`
- `openclaw_operator_bridge`

### `portable_tool`

Object is genuinely machine-agnostic or intentionally portable.

This is the main safe successor for many current `any` entries.

Examples:
- pure validators
- documentation/governance helpers
- readers that are intentionally repo-portable

### `compatibility_shim`

Object exists mainly for backward compatibility and should not be mistaken for the canonical runtime owner.

This is useful for future cases like shim layers, but should be introduced in implementation only where truly needed.

## Rule for `any`

After refinement, `any` should remain acceptable only when:

1. the object is genuinely portable, and
2. `placement_mode = portable_tool`

If the object is cross-machine, facade-like, or compatibility-oriented, `any` alone is no longer enough.
