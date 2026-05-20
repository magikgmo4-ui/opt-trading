---
doc_id: GO_EVENT_TAXONOMY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_EVENT_TAXONOMY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - signal_chain
  - event_taxonomy
  - contracts
  - routing
links:
  - docs/chantiers/GO_EVENT_TAXONOMY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/10_CURRENT_EVENT_SURFACES.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/20_CANONICAL_EVENT_ENVELOPE.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/30_EVENT_FAMILY_MAPPING.md
  - docs/chantiers/GO_EVENT_TAXONOMY_01/90_REPRISE_POINT.md
---

# INBOX - GO_EVENT_TAXONOMY_01

## Objet

Définir une taxonomie d’événements transverse, compatible avec le repo actuel (webhook, workers, Desk Pro, Telegram outbound, Sheets sync), pour permettre un routing propre sans collisions.

## Résultat

État établi :

- surfaces d'evenements relues et reconfirmees pour webhook, workers, Desk Pro et Telegram outbound
- preuves repo confirmees pour `schemas/webhook_event_v1.json`, `modules/desk_pro/signal_event_adapter.py`, `modules/signal_router/app/schema.py`, `modules/notification_dispatcher/app/events.py`
- validation relancee dans cette passe : `python -m pytest tests\test_signal_event_adapter.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_desk_pro_combined_input_smoke.py -q` -> `61 passed`
- aucune mutation runtime introduite ; taxonomie maintenue en lecture/contrat seulement

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans implementation live
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_TELEGRAM_EVENT_ROUTING_MAP_01`
- `Gaps encore ouverts` : intents NOTIFY, routing par famille, raccord inbound Telegram, propagation Sheets/Perf/Registry

## Point de reprise

```text
docs/chantiers/GO_EVENT_TAXONOMY_01/20_CANONICAL_EVENT_ENVELOPE.md
docs/chantiers/GO_EVENT_TAXONOMY_01/30_EVENT_FAMILY_MAPPING.md
docs/chantiers/GO_EVENT_TAXONOMY_01/90_REPRISE_POINT.md
```
