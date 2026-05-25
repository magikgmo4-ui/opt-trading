---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_INDEX
doc_type: index_inbox
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: open
lifecycle_stage: implementation
created_at: 2026-05-25
---

# Index — GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01

**Fixtures Google Sheets V1** — 11 tabs couverts, validateur R1-R10, 41 tests PASS.

## Chantier

`docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01/`

## Livrables

| Fichier | Rôle |
|---|---|
| `tests/fixtures/google_sheets_global_schema/*.jsonl` | 11 fixtures JSONL (1 par tab) |
| `tests/test_google_sheets_fixtures.py` | Validateur + 41 tests (0 FAIL) |

## Tabs couverts

```text
sheets_registry / daily_sessions / strategy_events / strategy_perf
strategy_gates / registry_candidates / market_metrics / desk_snapshots
visual_context / telegram_claims / watchlists
```

## Prochain GO

`GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01`
