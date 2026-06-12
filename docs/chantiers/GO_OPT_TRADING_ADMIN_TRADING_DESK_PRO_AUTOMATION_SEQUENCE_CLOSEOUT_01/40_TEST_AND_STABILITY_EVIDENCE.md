---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01_TEST_EVIDENCE
doc_type: test_and_stability_evidence
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 40_TEST_AND_STABILITY_EVIDENCE - Test and Stability Evidence

## Tests

```text
PYTHONPATH=/opt/trading python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py -q
53 passed in 0.17s
```

## Stability evidence

- `>= 10` natural post-fix timer runs observed
- all observed stable runs exited `0/SUCCESS`
- all observed stable runs returned payload `WARN`
- `errors=[]` on observed stable runs
- accepted warnings only:
  - `desk_snapshot missing: timer-only synthesis`
  - `visual_context missing: snapshot-only synthesis`

## Safety evidence

- `no_trade=true`
- `no_telegram=true`
- `no_webhook=true`
- `no_systemd=true`
- no runtime trade, Telegram, webhook, or forbidden mutation observed

## RISKS

- À qualifier.
