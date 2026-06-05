---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01_SYSTEMD_VISIBILITY
doc_type: systemd_visibility
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_SYSTEMD_VISIBILITY - Systemd Visibility

## Unit files installes

- source service: `modules/desk_pro/systemd/desk_pro_dry_run.service`
- source timer: `modules/desk_pro/systemd/desk_pro_dry_run.timer`
- destination service: `/etc/systemd/system/desk_pro_dry_run.service`
- destination timer: `/etc/systemd/system/desk_pro_dry_run.timer`

## Unit file states

```text
desk_pro_dry_run.service  static  -
desk_pro_dry_run.timer    enabled enabled
```

## Timer status

```text
Loaded: loaded (/etc/systemd/system/desk_pro_dry_run.timer; enabled; preset: enabled)
Active: inactive (dead)
Trigger: n/a
Triggers: desk_pro_dry_run.service
```

## Service status

```text
Loaded: loaded (/etc/systemd/system/desk_pro_dry_run.service; static)
Active: inactive (dead)
TriggeredBy: desk_pro_dry_run.timer
```

## Installed content visibility

`systemctl cat` confirme que le host expose exactement les definitions versionnees du repo pour `OnBootSec=5min`, `OnUnitActiveSec=15min`, `Type=oneshot`, `User=ghost`, `WorkingDirectory=/opt/trading` et `ExecStart=/opt/trading/modules/desk_pro/desk_pro_dry_run.sh`.

## RISKS

- À qualifier.
