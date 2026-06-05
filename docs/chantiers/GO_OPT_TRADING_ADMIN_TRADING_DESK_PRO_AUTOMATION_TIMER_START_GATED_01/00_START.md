---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
lifecycle_stage: start
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
parent_commit: baf586c
---

# 00_START - Timer Start Gated

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01` - PASS, pushed as `baf586c`

## Objectif

Demarrer uniquement `desk_pro_dry_run.timer`, observer l'etat systemd obtenu, et confirmer qu'aucun live runtime smoke ni start manuel du service n'a ete effectue.

## Scope

- prestart gates
- `systemctl start desk_pro_dry_run.timer`
- observation post-start
- journal et artefacts passifs
- rollback readiness uniquement

## RISKS

- À qualifier.
