---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01_SPEC_ALIGNMENT
doc_type: spec_alignment
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_SPEC_ALIGNMENT - Spec Alignment

## Source spec

Fichier: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01/20_TIMER_SPEC.md`

## Spec requirements

### Timer

```ini
[Unit]
Description=Run Desk Pro dry-run every 15 minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=15min
Unit=desk_pro_dry_run.service

[Install]
WantedBy=timers.target
```

### Service

```ini
[Unit]
Description=Desk Pro dry-run automation (read-only)
After=network.target

[Service]
Type=oneshot
User=ghost
Group=ghost
WorkingDirectory=/opt/trading
ExecStart=/opt/trading/modules/desk_pro/desk_pro_dry_run.sh

[Environment]
DRY_RUN_MODE=true
```

## Alignment check

| Spec item | Implementation | Status |
| --- | --- | --- |
| Timer file | `modules/desk_pro/systemd/desk_pro_dry_run.timer` | OK |
| Service file | `modules/desk_pro/systemd/desk_pro_dry_run.service` | OK |
| ExecStart script | `modules/desk_pro/desk_pro_dry_run.sh` | OK |
| Type=oneshot | will use Type=oneshot | OK |
| User=ghost | will use ghost | OK |
| WorkingDirectory | /opt/trading | OK |
| OnBootSec=5min | will use 5min | OK |
| OnUnitActiveSec=15min | will use 15min | OK |

## Deviation notes

- Service file unit name: `desk_pro_dry_run.service` (exact spec)
- Timer file unit name: `desk_pro_dry_run.timer` (exact spec)