---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_STATE_CLARIFICATION_01
doc_type: NEXT_ACTION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 40_NEXT_ACTION

## Recommended next GO

- `GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01`

## Why archival cleanup first

The dominant ambiguity is no longer generic registry modeling.

It is whether the remaining runnable assets should still exist as an active supported line at all.

If archival cleanup confirms retirement, then:

- remove the residual allowlist entry
- remove or realign the module registry entry in a dedicated follow-up GO if needed

## Alternative if the module must survive

- `GO_OPT_TRADING_MIMO_OPEN_OBSERVER_PLACEMENT_MODE_REALIGNMENT_01`

Use this only if a concrete product/runtime decision explicitly keeps the module alive as a supported student-side line.

## Registry consequence today

Keep the allowlist entry for `mimo_open_observer`.

Do not mutate `machine_target` or add `placement_mode` in this GO.
