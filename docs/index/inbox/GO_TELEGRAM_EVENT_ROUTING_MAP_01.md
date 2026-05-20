---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - signal_chain
  - telegram
  - routing
  - notifications
  - ops
links:
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/10_CURRENT_ROUTING_SURFACES.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/20_TARGET_ALIAS_MAP.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/30_ROUTING_CLASS_MATRIX.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/90_REPRISE_POINT.md
---

# INBOX - GO_TELEGRAM_EVENT_ROUTING_MAP_01

## Objet

Poser une cartographie de routing Telegram (bots/chats/topics) par type d’événement, compatible avec la taxonomie transverse (GO_EVENT_TAXONOMY_01) et l’implémentation actuelle du dispatcher.

## Résultat

État établi :

- surfaces outbound relues et reconfirmees pour `modules/notification_dispatcher/app/dispatcher.py`, `modules/notification_dispatcher/app/events.py` et `shared/telegram_notify.py`
- le routing actuel reste monolithique sur `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`
- validation relancee dans cette passe : `python -m pytest modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_signal_event_adapter.py tests\test_desk_pro_combined_input_smoke.py -q` -> `68 passed`
- aucune mutation runtime introduite ; le chantier reste doc-only

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans melanger inbound et outbound
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01`
- `Gaps encore ouverts` : alias -> env, multi-bots, topics, branchement progressif dans le dispatcher

## Point de reprise

```text
docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/20_TARGET_ALIAS_MAP.md
docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/30_ROUTING_CLASS_MATRIX.md
docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/40_GAPS_AND_NEXT_GO.md
```
