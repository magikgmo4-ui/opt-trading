---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
parent_go: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
lifecycle_stage: review
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 00_START - Admin Trading Webhook Runtime Review Reprise

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01`

## Parent GO

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`

## Base branch utilisee

- source: `origin/go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`
- parent tip confirme: `da57788 docs: add admin-trading child GO operating plan`
- branche locale de reprise: `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01`

## Objectif

Auditer en read-only le runtime `Webhook / TradingView / alertes` sur `admin-trading`, confirmer la surface active, les ports, les endpoints visibles et produire un premier brouillon du contrat producer `signal_event` sans mutation runtime.

## Invariants

- ne pas modifier le runtime
- ne pas start, stop, restart ou reload de service
- ne pas declencher de webhook reel
- ne pas envoyer Telegram
- ne pas lire ni afficher `.env`
- ne pas committer `journal.md`
- ne pas toucher `modules/bot_vision/headless_capture/`
- ne pas melanger `cursor-ai`, `db-layer`, `student` ou `fantome`
- lecture et documentation uniquement

## Point de depart

- le plan contract-first parent est disponible dans `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/55_CHILD_GO_OPERATING_PLAN.md`
- une ancienne branche distante `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01` existe deja et est close en PASS sur une base obsolescente
- cette reprise ouvre un chantier propre depuis le parent courant, sans reemployer cette ancienne branche comme base technique
