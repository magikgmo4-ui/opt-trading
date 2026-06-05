---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01_ROLLBACK
doc_type: rollback_procedure
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 40_ROLLBACK_PROCEDURE - Rollback Procedure

## Rollback commande

```bash
sudo systemctl disable --now desk_pro_dry_run.timer || true
sudo rm -f /etc/systemd/system/desk_pro_dry_run.service
sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer || true
```

## Statut du rollback dans ce GO

- rollback prepare: YES
- rollback execute: NO
- raison: installation PASS, pas de demande explicite de retrait

## Verification post-rollback attendue

- `systemctl list-unit-files | grep desk_pro_dry_run` ne retourne rien
- `systemctl status desk_pro_dry_run.timer --no-pager` signale l'absence du timer
- `systemctl status desk_pro_dry_run.service --no-pager` signale l'absence du service

## RISKS

- À qualifier.
