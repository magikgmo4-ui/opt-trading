---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_REALTIME_STRATEGY_ID_ADAPTER_READONLY_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_REALTIME_STRATEGY_ID_ADAPTER_READONLY_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Raccorder `trading_realtime_v1` à `modules/strategy.adapter` en lecture seule, pour valider `xau_session_open_v1` sans changer le comportement trading.

### 2_CONTEXTE

- `modules/strategy/adapter.py` opérationnel : `validate_strategy_id()`, `get_known_ids()`, `lookup_strategy()`, `get_all_entries()`.
- `trading_realtime_v1` contient deux hardcodes `STRATEGY_ID = "xau_session_open_v1"` :
  - `runtime_loop_v1.py:13`
  - `event_bridge_v1.py:11`
- Aucun engine n'importe encore `modules/strategy/`.

### 3_SCOPE

- Ajouter un import de `validate_strategy_id` dans les deux fichiers.
- Ajouter une validation read-only au chargement du module : warning si le strategy_id est inconnu, aucun changement sinon.
- Ne pas modifier les signaux, routing, ordres, timing ou outputs métier.
- Ajouter un test smoke si possible.

### 4_RESUME_POINT

Adapter strategy opérationnel. Premier raccord runtime read-only.
