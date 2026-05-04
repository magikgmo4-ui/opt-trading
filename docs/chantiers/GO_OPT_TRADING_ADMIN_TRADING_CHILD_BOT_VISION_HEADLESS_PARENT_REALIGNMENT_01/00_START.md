---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: realignment
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Bot Vision Headless Parent Realignment

## GO

GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01

## Parent canonique

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN, machine admin-trading)

## Branche

go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01
Base: origin/sot/mainline

## Probleme

Un review bot_vision_headless precedent a cree un parent specialise:
`GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01`

Ce parent n'est pas conforme au plan:
- Le plan post-PR197 dit: 1 parent par machine
- admin-trading a deja `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- Un deuxieme parent admin-trading cree une fragmentation
- bot_vision_headless est un workstream sous admin-trading, pas un parent autonome

## Objectif

- Ratacher bot_vision_headless comme child/workstream sous GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
- Classer le parent specialise comme absorbed/reclassified
- Preparer le child impl: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01
- Aucun runtime modifie

## Regles strictes

- Doc-only
- Aucun runtime
- Aucune suppression brutale
- Aucun index patch force
- Aucun nouveau parent admin-trading
