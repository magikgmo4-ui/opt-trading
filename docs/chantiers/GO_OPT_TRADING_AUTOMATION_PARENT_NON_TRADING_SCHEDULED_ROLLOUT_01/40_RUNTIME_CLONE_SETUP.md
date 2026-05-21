---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_RUNTIME_CLONE_SETUP
doc_type: runtime_setup
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: draft
---

# 40_RUNTIME_CLONE_SETUP

## Separation de scope

- Cette branche parent reste doc-only.
- Le runtime non-trading vit sur `go/runtime-non-trading-workers-01`.
- Une PR runtime distincte doit porter workers, LocalCMS runtime changes,
  artefacts de scheduler et tout code executable.

## Attendus de la PR runtime

- Exclure `signal_dry_run_worker.py`.
- Garder uniquement observe/draft/HITL/bridges/scheduler/canary non-trading.
- Documenter rollback et gates.
