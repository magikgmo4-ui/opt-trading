---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_NOTIFICATION_DISPATCHER_STRATEGY_ID_ADAPTER_READONLY_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_NOTIFICATION_DISPATCHER_STRATEGY_ID_ADAPTER_READONLY_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Raccorder `notification_dispatcher` à `modules.strategy.adapter` en lecture seule, pour valider les `strategy_id` avant notification sans modifier les templates ni l'envoi.

### 2_CONTEXTE

- `modules/strategy/adapter.py` opérationnel.
- `trading_realtime_v1`, `signal_router`, `proposition_engine` déjà raccordés.
- `notification_dispatcher` utilise `strategy_id` dans le template `signal_received`.
- Dernier maillon avant `trading_lab_v1`.

### 3_SCOPE

- Ajouter `validate_strategy_id()` dans `NotificationDispatcher.dispatch()`.
- Warning log si inconnu, pas de blocage.
- Pas de modification des templates, payloads, envoi ou format utilisateur.

### 4_RESUME_POINT

Proposition_engine terminé. Dernier maillon pipeline : notification_dispatcher.
