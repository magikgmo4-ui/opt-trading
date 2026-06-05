---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01
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
  - paper
  - regression
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section Commandes exactes"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_WORKFLOW_VALIDATION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01

## Classification

- type : child orchestrator PAPER regression suite
- statut : open
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- poste operateur : `fantome`
- machine cible unique : `db-layer`
- transport autorise : `SSH` controle uniquement

## But

Rejouer une mini-suite de regression PAPER bornee pour verifier que la chaine orchestrateur reste stable au-dela d'un run unique, sans live trading, sans ordre reel, sans secret et sans write libre.

## 7_CANONICAL_STATE

```text
fantome = poste operateur
db-layer = cible OpenClaw validee
runbook db-layer = merge PR #555
paper workflow validation = merge PR #563 (PASS)
objectif courant = regression PAPER bornee
```

## Cadre securite

- mode PAPER uniquement
- aucun live trading
- aucun ordre reel
- aucun secret
- aucun sudo
- aucun write libre
- writes autorises uniquement pour logs/artefacts PAPER prevus sous `data/desk_runs/`
- stop immediat si action hors runbook

## Commandes exactes (suite minimale)

1. baseline PAPER run

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json
```

2. status / explain

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
```

3. alternative safe

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

## Livrables

- `00_INITIAL_PROJECT_DOC.md`
- `DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_PLAN_01.md`
- `DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_REPORT_01.md`
- `90_CLOSEOUT.md`

## RISKS

- À qualifier.
