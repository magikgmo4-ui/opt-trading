---
doc_id: GO_EVENT_TAXONOMY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_EVENT_TAXONOMY_01/10_CURRENT_EVENT_SURFACES.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/20_CANONICAL_EVENT_ENVELOPE.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/30_EVENT_FAMILY_MAPPING.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Event taxonomy transverse

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram screener inbound
- Telegram notification outbound
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Fournir un langage commun (enveloppe + types + familles) pour:

- ingestion (webhook / observer / bot vision / headless)
- pipeline workers (router/proposition/gate/execute/track/write/feed)
- Desk Pro hub (synthèse + UI)
- routing Telegram (outbound) et futures surfaces inbound
- Sheets / Perf / Registry

## Contraintes

- documenter à partir du repo réel (pas de refactor runtime, pas de breaking change)
- conserver la compatibilité avec les objets existants (dataclasses `schema.py` et payloads dict)
- privilégier un envelope "read-only" d’abord (fixtures / dry-run), puis brancher routing

## Livrables dans ce GO

- `10_CURRENT_EVENT_SURFACES.md` : état réel des surfaces et formats existants
- `20_CANONICAL_EVENT_ENVELOPE.md` : envelope canonique minimal (V1)
- `30_EVENT_FAMILY_MAPPING.md` : mapping event_type ↔ familles ↔ owners ↔ routing impact
- `90_REPRISE_POINT.md` : reprise + next GO

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
fournit la taxonomie transverse minimale necessaire au produit final total, sans
creer de roadmap concurrente.

## Prochain item Kanban a faire

`GO_TELEGRAM_EVENT_ROUTING_MAP_01`

## Gaps encore ouverts

- intentions outbound Telegram encore non canonisees completement
- articulation avec les futures surfaces inbound Telegram encore ouverte
- integration Sheets / Perf / Registry via cette enveloppe encore a propager
