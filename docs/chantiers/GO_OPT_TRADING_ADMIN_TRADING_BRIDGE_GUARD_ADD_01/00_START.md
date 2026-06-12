---
doc_id: BRIDGE_GUARD_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: hardening
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Bridge Guard

## GO

GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

go/GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01

## Contexte

- INTEGRATION_SMOKE_01 = PASS (pipeline stable)
- desk_bridge crashait sur PIL.UnidentifiedImageError avant VISION_INBOX_REPAIR
- Headless capture ecrit atomiquement, mais ShareX/SFTP reste fallback

## Objectif

Empecher les crashs PIL sur fichiers 0-byte/.uploading.

## Regles

- Patch minimal
- Pas de refactor global
- Pas de modification downstream

## RISKS

- À qualifier.
