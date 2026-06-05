---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_REALTIME_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: test_plan
---

# 30_TEST_PLAN

## Tests existants

| Suite | Statut |
|-------|--------|
| `tests/test_strategy_adapter.py` | 12/12 — adapter functions OK |
| `modules/trading_realtime_v1/tests/test_runtime_loop_v1.py` | ? |
| `modules/trading_realtime_v1/tests/test_runtime_surfaces_v1.py` | ? |

## Nouveau test

Fichier : `modules/trading_realtime_v1/tests/test_strategy_id_adapter_readonly.py`

- `test_import_runtime_loop_validates_strategy_id` — vérifie que l'import de `runtime_loop_v1` ne lève pas d'exception
- `test_import_event_bridge_validates_strategy_id` — idem pour `event_bridge_v1`
- `test_strategy_id_xau_session_open_v1_is_registered` — vérifie que `xau_session_open_v1` est connu

## Validation finale

1. `python tools/strategy/validate_strategy_registry.py`
2. `python -m pytest tests/test_strategy_adapter.py -q`
3. `python -m pytest modules/trading_realtime_v1/tests/ -q`
4. Vérifier git diff limité à `trading_realtime_v1/` + nouveaux fichiers

## RISKS

- À qualifier.
