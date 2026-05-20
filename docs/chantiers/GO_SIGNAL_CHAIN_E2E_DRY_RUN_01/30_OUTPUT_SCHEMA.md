---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_OUTPUT_SCHEMA
doc_type: schema
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 30_OUTPUT_SCHEMA

## Pipeline report (dry_run_pipeline.py)

Top-level keys:

```json
{
  "pipeline": "E2E dry-run pipeline",
  "dry_run": true,
  "paper_mode": true,
  "started_at": "UTC ISO",
  "completed_at": "UTC ISO",
  "duration_s": 12.345,
  "all_ok": true,
  "steps": [
    {"step": "1_signal_router", "timestamp": "UTC ISO", "result": {}}
  ],
  "localcms": {"/health": {"ok": false}},
  "localcms_ok": false
}
```

Step `1c_notification_dispatcher_dry_run`:

```json
{
  "dispatch": [
    {"ok": true, "dry_run": true, "event_type": "signal_received", "message": "<html>...</html>"},
    {"ok": true, "dry_run": true, "event_type": "proposition_generated", "message": "<html>...</html>"},
    {"ok": true, "dry_run": true, "event_type": "result_known", "message": "<html>...</html>"}
  ]
}
```

## Daily session journal (daily_session_journal.py)

Artifacts:

- JSON: `data/journal/daily/<run_id>.json`
- CSV: `data/journal/daily/<run_id>.csv`

Extensions notables dans le JSON:

```json
{
  "run_id": "YYYYMMDD_###",
  "tmux_before": {"count": 0},
  "tmux_after": {"count": 0},
  "localcms": {"/health": {"ok": false}},
  "closeout_acknowledged": false,
  "sheets_sync": {
    "enabled": true,
    "mode": "dry_run",
    "returncode": 0,
    "stdout_tail": "..."
  }
}
```

## Ancrage umbrella

- `MASTER_TARGET` : standardiser les artifacts E2E du produit final total
- `Kanban bundle` : reste la carte de navigation principale
- `Prochain item Kanban exact` : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- `Gaps encore ouverts` : closeout umbrella absent, output final umbrella non agrege, evidence pack transverse non encore compile
