---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_PRODUCER_CONSUMER_MAP_DRAFT
doc_type: producer_consumer_map_draft
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: draft
source_kind: canonical
updated_at: 2026-05-24
---

# PRODUCER_CONSUMER_MAP_DRAFT — Google Sheets global schema

## Objectif

Assigner, pour chaque feuille canonique, au moins un producer ou un consumer existant ou planifié, en mode read-only d’abord.

## Surfaces déjà prouvées (repo)

| Surface | Preuve | Rôle |
| --- | --- | --- |
| daily session journal | `scripts/e2e/daily_session_journal.py` | producer local (JSON/CSV) |
| daily session sheets sync | `scripts/sheets/sync_daily_session.py` | writer contrôlé (dry-run default) |
| datasheet writer | `modules/datasheet_writer/app/writer.py` | producer CSV local (pas Sheets) |
| Desk Pro | `modules/desk_pro/*` | consumer/hub (inputs unifiés) |

## Mapping initial (à compléter)

| Feuille | Producer(s) | Consumer(s) | Statut |
| --- | --- | --- | --- |
| daily_sessions | `scripts/e2e/daily_session_journal.py` → `scripts/sheets/sync_daily_session.py` | dashboards (TBD), audit (TBD) | existing surface |
| strategy_events | Desk Pro (futur) | Perf / replay (futur) | cadrage |
| strategy_perf | Perf Engine (futur) | dashboards (futur) | cadrage |
| strategy_gates | gate job (futur) | registry promotion (futur) | cadrage |
| registry_candidates | registry tooling (futur) | dashboards (futur) | cadrage |

## Next

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_PRODUCER_CONSUMER_MAP_01
```

