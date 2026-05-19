---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: implementation
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Bot Vision Headless Implementation

## GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01

## Parent canonique

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
Base: origin/sot/mainline

## Contexte

7 GO admin-trading PASS precedents, incluant:
- DESK_PRO_SMOKE_01 (PASS, Desk Pro 11/11)
- VISION_INBOX_REPAIR_01 (PASS, inbox propre)
- BOT_VISION_HEADLESS_REVIEW_01 (PASS, faisabilite confirmee)
- BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01 (PASS, rattachement corrige)

## Objectif

Implementer V1 de bot_vision_headless: capture Playwright/Chromium avec ecriture atomique vers vision_inbox.

## Regles strictes

- Parent: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
- Ne pas creer de nouveau parent
- ShareX = fallback conserve
- desk_bridge et Desk Pro inchanges
- Aucun trading reel
- Ecriture atomique obligatoire
- Aucun .env expose
