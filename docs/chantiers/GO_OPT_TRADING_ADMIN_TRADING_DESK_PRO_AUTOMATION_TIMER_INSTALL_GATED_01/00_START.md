---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01
status: active
lifecycle_stage: start
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01
parent_commit: 8369fa2
---

# 00_START - Timer Install Gated

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01` - PASS, pushed as `8369fa2`

## Objectif

Installer de facon controlee les fichiers systemd versionnes pour Desk Pro dry-run, sans start et sans live runtime smoke.

## Scope

- installer `desk_pro_dry_run.service`
- installer `desk_pro_dry_run.timer`
- recharger systemd
- valider l'etat installe
- preparer le rollback

## Gates

- dry-run uniquement
- aucun trade
- aucun webhook reel
- aucun Telegram
- aucun live runtime smoke
