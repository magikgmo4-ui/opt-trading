---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01_FIXTURES_PLAN
doc_type: fixtures_plan
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01
status: open
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/10_COLUMNS_CONTRACTS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
---

# 20_FIXTURES_PLAN — fixtures-first (V1)

## Objectif

Définir un plan de fixtures minimal pour prouver que les contrats de colonnes V1 sont exploitables en lecture (parse/validate), sans dépendre de Google Sheets live.

## Conventions

```text
- Une fixture par tab canonique (au minimum).
- Format par défaut: CSV (UTF-8).
- Pour payloads: JSONL ou JSON (référencé via *_ref).
- Les timestamps de fixtures sont ISO UTC.
- Les fixtures ne contiennent pas de secrets et n’exposent pas d’identifiants sensibles.
```

## Coverage minimal attendu

| tab | fixture | cas minimum |
| --- | --- | --- |
| sheets_registry | sheets_registry_v1.csv | 3 tabs (planned/active/deprecated) |
| daily_sessions | daily_sessions_v1.csv | 1 run success + 1 run warn |
| strategy_events | strategy_events_v1.csv + payloads.jsonl | 1 signal_event.v1 + 1 event non-signal |
| strategy_perf | strategy_perf_v1.csv | 2 metrics / 2 windows |
| strategy_gates | strategy_gates_v1.csv | promote/hold/retire |
| registry_candidates | registry_candidates_v1.csv | 1 candidate + ref |
| market_metrics | market_metrics_v1.csv | 3 metrics (funding/oi/price) |
| desk_snapshots | desk_snapshots_v1.csv | 1 snapshot_ref path |
| visual_context | visual_context_v1.csv | 1 payload_ref |
| telegram_claims | telegram_claims_v1.csv + payloads.jsonl | fixtures-only |
| watchlists | watchlists_v1.csv | 3 pairs symbol/timeframe |

## Emplacement proposé

```text
docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/fixtures/
```

Ce child ne matérialise pas forcément les fixtures dans cette passe; il fixe d’abord le plan (formats + coverage + conventions) pour éviter la génération de fixtures non alignées.
