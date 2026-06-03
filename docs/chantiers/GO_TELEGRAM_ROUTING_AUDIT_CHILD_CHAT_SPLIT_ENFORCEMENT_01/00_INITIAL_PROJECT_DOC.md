---
doc_id: GO_TELEGRAM_ROUTING_AUDIT_CHILD_CHAT_SPLIT_ENFORCEMENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: telegram_routing
go_id: GO_TELEGRAM_ROUTING_AUDIT_CHILD_CHAT_SPLIT_ENFORCEMENT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - telegram
  - routing
  - multi_channel
  - audit
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-06-03
working_branch: go/GO_TELEGRAM_ROUTING_AUDIT_CHILD_CHAT_SPLIT_ENFORCEMENT_01
links:
  - configs/telegram/channel_map.yaml
  - shared/telegram_channels.py
  - shared/telegram_notify.py
  - shared/telegram_send_cli.py
  - webhook_server.py
  - perf/perf_app.py
  - modules/desk_pro/api/routes.py
  - modules/bot_vision_step2/app/bot_vision_step2.py
  - modules/bot_vision/headless_capture/scripts/run_vision_pipeline.py
  - modules/runtime_health/healthcheck.py
  - modules/health/scripts/health-alert
  - modules/desk_analyze/scripts/cmd.sh
---

# GO_TELEGRAM_ROUTING_AUDIT_CHILD_CHAT_SPLIT_ENFORCEMENT_01

## Concept

Migrer tous les callers Telegram encore sur `TELEGRAM_CHAT_ID` (default) vers les 4 canaux
dédiés : `alerts`, `pipeline`, `push`, `ops` — définis dans `configs/telegram/channel_map.yaml`.

Le `send_to_channel(channel, ...)` existe déjà via `shared/telegram_channels.py`.
Ce GO audite et migre les callers restants qui contournent encore ce routing.

## Règles

1. Aucun secret (`chat_id`) dans le repo — uniquement via `/etc/opt-trading/env.d/roles/telegram_collector.env`
2. Chaque flux va dans le canal logique correspondant (pipeline → décisions, alerts → santé système, push → données, ops → CLI)
3. Les scripts bash utilisent `shared/telegram_send_cli.py` comme pont
4. Ne pas casser les tests existants ni le routing déjà en place

## Scope

- Auditer tous les callers Telegram (Python + bash)
- Migrer les callers encore sur `TELEGRAM_CHAT_ID` / `send_telegram_with_metrics` direct
- Mettre à jour `channel_map.yaml` pour refléter l'état réel
- Ajouter un CLI wrapper pour les scripts bash
- Tester les 4 routes en réel
