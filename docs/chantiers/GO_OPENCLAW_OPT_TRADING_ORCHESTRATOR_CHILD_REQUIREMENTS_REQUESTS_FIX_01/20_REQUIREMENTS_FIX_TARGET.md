---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01_FIX_TARGET
doc_type: fix_target
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01
status: closed
created_at: 2026-05-26
---

# 20_REQUIREMENTS_FIX_TARGET — Cible des changements

## requirements.txt

**Aucun changement nécessaire.** `requests==2.32.5` était déjà présent.

Extrait (ligne 14) :
```
requests==2.32.5
```

## notification_dispatcher/app/__init__.py

**Aucun changement nécessaire.** Import lazy déjà en place depuis PR #830 :

```python
from .events import PipelineEvent, EventType       # stdlib only — toujours importable

try:
    from .dispatcher import NotificationDispatcher
except ImportError:
    NotificationDispatcher = None  # type: ignore   # dégradation si requests absent

__all__ = ["NotificationDispatcher", "PipelineEvent", "EventType"]
```

## Nouveau fichier ajouté

`modules/notification_dispatcher/tests/test_import_safety.py`

Contenu : 9 tests subprocess qui vérifient le contrat d'import sans requests :

| Test | Vérifie |
|------|---------|
| `test_events_importable_without_requests` | `events.py` importable (stdlib only) |
| `test_package_import_pipeline_event_without_requests` | `PipelineEvent` accessible via `__init__` |
| `test_notificationdispatcher_none_when_requests_absent` | `NotificationDispatcher` → None, pas raise |
| `test_import_does_not_trigger_network_call` | aucun appel réseau à l'import |
| `test_all_event_types_accessible_without_requests` | `ALL_EVENT_TYPES` accessible (7 types) |
| `test_validation_gate_imports_without_requests` | ValidationGate importable sans requests |
| `test_trade_executor_imports_without_requests` | TradeExecutor importable sans requests |
| `test_result_tracker_imports_without_requests` | ResultTracker importable sans requests |
| `test_pipeline_event_fallback_in_validation_gate` | `gate.dispatcher is None` si requests absent |

## Stratégie de test

Les 9 tests utilisent `subprocess` pour lancer un Python frais avec `sys.modules["requests"] = None` avant tout import. Cela simule rigoureusement l'absence de la dépendance sans modifier le venv courant.

Aucun appel HTTP réel n'est effectué dans aucun test (dry_run ou mode isolé).

## Résultat de validation

```
9 passed in 0.65s
```

Tous les tests de cette suite passent avec ou sans `requests` installé dans le venv.
