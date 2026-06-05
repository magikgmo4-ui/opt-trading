---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01_TIMER_REVAL
doc_type: timer_revalidation
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 50_TIMER_REVALIDATION - Timer Revalidation

## Timer stopped before patch

- stopped before patch: YES
- timer inactive after stop: YES
- service inactive after stop: YES

## Timer restarted

- restarted after fix: YES
- state after restart: `active (waiting)`
- next trigger visible: `Mon 2026-05-11 22:00:26 EDT`
- service manual start: NO

## Observation

The installed service `ExecStart` points to the repo script `modules/desk_pro/desk_pro_dry_run.sh` — which now writes to `/opt/trading/runtime/desk_pro_dry_run/` by default. The next natural trigger will produce the new artifacts.

## RISKS

- À qualifier.
