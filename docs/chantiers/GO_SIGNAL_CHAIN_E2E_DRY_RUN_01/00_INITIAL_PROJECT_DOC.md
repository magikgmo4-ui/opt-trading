---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/10_CURRENT_SURFACES.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/20_E2E_STEPS.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/30_OUTPUT_SCHEMA.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - E2E dry-run signal chain

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram screener inbound
- Telegram notification outbound multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Établir un runner E2E reproductible (fixtures-first) qui produit:

- un report pipeline (steps + timestamps)
- un daily session journal (JSON + CSV)
- une sync Sheets en dry-run (preview + audit log)

## Invariants

- aucun ordre live (PAPER only)
- pas d’écriture Google Sheets automatique (controlled-write explicite uniquement)
- pas de secrets dans les artifacts

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente la preuve E2E dry-run du produit final total et ne remplace pas le
Kanban bundle par une roadmap concurrente.

## Prochain item Kanban a faire

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- closeout final umbrella non prepare
- `40_GAPS_AND_NEXT_GO.md` etait incoherent et doit rester borne a des gaps reels
- dry-run global prouve mais pas encore synthese finale umbrella
