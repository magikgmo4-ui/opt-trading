---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01_TEST_REPORT
doc_type: test_report
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01
status: closed
verdict: PASS
created_at: 2026-05-26
---

# 30_TEST_REPORT — Résultats de validation

## Run de validation

### notification_dispatcher (complet)

```
python3 -m pytest modules/notification_dispatcher/tests -q
27 passed in 0.75s
```

| Suite | Tests | Résultat |
|-------|-------|----------|
| `test_dispatcher.py` | 11 | PASS |
| `test_strategy_id_adapter_readonly.py` | 7 | PASS |
| `test_import_safety.py` (nouveau) | 9 | PASS |
| **Total** | **27** | **ALL PASS** |

### Modules downstream

```
python3 -m pytest modules/validation_gate/tests modules/trade_executor/tests modules/result_tracker/tests -q
84 passed in 0.35s
```

| Module | Tests | Résultat |
|--------|-------|----------|
| `validation_gate` | 30 | PASS |
| `trade_executor` | 28 | PASS |
| `result_tracker` | 26 | PASS |
| **Total** | **84** | **ALL PASS** |

### Run global

```
python3 -m pytest tests -q
7 failed, 1035 passed, 10 warnings
```

Les 7 failures sont pré-existantes et non liées à ce GO :
- `test_desk_pro_artifact_output.py` (2) — desk_pro unrelated
- `test_desk_pro_combined_input_smoke.py` (1) — desk_pro unrelated
- `test_strategy_adapter.py` (4) — count mismatch strategy registry, non liée à requests

Aucune régression introduite.

## Détail des 9 tests import_safety

| Test | Simulation | Résultat |
|------|-----------|---------|
| `test_events_importable_without_requests` | subprocess + `requests=None` | PASS |
| `test_package_import_pipeline_event_without_requests` | subprocess + `requests=None` | PASS |
| `test_notificationdispatcher_none_when_requests_absent` | subprocess + `requests=None` | PASS |
| `test_import_does_not_trigger_network_call` | subprocess + socket.connect patché | PASS |
| `test_all_event_types_accessible_without_requests` | subprocess + `requests=None` | PASS |
| `test_validation_gate_imports_without_requests` | subprocess + `requests=None` | PASS |
| `test_trade_executor_imports_without_requests` | subprocess + `requests=None` | PASS |
| `test_result_tracker_imports_without_requests` | subprocess + `requests=None` | PASS |
| `test_pipeline_event_fallback_in_validation_gate` | subprocess + `requests=None` | PASS |

## Critères PASS validés

- [x] `requests` déclaré dans `requirements.txt`
- [x] `notification_dispatcher` reste import-safe (9 tests prouvent)
- [x] aucun test ne dépend d'un appel réseau réel
- [x] `validation_gate` / `trade_executor` / `result_tracker` stables (84 tests)
- [x] gap `requests absent du venv` documenté CLOSED
