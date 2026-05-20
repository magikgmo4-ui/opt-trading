---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/10_CURRENT_INPUT_SURFACES.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/30_PROOF_MATRIX_AND_CONSTRAINTS.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Desk Pro input expansion

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener -> Desk Pro
- Telegram screener inbound -> claims watch-only -> Desk Pro
- Telegram notification outbound multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Desk Pro est le hub consumer final du produit. Ce GO fixe:

- les inputs déjà consommés (réels) et leurs formats
- les inputs cibles à ajouter (contrats) sans implémenter de runtime live
- les jointures et contraintes (symbol/tf/timestamps)

## Contraintes

- doc-only: pas de démarrage runtime, pas de lecture `.env`, pas de Telegram live
- pas de breaking change: uniquement des contrats + cartographie
- rester aligné avec la taxonomie transverse (GO_EVENT_TAXONOMY_01)

## Livrables

- `10_CURRENT_INPUT_SURFACES.md` : inputs réels prouvés + chemins
- `20_TARGET_INPUT_CLASSES.md` : classes d’inputs cibles (V1) pour le hub
- `30_PROOF_MATRIX_AND_CONSTRAINTS.md` : preuves attendues + invariants
- `40_GAPS_AND_NEXT_GO.md` : plan après cadrage
- `90_REPRISE_POINT.md` : reprise + next GO bundle

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente le hub consumer Desk Pro du produit final total et ne remplace pas le
Kanban bundle par une roadmap concurrente.

## Prochain item Kanban a faire

`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01`

## Gaps encore ouverts

- classes d'inputs cibles non materialisees en wrappers read-only
- `vision_analysis`, `market_metrics` et `telegram_claim` encore contractuels seulement
- jointures refs/timestamps encore partielles selon les producers
