---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01_RESULTS
doc_type: smoke_results
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 30_SMOKE_RESULTS - Smoke Results

## Commandes exécutées

```bash
cd /opt/trading
python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py -q
```

## Résultat

```
40 passed in 0.16s
```

## Détail par classe

| Classe | Tests | Résultat |
| --- | --- | --- |
| `TestNormalize` | 12 | 12 passed |
| `TestValidate` | 10 | 10 passed |
| `TestPayloadHash` | 3 | 3 passed |
| `TestRoundTrip` | 4 | 4 passed |
| `TestSignalEventSmoke` | 3 | 3 passed |
| `TestVisualContextSmoke` | 2 | 2 passed |
| `TestDeskSnapshotSmoke` | 2 | 2 passed |
| `TestDeskProSynthesisSmoke` | 3 | 3 passed |
| **Total** | **40** | **40 passed** |

## Tests smoke détaillés

### TestSignalEventSmoke (3 tests)

| Test | Description | Résultat |
| --- | --- | --- |
| `test_minimal_v0_normalize_and_validate` | V0 minimal → V1 → validate | PASS |
| `test_complete_v0_normalize_and_validate` | V0 complet → V1 → validate | PASS |
| `test_hash_deterministic` | payload_hash déterministe | PASS |

### TestVisualContextSmoke (2 tests)

| Test | Description | Résultat |
| --- | --- | --- |
| `test_visual_context_fixture_valid` | Fixture V1 conforme | PASS |
| `test_visual_context_can_be_referenced_by_signal_event` | visual_context_ref linkage | PASS |

### TestDeskSnapshotSmoke (2 tests)

| Test | Description | Résultat |
| --- | --- | --- |
| `test_desk_snapshot_fixture_valid` | Fixture desk_snapshot conforme | PASS |
| `test_desk_snapshot_can_reference_visual_context` | Join symbol+timeframe | PASS |

### TestDeskProSynthesisSmoke (3 tests)

| Test | Description | Résultat |
| --- | --- | --- |
| `test_synthesis_object_contains_all_artifacts` | Synthesis contient 3 artefacts | PASS |
| `test_synthesis_join_keys_coherent` | Join keys compatibles | PASS |
| `test_synthesis_no_runtime_dependency` | Synthesis indépendant du runtime | PASS |

## Side effects

`NONE` — aucun appel réseau, aucun fichier écrit, aucun service modifié.
