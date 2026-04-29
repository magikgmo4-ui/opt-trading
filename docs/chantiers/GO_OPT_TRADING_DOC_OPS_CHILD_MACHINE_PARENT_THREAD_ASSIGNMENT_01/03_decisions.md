---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - machine
  - parent
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md
---

# 03_decisions — Decisions

## Decision 1 : 4 fils machine retenus

Les fils suivants sont retenus pour les parents machine :
- THREAD_MACHINE_ADMIN_TRADING : parent machine admin-trading
- THREAD_MACHINE_DB_LAYER : parent machine db-layer
- THREAD_MACHINE_STUDENT_DEFERRED : parent machine student (differe)
- THREAD_MACHINE_FANTOME_DEFERRED : parent machine fantome (differe)

## Decision 2 : admin-trading et db-layer -> KEEP

Les 2 parents machine ouverts restent en KEEP avec confiance ETABLI. Pas de changement de statut.

## Decision 3 : student et fantome -> DEFER

Les 2 parents machine differe restent en DEFER. Pas d'ouverture dans ce lot.

## Decision 4 : RESEAU_SSH -> lien secondaire seulement

GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 a un lien secondaire avec admin-trading et db-layer (machines cibles de reseau_ssh). Mais le GO reste un GO transverse de consolidation modules, pas un GO machine. Le lien est descriptif seulement.

## Decision 5 : GO transversaux non deplaces

Les GO suivants ne sont pas deplaces vers un parent machine :
- RESEAU_SSH_CONSOLIDATION_03 : transverse
- RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 : sous-GO transverse
- TMUX_IDE_OPT_TRADING_CADRAGE_01 : outillage
- TMUX_OPENCODE_OPENCLAW_RUNTIME_01 : runtime
- MULTI_AGENTS_CANON_PARENT_01 : gouvernance
- AI_TEAM_ARCHITECTURE_PARENT_01 : gouvernance
- RUNTIME_EXCEPTION_FAMILIES_01 : gouvernance
- REGISTRY_SCOPE_REALIGNMENT_01 : gouvernance

## Decision 6 : pas de modification de GO_INDEX.md

Ce lot ne modifie pas GO_INDEX.md.

## Decision 7 : pas de creation de GO_PARENT_THREAD_MAP.md

Ce lot ne cree pas docs/index/GO_PARENT_THREAD_MAP.md.

## Decision 8 : suite logique

Apres ce lot :
- les parents machine sont tous traites
- la suite logique est de traiter les GO orphelins
