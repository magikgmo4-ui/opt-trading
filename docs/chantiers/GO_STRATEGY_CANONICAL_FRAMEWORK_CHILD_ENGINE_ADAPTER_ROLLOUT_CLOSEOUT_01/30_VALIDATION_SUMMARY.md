---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_ADAPTER_ROLLOUT_CLOSEOUT_01
doc_type: validation_summary
---

# 30_VALIDATION_SUMMARY

## Validations consolidees

- `python tools/strategy/validate_strategy_registry.py`
  - `UNREGISTERED` prod : `0`
- `tests/test_strategy_adapter.py`
  - `12/12`
- `modules/trading_realtime_v1/tests/test_strategy_id_adapter_readonly.py`
  - `3/3`
- `modules/signal_router/tests/`
  - `19/19`
- `modules/proposition_engine/tests/`
  - `23/23`
- `modules/notification_dispatcher/tests/`
  - `18/18`
- `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py`
  - `4/4`

## Conclusion

Toutes les surfaces de raccord adapter ont ete validees sans regression fonctionnelle annoncee.
