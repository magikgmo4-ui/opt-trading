---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01_TEST_PLAN
doc_type: test_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_TEST_PLAN - Test Plan

## Structure

```
tests/test_signal_event_adapter.py
```

## Commande

```bash
cd /opt/trading
python -m pytest tests/test_signal_event_adapter.py -q
```

## Résultat

```
30 passed in 0.13s
```

## Couverture par classe

### TestNormalize (12 tests)

| Test | Payload | Vérification |
| --- | --- | --- |
| `test_full_payload` | V0 complet | Tous les champs V1 correctement mappés |
| `test_minimal_payload` | V0 minimal (pas de price/tp/sl) | Champs requis OK, meta/risk null |
| `test_meta_grouping` | V0 complet | price, tp, sl, reason, debug.client_ip dans meta |
| `test_risk_context_grouping` | V0 complet | qty, risk_usd, risk_real_usd dans risk_context |
| `test_payload_hash_present` | V0 complet | Hash présent, 64 chars hex |
| `test_payload_hash_deterministic` | V0 complet | Deux appels → même hash |
| `test_optional_refs_none` | V0 complet | raw_payload_ref, visual_context_ref, desk_snapshot_ref = null |
| `test_not_a_dict` | string | status=error, errors non vide |
| `test_missing_engine` | engine="" | "missing engine" dans errors |
| `test_missing_symbol` | symbol="" | "missing symbol" dans errors |
| `test_missing_timeframe` | tf="" | "missing timeframe" dans errors |
| `test_invalid_direction` | signal="HOLD" | "invalid direction" dans errors |
| `test_signal_case_insensitive` | signal="buy" | direction="BUY" |

### TestValidate (10 tests)

| Test | V1 event | Vérification |
| --- | --- | --- |
| `test_valid_full` | V1 complet depuis V0 | is_valid=True, errors=[] |
| `test_valid_minimal` | V1 minimal depuis V0 | is_valid=True |
| `test_missing_engine` | engine="" | is_valid=False |
| `test_missing_symbol` | symbol="" | is_valid=False |
| `test_missing_timeframe` | timeframe="" | is_valid=False |
| `test_invalid_direction` | direction="HOLD" | is_valid=False |
| `test_missing_timestamp` | timestamp="" | is_valid=False |
| `test_unparseable_timestamp` | timestamp="not-a-date" | is_valid=False |
| `test_unknown_status_non_blocking` | status="unknown" | is_valid=True (warning) |
| `test_not_a_dict` | None | is_valid=False |

### TestPayloadHash (3 tests)

| Test | Vérification |
| --- | --- |
| `test_deterministic` | Même payload → même hash |
| `test_different_payloads_different_hash` | V0_FULL ≠ V0_MINIMAL |
| `test_sha256_format` | 64 chars hexadécimaux |

### TestRoundTrip (4 tests)

| Test | Vérification |
| --- | --- |
| `test_full_roundtrip` | V0 → normalize → validate = valid |
| `test_minimal_roundtrip` | V0 minimal → normalize → validate = valid |
| `test_skipped_not_in_jsonl` | Adapter gère les skipped si présents |
| `test_no_side_effects` | Adapter pur, pas d'effets de bord |

## Side effects des tests

`NONE` — les tests n'écrivent aucun fichier, ne lisent aucun fichier réel, n'appellent aucun service.
