---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01_TIMER_SPEC
doc_type: timer_spec
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_TIMER_SPEC - Timer Requirements

## Timer definition

### desk_pro_dry_run.timer

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

### desk_pro_dry_run.service

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

## Frequency

| Parameter | Value | Justification |
| --- | --- | --- |
| `OnBootSec` | 5min | Attendre boot stable, network pret |
| `OnUnitActiveSec` | 15min | Assez frequent pour reactivite, pas surcharge |

## Safety gates

### Runtime guards

1. **no_trade** — Aucune action de trading
2. **no_telegram** — Pas de notification Telegram live
3. **no_webhook** — Pas de webhook外部
4. **no_systemd** — Timer inactive par defaut

### Pre-execution checks

- `DRY_RUN_MODE=true` requis
- Fichiers de config obligatoires
- Validation des contrats avant execution

## Execution flow

```
timer (15min) 
  → service desk_pro_dry_run.service 
    → desk_pro_dry_run.sh -m dry-run
      → modules/desk_pro/dry_run.py
        → output JSON synthesis
```

## Next step

Timer spec est **docs-only**. Prochain GO: `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01`