---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_NOTIFICATION_DISPATCHER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: test_plan
---

# 30_TEST_PLAN

## Tests existants

| Suite | Statut |
|-------|--------|
| `tests/test_strategy_adapter.py` | 12/12 |
| `modules/signal_router/tests/` | 19/19 |
| `modules/proposition_engine/tests/` | 23/23 |
| `modules/notification_dispatcher/tests/test_dispatcher.py` | ? |

## Nouveau test

Fichier : `modules/notification_dispatcher/tests/test_strategy_id_adapter_readonly.py`

- `test_known_strategy_id_silent` — `xau_session_open_v1` n'émet pas de warning
- `test_unknown_strategy_id_warns` — strategy_id inconnu produit warning log
- `test_no_strategy_id_no_validation` — pas de warning si strategy_id absent
- `test_message_output_unchanged` — le message formaté est identique

## Validation finale

1. `python tools/strategy/validate_strategy_registry.py`
2. `python -m pytest tests/test_strategy_adapter.py -q`
3. `python -m pytest modules/notification_dispatcher/tests/ -q`
4. Vérifier git diff limité à `notification_dispatcher/` + nouveaux fichiers
