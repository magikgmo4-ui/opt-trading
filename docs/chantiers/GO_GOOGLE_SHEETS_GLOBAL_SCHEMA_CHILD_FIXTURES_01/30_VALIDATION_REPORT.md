---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_VALIDATION_REPORT
doc_type: validation_report
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 30_VALIDATION_REPORT — Google Sheets fixtures V1

## Verdict

**PASS — 0 FAIL sur tous les tabs**

## Résultats tests

```
python3 -m pytest tests/test_google_sheets_fixtures.py -v
```

| Classe | Tests | Résultat |
|---|---|---|
| TestFixtureFilesExist | 11 | PASS |
| TestFixtureValidation | 11 | PASS |
| TestFixtureMinimumRows | 5 | PASS |
| TestValidatorEdgeCases | 14 | PASS |
| **Total** | **41** | **41 PASS, 0 FAIL** |

## Couverture par règle

| Règle | Résultat |
|---|---|
| R1 — tab canonique | PASS |
| R2 — schema_version | PASS (via R3 required) |
| R3 — colonnes required | PASS : 0 FAIL sur 11 fixtures + 2 edge-case tests |
| R4 — enum values | PASS : 3 edge-case tests (sheets_registry, daily_sessions, strategy_gates) |
| R5 — iso_utc_ts Z | PASS : 2 edge-case tests (format + timezone +00:00 rejeté) |
| R6 — PK non-null | PASS : 1 edge-case test |
| R7 — duplicate PK | PASS : 2 edge-case tests (simple + composite) |
| R8 — *_ref pas JSON payload | PASS : 1 edge-case test |
| R9 — write_mode | PASS implicite : aucun writer Google appelé |
| R10 — déterminisme | PASS : test_validator_deterministic |

## Couverture API / sécurité

```
test_no_google_api_calls → PASS
```

Aucun module `google.*` ou `gspread` chargé pendant les tests.

## Couverture par tab

| Tab | Rows | PK type | Enums testés | Timestamps | Refs | Statut |
|---|---|---|---|---|---|---|
| sheets_registry | 11 | composite | planned, active, deprecated | oui | — | 0 FAIL |
| daily_sessions | 3 | simple | success, warn, fail | oui | path_ref | 0 FAIL |
| strategy_events | 3 | simple | — | oui | json_ref (nullable) | 0 FAIL |
| strategy_perf | 3 | composite 4-col | — | oui | — | 0 FAIL |
| strategy_gates | 3 | composite 3-col | promote, hold | oui | — | 0 FAIL |
| registry_candidates | 2 | composite 3-col | — | oui | json_ref | 0 FAIL |
| market_metrics | 3 | composite 3-col | — | oui | path_ref | 0 FAIL |
| desk_snapshots | 2 | simple | — | oui | path_ref | 0 FAIL |
| visual_context | 2 | simple | — | oui | json_ref | 0 FAIL |
| telegram_claims | 2 | simple | — | oui | json_ref | 0 FAIL |
| watchlists | 3 | simple | — | — | — | 0 FAIL |

## Tolérance V1 acceptée

Règle : les WARN sont acceptables si explicitement listés.

| WARN potentiel | Décision |
|---|---|
| strategy_gates.decision ne couvre pas `retire` | Toléré V1 — enum défini, fixture minimale |
| ended_at null dans daily_sessions row `fail` | Toléré V1 — colonne nullable par contrat |
| source_surface null dans strategy_events | Toléré V1 — colonne nullable par contrat |
