---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01_SPEC
doc_type: payload_fix_spec
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_PAYLOAD_FIX_SPEC - Payload Fix Spec

## Compatible timer payload shape

Le timer doit produire un payload V0 minimal accepte par `normalize_signal_event_v1`:

```python
{
  "engine": "DESK_PRO_TIMER",
  "signal": "BUY",
  "symbol": "BTCUSDT",
  "tf": "H1",
  "_ts": "<iso8601 utc>",
}
```

## Expected dry-run result

- `signal_event` normalise en V1 canonique
- `status` global: `WARN` si seuls `desk_snapshot` et `visual_context` manquent
- `errors`: `[]`
- `warnings`: snapshot/visual context manquants
- `no_trade`, `no_telegram`, `no_webhook`, `no_systemd`: `true`

## RISKS

- À qualifier.
