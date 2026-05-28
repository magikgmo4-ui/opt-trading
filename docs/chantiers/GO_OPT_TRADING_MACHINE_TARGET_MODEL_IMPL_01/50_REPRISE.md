---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 50_REPRISE

## Summary

- first compatible `placement_mode` batch applied in `registry/modules_registry.yaml`
- `modules_registry_reader` exposes `placement_mode`
- governance tests now protect the refined `machine_target:any` contract

## Files touched

- `registry/modules_registry.yaml`
- `modules/modules_registry_reader/app/modules_registry_reader.py`
- `tests/governance/test_machine_target_model_impl.py`
- `docs/chantiers/GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01/*`

## Resume point

```text
CURRENT_GO = GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
STATUS = PR_OPENED_OR_READY
MODE = bounded registry/schema implementation
NEXT_IF_PASS = registry placement-mode rollout batch 02 or P3 closeout
```

## Verdict

`PASS`
