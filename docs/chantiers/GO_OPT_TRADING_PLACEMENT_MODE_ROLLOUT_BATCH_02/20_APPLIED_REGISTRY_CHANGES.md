---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: APPLIED_REGISTRY_CHANGES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 20_APPLIED_REGISTRY_CHANGES

## Registry mutation scope

Only `registry/modules_registry.yaml` is changed.

## Net effect of batch 02

- 3 of the 4 deferred entries are now qualified
- the deferred allowlist shrinks to one entry: `mimo_open_observer`

## Interpretation after batch 02

- `shared` and `reseau_ssh` now expose a clearer dominant anchor
- `shared_sshfs_permanent` remains `any`, but no longer unqualified
- only `mimo_open_observer` remains intentionally underspecified pending a dedicated runtime/state clarification
