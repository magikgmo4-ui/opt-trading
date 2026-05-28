---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: TARGET_DELTA
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 10_TARGET_DELTA

## Selected first batch

### `placement_mode: portable_tool`

- `validated_prompt_factory`
- `trae_module_validator`
- `workflow_post_change_v2`
- `modules_registry_reader`
- `machines_registry_reader`
- `wrappers_registry_reader`
- `registry_meta_reader`

## Why portable_tool

These entries are intentionally repo-portable helpers or readers. Their current `machine_target: any` is acceptable only if it is made explicit that they are not cross-host facades.

### `placement_mode: cross_host_facade`

- `gateway_openclaw`
- `openclaw_config_modulaire`
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `install_module_openclaw`
- `openclaw_operator_bridge`
- `registry_router`

## Why cross_host_facade

These entries span operator/runtime concerns across machines or act as bounded facades toward other surfaces. Their current `machine_target: any` was too ambiguous.

## Explicitly deferred from this GO

- `mimo_open_observer`
- `shared_sshfs_permanent`
- `shared`
- `reseau_ssh`

Reason:

Their anchor semantics still deserve a more specific audit before assigning `placement_mode`.
