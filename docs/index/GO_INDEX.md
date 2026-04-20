---
doc_id: OPT_TRADING_GO_INDEX
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - go_index
  - continuity
  - governance
surface: chantier
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_INDEX — opt-trading

## Objet

Ce document référence les GO connus et utiles à la continuité locale de `opt-trading`.

---

## Snapshot global système

- 2026-04-18  
  → docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md  
  → vue consolidée projets / infra / chantiers / runtime

---

## Forms / LocalCMS (cadrage)

- GO_LOCALCMS_FORMS_INTEGRATION_DOC_01  
  → docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md  
  → intégration future forms compatible avec localcms existant (doc-only)

---

## Règles

- l’index référence et synthétise
- il ne remplace ni le dossier chantier ni le closeout
- les GO clos, actifs, bloqués ou archivés peuvent y figurer si leur continuité locale le justifie
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent

---

## Tableau canonique des chantiers

Normalisation retenue :

- `PARENT = CHANTIER` si aucun parent explicite n'est prouvé dans le repo
- `SOUS_CHANTIER = —` si aucun sous-chantier explicite n'est prouvé dans le repo
- `STATUT` est normalisé en `OPEN`, `ACTIVE`, `CLOSED`, `REFERENCE`
- `DOSSIER_PRESENT` indique la présence d'un dossier direct sous `docs/chantiers/`

| PARENT | CHANTIER | SOUS_CHANTIER | STATUT | DOSSIER_PRESENT | SOURCE |
| --- | --- | --- | --- | --- | --- |
| GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md` |
| GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md` |
| GO_GIT_PROGRESSIVE_MIGRATION_START_13 | GO_GIT_PROGRESSIVE_MIGRATION_START_13 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` |
| GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md` |
| GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_HARDENING_01 | GO_UNIFORM_CONTINUITY_HARDENING_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md` |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md` |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`<br>`docs/governance/REPO_ROOT_POLICY.md` |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md` |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`<br>`registry/README.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00B_parent_scope_and_structure.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md` |
| GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md` |
| GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md` |
| GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md` |
| GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01 | GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01 | — | OPEN | non | `docs/index/GO_INDEX.md`<br>`docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md` |
| GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04 | GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md` |
| GO_OPT_TRADING_JOURNAL_FULL_READING_03 | GO_OPT_TRADING_JOURNAL_FULL_READING_03 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` |
| GO_RANGE_STRATEGY_V1_STRUCT_01 | GO_RANGE_STRATEGY_V1_STRUCT_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/90_closeout.md` |
| GO_STRATEGY_KERNEL_SHARED_LAYER_01 | GO_STRATEGY_KERNEL_SHARED_LAYER_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/90_closeout.md` |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | — | ACTIVE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md` |
| GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | CLOSED | oui | `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/00_cadrage.md` |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_LOCALCMS_FORMS_INTEGRATION_DOC_01/00_cadrage.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | — | OPEN | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01 | REFERENCE | non | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01 | — | REFERENCE | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | — | ACTIVE | oui | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md`<br>`docs/index/REPRISE.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONVENTIONS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_OPENCLAW_COMMAND_SCOPE_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_RUNTIME_CONTRACT_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_MODES_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO_RUNTIME_GUARDRAILS_01 | REFERENCE | non | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md` |

---

## Priorité opératoire (11 GO non clos)

- P0 : `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01`, `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`
- P1 : `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`, `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`, `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`, `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- P2 : `GO_OPT_TRADING_JOURNAL_FULL_READING_03`, `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`

Le passage de 10 à 11 GO non clos correspond à l’ouverture du parent :
- `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01`

Historique (PHASE 4) :
- le passage de 10 à 11 GO non clos a correspondu à l’ouverture de `GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01`
- ce GO est clos (PASS), donc il reste hors exécution courante

Le passage de 8 à 10 GO non clos correspond à l’ouverture PHASE 3 des parents :
- `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01`
- `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01`

Le passage de 6 à 8 GO non clos correspond à l’ouverture PHASE 2 des parents :
- `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01`

---

## Entrées

### GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01
- repo : opt-trading
- type : gouvernance / continuité
- statut : reference
- titre court : plan maître uniforme de continuité
- dernier état connu : référentiel consolidé validé comme base documentaire
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_FINAL_MASTER_PLAN_01/00_cadrage.md`

### GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01
- repo : opt-trading
- type : gouvernance / continuité produit
- statut : pass
- titre court : hiérarchie produit multi-chantier canonisée
- dernier état connu : structuration Couche 0 / Anneau A / Anneau B posée comme source canonique de continuité produit
- lien utile : `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md`, `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`

### GO_GIT_PROGRESSIVE_MIGRATION_START_13
- repo : opt-trading
- type : migration documentaire
- statut : active
- titre court : démarrage de la migration Git progressive
- dernier état connu : gouvernance locale initiale créée sur `sot/mainline`
- lien utile : `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md`, `docs/governance/REPO_ROLE.md`, `docs/governance/DOC_LAYERS.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01
- repo : opt-trading
- type : continuité locale / bootstrap
- statut : pass
- titre court : socle documentaire local posé
- dernier état connu : closeout PASS avec gouvernance locale, index et reprise locale en place
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md`, `docs/index/REPRISE.md`

### GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
- repo : opt-trading
- type : chantier pilote / memory_bricks
- statut : pass
- titre court : pilote canonique `memory_bricks`
- dernier état connu : closeout PASS posé comme second pilote local directement ancré sur `memory_bricks`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_UNIFORM_CONTINUITY_HARDENING_01
- repo : opt-trading
- type : hardening documentaire
- statut : pass
- titre court : réalignement final des index locaux
- dernier état connu : hardening appliqué sur les index `opt-trading` ; `localcms` hors-scope dans ce flux ; closeout PASS
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md`, `docs/index/ACTIVE_STREAMS.md`

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : réalignement continuité index
- dernier état connu : chantier parent ouvert pour réaligner `docs/index/*` et déclasser `docs/next/NEXT_GO_CANDIDATES.md`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md`

### GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : carte canonique des surfaces du repo
- dernier état connu : parent PHASE 2 LOT 3 ouvert ; carte humaine `REPO_SURFACES_MAP.md` posée sans duplication de `registry/*`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md`, `docs/architecture/REPO_SURFACES_MAP.md`

### GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : politique racine canonique interne du repo
- dernier état connu : parent PHASE 2 LOT 4 ouvert ; `REPO_ROOT_POLICY.md` posé sans redéfinir la frontière repo/hors-repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`, `docs/governance/REPO_ROOT_POLICY.md`

### GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
- repo : opt-trading
- type : audit / qualification / préparation reclassement physique
- statut : active
- titre court : audit obsolete / déclassé / archive / legacy / sous arbitrage
- dernier état connu : parent ouvert (audit repo-first non destructif) ; groupes racine / workflow_post_change / docs historiques / supports locaux ciblés
- lien utile : `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md`

### GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : familles mixtes / lignées runtime-exception
- dernier état connu : parent PHASE 3 LOT 5 ouvert ; fiches status courtes posées et rattachées à l’audit famille
- lien utile : `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md`

### GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : active
- titre court : réalignement scope registry
- dernier état connu : parent PHASE 3 LOT 6 ouvert ; `registry/README.md` complété sur périmètre/exceptions
- lien utile : `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`, `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`, `registry/README.md`

### GO_GITHUB_PARK_AUDIT_EXPANSION_01
- repo : opt-trading
- type : audit / parc GitHub
- statut : pass
- titre court : expansion de l’audit du parc GitHub
- dernier état connu : cible finale atteinte ; cross-audit consolidé et intégrité canonique `GO_INDEX ↔ 04_branch_trunk_cross_audit_target.md` rétablie sur `sot/mainline`
- lien utile : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md`

### GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01
- repo : opt-trading
- type : patch local / doc-only
- statut : pass
- titre court : isolation des modifications locales audit GitHub Park
- dernier état connu : les 2 docs locaux du chantier GitHub Park ont été isolés sur branche dédiée avec commit `a4ce731` et worktree propre
- lien utile : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md`


### GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01
- repo : opt-trading
- type : gouvernance / git / branches
- statut : pass
- titre court : méthode canonique de ménage des branches Git
- dernier état connu : méthode récurrente figée sur base `origin/sot/mainline`, avec tri standard `DELETE_NOW / KEEP / REVIEW`, revue manuelle obligatoire pour les familles sensibles, et extraction Skill explicitement postérieure à la doc canonique
- lien utile : `docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md`, `docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md`, `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md`

### GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01
- repo : opt-trading
- type : intégration doc-only
- statut : pass
- titre court : intégration bornée du pack trading dual stack
- dernier état connu : intégration via checkout borné sur `docs/trading/*` sans merge global, commit `5d46981`, worktree propre
- lien utile : `docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md`

### GO_COLLECTORS_LIFECYCLE_COMPAT_CADRAGE_01
- repo : opt-trading
- type : cadrage module durable / collectors
- statut : open
- titre court : cadrage compatibilité lifecycle collectors
- dernier état connu : diagnostic repo-first réalisé sur `origin/inventory/collectors-baseline-01` avec verdict `RE-SCOPE` (risque cassant sur `relref()/relative_to(MODULE_DIR)` si `OUTPUT_DIR` est relatif au root projet), écarts spec/runtime tracés
- lien utile : `docs/COLLECTORS_LIFECYCLE_COMPAT_SPEC_01.md`

### GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04
- repo : opt-trading
- type : journal / lecture canonique
- statut : active
- titre court : lecture canonique orientée intention projet
- dernier état connu : reprise de lecture après LOT_S23 avec angle intention / objectif / choix / pourquoi, premier bloc visé LOT_S24 à LOT_S28
- lien utile : `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md`

### GO_OPT_TRADING_JOURNAL_FULL_READING_03
- repo : opt-trading
- type : journal / lecture complète
- statut : active
- titre court : lecture complète du journal canon
- dernier état connu : cadre inter-repos posé, mais couche humaine vivante pas encore réinjectée proprement dans la continuité stable
- lien utile : `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md`

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- repo : opt-trading
- type : consolidation modules / reseau_ssh
- statut : open
- titre court : consolidation ciblée de la famille reseau_ssh*
- dernier état connu : survivant canonique confirmé modules/reseau_ssh_step2, avec step1b conservé comme prérequis intermédiaire
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`

### GO_RANGE_STRATEGY_V1_STRUCT_01
- repo : opt-trading
- type : trading / stratégie range
- statut : pass
- titre court : cadrage stratégie range v1
- dernier état connu : chantier documentaire range strategy v1 aligné sur la gate de session avec ancrage métier trading créé
- lien utile : `docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/90_closeout.md`

### GO_STRATEGY_KERNEL_SHARED_LAYER_01
- repo : opt-trading
- type : trading / noyau stratégie
- statut : pass
- titre court : cadrage noyau stratégie partagé
- dernier état connu : sujet désormais couvert par un chantier canonique propre, aligné sur l’intention figée et l’état réel du repo
- lien utile : `docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/90_closeout.md`

### GO_TMUX_IDE_OPT_TRADING_CADRAGE_01
- repo : opt-trading
- type : outillage / tmux-ide
- statut : active
- titre court : cadrage IDE terminale tmux-ide
- dernier état connu : bundle préparé, cadrage canonique ouvert, next GO GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
- lien utile : `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md`

### GO_UNIFORM_CONTINUITY_HARDENING_02
- repo : opt-trading
- type : hardening documentaire
- statut : pass
- titre court : normalisation des headings workflow / mémoire / documentation
- dernier état connu : cadrage canonique posé + lot patchable appliqué en docs-only ; closeout PASS
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`, `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/90_closeout.md`

### GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01
- repo : opt-trading
- type : exécution doc-only (lot fermé)
- statut : pass
- titre court : application normalisation headings (workflow / mémoire / documentation)
- dernier état connu : closeout PASS ; patch headings-only limité au lot fermé, sans réécriture de fond
- lien utile : `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/02_journal_technique.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/03_decisions.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md`

### GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
- repo : opt-trading
- type : pack IDE / transmission
- statut : pass
- titre court : pack d’exécution IDE pour le hardening
- dernier état connu : chantier documentaire de transmission complet et immédiatement exploitable par l’IDE
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/IDE_EXECUTION_PACK.md`

### GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
- repo : opt-trading
- type : intégration UI / producer-consumer
- statut : open
- titre court : chantier parent UI opt-trading producer → localcms consumer
- dernier état connu : cadrage parent posé ; `opt-trading` reste producer canonique et `localcms` consumer UI ; reprise recommandée sur `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`
- lien utile : `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md`

### GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01
- repo : opt-trading
- type : gouvernance / extraction / documentation
- statut : reference
- titre court : méthode canonique d’extraction par tags
- dernier état connu : fiche de référence initiale créée sur `sot/mainline` pour séparer extraction, classification, routage mémoire vs doc et écriture contrôlée
- lien utile : `docs/chantiers/GO_EXTRACTEUR_TAGS_CANONICAL_METHOD_01/EXTRACTEUR_TAGS__METHODE_CANONIQUE_V1.md`
