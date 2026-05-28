---
go_id: GO_OPT_TRADING_REGISTRY_MODEL_P3_CLOSEOUT_01
doc_type: APPLIED_MODEL_STATE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 20_APPLIED_MODEL_STATE

## Applied mutations across P3

### Source-of-truth layer

- readers expose `source_kind`
- readers expose `is_canonical_source`
- `ui_registry_msi` reports explicit fallback-seed degraded mode

### DeepSeek family outcome

- central representation stays on:
  - `deepseek_hub`
  - `deepseek_response`
  - `deepseek_thinking`
- `deepseek_student` receives no module registry entry
- no wrapper triplet is added for `deepseek_student`
- no UI surface registry entry is added for `deepseek_student`

### Machine / placement layer

- `placement_mode` exists as an optional field in `registry/modules_registry.yaml`
- batch 01 qualified:
  - portable readers/helpers
  - OpenClaw facades/bridges
  - `registry_router`
- batch 02 qualified:
  - `shared_sshfs_permanent`
  - `shared`
  - `reseau_ssh`

## Canonical current interpretation

### `machine_target`

- dominant compatible anchor
- still mandatory

### `placement_mode`

- optional but semantically authoritative when present
- allowed vocabulary:
  - `single_host`
  - `operator_entry`
  - `cross_host_facade`
  - `portable_tool`
  - `compatibility_shim`

### `machine_target: any`

- no longer accepted as an ambiguous shortcut
- valid only when qualified or explicitly deferred
