---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01_PRODUCER_CONSUMER_MAP
doc_type: producer_consumer_map
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01
status: open
source_kind: canonical
updated_at: 2026-05-25
---

# 20_PRODUCER_CONSUMER_MAP — draft enrichi (repo-first)

## Règle

Une feuille canonique doit avoir au moins un producer ou consumer identifié (existant ou explicitement “futur”), et son statut (`implemented` / `not_started` / `doc_only`) doit être explicite.

## Surfaces existantes (repo)

| Surface | PF | Producer | Consumer | Statut | Preuves |
| --- | --- | --- | --- | --- | --- |
| daily session (local journal) | PF_RUNTIME_ORCHESTRATOR | `scripts/e2e/daily_session_journal.py` | `scripts/sheets/sync_daily_session.py` | implemented | scripts + tests e2e |
| google sheets market reporting (data center) | PF_GOOGLE_SHEETS_CONSUMER | (TBD) | `modules/data_center/registry/consumers.json` | not_started | registry data center |
| datasheet trades csv | PF_TRADING_RESULTS | `modules/datasheet_writer/app/writer.py` | (dashboards TBD) | implemented (csv) | module + outputs `data/datasheet/` |
| strategy tools csv exports | PF_STRATEGY_RESEARCH | `tools/strategy/**` | (humain/offline) | implemented (offline) | outils stratégie |

## Mapping tab → surface (pré-cadrage)

| Tab candidate | Surface source | Statut |
| --- | --- | --- |
| `daily_sessions` | daily session sync (sheet1 aujourd’hui) | existing, à figer |
| `strategy_events` | Desk Pro (futur) | doc_only |
| `strategy_perf` | Perf Engine (futur) | doc_only |
| `strategy_gates` | gates/registry (futur) | doc_only |
| `registry_candidates` | registry tooling (futur) | doc_only |

