---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_BRANCH_STATE
doc_type: branch_state
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# BRANCH_STATE

## Current branch

- Doc-only repair continues on `go/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01`.
- Runtime split branch: `go/runtime-non-trading-workers-01`.

## Decision

- `#676` remains blocked until governance repair is complete.
- Runtime changes are not in merge scope for `#676`.

## Next actions

1. Finaliser recanonisation parent.
2. Push clean doc-only diff.
3. Update PR #676 body.
4. Open runtime PR separately.
