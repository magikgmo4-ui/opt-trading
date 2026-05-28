---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: VALIDATION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
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

- batch 02 changes pass governance tests
- the allowlist shrinks to the minimal residual case
- no unrelated registry file is touched
