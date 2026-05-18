---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
topic_keys:
  - openclaw
  - db-layer
  - ssh
  - orchestrator
  - dashboard
  - readonly_workflow
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 7_CANONICAL_STATE"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_01

## Classification

- type : child smoke read-only workflow
- statut : open
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- poste operateur : `fantome`
- machine cible unique : `db-layer`
- transport autorise : `SSH` controle uniquement
- mode d'execution vise : workflow reel borne via l'orchestrateur `sample-run` en mode PAPER, sans live ni write libre

## But

Appliquer le runbook db-layer figé sur un workflow réel mais read-only, en utilisant la façade opérateur `desk_pro_runner` pour inspecter le dernier run existant sans déclencher de write libre ni de nouveau pipeline.

## 7_CANONICAL_STATE

```text
fantome = poste operateur
db-layer = cible OpenClaw validee
SSH = transport controle valide
OpenClaw db-layer = orchestrateur valide + runbook operationnel fige
workflow smoke = `sample-run` PAPER mode avec sorties controlees
```

## Verification pre-execution

1. verifier `sot/mainline` propre au moins au merge `a746c100`
2. verifier `ssh db-layer` joignable
3. verifier `hostname`, `pwd`, `git status` cote `db-layer`
4. relire le runbook db-layer mergé via PR `#555`
5. confirmer la commande exacte du workflow borne

## Commande exacte du workflow read-only

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

## Cadre

- `desk_pro_orchestrator status` et `desk_pro_orchestrator explain` sont autorises comme preflight read-only
- `sample-run` est le workflow borne du smoke et ecrit uniquement sous `data/desk_runs/`
- aucun write libre hors sorties controlees
- aucun secret
- aucun live trading
- aucun sudo

## Livrables

- `00_INITIAL_PROJECT_DOC.md`
- `DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_PLAN_01.md`
- `DBLAYER_ORCHESTRATOR_READONLY_WORKFLOW_SMOKE_REPORT_01.md`
- `90_CLOSEOUT.md`

## Hors Perimetre

- `run-and-show`
- creation d'un nouveau `desk_run_*`
- write dans repo
- secret
- live trading
- `sudo`
