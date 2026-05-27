# 40 — Test Plan

## Tests à ajouter dans tests/test_strategy_adapter.py

### TestUnknownStrategyWarningPayload

| Test | Assert |
|---|---|
| `test_payload_keys_present` | Tous les champs canoniques présents |
| `test_payload_event_value` | `event == "STRATEGY_ID_UNKNOWN"` |
| `test_payload_metric_value` | `metric == "strategy_id.unknown.warning"` |
| `test_payload_mode_warning_only` | `mode == "warning_only"` |
| `test_payload_runtime_action_continue` | `runtime_action == "continue"` |
| `test_payload_registry_known_false` | `registry_known is False` |
| `test_payload_strategy_id_passthrough` | `strategy_id` reflète l'argument reçu |
| `test_payload_source_passthrough` | `source` reflète l'argument reçu |

### TestLogUnknownStrategyIdWarning

| Test | Assert |
|---|---|
| `test_emits_warning_level` | Level WARNING dans caplog |
| `test_emits_event_key` | `STRATEGY_ID_UNKNOWN` dans le message |
| `test_emits_strategy_id` | L'ID apparaît dans le message |
| `test_validate_strategy_id_still_valid` | `validate_strategy_id("xau_session_open_v1") is True` |
| `test_validate_strategy_id_still_false` | `validate_strategy_id("nonexistent") is False` |

## Tests de non-régression existants

Ces tests passent avant et après sans modification :

- `tests/test_strategy_adapter.py` — TestValidateStrategyId, TestGetKnownIds, TestLookupStrategy, TestGetAllEntries, TestIdempotent
- `modules/signal_router/tests/test_strategy_id_adapter_readonly.py`
- `modules/proposition_engine/tests/test_strategy_id_adapter_readonly.py`
- `modules/notification_dispatcher/tests/test_strategy_id_adapter_readonly.py`

## Commandes de validation

```bash
python tools/strategy/validate_strategy_registry.py
python -m pytest tests/test_strategy_adapter.py -q
python -m pytest modules/signal_router/tests/test_strategy_id_adapter_readonly.py modules/proposition_engine/tests/test_strategy_id_adapter_readonly.py modules/notification_dispatcher/tests/test_strategy_id_adapter_readonly.py -q
```

## Critère de succès

`PASS_ADAPTER_OBSERVABILITY_WARNING_METRICS_01` — tous les tests passent, zéro régression.
