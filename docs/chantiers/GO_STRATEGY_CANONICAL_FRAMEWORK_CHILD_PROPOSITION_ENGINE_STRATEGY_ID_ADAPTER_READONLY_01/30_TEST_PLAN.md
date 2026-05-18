---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_PROPOSITION_ENGINE_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: test_plan
---

# 30_TEST_PLAN

## Tests existants

| Suite | Statut |
|-------|--------|
| `tests/test_strategy_adapter.py` | 12/12 |
| `modules/signal_router/tests/` | 19/19 |
| `modules/proposition_engine/tests/test_proposition.py` | ? |

## Nouveau test

Fichier : `modules/proposition_engine/tests/test_strategy_id_adapter_readonly.py`

- `test_known_strategy_id_silent` — `xau_session_open_v1` n'émet pas de warning
- `test_unknown_strategy_id_warns` — strategy_id inconnu produit warning log
- `test_proposal_output_unchanged` — la proposition retournée est identique quel que soit le strategy_id

## Validation finale

1. `python tools/strategy/validate_strategy_registry.py`
2. `python -m pytest tests/test_strategy_adapter.py -q`
3. `python -m pytest modules/proposition_engine/tests/ -q`
4. Vérifier git diff limité à `proposition_engine/` + nouveaux fichiers
