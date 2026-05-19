---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_EXECUTION_01_QUOTA
doc_type: quota_observations
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01
status: active
updated_at: 2026-05-14
---

# QUOTA_OBSERVATIONS_01

| Quota | Phase 1 limit | Observed | Headroom | Notes |
| --- | --- | --- | --- | --- |
| Max runs/day | 192 | ~20 in ~5h | 172 | Timer self-regulating at 4 runs/h |
| Max artifact size | 1GB | ~0.2MB | ~1023MB | Well within limits |
| Max history/day | 2500 lines | ~20/h | ~2300 | Linear growth expected |
| Max FAIL/h | 1 | 0 | OK | Clean runs |
| Max consecutive WARN | 35 | continuous | OK | Expected WARN (visual_context missing) |

All quotas well within Phase 1 limits.
