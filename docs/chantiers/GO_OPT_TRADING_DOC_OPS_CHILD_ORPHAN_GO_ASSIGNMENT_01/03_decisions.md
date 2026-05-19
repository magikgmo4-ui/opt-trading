---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - orphan
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01/02_assignment_matrix.md
---

# 03_decisions — Decisions

## Decision 1 : pas de vrai orphelin

Tous les GO de GO_INDEX ont un dossier ou une source canonique. Il n'y a pas d'orphelin reel. Les GO non couverts sont simplement des GO qui n'etaient pas dans les perimetres gouvernance/methode ou machine.

## Decision 2 : 7 fils nouveaux proposes

Les fils suivants sont proposes pour les GO non couverts :
- THREAD_GOVERNANCE_AUTONOME : parents gouvernance autonomes
- THREAD_TRANSVERSE_MODULES : modules transversaux multi-machines
- THREAD_OUTILLAGE : outillage IDE/terminal
- THREAD_PROJET_UI : projet UI producer/consumer
- THREAD_RUNTIME : runtime openclaw
- THREAD_GOVERNANCE_RUNTIME : gouvernance runtime/familles
- THREAD_GOVERNANCE_REGISTRY : gouvernance registry

## Decision 3 : GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 -> ASSIGN vers parent UI

Confirmee. Ce GO se rattache a GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01.

## Decision 4 : GO transversaux non deplaces

RESEAU_SSH_CONSOLIDATION_03 et TMUX_IDE_OPT_TRADING_CADRAGE_01 restent autonomes. Pas d'absorption par un parent machine.

## Decision 5 : sous-GO REFERENCE non traites individuellement

Les sous-GO REFERENCE (UI_LOCALCMS_*, TMUX_RUNTIME_*, OPENCLAW_*, GUARDRAILS) restent rattaches a leur parent. Pas de traitement individuel.

## Decision 6 : pas de modification de GO_INDEX.md

Ce lot ne modifie pas GO_INDEX.md.

## Decision 7 : total GO couverts apres ce lot

Apres ce lot, tous les GO de GO_INDEX sont couverts :
- 16 gouvernance/methode
- 4 machine
- 10 orphelins/transversaux/runtime/projet
- 11 sous-GO REFERENCE (non traites individuellement)
