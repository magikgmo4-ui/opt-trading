# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01

## Objectif

Ajouter une observabilité minimale et canonique autour des warnings `strategy_id` inconnus émis par les surfaces runtime, sans modifier le comportement trading.

## Contexte

L'adaptateur central `modules/strategy/adapter.py` expose `validate_strategy_id()`. Plusieurs surfaces émettent un warning lorsque cet appel retourne `False`, mais chaque surface formule ce warning différemment (format, champs, logger). Ces warnings ne sont pas comparables ni auditables de façon homogène.

## Périmètre

- Ajouter deux helpers dans `modules/strategy/adapter.py` :
  - `build_unknown_strategy_warning_payload(strategy_id, source)` — construit un dict canonique
  - `log_unknown_strategy_id_warning(strategy_id, source)` — logue via `strategy.observability`
- Remplacer les warnings directs dans les 5 surfaces par l'appel au helper
- Ajouter les tests smoke correspondants

## Invariants

- Aucun hard-fail introduit
- Aucun rejet de signal, proposition ou notification
- `validate_strategy_id()` reste inchangé et compatible
- Aucune nouvelle stratégie dans la registry
- Aucune dépendance externe ajoutée
- Comportement trading identique avant/après

## Surfaces concernées

| Surface | Fichier |
|---|---|
| signal_router | `modules/signal_router/app/router.py` |
| proposition_engine | `modules/proposition_engine/app/engine.py` |
| notification_dispatcher | `modules/notification_dispatcher/app/dispatcher.py` |
| trading_realtime_v1 event_bridge | `modules/trading_realtime_v1/app/event_bridge_v1.py` |
| trading_realtime_v1 runtime_loop | `modules/trading_realtime_v1/app/runtime_loop_v1.py` |
| trading_lab_v1 | `modules/trading_lab_v1/app/trading_lab_v1.py` |

## Issue

GitHub #579
