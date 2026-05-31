---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_PAPER_STABILITY_FIRST_JOB_PARENT_01_CADRAGE
doc_type: cadrage_parent
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_PAPER_STABILITY_FIRST_JOB_PARENT_01
status: open
lifecycle_stage: cadrage
created_at: 2026-05-30
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
pf_source: PAPER_PROMOTION_GATE_01
machine_cible: db-layer
machine_operateur: fantome
---

# 00_CADRAGE_PARENT — OpenClaw db-layer : Stabilité PAPER + Premier Job Boucle

## 1_MASTER_TARGET

Consolider la fenêtre de stabilité PAPER de l'orchestrateur sur db-layer et exécuter le premier job complet via la boucle OpenClaw contractuelle (FORMAT 1→5), avec gate humain obligatoire — toujours hors live.

## 2_PRECONDITIONS_VALIDEES

```text
PF_OPENCLAW_ORCHESTRATOR_FULL = PASS (GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01, fermé 2026-05-25)
db-layer PAPER smoke         = PASS (READONLY_WORKFLOW_SMOKE_01, 11/11 OK)
db-layer PAPER first op      = PASS (PAPER_FIRST_REGULAR_OPERATION_01, run desk_run_20260518_195528)
db-layer PAPER workflow val  = PASS (PAPER_WORKFLOW_VALIDATION_01)
db-layer PAPER regression    = PASS (PAPER_REGRESSION_SUITE_01)
db-layer PAPER promotion gate = PASS (PAPER_PROMOTION_GATE_01 — seuil: runs>=4, 11/11 OK, 0 failed)
loop contract                 = formalisé 5 formats (docs/openclaw/loop_contract/)
fleet                         = cursor-ai PASS + fantome PASS (docs/openclaw/fleet/INDEX.md)
```

## 3_GAPS_IDENTIFIES

| GAP | Description | Child GO cible |
| --- | --- | --- |
| GAP 1 | Fenêtre de stabilité PAPER non encore ouverte | CHILD_PAPER_STABILITY_WINDOW_01 |
| GAP 2 | Premier job complet via boucle FORMAT 1→5 non exécuté | CHILD_FIRST_LOOP_JOB_01 |
| GAP 3 | Gate humain FORMAT 5 jamais exercé sur un job réel | part de GAP 2 |

## 4_CHILD_GOs

| Child | Portée | Gate |
| --- | --- | --- |
| `CHILD_PAPER_STABILITY_WINDOW_01` | Runs PAPER consécutifs sur fenêtre 7j — logs + run IDs | PR + gate |
| `CHILD_FIRST_LOOP_JOB_01` | FORMAT 1 → OpenClaw → desk_pro_orchestrator → FORMAT 3/4 → FORMAT 5 humain | PR + gate humain |

## 5_INVARIANTS

```text
- Mode PAPER exclusif — aucun ordre réel, aucun live trading
- 0 runtime modifié hors scope
- FILE_SCOPE.txt dans chaque child dès J1
- Chaque PR gated sur sot/mainline
- Gate humain FORMAT 5 obligatoire avant tout merge impactant
- Aucun secret dans les commits
- Opérateur = fantome ; cible = db-layer via SSH
```

## 6_BOUCLE_REFERENCE

```yaml
# FORMAT 1 — job spec OpenClaw
job_id: FIRST_LOOP_JOB_DB_LAYER_01
intent: exécuter desk_pro_orchestrator en PAPER mode sur db-layer, retourner résultats
scope:
  machine: db-layer
  mode: PAPER
  command: python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json
allowed_ops: [read, execute_paper, log]
output_expected: FORMAT_3 avec run_id + module_results + verdict
```

## 7_CONFIGURATION

```text
Gateway OpenClaw db-layer : port 18789, user openclaw, session openclaw-gateway (tmux)
Orchestrateur             : python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator
Config exemple            : modules/desk_pro_orchestrator/config/run_config.example.json
SSH transport             : fantome → db-layer (validé PR #572 et suivants)
```

## 12_INVARIANTS

```text
- Doc-only au niveau parent (0 runtime)
- Children peuvent toucher docs + scripts de lancement uniquement
- Promotion hors PAPER = hors scope de ce parent
- Loop contract = docs/openclaw/loop_contract/ (non modifiable ici)
```

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_PAPER_STABILITY_FIRST_JOB_PARENT_01/00_INITIAL_PROJECT_DOC.md
Prochain : ouvrir CHILD_PAPER_STABILITY_WINDOW_01
```
