---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: VALIDATION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 40_VALIDATION

## Minimal validation

```bash
python3 -m pytest tests/governance/test_machine_target_model_impl.py -q
python3 -m pytest tests/governance -q
git diff --check
git status --short --branch
```

## Expected results

- no allowlist entry remains for `mimo_open_observer`
- the registry module entry is no longer `machine_target:any`
- governance tests still pass
