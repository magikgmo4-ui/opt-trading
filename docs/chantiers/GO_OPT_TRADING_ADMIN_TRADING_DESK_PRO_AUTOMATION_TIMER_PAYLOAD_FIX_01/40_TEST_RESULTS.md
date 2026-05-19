---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01_TEST_RESULTS
doc_type: test_results
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_TEST_RESULTS - Test Results

## Commands executed

```bash
bash -n modules/desk_pro/desk_pro_dry_run.sh
PYTHONPATH=/opt/trading python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py -q
PYTHONPATH=/opt/trading modules/desk_pro/desk_pro_dry_run.sh
```

## Results

- `bash -n`: PASS
- `pytest`: `53 passed in 0.19s`
- local script exit: `0`
- local script payload status: `WARN`

## Local payload observation

- `errors`: `[]`
- warnings include `desk_snapshot missing: timer-only synthesis`
- warnings include `visual_context missing: snapshot-only synthesis`
