---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_INITIAL
doc_type: initial_project_doc
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - tradingview/
  - adapters/
  - data/collectors/
  - config/machine_runtime_map.yml
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/10_GAPS_REGISTER.md
---

# GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01

## Objectif

Automatiser la chaîne de signal en dry-run : schéma, sources, recroisement, journal, backtest, dry-run guard, without live order (GAP_10 du parent).

## Périmètre

- Signal schema (format, champs, validation)
- Source adapters (TradingView, Telegram, collecteurs)
- Recroisement (vérification croisée des sources)
- Invalidation (règles de rejet)
- Dry-run guard (blocage d'ordre live)
- Journal (log des signaux reçus et traités)
- Backtest stats (statistiques de performance)
- Aucun ordre live

## Preuve concrète pour l'ouverture

- `tradingview/` : répertoire webhook et adaptateurs existants
- `adapters/` : bridges de collecte présents
- `config/machine_runtime_map.yml` : machines et services trading déclarés

## Livrables

- Signal schema
- Source adapters documentés
- Recroisement policy
- Invalidation rules
- Dry-run guard
- Journal
- Backtest stats
