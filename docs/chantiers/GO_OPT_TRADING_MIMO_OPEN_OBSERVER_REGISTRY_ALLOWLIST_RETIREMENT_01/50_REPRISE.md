---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 50_REPRISE

## Summary

- `mimo_open_observer` no longer relies on the residual `machine_target:any` allowlist
- the module is now registry-anchored on `student`
- `placement_mode: single_host` records that the residual runnable surface is local to one dominant host, even though the module is archival-oriented

## Files touched

- `registry/modules_registry.yaml`
- `tests/governance/test_machine_target_model_impl.py`
- `docs/chantiers/GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01/*`

## Resume point

```text
CURRENT_GO = GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
STATUS = PR_OPENED_OR_READY
MODE = bounded registry cleanup

NEXT_IF_PASS:
PAUSE_REGISTRY_MODEL_WORK
```

## Verdict

`PASS`
