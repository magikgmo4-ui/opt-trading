---
go_id: GO_OPT_TRADING_MACHINE_TARGET_MODEL_IMPL_01
doc_type: VALIDATION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 40_VALIDATION

## Minimal validation

```bash
python3 -m pytest tests/governance -q
git diff --check
git status --short --branch
```

## Expected results

- governance tests pass
- `placement_mode` is visible in modules reader output
- no unrelated registry file is changed
- `secrets/` remains untouched
