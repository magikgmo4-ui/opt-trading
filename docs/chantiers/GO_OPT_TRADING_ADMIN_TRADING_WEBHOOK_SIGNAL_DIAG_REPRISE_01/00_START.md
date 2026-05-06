---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
lifecycle_stage: diagnostics
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 00_START - Admin Trading Webhook Signal Diagnostics Reprise

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01`

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`

## Previous GO

`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01`

## Base branch utilisee

- source: `origin/go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01`
- base tip confirme: `0a0b01c docs: open admin-trading webhook runtime review`
- branche locale de reprise: `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01`

## Objectif

Diagnostiquer en read-only les signaux produits par le webhook `TradingView -> /tv`, formaliser le contrat canonique `signal_event` V1, et verifier sa compatibilite consumer pour la suite du plan contract-first sans mutation runtime ni alerte reelle.

## Invariants

- ne pas modifier le runtime
- ne pas start, stop, restart ou reload de service
- ne pas declencher de webhook reel
- ne pas envoyer Telegram
- ne pas lire ni afficher `.env`
- ne pas committer `journal.md`
- ne pas committer `..env.swp`
- ne pas toucher `modules/bot_vision/headless_capture/`
- ne pas melanger `cursor-ai`, `db-layer`, `student` ou `fantome`
- diagnostic documentaire et read-only seulement

## Runtime side effects attendus

`NONE`

## Note de branche

La branche distante `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` existe deja. Cette ouverture se fait donc en reprise propre sur `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01`.
