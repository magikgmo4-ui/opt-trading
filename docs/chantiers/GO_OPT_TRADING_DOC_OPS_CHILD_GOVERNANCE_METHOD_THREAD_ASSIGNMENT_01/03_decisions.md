---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01_DECISIONS
doc_type: decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - governance
  - method
  - decisions
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Decisions"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
---

# 03_decisions — Decisions

## Decision 1 : 6 fils de continuite retenus

Les fils suivants sont retenus pour les GO gouvernance/methode :
- THREAD_DOC_OPS : operations documentaires
- THREAD_GOVERNANCE_METADATA : gouvernance metadata/derivation
- THREAD_NAMING_CANON : nommage canonique
- THREAD_CONTINUITY_INDEX : continuite/index
- THREAD_METHOD_WORKFLOW : methode de travail/structure
- THREAD_ARCHIVE_REFERENCE : archives/references stables

## Decision 2 : THREAD_DOC_OPS = fil principal du parent doc-ops

Le fil THREAD_DOC_OPS regroupe le parent MATRICE_DOC_OPS_PARENT_01 et ses sous-enfants (DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT, CHILD_PARENT_CONFORMITY_AUDIT, CHILD_GO_PARENT_THREAD_MAP). C'est le fil le plus structure.

## Decision 3 : GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 -> THREAD_ARCHIVE_REFERENCE (A_VALIDER)

Ce GO traite de l'audit des obsolete/archive/legacy. Il pourrait aussi relever de THREAD_METHOD_WORKFLOW. Affectation proposee : THREAD_ARCHIVE_REFERENCE, sous reserve de validation.

## Decision 4 : GO_GIT_PROGRESSIVE_MIGRATION_START_13 -> THREAD_METHOD_WORKFLOW (A_VALIDER)

Ce GO traite de la migration Git progressive. C'est un GO simple autonome. Affectation proposee : THREAD_METHOD_WORKFLOW, sous reserve de validation.

## Decision 5 : pas de modification de GO_INDEX.md

Ce lot ne modifie pas GO_INDEX.md. Les affectations de fil restent dans le dossier chantier.

## Decision 6 : pas de creation de GO_PARENT_THREAD_MAP.md

Ce lot ne cree pas docs/index/GO_PARENT_THREAD_MAP.md. La matrice d'affectation reste dans le dossier chantier.

## Decision 7 : GO_REFERENCE_ONLY conserves tels quels

Les 2 GO REFERENCE (UNIFORM_CONTINUITY_FINAL_MASTER_PLAN, EXTRACTEUR_TAGS_CANONICAL_METHOD) restent en REFERENCE_ONLY sans changement.

## RISKS

- À qualifier.
