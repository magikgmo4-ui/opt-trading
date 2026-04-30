---
doc_id: OPT_TRADING_GO_CLOSED_INDEX
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - go_closed_index
  - continuity
  - governance
surface: continuity
source_kind: canonical
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_CLOSED_INDEX — opt-trading

## Objet

Ce document référence les chantiers clos/pass sortis de `docs/index/GO_INDEX.md`.

---

## Règles

- l’index référence et synthétise les chantiers `CLOSED`/`PASS`
- il ne remplace ni le dossier chantier ni le closeout
- lorsqu’un chantier passe en `CLOSED`/`PASS`, sa ligne canonique doit être retirée de `docs/index/GO_INDEX.md` et déplacée ici
- les entrées `REFERENCE` ne sont pas reclassées automatiquement comme `CLOSED`/`PASS`
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent

---

## Tableau canonique des chantiers clos/pass

Normalisation retenue :

- `PARENT = CHANTIER` si aucun parent explicite n'est prouvé dans le repo
- `SOUS_CHANTIER = —` si aucun sous-chantier explicite n'est prouvé dans le repo
- `STATUT` est normalisé en `OPEN`, `ACTIVE`, `CLOSED`, `REFERENCE`
- `DOSSIER_PRESENT` indique la présence d'un dossier direct sous `docs/chantiers/`

| PARENT | CHANTIER | SOUS_CHANTIER | STATUT | DOSSIER_PRESENT | SOURCE |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01 | GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md`<br>`docs/governance/MATRICE_GOUVERNANTE_V2.md` |
| GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md` |
| GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md` |
| GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_HARDENING_01 | GO_UNIFORM_CONTINUITY_HARDENING_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00B_parent_scope_and_structure.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md` |
| GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md` |
| GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md` |
| GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md` |
| GO_RANGE_STRATEGY_V1_STRUCT_01 | GO_RANGE_STRATEGY_V1_STRUCT_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/90_closeout.md` |
| GO_STRATEGY_KERNEL_SHARED_LAYER_01 | GO_STRATEGY_KERNEL_SHARED_LAYER_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/90_closeout.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md` |
| GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | CLOSED | oui | `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/00_cadrage.md` |
| GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS | GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS | — | CLOSED | oui | `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/00_cadrage.md`<br>`docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/90_closeout.md` |
| GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01 | GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md` |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/90_closeout.md` |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md` |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/10_closeout.md`<br>`docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md` |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`<br>`registry/README.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`<br>`docs/ot/trae/trae_pack_texts/README.md` |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md`<br>`docs/index/GO_INDEX.md` |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md`<br>`docs/governance/REPO_ROOT_POLICY.md` |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/90_closeout.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/90_closeout.md`<br>`modules/naming_normalizer/README.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/90_closeout.md`<br>`modules/naming_normalizer/output/naming_audit_report.md` |

---

## Entrées closes/pass

Ces entrées détaillées sont sorties de `docs/index/GO_INDEX.md`.

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01
- repo : opt-trading
- type : gouvernance / doc-only / canonisation
- statut : pass
- titre court : promotion canonique de la matrice gouvernante V2
- dernier état connu : la matrice V2 issue du bundle clos a été promue dans `docs/governance/` avec maintien de `GO_INDEX.md` comme vérité de liste, `REPRISE.md` comme surface opératoire seulement, `BRANCH_STATE.md` comme surface branches, et limite AI team conservée comme report borné
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md`, `docs/governance/MATRICE_GOUVERNANTE_V2.md`

### GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01
- repo : opt-trading
- type : gouvernance / continuité produit
- statut : pass
- titre court : hiérarchie produit multi-chantier canonisée
- dernier état connu : structuration Couche 0 / Anneau A / Anneau B posée comme source canonique de continuité produit
- lien utile : `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md`, `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`

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

### GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS
- repo : opt-trading
- type : collectors / lifecycle compatibility
- statut : pass
- titre court : séquence lifecycle compat collectors canonisée en lot fermé
- dernier état connu : séquence baseline -> scope -> spec -> closeout canonisée sous une forme close `_CLOS` ; closeout historique conservé ; aucun next GO ouvert automatiquement
- lien utile : `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/00_cadrage.md`, `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/90_closeout.md`, `docs/COLLECTORS_LIFECYCLE_COMPAT_CLOSEOUT_01.md`

### GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
- repo : opt-trading
- type : sous-lot d'execution / suite modules / openclaw
- statut : pass
- titre court : consolidation bornee de la suite OpenClaw
- dernier état connu : sous-lot ferme en doc-only apres cartographie de suite, matrice des wrappers, runbook unique, conventions de famille et audit de duplication ; aucun patch shell transverse publie
- lien utile : `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md`, `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/04_step_02_runbook_de_suite.md`

### GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- repo : opt-trading
- type : gouvernance / chantier parent / orchestration de reprise repo-first
- statut : pass
- titre court : parent canonique de reprise avant structuration project/machine
- dernier état connu : closeout dedie publie le 2026-04-29 ; sequence enfant complete, `admin-trading` et `db-layer` conformes, `student` et `fantome` differes, `localcms` fusionne
- lien utile : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/02_final_state.md`

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01
- repo : opt-trading
- type : doc-only / sous-go d'audit final des parents ouverts
- statut : pass
- titre court : audit final de conformite des parents ouverts
- dernier état connu : `90_closeout.md` en `pass` ; conformite finale des parents audites et propagation de continuite corrigee
- lien utile : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/01_conformity_matrix.md`

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
- repo : opt-trading
- type : gouvernance / metadata derivee / doc-only
- statut : closed
- titre court : doctrine legere de derivation post-matrice
- dernier état connu : `10_closeout.md` ferme la sequence documentaire et recommande le gel ; reouverture seulement sous condition explicite
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/10_closeout.md`, `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

### GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : réalignement scope registry
- dernier état connu : `registry/README.md` clarifie le périmètre, la limite repo/package et les exceptions sans créer de doctrine parallèle
- lien utile : `registry/README.md`, `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`

### GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
- repo : opt-trading
- type : patch local / doc-only / reclassement documentaire
- statut : closed
- titre court : révision et relocalisation documentaire de `trae_pack_texts`
- dernier état connu : `docs/ot/trae/trae_pack_texts/README.md` est l'entrée vivante, `trae_pack/` est archive de lecture et le pack n'est plus opposable face au canon repo-first
- lien utile : `docs/ot/trae/trae_pack_texts/README.md`, `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : realignement continuite index
- dernier état connu : la couche `docs/index/*` est coherente, `docs/next/NEXT_GO_CANDIDATES.md` est declassé, et les anciennes surfaces `journal*` ne sont plus actives dans le repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md`, `docs/index/GO_INDEX.md`, `docs/next/NEXT_GO_CANDIDATES.md`

### GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : carte canonique des surfaces du repo
- dernier état connu : `docs/architecture/REPO_SURFACES_MAP.md` est la carte humaine de reference et `docs/INDEX.md` / `docs/ARCHITECTURE.md` sont alignes sans duplication de `registry/*`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md`, `docs/architecture/REPO_SURFACES_MAP.md`, `docs/ARCHITECTURE.md`

### GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : politique racine canonique interne du repo
- dernier état connu : `REPO_ROOT_POLICY.md` qualifie desormais la racine reelle, y compris le shim `bitget_bridge.py` comme exception legacy de compatibilite explicite, sans arbitrage ouvert residuel
- lien utile : `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md`, `docs/governance/REPO_ROOT_POLICY.md`

### GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
- repo : opt-trading
- type : audit / qualification / préparation reclassement physique
- statut : closed
- titre court : audit obsolete / archive / legacy / sous arbitrage
- dernier état connu : la matrice d'audit est jugee suffisante, les lots executes sont documentes et aucun move/delete/archive supplementaire n'est requis pour le closeout
- lien utile : `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`

### GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01
- repo : opt-trading
- type : module durable audit-only
- statut : closed
- titre court : module naming_normalizer
- dernier état connu : le module audit-only est livre avec README, wrappers shell, moteur Python et configuration declarative, sans apply automatique du repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/90_closeout.md`, `modules/naming_normalizer/README.md`

### GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
- repo : opt-trading
- type : audit repo-first
- statut : closed
- titre court : inventaire des ecarts de nommage
- dernier état connu : inventaire repo-first produit sur `docs/chantiers/`, `docs/governance/`, `modules/`, scripts et branches locales, avec classification `CANON / LEGACY_TOLERE / A_CORRIGER_PLUS_TARD / REVIEW_REQUIRED / REFERENCE_ONLY`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/90_closeout.md`, `modules/naming_normalizer/output/naming_audit_report.md`, `modules/naming_normalizer/output/naming_audit_report.json`
