---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_FIXTURE_CONTRACT_MAP
doc_type: fixture_contract_map
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 20_FIXTURE_CONTRACT_MAP — Google Sheets fixtures V1

## Résumé des règles de validation appliquées

Validateur implémenté dans `tests/test_google_sheets_fixtures.py`.

| Règle | Implémentée | Couverte par tests edge-case |
|---|---|---|
| R1 — tab_name canonique | oui | `test_r1_unknown_tab` |
| R2 — schema_version (sheets_registry) | via required | `test_r4_bad_enum` |
| R3 — colonnes required présentes et non-null | oui | `test_r3_missing_required_column`, `test_r3_null_required_column` |
| R4 — enum valeurs | oui | `test_r4_bad_enum`, `test_daily_sessions_enum_fail`, `test_strategy_gates_enum_fail` |
| R5 — timestamps ISO UTC Z | oui | `test_r5_bad_timestamp_format`, `test_r5_timestamp_missing_z` |
| R6 — PK colonnes présentes et non-null | oui | `test_r6_pk_null` |
| R7 — duplicate PK detection | oui | `test_r7_duplicate_pk`, `test_market_metrics_composite_pk_duplicate` |
| R8 — *_ref pas payload complet | oui | `test_r8_ref_is_full_json_payload` |
| R9 — write_mode non exercé | implicite | fixtures doc_only ou controlled (daily_sessions) ; aucun writer appelé |
| R10 — déterminisme | oui | `test_validator_deterministic` |

## Map fixture → contrat de colonnes

### sheets_registry

```text
Source: CANONICAL_SHEETS.md + COLUMNS_CONTRACTS
Colonnes required: tab_name (string), schema_version (string), owner_pf (string),
                   schema_status (enum:planned,active,deprecated), updated_at (iso_utc_ts)
PK: tab_name + schema_version
Enum schema_status couverts: planned, active, deprecated (toutes présentes)
write_mode: doc_only → aucun writer exercé
```

### daily_sessions

```text
Source: COLUMNS_CONTRACTS (daily_sessions)
Colonnes required: run_id (string), started_at (iso_utc_ts), status (enum:success,fail,warn)
Colonnes nullable: ended_at (iso_utc_ts), machine_id (string), report_ref (path_ref)
PK: run_id
Enum status couverts: success, warn, fail (toutes présentes)
write_mode: controlled_write (dry-run default) — seul tab write-enabled V1
```

### strategy_events

```text
Source: COLUMNS_CONTRACTS (strategy_events) + signal_event.v1 (modules/desk_pro)
Colonnes required: event_id (string), event_type (string), event_ts (iso_utc_ts)
Colonnes nullable: symbol, timeframe, payload_ref (json_ref), source_surface (string)
PK: event_id
event_type non-enum (ouvert) — inclut signal_event.v1 et market_context.v1
payload_ref = path_ref stable (pas payload inline)
write_mode: doc_only
```

### strategy_perf

```text
Source: COLUMNS_CONTRACTS (strategy_perf)
Colonnes required: as_of (iso_utc_ts), strategy_id (string), metric_name (string),
                   window (string), value (float)
PK composite: as_of + strategy_id + metric_name + window
write_mode: doc_only
```

### strategy_gates

```text
Source: COLUMNS_CONTRACTS (strategy_gates)
Colonnes required: as_of (iso_utc_ts), strategy_id (string), gate_name (string),
                   decision (enum:promote,hold,retire)
Colonnes nullable: reason (string)
PK composite: as_of + strategy_id + gate_name
Enum decision couverts: promote, hold (retire = gap toléré V1)
write_mode: doc_only
```

### registry_candidates

```text
Source: COLUMNS_CONTRACTS (registry_candidates)
Colonnes required: as_of (iso_utc_ts), strategy_id (string), candidate_name (string),
                   candidate_ref (json_ref)
PK composite: as_of + strategy_id + candidate_name
candidate_ref = path_ref (artefact), non payload inline
write_mode: doc_only
```

### market_metrics

```text
Source: market_metrics.v1 (PF_DATA_CENTER) + COLUMNS_CONTRACTS
Colonnes required: as_of (iso_utc_ts), symbol (symbol), metric_name (string), value (float)
Colonnes nullable: source_ref (path_ref)
PK composite: as_of + symbol + metric_name
source_ref → data/data_center/views/* (views, pas producers root) — conforme règle canonique
write_mode: doc_only ; consumer = google_sheets__market_reporting (not_started)
```

### desk_snapshots

```text
Source: COLUMNS_CONTRACTS (desk_snapshots)
Colonnes required: snapshot_id (string), created_at (iso_utc_ts), snapshot_ref (path_ref)
Colonnes nullable: notes (string)
PK: snapshot_id
snapshot_ref = path artefact image, pas payload inline
write_mode: doc_only
```

### visual_context

```text
Source: vision_analysis.v1 refs (PF_DESK_PRO) + COLUMNS_CONTRACTS
Colonnes required: context_id (string), created_at (iso_utc_ts), payload_ref (json_ref)
Colonnes nullable: notes (string)
PK: context_id
payload_ref = path artefact JSON, pas payload inline
write_mode: doc_only
```

### telegram_claims

```text
Source: telegram_claim.v1 (PF_TELEGRAM_SCREENER) + COLUMNS_CONTRACTS
Colonnes required: claim_id (string), claim_ts (iso_utc_ts), claim_type (string),
                   payload_ref (json_ref)
PK: claim_id
payload_ref → fixtures/admin_trading_contract_smoke/telegram_claim_v1_minimal.json (local)
Aucun appel Telegram. Pas de channel live.
write_mode: doc_only
```

### watchlists

```text
Source: COLUMNS_CONTRACTS (watchlists) — CONTROL_INPUT (futur)
Colonnes required: watchlist_id (string), symbol (symbol), timeframe (timeframe),
                   enabled (bool)
PK: watchlist_id
enabled = false couvert (wl_sol_h1_disabled)
write_mode: doc_only (CONTROL_INPUT validé si future activation)
```
