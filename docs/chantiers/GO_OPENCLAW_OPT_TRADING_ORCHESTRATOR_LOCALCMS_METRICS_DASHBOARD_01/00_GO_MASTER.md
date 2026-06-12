---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_METRICS_DASHBOARD_01
doc_type: go_master
repo: opt-trading
status: closed
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #506  (Daily session baseline final closeout — merged)
  - PR #508  (Next phase decision — merged, Option C sélectionnée)
created_at: 2026-05-17
closed_at: 2026-05-17
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_METRICS_DASHBOARD_01

## Objectif

Ajouter un dashboard métriques agrégées dans LocalCMS, basé sur les
données de journal existantes, en lecture seule.

## Périmètre

- `modules/localcms/app/main.py` — nouveaux endpoints + helper
- `tests/test_localcms.py` — 10 nouveaux tests

## Endpoints ajoutés

| Endpoint         | Type | Description                               |
| ---------------- | ---- | ----------------------------------------- |
| `GET /metrics`   | HTML | Dashboard visuel agrégé                   |
| `GET /metrics/daily` | JSON | API métriques daily session           |

## Métriques exposées

- `total_runs`, `pass_count`, `fail_count`
- `win_count`, `loss_count`, `breakeven_count`
- `pnl_cumulative`, `win_rate`
- `last_run` — résumé dernière session
- `sheets_sync` — dry_run / written / blocked / failed

## Sources de données

- `data/journal/daily/*.json` — entrées journal
- `data/journal/sync_log.jsonl` — historique sync Sheets

## Contraintes

- Read-only (GET uniquement, testé)
- No live trade / No Bitget order
- No automatic Sheets write
- LocalCMS read-only
- No secrets

## RISKS

- À qualifier.
