---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - strategy_registry
  - telegram
  - latency
  - perf_engine
  - gates
links:
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/10_CURRENT_REGISTRY_SURFACES.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/20_REGISTRY_FIELD_UPDATE.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/30_VALIDATION_FLOW.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/90_REPRISE_POINT.md
---

# INBOX - GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01

## Objet

Ajouter une dimension `telegram_latency` au Strategy Registry (après validation), en s’appuyant sur la telemetry `sendMessage` et le backtest offline, sans impacter le runtime trading.

## Résultat

État établi :

- surfaces registry et latency relues et reconfirmees pour `95_STRATEGY_REGISTRY.md`, `modules/strategy/registry.py`, `modules/strategy/adapter.py`, `shared/telegram_notify.py` et `modules/notification_dispatcher/app/dispatcher.py`
- la table `2_REGISTRY` contient deja la colonne `telegram_latency` et les entrees strategies exposent deja `telegram_latency_status`
- le dispatcher outbound pousse bien les tags `strategy_id` et `strategy_version` vers `send_telegram_html(...)`
- validation relancee dans cette passe : `python -m pytest tests\e2e\test_telegram_latency_backtest.py modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py -q` -> `8 passed`

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via le couplage Strategy Registry / Telegram latency
- `Tableau Kanban du bundle` : reste la reference principale
- `Prochain item Kanban exact` : `GO_SIGNAL_CHAIN_E2E_DRY_RUN_01`
- `Gaps encore ouverts` : couverture tags incomplete, seuils produits non fixes, evidence refs registry encore a remplir

## Point de reprise

```text
docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/20_REGISTRY_FIELD_UPDATE.md
docs/chantiers/GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01/30_VALIDATION_FLOW.md
```
