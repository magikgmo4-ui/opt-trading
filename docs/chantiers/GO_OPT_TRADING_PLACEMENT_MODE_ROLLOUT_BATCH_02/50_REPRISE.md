---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 50_REPRISE

## Summary

- batch 02 qualifies `shared_sshfs_permanent`, `shared`, and `reseau_ssh`
- the residual allowlist is reduced to `mimo_open_observer` only
- the rollout remains bounded and avoids forcing a false precision where proof is still mixed

## Files touched

- `registry/modules_registry.yaml`
- `tests/governance/test_machine_target_model_impl.py`
- `docs/chantiers/GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02/*`

## Resume point

```text
CURRENT_GO = GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
STATUS = PR_OPENED_OR_READY
MODE = bounded registry/schema rollout

NEXT_IF_PASS:
GO_OPT_TRADING_REGISTRY_MODEL_P3_CLOSEOUT_01
```

## Verdict

`PASS`
