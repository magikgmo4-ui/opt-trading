---
doc_id: INTEGRATION_SMOKE_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: integration_smoke
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Bot Vision Headless Integration Smoke

## GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01
Base: origin/sot/mainline

## Contexte

- BOT_VISION_HEADLESS_SYSTEMD_01 = PASS (timer 10 min actif)
- DESK_BRIDGE_RETRY_01 = PASS (pipeline deverrouille)
- DESK_PRO_SMOKE_01 = PASS (11/11 OK)

## Objectif

Valider l'integration complete: headless capture → vision_bot → desk_bridge → Desk Pro.

## Regles

- PAPER mode uniquement
- Pas de trading reel
- Pas de modification de code
- ShareX fallback conserve
