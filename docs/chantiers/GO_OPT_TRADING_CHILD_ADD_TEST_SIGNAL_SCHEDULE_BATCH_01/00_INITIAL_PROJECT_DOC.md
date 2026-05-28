---
doc_id: GO_OPT_TRADING_CHILD_ADD_TEST_SIGNAL_SCHEDULE_BATCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
module: ai_workers
go_id: GO_OPT_TRADING_CHILD_ADD_TEST_SIGNAL_SCHEDULE_BATCH_01
status: closed
lifecycle_stage: done
created_at: 2026-05-28
closed_at: 2026-05-28
pr: pending
links:
  - tests/test_signal_workers.py
  - scripts/ai/workers/signal_processor.py
  - scripts/ai/workers/signal_stats.py
  - .github/workflows/strict-workers-schedule.yml
  - docs/registry/JOBS_REGISTRY.md
---

# GO_OPT_TRADING_CHILD_ADD_TEST_SIGNAL_SCHEDULE_BATCH_01

## Objectif

Ajouter des tests unitaires pour les 3 entrées du JOBS_REGISTRY en `add_test` :
- `aw_signal_processor` (`signal_processor.py`) — candidate, high risk
- `aw_signal_stats` (`signal_stats.py`) — candidate, medium risk
- `gha_strict_workers_schedule` (`strict-workers-schedule.yml`) — active, medium risk

## Livrable

`tests/test_signal_workers.py` — 34 tests, 4 classes :
- `TestValidate` (9) — validate() : confidence, type, direction, price
- `TestCrossCheck` (5) — cross_check() : confirmed/pending/conflicting
- `TestDryRunGuard` (4) — dry_run_guard() : order generation, file write, no-order paths
- `TestComputeStats` (5) — compute_stats() : empty, single, mixed, top_sources, avg_ms
- `TestLoadJournal` (4) — load_journal() : empty dir, JSONL, multi-file, empty lines
- `TestScheduleWorkflow` (7) — YAML structure, cron, dispatch, permissions, packet ref

## Verdict

```
34/34 PASS
JOBS_REGISTRY.md v1.3 mis à jour :
  aw_signal_processor : add_test → keep
  aw_signal_stats     : add_test → keep
  gha_strict_workers_schedule : add_test → keep (tests: test_signal_workers.py)
```
