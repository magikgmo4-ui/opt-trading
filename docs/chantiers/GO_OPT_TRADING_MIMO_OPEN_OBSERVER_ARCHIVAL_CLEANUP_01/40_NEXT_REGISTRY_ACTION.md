---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: NEXT_REGISTRY_ACTION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 40_NEXT_REGISTRY_ACTION

## Next registry GO if cleanup is accepted

- `GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01`

## Goal of that GO

1. remove `mimo_open_observer` from the residual allowlist
2. decide whether the module registry entry should become explicitly archival-facing or be removed from active central representation
3. keep this decision separate from the runtime cleanup already done here
