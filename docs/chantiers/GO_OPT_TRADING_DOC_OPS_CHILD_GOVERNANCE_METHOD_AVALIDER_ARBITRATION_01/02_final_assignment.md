---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01_FINAL_ASSIGNMENT
doc_type: matrice_finale
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - governance
  - method
  - final_assignment
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md
point_de_reprise: "Section Affectation finale"
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/01_avalider_review.md
---

# 02_final_assignment — Affectation finale

## Arbitrage des 2 GO A_VALIDER

| go_id | ancien fil propose | fil retenu | changement | confiance | justification |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | THREAD_ARCHIVE_REFERENCE | THREAD_ARCHIVE_REFERENCE | non | ETABLI | GO d'audit/qualification/classement des items obsolete/archive/legacy ; les regles definies servent l'archivage, pas une methode de travail generale |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | THREAD_METHOD_WORKFLOW | THREAD_METHOD_WORKFLOW | non | ETABLI | GO simple autonome qui organise une methode progressive de migration Git ; methode de travail structurante |

## Matrice mise a jour (2 GO arbitres)

| go_id | statut | parent_canonical | fil_principal | action | confiance | justification |
| --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | ACTIVE | self | THREAD_ARCHIVE_REFERENCE | KEEP | ETABLI | audit/qualification/classement obsolete/archive/legacy |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | ACTIVE | self | THREAD_METHOD_WORKFLOW | KEEP | ETABLI | methode progressive migration Git |

## Impact sur la repartition par fil

Aucun changement. Les 2 GO restent dans les fils initialement proposes.

| fil | nombre | GO |
| --- | --- | --- |
| THREAD_DOC_OPS | 4 | MATRICE_DOC_OPS_PARENT, DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT, CHILD_PARENT_CONFORMITY_AUDIT, CHILD_GO_PARENT_THREAD_MAP |
| THREAD_GOVERNANCE_METADATA | 1 | MATRICE_GOUVERNANTE_METADATA_DERIVATION |
| THREAD_NAMING_CANON | 3 | PARENT_NAMING_CANON, CHILD_NAMING_INVENTORY, CHILD_NAMING_NORMALIZER |
| THREAD_CONTINUITY_INDEX | 1 | CONTINUITY_INDEX_REALIGNMENT |
| THREAD_METHOD_WORKFLOW | 4 | CANON_STRUCTURE_REALIGNMENT, ROOT_POLICY_AND_RECLASS, TRAE_PACK_TEXTS_REVISION, GIT_PROGRESSIVE_MIGRATION_START |
| THREAD_ARCHIVE_REFERENCE | 3 | UNIFORM_CONTINUITY_FINAL_MASTER_PLAN, EXTRACTEUR_TAGS_CANONICAL_METHOD, OBSOLETE_RECLASS_ARCHIVE_AUDIT |

## Synthese finale

- **GO dans le perimetre** : 16
- **KEEP** : 16 (dont 2 REFERENCE_ONLY)
- **A_VALIDER** : 0
- **tous les GO gouvernance/methode sont desormais ETABLI**
