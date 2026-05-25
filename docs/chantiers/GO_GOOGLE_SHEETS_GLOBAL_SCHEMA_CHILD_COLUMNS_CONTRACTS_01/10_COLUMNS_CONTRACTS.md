---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01_COLUMNS_CONTRACTS
doc_type: columns_contracts
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_COLUMNS_CONTRACTS_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: open
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
---

# 10_COLUMNS_CONTRACTS — Google Sheets global schema (V1)

## Conventions V1

```text
- Les colonnes sont décrites de façon stable (pas de drift implicit).
- Les timestamps sont ISO UTC: YYYY-MM-DDTHH:MM:SSZ.
- Les payloads volumineux ne vont pas en cellule: utiliser *_ref (path/id).
- Un event unifié va dans strategy_events (inclut signal_event.v1 via event_type).
- PK candidate obligatoire (même composite).
```

## Types autorisés (V1)

```text
string | int | float | bool | iso_utc_ts | json_ref | path_ref
enum:<values> | currency | symbol | timeframe
```

## sheets_registry

PK candidate: `tab_name + schema_version`

| column | type | required | notes |
| --- | --- | --- | --- |
| tab_name | string | yes | doit correspondre exactement au nom de tab |
| schema_version | string | yes | ex: v1 |
| owner_pf | string | yes | PF_* |
| schema_status | enum:planned,active,deprecated | yes | état du contrat |
| updated_at | iso_utc_ts | yes | |

## daily_sessions

Surface existante (writer contrôlé) : daily_session_journal → sync_daily_session.

PK candidate: `run_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| run_id | string | yes | id stable du run |
| started_at | iso_utc_ts | yes | |
| ended_at | iso_utc_ts | no | |
| status | enum:success,fail,warn | yes | |
| machine_id | string | no | |
| report_ref | path_ref | no | ref vers artefact local |

## strategy_events

Enveloppe unifiée : inclut `signal_event.v1` via `event_type`.

PK candidate: `event_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| event_id | string | yes | id stable |
| event_type | string | yes | ex: signal_event.v1 |
| event_ts | iso_utc_ts | yes | timestamp de l’event |
| symbol | symbol | no | |
| timeframe | timeframe | no | |
| payload_ref | json_ref | no | référence vers jsonl/artefact |
| source_surface | string | no | ex: modules/desk_pro |

## strategy_perf

PK candidate: `as_of + strategy_id + metric_name + window`

| column | type | required | notes |
| --- | --- | --- | --- |
| as_of | iso_utc_ts | yes | |
| strategy_id | string | yes | |
| metric_name | string | yes | |
| window | string | yes | ex: 1d, 7d |
| value | float | yes | |

## strategy_gates

PK candidate: `as_of + strategy_id + gate_name`

| column | type | required | notes |
| --- | --- | --- | --- |
| as_of | iso_utc_ts | yes | |
| strategy_id | string | yes | |
| gate_name | string | yes | |
| decision | enum:promote,hold,retire | yes | |
| reason | string | no | |

## registry_candidates

PK candidate: `as_of + strategy_id + candidate_name`

| column | type | required | notes |
| --- | --- | --- | --- |
| as_of | iso_utc_ts | yes | |
| strategy_id | string | yes | |
| candidate_name | string | yes | |
| candidate_ref | json_ref | yes | |

## market_metrics

PK candidate: `as_of + symbol + metric_name`

| column | type | required | notes |
| --- | --- | --- | --- |
| as_of | iso_utc_ts | yes | |
| symbol | symbol | yes | |
| metric_name | string | yes | |
| value | float | yes | |
| source_ref | path_ref | no | vue/artefact, pas producers roots |

## desk_snapshots

PK candidate: `snapshot_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| snapshot_id | string | yes | |
| created_at | iso_utc_ts | yes | |
| snapshot_ref | path_ref | yes | ref artefact (image) |
| notes | string | no | |

## visual_context

PK candidate: `context_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| context_id | string | yes | |
| created_at | iso_utc_ts | yes | |
| payload_ref | json_ref | yes | ref artefact |
| notes | string | no | |

## telegram_claims

PK candidate: `claim_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| claim_id | string | yes | |
| claim_ts | iso_utc_ts | yes | |
| claim_type | string | yes | |
| payload_ref | json_ref | yes | fixtures-only |

## watchlists

PK candidate: `watchlist_id`

| column | type | required | notes |
| --- | --- | --- | --- |
| watchlist_id | string | yes | |
| symbol | symbol | yes | |
| timeframe | timeframe | yes | |
| enabled | bool | yes | |
