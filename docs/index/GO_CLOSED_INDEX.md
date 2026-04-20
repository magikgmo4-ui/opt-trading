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
surface: chantier
source_kind: canonical
updated_at: 2026-04-20
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
