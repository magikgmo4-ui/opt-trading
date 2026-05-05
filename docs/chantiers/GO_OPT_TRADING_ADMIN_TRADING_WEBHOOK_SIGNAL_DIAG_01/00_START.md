---
doc_id: SIGNAL_DIAG_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 00_START — Webhook Signal Diagnosis

## GO

GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Contexte

WEBHOOK_RUNTIME_REVIEW_01 = PASS. Dernier POST /tv: April 1. 33 jours sans signal.

## Objectif

Diagnostiquer l'arret des signaux TradingView.

## Regles

- Read-only, pas de POST /tv, pas de trading
- Pas de secrets, pas de .env
