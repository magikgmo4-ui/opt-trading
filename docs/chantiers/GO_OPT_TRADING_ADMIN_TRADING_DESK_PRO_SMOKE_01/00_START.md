---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: smoke_test
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Desk Pro Smoke Test

## GO

GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Base

- Branche: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01
- Source: origin/sot/mainline
- Contexte: GO_DESK_BRIDGE_RETRY_01 = PASS (pipeline Vision deverrouille)

## Objectif

Executer un smoke test Desk Pro en PAPER mode avec donnee fraiche, sans trading reel.

## Regles strictes

- PAPER mode uniquement
- Aucun ordre reel
- Aucun webhook declenche
- Aucun secret expose
- Aucun .env lu
- Backup /shared/desk_pro/latest/ avant run
