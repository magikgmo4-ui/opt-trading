---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_ROLLBACK
doc_type: rollback_readiness
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 50_ROLLBACK_READINESS - Rollback Readiness

## Rollback commands

```bash
sudo systemctl disable --now desk_pro_dry_run.timer || true
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer || true
```

## Rollback status in this GO

- rollback prepared: YES
- rollback executed: NO
- reason: timer entered expected waiting state and no forbidden side effect was observed

## Conditions for rollback

- timer or service enters critical error state
- forbidden side effect appears in logs
- explicit user request
- follow-up fix GO decides to revert timer activation

## RISKS

- À qualifier.
