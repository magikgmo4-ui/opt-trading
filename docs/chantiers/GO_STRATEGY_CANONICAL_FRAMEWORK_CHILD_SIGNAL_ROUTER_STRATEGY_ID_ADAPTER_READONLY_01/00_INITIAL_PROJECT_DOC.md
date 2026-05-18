---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_SIGNAL_ROUTER_STRATEGY_ID_ADAPTER_READONLY_01
go_type: child
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
repo: opt-trading
status: open
created_at: 2026-05-18
surface: code / doc
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_SIGNAL_ROUTER_STRATEGY_ID_ADAPTER_READONLY_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Valider les `strategy_id` entrants dans `signal_router` via `modules.strategy.adapter`, en lecture seule, sans changer le routing ni rejeter les signaux.

### 2_CONTEXTE

- `modules/strategy/adapter.py` opérationnel.
- `trading_realtime_v1` déjà raccordé en lecture seule.
- `signal_router` normalise des signaux entrants et propage `strategy_id` vers `proposition_engine` / `notification_dispatcher`.
- Le `strategy_id` peut être invalide (non registré) sans alerte actuellement.

### 3_SCOPE

- Ajouter `validate_strategy_id()` dans `route()` après normalisation.
- Warning log si inconnu, pas de rejet, pas de modification du signal.
- Pas de changement de routing, schéma, ou format.
- Pas de modification de `proposition_engine` ou `notification_dispatcher`.

### 4_RESUME_POINT

Trading realtime raccordé. Prochaine frontière : signal_router.
