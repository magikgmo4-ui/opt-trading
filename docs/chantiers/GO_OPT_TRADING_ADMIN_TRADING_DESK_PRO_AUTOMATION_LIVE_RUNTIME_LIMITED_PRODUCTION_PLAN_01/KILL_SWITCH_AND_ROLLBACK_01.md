---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01_KILL_SWITCH
doc_type: kill_switch_and_rollback
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01
status: active
updated_at: 2026-05-13
---

# KILL_SWITCH_AND_ROLLBACK_01

## Kill-switch commands

```bash
sudo systemctl stop desk_pro_dry_run.timer
sudo systemctl disable desk_pro_dry_run.timer
```

## Full rollback

```bash
sudo systemctl disable --now desk_pro_dry_run.timer
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer
```

## Activation conditions

- Any safety flag becomes `false`
- Quota exceeded
- Manual override requested
- Consecutive FAIL >= 3
- Secret leak detected
