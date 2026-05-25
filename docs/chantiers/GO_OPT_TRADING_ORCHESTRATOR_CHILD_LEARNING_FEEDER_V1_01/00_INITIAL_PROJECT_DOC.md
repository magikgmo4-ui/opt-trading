---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
master_project_plan_id: MPP_OPENCLAW_ORCHESTRATOR_FULL
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: modules/learning_feeder
source_kind: canonical
updated_at: 2026-05-25
topic_keys:
  - openclaw
  - orchestration
  - learning-feedback
  - bridge
  - learning-brick
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/00_SYSTEM_MASTER_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_01/00_INITIAL_PROJECT_DOC.md
---

# 00_INITIAL_PROJECT_DOC — Learning Feeder V1

## 1_MASTER_TARGET

Contribuer à `PF_OPENCLAW_ORCHESTRATOR_FULL` en ouvrant `modules/learning_feeder/` — feedback cycle OpenClaw pour trades complétés.

## 2_INITIAL_PROJECT_DOC

Cette fiche ouvre le child produit `GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01`.

## 3_INITIAL_NEED

Dernière étape de la chaîne produit. Boucle d'apprentissage : trade → résultat → feedback → OpenClaw.

## 4_MASTER_PROJECT_PLAN

```text
signal_router PASS → proposition_engine PASS → validation_gate PASS → trade_executor PASS → result_tracker PASS → datasheet_writer V1 → learning_feeder V1 (ce GO)
```

## 5_GO_PLAN

```text
FINAL_TARGET: learning_feeder V1 complet, convention module, tests, smoke
```

## 6_FINAL_TARGET

- Ajouter `__init__.py`, `app/__init__.py`, `app/__main__.py`
- Ajouter `scripts/cmd.sh`, `menu.sh`, `install_shortcuts.sh`
- Ajouter `README.md`
- Vérifier tests (29) + sanity

## 7_CANONICAL_STATE

```text
DATASHEET_WRITER = PASS
LEARNING_FEEDER = code existant + 29 tests, GO non ouvert
```
