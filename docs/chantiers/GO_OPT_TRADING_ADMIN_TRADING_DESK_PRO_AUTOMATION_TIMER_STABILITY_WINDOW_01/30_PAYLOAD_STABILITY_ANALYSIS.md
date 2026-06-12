---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01_PAYLOAD
doc_type: payload_stability_analysis
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 30_PAYLOAD_STABILITY_ANALYSIS - Payload Stability Analysis

## Stable payload characteristics across observed runs

- `status=WARN`
- `errors=[]`
- warnings limited to:
  - `desk_snapshot missing: timer-only synthesis`
  - `visual_context missing: snapshot-only synthesis`
- `no_trade=true`
- `no_telegram=true`
- `no_webhook=true`
- `no_systemd=true`
- `source=tradingview.webhook`
- `event_type=signal_event`
- `engine=DESK_PRO_TIMER`
- `symbol=BTCUSDT`
- `timeframe=H1`
- `direction=BUY`
- `timestamp` present each run

## Stability verdict

Payload behavior is stable and contract-compatible over the observed natural run window.

## RISKS

- À qualifier.
