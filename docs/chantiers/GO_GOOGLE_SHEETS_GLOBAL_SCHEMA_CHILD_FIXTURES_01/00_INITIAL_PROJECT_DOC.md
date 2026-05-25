---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
pf_id: PF_GOOGLE_SHEETS_CONSUMER
status: open
lifecycle_stage: implementation
surface: tests/fixtures/google_sheets_global_schema
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
upstream:
  - PF_DATA_CENTER
  - PF_DESK_PRO
  - PF_OPENCLAW_ORCHESTRATOR_FULL
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/VALIDATION_RULES.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01/10_COLUMNS_CONTRACTS.md
---

# 00_INITIAL_PROJECT_DOC — Google Sheets Global Schema Fixtures V1

## Objectif

Créer et valider un pack de fixtures Google Sheets couvrant les 11 tabs du schéma global V1, après merge des validation rules.

Prouver que :
- les colonnes, types, required fields, optional fields et règles de validation acceptent des payloads fixtures cohérents
- le validateur (règles R1-R10 de `VALIDATION_RULES.md`) est fonctionnel et déterministe
- aucun appel Google API n'est nécessaire pour ce proof-of-concept

## Périmètre

### Fixtures couvertes

11 tabs canoniques selon `CANONICAL_SHEETS.md` :

| Tab | Fixture | PK |
|---|---|---|
| sheets_registry | sheets_registry.jsonl | tab_name + schema_version |
| daily_sessions | daily_sessions.jsonl | run_id |
| strategy_events | strategy_events.jsonl | event_id |
| strategy_perf | strategy_perf.jsonl | as_of + strategy_id + metric_name + window |
| strategy_gates | strategy_gates.jsonl | as_of + strategy_id + gate_name |
| registry_candidates | registry_candidates.jsonl | as_of + strategy_id + candidate_name |
| market_metrics | market_metrics.jsonl | as_of + symbol + metric_name |
| desk_snapshots | desk_snapshots.jsonl | snapshot_id |
| visual_context | visual_context.jsonl | context_id |
| telegram_claims | telegram_claims.jsonl | claim_id |
| watchlists | watchlists.jsonl | watchlist_id |

### Règles canoniques respectées

- Data Center = source normalisée. Les fixtures `market_metrics` pointent vers `data/data_center/views/*` via `source_ref`.
- Google Sheets = consumer/export/reporting/control. Sheets n'est pas une source trading canonique.
- Les `*_ref` sont des path_ref (chemins/ids), jamais des payloads JSON complets.
- Aucun appel Google Sheets API. Aucun credential. Aucune spreadsheet réelle.

## NE PAS FAIRE

- Appeler Google Sheets API
- Créer une spreadsheet réelle
- Écrire des credentials
- Modifier `.env`
- Appeler Data Center live
- Appeler Telegram
- Trader
- Faire de Sheets une source canonique trading
- Mélanger avec datasheet_writer runtime
