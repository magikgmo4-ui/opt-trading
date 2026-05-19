---
doc_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/20_REUSE_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Repo Inventory (Signal Monitoring)

## But

Produire une lecture exacte, repo-first, des surfaces existantes qui composent déjà une partie du produit "signal chain total":

- ingestion TradingView/webhook (signal_event)
- pipeline workers (router/proposition/gate/execute/track/write/feed)
- consumer Desk Pro (synthèse et UI)
- notification / dispatcher
- journalisation / sync Sheets (au moins daily session)
- ponts "vision/headless" présents ou en cours

## Contraintes

- ne pas implémenter de runtime live, ni de Telegram inbound parser, ni de Google Sheets global writer tant que l'inventaire n'est pas posé
- aucune mutation de secrets, aucune écriture de fichiers runtime (objectif: doc + tests)

## Sorties attendues (dans ce GO)

- une preuve par chemins (map surface → fichiers/modules) : `10_CHAIN_SURFACE_PROOF_MAP.md`
- une matrice de réutilisation + contraintes (what exists / what missing / next GO) : `20_REUSE_MATRIX_AND_CONSTRAINTS.md`
- un point de reprise opératoire : `90_REPRISE_POINT.md`
