---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01_PLAN
doc_type: execution_plan
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: planned
updated_at: 2026-05-18
---

# DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_PLAN_01

## Pre-flight

1. SSH `db-layer` reachable
2. `hostname` = `db-layer`
3. repo `/home/ghost/opt-trading` present
4. `git status` clean
5. `openclaw --version` present
6. runbook merged via PR `#555` reviewed
7. latest run exists in `data/desk_runs/`

## Workflow exact

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

## Preflight read-only commands

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
```

## Expected evidence

- status confirms the orchestrator entry point is available
- explain confirms the pipeline order and the bounded sample-run workflow
- sample-run execute le pipeline Desk Pro en mode PAPER et ecrit uniquement les artefacts controles sous `data/desk_runs/`
- `git status` remains clean before and after

## Stop conditions

| Condition | Action |
|---|---|
| write required outside `data/desk_runs/` | STOP |
| secret detected | STOP |
| live trading detected | STOP |
| sudo required | STOP |
| runbook mismatch | STOP |

## RISKS

- À qualifier.
