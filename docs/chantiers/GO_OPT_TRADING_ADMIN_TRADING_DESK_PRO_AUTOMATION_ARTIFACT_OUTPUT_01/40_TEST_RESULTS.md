---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01_TEST_RESULTS
doc_type: test_results
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 40_TEST_RESULTS - Test Results

## Command

```bash
PYTHONPATH=/opt/trading python -m pytest \
  tests/test_signal_event_adapter.py \
  tests/test_admin_trading_contract_compatibility_smoke.py \
  tests/test_desk_pro_dry_run.py \
  tests/test_desk_pro_artifact_output.py \
  -q
```

## Result

```
62 passed in 0.31s
```

## Local script validation

- `bash -n`: PASS
- exit code: `0`
- `latest.json` produced: YES
- `latest.md` produced: YES
- `history.jsonl` produced: YES
- status: `WARN`
- `errors=[]`
- all safety flags true

## RISKS

- À qualifier.
