---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: VALIDATION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_VALIDATION

## Minimal validation

```bash
git diff --check
python3 -m pytest tests/governance/test_machine_target_model_impl.py -q
git status --short --branch
```

## Expected results

- no registry mutation appears in the diff
- governance allowlist still passes unchanged
- only `mimo_open_observer` and chantier docs are touched
