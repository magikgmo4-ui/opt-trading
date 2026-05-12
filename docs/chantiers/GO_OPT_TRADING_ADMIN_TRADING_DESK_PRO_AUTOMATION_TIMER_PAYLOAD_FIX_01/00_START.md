---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01
status: active
lifecycle_stage: start
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
parent_commit: 3830fda
---

# 00_START - Timer Payload Fix

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01` - PASS, pushed as `3830fda`

## Objectif

Corriger le payload d'entree du timer dry-run pour obtenir un resultat contract-compatible `PASS` ou `WARN`, sans start manuel du service.

## Safety gate

- timer pause avant patch: requis
- aucun start manuel du service
- tests locaux obligatoires
