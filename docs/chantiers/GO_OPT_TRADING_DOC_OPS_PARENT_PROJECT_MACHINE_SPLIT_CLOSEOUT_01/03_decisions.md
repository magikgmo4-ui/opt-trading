---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - doc_ops
  - parent
  - closeout
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/01_parent_closeout_review.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/02_final_state.md
---

# 03_decisions — Decisions

## Decision 1 : CLOSE le parent

GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 passe en CLOSED/PASS.

Justification :
- la sequence de 6 etapes initiales est consommee
- 7 enfants supplementaires ont ete ouverts et clos
- les parents machine sont ouverts et conformes (ou differes)
- LOCALCMS est fusionne
- GO_PARENT_THREAD_MAP.md existe comme index derive
- aucun ecart structurel bloquant
- aucun lot complementaire reel

## Decision 2 : ne pas modifier GO_INDEX.md dans ce lot

Le passage du parent en CLOSED/PASS sera propage dans GO_INDEX.md dans un lot de propagation separe, si decide.

## Decision 3 : ne pas modifier BRANCH_STATE.md

BRANCH_STATE.md reste inchange sauf incoherence prouvee.

## Decision 4 : ne pas ouvrir de nouveau parent

Ce lot est un closeout. Aucun nouveau parent n'est ouvert.

## Decision 5 : GO_PARENT_THREAD_MAP.md reste derive

L'index reste une vue derivee subordonnee a GO_INDEX.md. Il ne devient pas une verite de liste concurrente.

## RISKS

- À qualifier.
