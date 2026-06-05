---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_MAP_DRAFT
doc_type: matrice_draft
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_thread_map
  - draft
  - mapping
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Matrice draft"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/01_parent_inventory.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/02_machine_parent_inventory.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/03_go_inventory.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/04_assignment_rules.md
---

# 05_parent_thread_map_draft — Matrice draft

## Regle

Cette matrice est un draft dans le dossier chantier. Elle n'est pas encore la surface canonique `GO_PARENT_THREAD_MAP.md`.

## Matrice draft : GO -> parent canonique -> fil principal

| GO | statut | parent_actuel | parent_canonical_propose | fil_principal | fils_secondaires | confiance | action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | OPEN | self | GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | parent -> inbox -> GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01 | — | ETABLI | KEEP |
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | REFERENCE | self | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | reference standalone | — | ETABLI | REFERENCE_ONLY |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | OPEN | self | GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | parent -> alignement surfaces proches | — | ETABLI | KEEP |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | OPEN | self | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | parent -> CONFORMITY_AUDIT -> GO_PARENT_THREAD_MAP | — | ETABLI | KEEP |
| GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01 | OPEN | DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | fil principal du parent | — | ETABLI | KEEP |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | OPEN | self | GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | parent machine -> inventaire -> futur enfant | — | ETABLI | KEEP |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | OPEN | self | GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | parent machine -> inventaire -> futur enfant | — | ETABLI | KEEP |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | ACTIVE | self | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO simple autonome — migration Git progressive | — | ETABLI | KEEP |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | ACTIVE | self | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | realignement index | — | ETABLI | KEEP |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | ACTIVE | self | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | carte surfaces | — | ETABLI | KEEP |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | ACTIVE | self | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | politique racine + reclassement | TRAE_PACK_TEXTS_REVISION_01 | ETABLI | KEEP |
| GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | ACTIVE | ROOT_POLICY_AND_RECLASS_01 | ROOT_POLICY_AND_RECLASS_01 | fil de ROOT_POLICY | — | ETABLI | KEEP |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | ACTIVE | self | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | audit obsolete -> matrice -> plan | — | ETABLI | KEEP |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | ACTIVE | self | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | familles mixtes | — | ETABLI | KEEP |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | ACTIVE | self | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | scope registry | — | ETABLI | KEEP |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | OPEN | self | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | consolidation reseau_ssh | UNIFIED_MODULE_CADRAGE_01 | ETABLI | KEEP |
| GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | OPEN | RESEAU_SSH_CONSOLIDATION_03 | RESEAU_SSH_CONSOLIDATION_03 | fil de RESEAU_SSH_CONSOLIDATION_03 | — | ETABLI | KEEP |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | ACTIVE | self | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | cadrage tmux-ide -> impl | — | ETABLI | KEEP |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | OPEN | self | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | fil du parent UI LocalCMS (project=localcms, integration forms) | — | ETABLI | ASSIGN |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | OPEN | self | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | parent AI team -> futur enfant | — | ETABLI | KEEP |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | OPEN | self | GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | doctrine derivation | — | ETABLI | KEEP |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | OPEN | self | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | parent naming -> inventory -> normalizer | CHILD_NAMING_INVENTORY_01, CHILD_NAMING_NORMALIZER_01 | ETABLI | KEEP |
| GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | OPEN | PARENT_NAMING_CANON_01 | PARENT_NAMING_CANON_01 | fil de PARENT_NAMING_CANON | — | ETABLI | KEEP |
| GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | OPEN | PARENT_NAMING_CANON_01 | PARENT_NAMING_CANON_01 | fil de PARENT_NAMING_CANON | — | ETABLI | KEEP |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | OPEN | self | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | parent UI -> inventory -> matrix -> contracts -> pilot | INVENTORY, MATRIX, CONTRACTS, PILOT_READONLY (REFERENCE) | ETABLI | KEEP |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | REFERENCE | self | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | reference standalone | — | ETABLI | REFERENCE_ONLY |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | ACTIVE | self | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | runtime openclaw -> sous-GO reference | RUNTIME_CONVENTIONS, COMMAND_SCOPE, RUNTIME_CONTRACT, OPENCLAW_MODES, GUARDRAILS (tous REFERENCE) | ETABLI | KEEP |

## Synthese

- **GO inventories** : 27
- **GO deja clairement assignes (KEEP)** : 24
- **GO a assigner (ASSIGN)** : 1 (GO_LOCALCMS_FORMS_INTEGRATION_DOC_01)
- **GO a reviewer (REVIEW)** : 0
- **GO REFERENCE_ONLY** : 2
- **GO ambigus** : 0
- **GO a ne pas deplacer** : tous les GO machine parents + GO differe

## Decision GO_LOCALCMS_FORMS_INTEGRATION_DOC_01

Ce GO traite de l'integration forms compatible avec localcms. Il devrait logiquement se rattacher a `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` comme sous-GO. Action proposee : ASSIGN vers ce parent, sous reserve de verification que le contenu du GO couvre bien une integration UI.

## Decision GO_GIT_PROGRESSIVE_MIGRATION_START_13

Ce GO est ACTIVE et traite de la migration Git progressive. C'est un GO simple autonome sans parent prouve. Il reste en KEEP comme GO simple, rattaché a lui-même.

## Matrice canonique creee ?

Non. Dans ce premier lot, la matrice reste dans le dossier chantier. La creation de `docs/index/GO_PARENT_THREAD_MAP.md` n'est pas prevue ici.

## RISKS

- À qualifier.
