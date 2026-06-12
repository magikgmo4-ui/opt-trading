---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01_PLAN
doc_type: execution_plan
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: planned
updated_at: 2026-05-18
---

# DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_PLAN_01

## Pre-flight

1. SSH `db-layer` reachable (valide)
2. `hostname` = `db-layer`
3. repo `/home/ghost/opt-trading` present
4. `git status` clean
5. CLI `/usr/local/bin/openclaw` present (version `2026.3.11`)
6. Gateway V2 config present (`/home/ghost/.openclaw/`)
7. Orchestrateur module present (`modules/desk_pro_orchestrator/`)

## Steps

### Step 1 — status (read-only)

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
```

Verifie que l'orchestrateur est fonctionnel et que les modules sont enregistres.

### Step 2 — explain (read-only)

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
```

Affiche la documentation du pipeline sans execution.

### Step 3 — sample-run (PAPER mode, dry-run)

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

Execute un sample-run avec la configuration exemple :
- mode: PAPER
- toutes les commandes en mode `sample`
- aucun trading live
- aucun write non controle
- sortie dans `data/desk_runs/`

## Stop conditions

| Condition | Action |
|---|---|
| `openclaw` absent | NEEDS_APPROVAL_INSTALL_DB_LAYER |
| write hors `data/desk_runs/` detecte | STOP |
| secret detecte | STOP |
| live trading detecte | STOP |
| `sudo` detecte | STOP |
| commande non prevue | STOP |

## Post-execution verification

1. Verifier que la sortie est dans `data/desk_runs/`
2. Verifier le `run_summary.json`
3. Verifier que tous les modules sont OK
4. Verifier `git status` reste clean

## RISKS

- À qualifier.
