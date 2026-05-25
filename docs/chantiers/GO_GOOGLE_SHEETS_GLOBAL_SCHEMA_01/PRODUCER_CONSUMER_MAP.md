---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_PRODUCER_CONSUMER_MAP
doc_type: producer_consumer_map
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/CANONICAL_SHEETS.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01/10_REPO_INVENTORY.md
  - modules/data_center/registry/consumers.json
  - modules/data_center/registry/producers.json
---

# PRODUCER_CONSUMER_MAP — Google Sheets global schema (V1)

## Surfaces prouvées (repo)

| Surface | Producer | Consumer | Preuves | Statut |
| --- | --- | --- | --- | --- |
| daily session (local) | `scripts/e2e/daily_session_journal.py` | `scripts/sheets/sync_daily_session.py` | scripts + `tests/e2e/test_sync_daily_session.py` | implemented |
| data_center market_metrics (views) | `derivatives_collector__bitget/binance` → views | `google_sheets__market_reporting` | `modules/data_center/registry/*.json` | consumer not_started |

## Mapping tab → surfaces

| tab | producer(s) | consumer(s) | write_enabled | notes |
| --- | --- | --- | --- | --- |
| sheets_registry | doc-only (manual) | tous | false | meta schema ; support fixtures-only |
| daily_sessions | daily_session_journal → sync_daily_session | dashboards/audit (TBD) | true (controlled) | writer actuel = `sheet1` ; tab canonical = `daily_sessions` |
| strategy_events | Desk Pro (futur) | Perf/Replay/Registry (futur) | false | inclut `signal_event.v1` comme `event_type` |
| strategy_perf | Perf Engine (futur) | dashboards (futur) | false | n/a |
| strategy_gates | gates job (futur) | registry tooling (futur) | false | n/a |
| registry_candidates | registry tooling (futur) | dashboards (futur) | false | n/a |
| market_metrics | Data Center views (`market_metrics.v1`) | `google_sheets__market_reporting` (not_started) | false | consumer doit lire views, pas producers roots |
| desk_snapshots | Desk Pro (futur) | Sheets consumers (futur) | false | fixtures-first ; refs seulement |
| visual_context | vision/headless (futur) | Desk Pro + Sheets (futur) | false | fixtures-first ; refs seulement |
| telegram_claims | telegram screener inbound (futur, non-live) | Desk Pro + Sheets (futur) | false | fixtures-only ; pas de Telegram live |
| watchlists | tooling (futur) | Desk Pro/Telegram (futur) | false | contractuel |

