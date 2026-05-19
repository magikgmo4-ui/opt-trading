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
