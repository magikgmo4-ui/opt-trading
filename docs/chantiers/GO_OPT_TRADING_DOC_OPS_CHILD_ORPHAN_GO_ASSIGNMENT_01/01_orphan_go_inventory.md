---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01_INVENTORY
doc_type: inventaire
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - orphan
  - go_inventory
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Inventaire GO non couverts"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md
---

# 01_orphan_go_inventory — Inventaire des GO non couverts

## Methode

Croisement entre :
- la liste GO_INDEX (37 entrees)
- les GO couverts par THREAD_ASSIGNMENT (16 gouvernance/methode)
- les GO couverts par MACHINE_ASSIGNMENT (4 parents machine)
- les GO couverts par AVALIDER_ARBITRATION (2 GO arbitres)
- les sous-GO REFERENCE rattaches a des parents deja couverts

## GO deja couverts par les lots precedents

### Gouvernance/methode (16 GO, tous ETABLI)
MATRICE_DOC_OPS_PARENT, DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT, CHILD_PARENT_CONFORMITY_AUDIT, CHILD_GO_PARENT_THREAD_MAP, MATRICE_GOUVERNANTE_METADATA_DERIVATION, PARENT_NAMING_CANON, CHILD_NAMING_INVENTORY, CHILD_NAMING_NORMALIZER, CONTINUITY_INDEX_REALIGNMENT, UNIFORM_CONTINUITY_FINAL_MASTER_PLAN, EXTRACTEUR_TAGS_CANONICAL_METHOD, CANON_STRUCTURE_REALIGNMENT, ROOT_POLICY_AND_RECLASS, TRAE_PACK_TEXTS_REVISION, OBSOLETE_RECLASS_ARCHIVE_AUDIT, GIT_PROGRESSIVE_MIGRATION_START

### Machine (4 parents)
MACHINE_ADMIN_TRADING_PARENT, MACHINE_DB_LAYER_PARENT, MACHINE_STUDENT_PARENT (DEFER), MACHINE_FANTOME_SUPPORT_PARENT (DEFER)

### Sous-GO REFERENCE rattaches a des parents deja couverts
- UI_LOCALCMS_INVENTORY, UI_LOCALCMS_MATRIX, UI_LOCALCMS_CONTRACTS, UI_LOCALCMS_PILOT_READONLY : sous-GO REFERENCE du parent UI_LOCALCMS_CONSUMER_PARENT
- TMUX_RUNTIME_CONVENTIONS, OPENCLAW_COMMAND_SCOPE, TMUX_RUNTIME_CONTRACT, OPENCLAW_MODES, GUARDRAILS : sous-GO REFERENCE du parent TMUX_OPENCODE_OPENCLAW_RUNTIME

## GO non couverts a traiter

| go_id | statut | parent_actuel | categorie |
| --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | OPEN | self | transversal gouvernance |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | OPEN | self | transversal modules |
| GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | OPEN | RESEAU_SSH_CONSOLIDATION_03 | sous-GO transversal |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | ACTIVE | self | outillage |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | OPEN | self | projet UI |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | OPEN | self | projet UI parent |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | OPEN | self | gouvernance architecture |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | ACTIVE | self | runtime |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | ACTIVE | self | gouvernance runtime |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | ACTIVE | self | gouvernance registry |

## Observations

- 10 GO restent a clarifier
- aucun n'est un orphelin reel : tous ont un dossier present dans GO_INDEX
- les GO transversaux (RESEAU_SSH, TMUX_IDE, RUNTIME) ne doivent pas etre absorbes par un parent machine
- GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 a ete propose pour ASSIGN vers parent UI dans le mapping initial
- GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 est un parent gouvernance deja dans GO_INDEX mais non couvert par le lot gouvernance
