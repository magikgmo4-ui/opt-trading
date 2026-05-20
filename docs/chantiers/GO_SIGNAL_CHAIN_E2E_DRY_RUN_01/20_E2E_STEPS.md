---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_E2E_STEPS
doc_type: runbook
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_E2E_STEPS

## Pipeline (proof)

Source: `scripts/e2e/dry_run_pipeline.py`

1) `1_signal_router`
2) `1b_desk_pro_dry_run`
3) `1c_notification_dispatcher_dry_run`
   - events: `signal_received`, `proposition_generated`, `result_known`
   - output: liste de dispatch dry-run avec message rendu
4) `2_proposition_engine`
5) `3_validation_gate`
6) `4_trade_executor` (paper/dry-run)
7) `5_result_tracker`
8) `6_datasheet_writer` (dry-run)
9) `7_learning_feeder` (dry-run, sans stockage brick)
10) `8_localcms_endpoints` (best-effort)

## Journal (daily session)

Source: `scripts/e2e/daily_session_journal.py`

1) Run pipeline (in-process)
2) Snapshot tmux + LocalCMS (before/after)
3) Persist report JSON + CSV
4) Optionnel: `--sync-sheets` (subprocess, dry-run par defaut)
5) Print un summary humain sur stdout (ASCII safe)
