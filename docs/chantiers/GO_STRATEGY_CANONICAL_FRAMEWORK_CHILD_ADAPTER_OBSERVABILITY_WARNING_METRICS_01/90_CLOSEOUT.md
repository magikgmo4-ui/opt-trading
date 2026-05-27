# 90 — Closeout

## Statut

EN COURS — à compléter après validation des tests.

## Verdict attendu

`PASS_ADAPTER_OBSERVABILITY_WARNING_METRICS_01`

## Checklist

- [ ] Helper `build_unknown_strategy_warning_payload` implémenté dans `adapter.py`
- [ ] Helper `log_unknown_strategy_id_warning` implémenté dans `adapter.py`
- [ ] signal_router warning remplacé
- [ ] proposition_engine warning remplacé
- [ ] notification_dispatcher warning remplacé
- [ ] trading_realtime_v1/event_bridge_v1 print remplacé
- [ ] trading_realtime_v1/runtime_loop_v1 print remplacé
- [ ] trading_lab_v1 warning remplacé
- [ ] Tests smoke ajoutés dans `tests/test_strategy_adapter.py`
- [ ] `python tools/strategy/validate_strategy_registry.py` → PASS
- [ ] `python -m pytest tests/test_strategy_adapter.py -q` → PASS
- [ ] Tests readonly surfaces → PASS
- [ ] Aucun hard-fail introduit
- [ ] Aucun rejet de signal/proposition/notification
