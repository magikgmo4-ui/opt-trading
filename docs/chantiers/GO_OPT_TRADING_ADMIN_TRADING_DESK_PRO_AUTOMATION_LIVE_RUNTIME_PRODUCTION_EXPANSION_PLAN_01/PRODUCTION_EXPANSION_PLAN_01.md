---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01
doc_type: production_expansion_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01
status: active
updated_at: 2026-05-13
---

# PRODUCTION_EXPANSION_PLAN_01

## 1_INITIAL_NEED

After production readiness review GO, plan a controlled expansion of Desk Pro dry-run runtime with reinforced quotas, windows, and safety guards.

## 4_MASTER_PROJECT_PLAN linkage

Depends on:
- PR #303 (dry-run/timer)
- PR #325 (artifact output)
- PR #347 (input enrichment)
- PR #349, #350 (smoke plan + exec)
- PR #353, #358 (controlled pilot)
- PR #360, #363 (limited production)
- PR #368 (readiness review GO)

## 6_FINAL_TARGET

Plan a **production expansion** GO with:
- increased quotas (2x current)
- extended windows (continuous, with monitoring)
- reinforced safety guards
- observability metrics
- automated kill-switch
- clear expansion limits

## 7_CANONICAL_STATE

- sot/mainline @ 0fcdfa3
- Readiness review: GO
- Timer: active/waiting since May 11, 5+ days continuous
- Service: exit 0/SUCCESS for all runs
- Errors: [], safety flags: all true
- STOP triggers: 0 across entire chain
- History: 196+ lines

## 8_VALIDATED_PLAN

Docs-only. No execution in this GO.

## 12_INVARIANTS

- No production free
- Guards remain active
- Kill-switch remains accessible
- No secret exposure
- No runtime artifacts committed

## Expansion perimeter

- Desk Pro dry-run only (same scope as limited production)
- No live trade, Telegram, webhook
- Observation + artifact generation only

## Expanded quotas

| Quota | Limited (current) | Expansion (proposed) |
| --- | --- | --- |
| Max runs/window | 96/day | 288/day (every 5min) |
| Max artifact size | 500MB | 2GB |
| Max consecutive WARN | 20 | 50 |
| Max FAIL/h | 1 | 2 |
| Max history/day | 1000 lines | 5000 lines |
| Max runtime before review | 7 days | 14 days |

## Rollout strategy

1. Phase 1: Double current quotas
2. Phase 2: If stable 48h, apply full expansion quotas
3. Stop + revert on any STOP trigger

## Conditions d'entrée

- Readiness review: GO
- Tests 84/84 on entry
- Safety flags true
- No pending rollback
- No STOP triggers in prior 48h

## Conditions de sortie

- STOP trigger fired
- Quota exceeded
- Manual kill-switch
- 14d review cycle

## Kill-switch

- `sudo systemctl stop desk_pro_dry_run.timer`
- `sudo systemctl disable desk_pro_dry_run.timer`

## Rollback

Full rollback: `KILL_SWITCH_AND_ROLLBACK_01.md` (same as limited production)

## Actions interdites

- `systemctl start desk_pro_dry_run.service`
- Edit installed systemd units
- Disable safety flags
- Trade, Telegram, webhook
- Secret exposure

## Next GO

After this plan merges:
`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_EXECUTION_01`
