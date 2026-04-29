---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_PARENT_INVENTORY
doc_type: inventaire
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_inventory
  - go_index
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Tableau des parents"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 01_parent_inventory — Inventaire des parents

## Source

`docs/index/GO_INDEX.md` — Tableau canonique des chantiers + Entrees.

## Methode

Extraction de toutes les lignes ou PARENT != CHANTIER, ou ou le GO est explicitement declare comme parent dans les Entrees.

## Tableau des parents

| parent_id | type | statut | dossier_present | source_canonique | fil_de_continuite_propose |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/` | parent -> inbox -> GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01 |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/` | parent -> alignement surfaces proches |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/` | parent -> CHILD_PARENT_CONFORMITY_AUDIT -> CHILD_GO_PARENT_THREAD_MAP |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | MACHINE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/` | parent -> inventaire machine -> futur enfant |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | MACHINE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/` | parent -> inventaire machine -> futur enfant |
| GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 | MACHINE | DEFERRED | non | — | differe ; pas de dossier |
| GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 | MACHINE | DEFERRED | non | — | differe ; pas de dossier |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | PROJECT | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/` | parent -> INVENTORY -> MATRIX -> CONTRACTS -> PILOT |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/` | parent -> CHILD_NAMING_INVENTORY -> CHILD_NAMING_NORMALIZER |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/` | parent -> futur enfant audit doc |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GOVERNANCE | ACTIVE | oui | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/` | parent -> reclassement racine |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GOVERNANCE | ACTIVE | oui | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/` | parent -> matrice canonique -> plan lots physiques |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GOVERNANCE | OPEN | oui | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/` | parent -> reduction compat -> qualification step1b |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | RUNTIME | ACTIVE | oui | `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/` | parent -> sous-GO reference multiples |

## Observations

- 14 parents identifies au total
- 4 parents machine dont 2 differe (student, fantome)
- les parents GOVERNANCE dominent la structure
- aucun parent PROJECT hors LocalCMS
- aucun parent SUPPORT ou REFERENCE explicite dans le tableau canonique

## Parents non retenus dans GO_INDEX mais presents dans les dossiers chantier

Certains dossiers chantier existent sans ligne parent explicite dans GO_INDEX. Ils restent des GO simples ou des sous-GO et ne sont pas promus parents ici.
