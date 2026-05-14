---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01_SAFETY
doc_type: safety_guards_kill_switch
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01
status: active
updated_at: 2026-05-13
---

# SAFETY_GUARDS_AND_KILL_SWITCH_01

## Active guards (unchanged from limited production)

- `no_trade=true` mandatory
- `no_telegram=true` mandatory
- `no_webhook=true` mandatory
- `no_systemd=true` mandatory

## Kill-switch

```bash
sudo systemctl stop desk_pro_dry_run.timer
sudo systemctl disable desk_pro_dry_run.timer
```

## Rollback

```bash
sudo systemctl disable --now desk_pro_dry_run.timer
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
```

## STOP triggers (unchanged)

- Any safety flag becomes `false`
- Quota exceeded
- Manual kill-switch
- Consecutive FAIL >= 3
- Secret leak
