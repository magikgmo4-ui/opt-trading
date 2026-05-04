---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01_DATA
doc_type: data_outputs_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 30_DESK_PRO_DATA_AND_OUTPUTS

## Arborescence Desk Pro

```
/opt/trading/
  data/
    desk_runs/          (38 runs, mars-avril 2026)
      desk_run_*/       (run_summary.json, engine outputs)
    desk_pro/           (vision data, config)
    logs/desk_pro/      (run logs + journal)
      latest_status.txt   "SUCCESS"
      latest_run_id.txt   "desk_run_20260405_010912"
      session_journal.log  (5 entries)
      latest.log -> desk_run_20260405_010912.log
  modules/
    desk_pro/           (core library: API, models, mount, UI)
    desk_pro_runner/    (operator facade CLI)
    desk_pro_orchestrator/ (execution pipeline)
    desk_pro_dashboard/ (visualization/export)
    desk_analyze/       (on-demand analysis)
    desk_capture_inputs/ (manual signal input)
    desk_snapshot_ingest/ (snapshot ingestion)
    desk_retention/     (data retention/pruning)
    desk_state/         (quick state view)
    desk_common/        (shared logic)

/shared/desk_pro/latest/    (canonical export, consumed by db-layer/student)
  dashboard_latest.html     (3166 B, 4 avril)
  journal_engine.json       (1172 B, 4 avril)
  perf_engine.json          (1040 B, 4 avril)
  portfolio_engine.json     (1168 B, 4 avril)
  run_summary.json          (2195 B, 4 avril)
```

## Historique des runs

| Periode | Nombre de runs | Dernier statut |
| --- | --- | --- |
| Mars 2026 | ~30 | SUCCESS |
| Avril 2026 | ~8 | SUCCESS |
| Mai 2026 | 0 | - |

Tous les runs documentes sont SUCCESS (OK: 11, Failed: 0 pour le dernier).

## Session journal

```
[2026-03-07] Run desk_run_20260307_005524 SUCCESS
[2026-03-07] test note from admin-trading
[2026-04-04] OT_DESK_PRO_HARDENING_01 validation note
[2026-04-04] Run desk_run_20260404_161017 SUCCESS
[2026-04-05] Run desk_run_20260405_010912 SUCCESS
```

## Wrappers globaux (/usr/local/bin)

Wrappers Desk Pro installes :
- cmd-desk_pro, menu-desk_pro, sanity-desk_pro
- cmd-desk_pro_runner
- cmd-desk_pro_dashboard
- cmd-desk_pro_orchestrator
- cmd-desk_analyze, cmd-desk_capture_inputs, cmd-desk_common
- cmd-desk_retention, cmd-desk_snapshot_ingest, cmd-desk_state

## Consommateurs

| Machine | Consommation | Source |
| --- | --- | --- |
| db-layer | desk_pro_db_cmd.sh | /shared/desk_pro/latest/ |
| student | desk_pro_student_cmd.sh | /shared/desk_pro/latest/ |

## Fraicheur

- Dernier run: 2026-04-05 (~1 mois)
- Outputs /shared: 2026-04-04 (dashboard mis a jour apres run)
- Donnees STALE mais historiquement SUCCESS
- Aucune donnee de mai 2026
