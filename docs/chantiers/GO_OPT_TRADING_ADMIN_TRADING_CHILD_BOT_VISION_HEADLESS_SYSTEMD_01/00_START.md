---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: implementation
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Bot Vision Headless Systemd Automation

## GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01

## Parent canonique

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01
Base: origin/sot/mainline

## Contexte

GO_BOT_VISION_HEADLESS_IMPL_01 = PASS (module capture fonctionnel)
Module: modules/bot_vision/headless_capture/
Playwright 1.59.1 + Chromium 147 installes

## Objectif

Automatiser la capture headless via systemd timer.

## Regles strictes

- Parent: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
- Ne pas modifier services critiques
- Ecriture atomique preservee
- ShareX = fallback conserve
- Freq initiale: 10 min
