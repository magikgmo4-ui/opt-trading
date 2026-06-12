---
doc_id: DB_LAYER_BRANCH_DOC_RECONCILIATION_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01
parent_go: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
status: active
lifecycle_stage: doc_reconciliation
surface: chantier
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
---

# 00_START - DB_LAYER Branch Doc Reconciliation

## GO

GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01

## Parent

GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 (OPEN)

## Scope

Chantier strictement doc-only sur la surface `db-layer / OpenClaw`.

## Contraintes

- ne toucher a aucun runtime OpenClaw/db-layer
- ne pas relancer TMUX
- ne pas rouvrir `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01`
- ne pas toucher `admin-trading`
- aucune suppression Git
- aucun cleanup
- ne pas modifier `GO_INDEX` / `ACTIVE_STREAMS` / `REPRISE` sauf necessite prouvee et explicitee

## Objectif

- recroiser `MACHINE_WORK_SPLIT` bloc `DB_LAYER`
- recroiser `BRANCH_STATE.md`
- lister les branches Git reelles `db-layer/OpenClaw`
- classer chaque branche : `ACTIVE` / `REFERENCE` / `DROP_MERGED` / `A_VERIFIER`
- identifier les ecarts documentaires
- produire un verdict clair + `NEXT_GO`

## RISKS

- À qualifier.
