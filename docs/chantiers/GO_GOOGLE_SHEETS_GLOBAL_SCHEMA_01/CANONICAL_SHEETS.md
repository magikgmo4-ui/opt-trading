---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_CANONICAL_SHEETS
doc_type: schema_tables
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/INVENTORY.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01/10_REPO_INVENTORY.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/20_GLOBAL_SCHEMA_TARGET.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/PRODUCER_CONSUMER_MAP.md
---

# CANONICAL_SHEETS — liste canonique des feuilles (V1)

## Décision

La liste V1 est volontairement compacte et découpe :

- journal / run logs (daily session)
- événements (unifiés dans `strategy_events`)
- perf / gates / registry (contrats)
- contextes consommables (market_metrics / desk_snapshot / visual_context / telegram_claims)
- meta (registry de schéma)

Les contrats de colonnes complets sont hors-scope ici (child `COLUMNS_CONTRACTS`).

## Règles

```text
- Chaque feuille doit avoir une finalité (purpose) et au moins un producer ou un consumer identifié.
- Aucun payload complet en cellule: utiliser *_ref (path/id).
- Timestamps ISO UTC: YYYY-MM-DDTHH:MM:SSZ.
- PK candidate obligatoire (même composite).
- write_mode contrôlé: dry-run default ; controlled-write explicite si un writer existe.
```

## Feuilles canoniques (V1)

| sheet_name | purpose | owner / producer | consumer | source_surface | write_mode | read_mode | primary_key candidate | schema_status | fixture_required | migration_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sheets_registry | registry du schéma (tabs + versions + owners) | PF_GOOGLE_SHEETS_CONSUMER (doc-only) | tous | docs/chantiers | doc_only | read_only | `tab_name + schema_version` | planned | yes | n/a |
| daily_sessions | 1 ligne par run daily session | `scripts/e2e/daily_session_journal.py` → `scripts/sheets/sync_daily_session.py` | dashboards/audit (TBD) | scripts | controlled_write (dry-run default) | read_only | `run_id` | existing (sheet1 today) | yes | worksheet title à aligner sur `daily_sessions` |
| strategy_events | enveloppe d’events observés/enrichis (inclut `signal_event.v1`) | Desk Pro (futur) | Perf/Replay/Registry (futur) | modules/desk_pro | doc_only | read_only | `event_id` | planned | yes | remplace le besoin d’un tab `signal_events` séparé |
| strategy_perf | agrégats / score vectors | Perf Engine (futur) | dashboards (futur) | modules/perf_engine (TBD) | doc_only | read_only | `as_of + strategy_id + metric_name + window` | planned | yes | n/a |
| strategy_gates | décisions de promotion/retrait | gate job (futur) | registry promotion (futur) | jobs/scripts (TBD) | doc_only | read_only | `as_of + strategy_id + gate_name` | planned | yes | n/a |
| registry_candidates | candidats registry (draft) | registry tooling (futur) | dashboards/registry (futur) | registry/tools (TBD) | doc_only | read_only | `as_of + strategy_id + candidate_name` | planned | yes | n/a |
| market_metrics | contexte marché (contract `market_metrics.v1`) pour reporting | Data Center producers (`derivatives_collector__*`) | `google_sheets__market_reporting` (not_started) | modules/data_center | doc_only (writer Sheets absent) | read_only | `as_of + symbol + metric_name` | planned | yes | source de vérité = `data_center/views/*`, pas un producer path |
| desk_snapshots | snapshots Desk Pro (références) | Desk Pro (futur) | Sheets consumers (futur) | modules/desk_pro | doc_only | read_only | `snapshot_id` | planned | yes | stocker `path_ref` (artefact) plutôt que l’image |
| visual_context | contexte visuel (références) | vision/headless (futur) | Desk Pro + Sheets (futur) | vision tooling (TBD) | doc_only | read_only | `context_id` | planned | yes | stocker `payload_ref` (artefact) |
| telegram_claims | inbound claims Telegram (enveloppes) | Telegram screener inbound (futur, non-live ici) | Desk Pro + Sheets (futur) | telegram tooling (TBD) | doc_only | read_only | `claim_id` | planned | yes | pas de Telegram live ; fixtures-only |
| watchlists | listes symbol/timeframe (contractuel) | tooling (futur) | Desk Pro / Telegram (futur) | tools/registry (TBD) | doc_only | read_only | `watchlist_id` | planned | yes | n/a |

