---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: retry
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Desk Bridge Retry

## GO

GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Base

- Branche: go/GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01
- Source: origin/sot/mainline
- Contexte: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01 = PASS

## Objectif

Relancer desk_bridge apres nettoyage de l'inbox vision pour confirmer que le pipeline n'est plus bloque par les inputs corrompus.

## Regles strictes

- Pas de trading reel
- Pas de webhook declenche
- Pas de redemarrage des services critiques
- Pas de suppression de fichiers
- Pas d'exposition de secrets
- Executer uniquement l'entrypoint prouve
