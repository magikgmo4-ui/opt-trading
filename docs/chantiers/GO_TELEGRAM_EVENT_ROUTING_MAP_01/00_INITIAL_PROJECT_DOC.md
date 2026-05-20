---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/10_CURRENT_ROUTING_SURFACES.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/20_TARGET_ALIAS_MAP.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/30_ROUTING_CLASS_MATRIX.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Telegram routing map

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- Telegram notification outbound multi-destinations
- Telegram screener inbound
- TradingView/webhook -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Définir un routing Telegram lisible et robuste pour les événements du produit:

- éviter le bruit (tout dans un seul chat)
- séparer les niveaux (ops / trading / debug / erreurs)
- garantir un mode dry-run (pas d'envoi live en test)

## Contraintes

- rester compatible avec l’implémentation existante:
  - `modules/notification_dispatcher/app/dispatcher.py`
  - `shared/telegram_notify.py`
- ne pas introduire de secret dans le repo
- ne pas créer de runtime live dans ce GO (doc-only + plan)

## Livrables

- `10_CURRENT_ROUTING_SURFACES.md` : ce qui existe déjà (surfaces + config env)
- `20_TARGET_ALIAS_MAP.md` : alias map (bots/chats/topics) à standardiser
- `30_ROUTING_CLASS_MATRIX.md` : event_type/family → destination + policy
- `40_GAPS_AND_NEXT_GO.md` : ce qui manque pour implémenter sans casser
- `90_REPRISE_POINT.md` : reprise + next GO bundle

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente le routing outbound du produit final total et ne remplace pas le
Kanban bundle par une roadmap concurrente.

## Prochain item Kanban a faire

`GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01`

## Gaps encore ouverts

- resolution alias -> env non implementee
- support multi-bots et topics non concretise
- policy dry-run vs live a brancher progressivement dans le dispatcher
