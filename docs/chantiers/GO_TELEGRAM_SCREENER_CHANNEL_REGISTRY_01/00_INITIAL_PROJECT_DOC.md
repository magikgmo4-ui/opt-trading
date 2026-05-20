---
doc_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/10_CURRENT_INBOUND_SURFACES.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/20_REGISTRY_SCHEMA_TARGET.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Telegram screener inbound: channel registry

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- Telegram screener inbound
- Telegram notification outbound multi-destinations
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Poser un registry canonique des sources Telegram inbound (channels/groups) qui peuvent produire des signaux/screeners, avec:

- catégories (macro/news/liquidations/signals/alpha)
- trust tiers (A/B/C/D) et politiques d’activation
- “parsers” attendus (trade/setup/news) sans implémenter le parsing dans ce GO

## Contraintes

- ne pas mélanger inbound screener et outbound notifications
- ne pas introduire de secrets / chat_id réels dans le repo
- doc-only: aucun bot live, aucune ingestion Telegram réelle

## Livrables

- `10_CURRENT_INBOUND_SURFACES.md` : ce qui existe (et ce qui manque) dans le repo
- `20_REGISTRY_SCHEMA_TARGET.md` : schéma cible du registry (format fichier + champs)
- `30_PROOF_MATRIX_AND_CONSTRAINTS.md` : preuves attendues + contraintes de sécurité
- `40_GAPS_AND_NEXT_GO.md` : plan d’implémentation après registry
- `90_REPRISE_POINT.md` : reprise + prochain GO bundle

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente l'inbound screener du produit final total et ne remplace pas le
Kanban bundle par une roadmap concurrente.

## Prochain item Kanban a faire

`GO_DESKPRO_INPUT_EXPANSION_01`

## Gaps encore ouverts

- registry non materialise sous `registry/telegram_screener_channels.yaml`
- aucun parser `trade/setup/news` encore defini en fixtures-first
- aucune surface listener inbound separee et gouvernee encore posee
