---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01_PLAN
doc_type: execution_plan
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: planned
updated_at: 2026-05-18
---

# DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_PLAN_01

## Prechecks

1. base locale >= `9ef55ca0`
2. SSH `db-layer` reachable
3. `hostname`, `pwd`, `git status` db-layer
4. `openclaw --version`
5. runbook PR `#555` relu
6. closeout PAPER validation PR `#563` relu

## Mini-suite de regression PAPER

### Step A — baseline PAPER run

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json
```

### Step B — status/explain

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
```

### Step C — safe alternative run

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

## Contrôles attendus

- run IDs capturés pour Step A et Step C
- mode `PAPER`
- `11/11` modules OK (ou ecarts documentes)
- actions `NO_ACTION` / `PREPARE_LONG` / `PREPARE_SHORT` uniquement
- aucun champ secret (`api_key`, `secret`, `token`, `password`)
- `git status` clean apres chaque run

## Stop conditions

| Condition | Action |
|---|---|
| mode != PAPER | STOP |
| action hors allowlist | STOP |
| ordre reel detecte | STOP |
| secret detecte | STOP |
| sudo requis | STOP |
| write hors `data/desk_runs/` | STOP |
| commande hors runbook | STOP |

## RISKS

- À qualifier.
