---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_SHEET_FIXTURE_INVENTORY
doc_type: sheet_fixture_inventory
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 10_SHEET_FIXTURE_INVENTORY — Google Sheets fixtures V1

## Inventaire complet

| sheet_name | fixture_file | source_contract | required_columns | optional_columns | validation_status |
|---|---|---|---|---|---|
| sheets_registry | tests/fixtures/google_sheets_global_schema/sheets_registry.jsonl | CANONICAL_SHEETS.md + COLUMNS_CONTRACTS | tab_name, schema_version, owner_pf, schema_status, updated_at | — | 0 FAIL |
| daily_sessions | tests/fixtures/google_sheets_global_schema/daily_sessions.jsonl | COLUMNS_CONTRACTS (daily_sessions) | run_id, started_at, status | ended_at, machine_id, report_ref | 0 FAIL |
| strategy_events | tests/fixtures/google_sheets_global_schema/strategy_events.jsonl | COLUMNS_CONTRACTS (strategy_events) | event_id, event_type, event_ts | symbol, timeframe, payload_ref, source_surface | 0 FAIL |
| strategy_perf | tests/fixtures/google_sheets_global_schema/strategy_perf.jsonl | COLUMNS_CONTRACTS (strategy_perf) | as_of, strategy_id, metric_name, window, value | — | 0 FAIL |
| strategy_gates | tests/fixtures/google_sheets_global_schema/strategy_gates.jsonl | COLUMNS_CONTRACTS (strategy_gates) | as_of, strategy_id, gate_name, decision | reason | 0 FAIL |
| registry_candidates | tests/fixtures/google_sheets_global_schema/registry_candidates.jsonl | COLUMNS_CONTRACTS (registry_candidates) | as_of, strategy_id, candidate_name, candidate_ref | — | 0 FAIL |
| market_metrics | tests/fixtures/google_sheets_global_schema/market_metrics.jsonl | market_metrics.v1 (PF_DATA_CENTER) | as_of, symbol, metric_name, value | source_ref | 0 FAIL |
| desk_snapshots | tests/fixtures/google_sheets_global_schema/desk_snapshots.jsonl | COLUMNS_CONTRACTS (desk_snapshots) | snapshot_id, created_at, snapshot_ref | notes | 0 FAIL |
| visual_context | tests/fixtures/google_sheets_global_schema/visual_context.jsonl | vision_analysis.v1 (PF_DESK_PRO) | context_id, created_at, payload_ref | notes | 0 FAIL |
| telegram_claims | tests/fixtures/google_sheets_global_schema/telegram_claims.jsonl | telegram_claim.v1 (PF_TELEGRAM_SCREENER) | claim_id, claim_ts, claim_type, payload_ref | — | 0 FAIL |
| watchlists | tests/fixtures/google_sheets_global_schema/watchlists.jsonl | COLUMNS_CONTRACTS (watchlists) | watchlist_id, symbol, timeframe, enabled | — | 0 FAIL |

## Notes par tab

### sheets_registry
- Contient 11 rows — une par tab canonique.
- PK composite : `tab_name + schema_version`.
- Preuve de couverture complète du schéma V1.

### daily_sessions
- 3 rows couvrant les 3 statuts enum : `success`, `warn`, `fail`.
- `ended_at` nullable : la row `fail` a `null`.
- `report_ref` nullable : couvert.

### strategy_events
- Inclut 2 `signal_event.v1` et 1 `market_context.v1` (enveloppe unifiée).
- `payload_ref` nullable : couvert avec `null` et `path_ref` stable.
- Source : `modules/desk_pro` et `modules/data_center`.

### strategy_perf / strategy_gates / registry_candidates
- PKs composites prouvées.
- `strategy_gates.decision` couvre 2 valeurs enum (`promote`, `hold`).

### market_metrics
- 3 rows : 2 symbols (BTCUSDT, ETHUSDT), 2 metrics (open_interest_usd, funding_rate).
- `source_ref` pointe vers `data/data_center/views/market_metrics/latest.json` — pas vers un producer root.
- Conforme à la règle canonique : Data Center = source normalisée.

### desk_snapshots / visual_context
- Refs uniquement (path_ref). Pas d'images inlinées.
- `notes` nullable : couvert.

### telegram_claims
- `payload_ref` pointe vers fixtures locales — pas de Telegram live.
- Conforme : pas d'appel Telegram.

### watchlists
- 3 symbols/timeframes. Couvre `enabled = false`.

## Source canonique par tab

| Tab | Source | Note |
|---|---|---|
| sheets_registry | Doc-only (manuel) | CONTROL_INPUT |
| daily_sessions | scripts/e2e/daily_session_journal.py | Seul tab write_enabled (controlled) |
| strategy_events | modules/desk_pro (futur) | doc_only |
| strategy_perf | modules/perf_engine (futur) | doc_only |
| strategy_gates | jobs/scripts (futur) | doc_only |
| registry_candidates | registry/tools (futur) | doc_only |
| market_metrics | PF_DATA_CENTER (views) | google_sheets__market_reporting = not_started |
| desk_snapshots | modules/desk_pro (futur) | doc_only, refs only |
| visual_context | vision tooling (futur) | doc_only, refs only |
| telegram_claims | telegram tooling (futur, non-live) | fixtures-only |
| watchlists | tooling (futur) | CONTROL_INPUT (futur) |
