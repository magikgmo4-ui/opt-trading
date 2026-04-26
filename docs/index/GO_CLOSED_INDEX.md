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
updated_at: 2026-04-25
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
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/90_closeout.md` |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/90_closeout.md` |

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

### GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03
- repo : opt-trading
- type : consolidation modules / reseau_ssh
- statut : pass
- titre court : consolidation intégrale de la famille reseau_ssh
- dernier état connu : un seul module top-level actif `modules/reseau_ssh` reste en place ; l'implémentation `reseau_ssh_step2` est interne au canonique ; un seul jeu d'alias publiés `menu/cmd/sanity-reseau_ssh` reste en place ; `db-layer`, `admin-trading`, `student` et `fantome` passent `sanity-reseau_ssh`
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/90_closeout.md`, `docs/status/reseau_ssh_canonique.md`

### GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
- repo : opt-trading
- type : unification de module / reseau_ssh
- statut : pass
- titre court : cadrage de module unique absorbe
- dernier état connu : le cadrage a atteint sa cible et est absorbé dans le closeout final du parent `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
- lien utile : `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/90_closeout.md`
