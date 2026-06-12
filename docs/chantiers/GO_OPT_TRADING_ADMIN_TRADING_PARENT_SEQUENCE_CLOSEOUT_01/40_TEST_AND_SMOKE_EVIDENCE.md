---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01_TEST_EVIDENCE
doc_type: test_and_smoke_evidence
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_TEST_AND_SMOKE_EVIDENCE - Test and Smoke Evidence

## Adapter tests (GO 6: Schema Adapter)

```
Command: python -m pytest tests/test_signal_event_adapter.py -q
Result: 30 passed in 0.13s
```

| Classe | Tests | Résultat |
| --- | --- | --- |
| TestNormalize | 12 | PASS |
| TestValidate | 10 | PASS |
| TestPayloadHash | 3 | PASS |
| TestRoundTrip | 4 | PASS |

## Compatibility smoke (GO 7: Contract Smoke)

```
Command: python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py -q
Result: 40 passed in 0.16s
```

| Classe | Tests | Résultat |
| --- | --- | --- |
| TestSignalEventSmoke | 3 | PASS |
| TestVisualContextSmoke | 2 | PASS |
| TestDeskSnapshotSmoke | 2 | PASS |
| TestDeskProSynthesisSmoke | 3 | PASS |

## Preuves de compatibilité producer/consumer

| Chaîne | Preuve | Status |
| --- | --- | --- |
| Webhook V0 → signal_event V1 → Desk Pro | adapter + 30 tests | VALIDATED |
| visual_context V1 → Desk Pro | fixture + smoke | VALIDATED |
| desk_snapshot → Desk Pro | runtime + fixture + smoke | CONFIRMED |
| signal_event + visual_context + desk_snapshot → synthesis | smoke test | VALIDATED |

## Runtime side effects

**NONE** — tous les tests sont locaux, sans appel réseau, sans écriture fichier, sans service modifié.

## Fichiers de test

| Fichier | Tests | Description |
| --- | --- | --- |
| `tests/test_signal_event_adapter.py` | 30 | Adapter V0→V1 |
| `tests/test_admin_trading_contract_compatibility_smoke.py` | 10 | Smoke producer/consumer |
| `tests/fixtures/admin_trading_contract_smoke/*.json` | 4 | Fixtures synthétiques |

## RISKS

- À qualifier.
