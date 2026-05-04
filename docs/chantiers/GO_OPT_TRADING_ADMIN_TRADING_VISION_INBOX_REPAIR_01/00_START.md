---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: repair
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Vision Inbox Repair

## GO

GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Base

- Branche: go/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
- Source: origin/sot/mainline
- Contexte: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01 = PASS

## Objectif

Reparer les entrees corrompues qui bloquent desk_bridge et desactiver le timer macro-xau obsolete.

## Regles strictes

- Quarantaine uniquement, pas de suppression directe
- Ne deplacer que fichiers 0-byte prouves et .uploading partiels
- Ne pas toucher aux fichiers valides
- Ne pas declencher de trading reel
- Ne pas exposer de secrets
- Ne pas reconstruire macro-xau
