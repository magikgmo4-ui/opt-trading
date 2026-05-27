# 90 — Closeout

## Statut

FERMÉ — 2026-05-26

## Verdict

`PASS_ADAPTER_OBSERVABILITY_WARNING_METRICS_01`

## Checklist

- [x] Helper `build_unknown_strategy_warning_payload` implémenté dans `adapter.py`
- [x] Helper `log_unknown_strategy_id_warning` implémenté dans `adapter.py`
- [x] signal_router warning remplacé
- [x] proposition_engine warning remplacé
- [x] notification_dispatcher warning remplacé
- [x] trading_realtime_v1/event_bridge_v1 print remplacé
- [x] trading_realtime_v1/runtime_loop_v1 print remplacé
- [x] trading_lab_v1 warning remplacé
- [x] Tests smoke ajoutés dans `tests/test_strategy_adapter.py` (15 nouveaux tests)
- [x] `python tools/strategy/validate_strategy_registry.py` → WARNINGS (pré-existants, UNREGISTERED=0)
- [x] `python -m pytest tests/test_strategy_adapter.py -q` → 23 passed, 4 failed pré-existants (registry count drift)
- [x] Tests readonly surfaces → 7+5+7 = 19 passed
- [x] Aucun hard-fail introduit
- [x] Aucun rejet de signal/proposition/notification

## Notes de clôture

Les 4 échecs pré-existants dans `tests/test_strategy_adapter.py` (TestGetKnownIds, TestGetAllEntries) sont dus à un drift entre la registry (9 IDs) et les constantes du test (7 IDs). Ce drift existait avant ce GO et est hors périmètre.
