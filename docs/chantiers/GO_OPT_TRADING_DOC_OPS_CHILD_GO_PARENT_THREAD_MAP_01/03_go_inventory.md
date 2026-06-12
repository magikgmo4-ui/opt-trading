---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_GO_INVENTORY
doc_type: inventaire
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - go_inventory
  - parent_thread_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Tableau GO"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 03_go_inventory — Inventaire des GO

## Source

`docs/index/GO_INDEX.md` — Tableau canonique + Entrees + Priorite operatoire.

## Tableau GO

| go_id | parent_actuel_go_index | statut | dossier_present | parent_canonical_propose | fil_principal_propose | fils_secondaires | confiance | action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | parent -> inbox -> GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01 | — | ETABLI | KEEP |
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | self | REFERENCE | oui | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | reference standalone | — | ETABLI | REFERENCE_ONLY |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | parent -> alignement surfaces proches | — | ETABLI | KEEP |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | self | OPEN | oui | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | parent -> CHILD_PARENT_CONFORMITY_AUDIT -> CHILD_GO_PARENT_THREAD_MAP | — | ETABLI | KEEP |
| GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01 | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | OPEN | oui | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | fil principal du parent | — | ETABLI | KEEP |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | parent machine -> inventaire -> futur enfant | — | ETABLI | KEEP |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | parent machine -> inventaire -> futur enfant | — | ETABLI | KEEP |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | self | ACTIVE | oui | GO_GIT_PROGRESSIVE_MIGRATION_START_01 | migration Git progressive | — | A_VALIDER | REVIEW |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | self | ACTIVE | oui | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | realignement index continuite | — | ETABLI | KEEP |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | self | ACTIVE | oui | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | carte surfaces repo | — | ETABLI | KEEP |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | self | ACTIVE | oui | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | politique racine + reclassement | GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 (fils) | ETABLI | KEEP |
| GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | ACTIVE | oui | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | fil de ROOT_POLICY | — | ETABLI | KEEP |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | self | ACTIVE | oui | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | audit obsolete -> matrice -> plan lots | — | ETABLI | KEEP |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | self | ACTIVE | oui | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | familles mixtes runtime-exception | — | ETABLI | KEEP |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | self | ACTIVE | oui | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | realignement scope registry | — | ETABLI | KEEP |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | self | OPEN | oui | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | consolidation reseau_ssh | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 (fils) | ETABLI | KEEP |
| GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | OPEN | oui | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | fil de RESEAU_SSH_CONSOLIDATION_03 | — | ETABLI | KEEP |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | self | ACTIVE | oui | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | cadrage tmux-ide -> impl base | — | ETABLI | KEEP |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | self | OPEN | oui | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | forms integration doc-only | — | A_VALIDER | REVIEW |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | parent AI team -> futur enfant audit | — | ETABLI | KEEP |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | self | OPEN | oui | GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | doctrine derivation metadata | — | ETABLI | KEEP |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | self | OPEN | oui | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | parent naming -> inventory -> normalizer | GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01, GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | ETABLI | KEEP |
| GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | OPEN | oui | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | fil de PARENT_NAMING_CANON | — | ETABLI | KEEP |
| GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | OPEN | oui | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | fil de PARENT_NAMING_CANON | — | ETABLI | KEEP |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | self | OPEN | oui | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | parent UI -> inventory -> matrix -> contracts -> pilot | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01, GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01, GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01, GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01 (tous REFERENCE) | ETABLI | KEEP |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | self | REFERENCE | non | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | reference standalone | — | ETABLI | REFERENCE_ONLY |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | self | ACTIVE | oui | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | runtime openclaw -> sous-GO reference | GO_TMUX_RUNTIME_CONVENTIONS_01, GO_OPENCLAW_COMMAND_SCOPE_01, GO_TMUX_RUNTIME_CONTRACT_01, GO_TMUX_OPENCODE_OPENCLAW_MODES_01, GO_RUNTIME_GUARDRAILS_01 (tous REFERENCE) | ETABLI | KEEP |

## Synthese

- **GO inventories** : 27 entrees au total (parents + enfants + reference)
- **GO deja clairement assignes** : 23 (parent canonique = parent actuel, confiance ETABLI)
- **GO ambigus** : 2 (GO_GIT_PROGRESSIVE_MIGRATION_START_13, GO_LOCALCMS_FORMS_INTEGRATION_DOC_01)
- **GO a ne pas deplacer** : tous les GO machine (admin-trading, db-layer) et les GO differe (student, fantome)
- **GO REFERENCE** : 2 (GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01, GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01)

## Notes sur les GO ambigus

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- statut ACTIVE mais la suite autonome n'est pas assez explicite
- parent actuel = self
- action REVIEW : verifier si ce GO doit rester autonome ou se rattacher a un parent gouvernance

### GO_LOCALCMS_FORMS_INTEGRATION_DOC_01
- statut OPEN mais pas de lien explicite avec GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
- action REVIEW : verifier si ce GO doit se rattacher au parent UI LocalCMS ou rester autonome

## RISKS

- À qualifier.
