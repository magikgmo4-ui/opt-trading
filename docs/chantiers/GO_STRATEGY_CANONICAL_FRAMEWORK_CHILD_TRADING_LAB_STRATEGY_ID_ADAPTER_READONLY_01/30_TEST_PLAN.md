---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_STRATEGY_ID_ADAPTER_READONLY_01
doc_type: test_plan
---

# 30_TEST_PLAN

## Smoke tests ajoutes

- YAML avec `strategy_id` connu : pas de warning
- YAML avec `strategy_id` inconnu : warning
- YAML sans `strategy_id` : fallback `xau_session_open_v1` valide
- sortie de `build_market_event()` inchangee

## Validations attendues

- `python tools/strategy/validate_strategy_registry.py`
- `python -m pytest tests/test_strategy_adapter.py -q`
- `python -m pytest modules/trading_realtime_v1/tests/test_strategy_id_adapter_readonly.py -q`
- `python -m pytest modules/signal_router/tests/ -q`
- `python -m pytest modules/proposition_engine/tests/ -q`
- `python -m pytest modules/notification_dispatcher/tests/ -q`
- `python -m pytest modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py -q`
- tests trading_lab pertinents disponibles

## RISKS

- À qualifier.
