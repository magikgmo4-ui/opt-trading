---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_SIGNAL_ROUTER_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: test_plan
---

# 30_TEST_PLAN

## Tests existants

| Suite | Statut |
|-------|--------|
| `tests/test_strategy_adapter.py` | 12/12 |
| `modules/signal_router/tests/test_router.py` | ? |

## Nouveau test

Fichier : `modules/signal_router/tests/test_strategy_id_adapter_readonly.py`

- `test_known_strategy_id_does_not_warn` — validated strategy_id silencieux
- `test_unknown_strategy_id_warns` — strategy_id inconnu produit warning log
- `test_signal_output_unchanged` — le signal retourné est identique quel que soit le strategy_id
- `test_import_router_does_not_raise` — l'import du module ne lève pas d'exception

## Validation finale

1. `python tools/strategy/validate_strategy_registry.py`
2. `python -m pytest tests/test_strategy_adapter.py -q`
3. `python -m pytest modules/signal_router/tests/ -q`
4. Vérifier git diff limité à `signal_router/` + nouveaux fichiers

## RISKS

- À qualifier.
