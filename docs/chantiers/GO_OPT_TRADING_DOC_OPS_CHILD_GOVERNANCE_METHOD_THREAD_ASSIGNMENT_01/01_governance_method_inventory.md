---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01_INVENTORY
doc_type: inventaire
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
  - inventory
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Inventaire GO gouvernance/methode"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
---

# 01_governance_method_inventory — Inventaire GO gouvernance/methode

## Perimetre

GO de gouvernance, matrice, methode de travail, continuite et index. Exclut : machine, runtime, projet UI, outillage, orphelins.

## Inventaire

| go_id | type | statut | parent_actuel | dossier_present | fil_propose | justification |
| --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | gouvernance | OPEN | self | oui | THREAD_DOC_OPS | parent matrice maitre doc ops |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | gouvernance | OPEN | self | oui | THREAD_DOC_OPS | parent canonique de reprise repo-first |
| GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01 | gouvernance | OPEN | DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | oui | THREAD_DOC_OPS | sous-GO d'audit conformite parents |
| GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01 | gouvernance | PASS | DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | oui | THREAD_DOC_OPS | cartographie parent/fil/GO (recemment clos) |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | gouvernance | OPEN | self | oui | THREAD_GOVERNANCE_METADATA | doctrine derivation metadata post-matrice |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | gouvernance | OPEN | self | oui | THREAD_NAMING_CANON | parent canonique naming |
| GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | gouvernance | OPEN | PARENT_NAMING_CANON_01 | oui | THREAD_NAMING_CANON | inventaire ecarts nommage |
| GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | gouvernance | OPEN | PARENT_NAMING_CANON_01 | oui | THREAD_NAMING_CANON | module naming normalizer |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | continuite | ACTIVE | self | oui | THREAD_CONTINUITY_INDEX | realignement index continuite |
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | continuite | REFERENCE | self | oui | THREAD_ARCHIVE_REFERENCE | plan maitre uniforme continuite |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | methode | REFERENCE | self | non | THREAD_ARCHIVE_REFERENCE | methode canonique extraction tags |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | gouvernance | ACTIVE | self | oui | THREAD_METHOD_WORKFLOW | carte canonique surfaces repo |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | gouvernance | ACTIVE | self | oui | THREAD_METHOD_WORKFLOW | politique racine canonique |
| GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | gouvernance | ACTIVE | ROOT_POLICY_AND_RECLASS_01 | oui | THREAD_METHOD_WORKFLOW | revision trae pack texts |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | gouvernance | ACTIVE | self | oui | THREAD_ARCHIVE_REFERENCE | audit obsolete/archive/legacy |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | gouvernance | ACTIVE | self | oui | THREAD_METHOD_WORKFLOW | migration Git progressive |

## Observations

- 16 GO dans le perimetre gouvernance/methode
- 4 fils de continuite distincts identifies : THREAD_DOC_OPS, THREAD_GOVERNANCE_METADATA, THREAD_NAMING_CANON, THREAD_CONTINUITY_INDEX
- 2 fils supplementaires proposes : THREAD_METHOD_WORKFLOW, THREAD_ARCHIVE_REFERENCE
- 2 GO REFERENCE (hors execution courante)
- 1 GO recemment PASS (GO_PARENT_THREAD_MAP)
