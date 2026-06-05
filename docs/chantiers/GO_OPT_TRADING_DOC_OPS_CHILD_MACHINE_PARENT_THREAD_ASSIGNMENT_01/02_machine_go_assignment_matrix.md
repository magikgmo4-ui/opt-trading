---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01_MATRIX
doc_type: matrice_affectation
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - machine
  - parent
  - thread_assignment
  - matrix
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Matrice d'affectation"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/01_machine_parent_review.md
---

# 02_machine_go_assignment_matrix — Matrice d'affectation machine

## Fils machine retenus

| thread_id | objet | perimetre |
| --- | --- | --- |
| THREAD_MACHINE_ADMIN_TRADING | parent machine admin-trading, interfaces operateur, futurs enfants | MACHINE_ADMIN_TRADING_PARENT |
| THREAD_MACHINE_DB_LAYER | parent machine db-layer, interfaces consultation/export/ingestion, futurs enfants | MACHINE_DB_LAYER_PARENT |
| THREAD_MACHINE_STUDENT_DEFERRED | parent machine student, differe, pas ouvert | MACHINE_STUDENT_PARENT |
| THREAD_MACHINE_FANTOME_DEFERRED | parent machine fantome, differe, pas ouvert | MACHINE_FANTOME_SUPPORT_PARENT |

## Matrice d'affectation parents machine

| go_id | statut | fil_principal | action | confiance | justification |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | OPEN | THREAD_MACHINE_ADMIN_TRADING | KEEP | ETABLI | parent machine ouvert, conformite PASS, doc-only |
| GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 | OPEN | THREAD_MACHINE_DB_LAYER | KEEP | ETABLI | parent machine ouvert, conformite PASS, doc-only |
| GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 | DEFERRED | THREAD_MACHINE_STUDENT_DEFERRED | DEFER | ETABLI | parent machine differe, pas de dossier |
| GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 | DEFERRED | THREAD_MACHINE_FANTOME_DEFERRED | DEFER | ETABLI | parent machine differe, pas de dossier |

## GO a rattachement secondaire

| go_id | parent_principal | parent_machine_secondaire | type_lien | justification |
| --- | --- | --- | --- | --- |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | self (THREAD_METHOD_WORKFLOW equivalent) | admin-trading, db-layer | machine cible | admin-trading et db-layer sont des machines cibles de reseau_ssh (alias migres PASS) ; lien secondaire descriptif seulement |

## GO a ne pas deplacer vers un parent machine

| go_id | raison |
| --- | --- |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | GO transverse consolidation modules ; traverse 4 machines |
| GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | sous-GO de RESEAU_SSH_CONSOLIDATION_03 |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | GO outillage tmux-ide ; admin-trading est une cible mais pas le parent |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | GO runtime transverse |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | GO gouvernance multi-agents |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | GO gouvernance architecture |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | GO gouvernance familles mixtes |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO gouvernance scope registry |

## Synthese

- **parents machine** : 4
- **KEEP** : 2 (admin-trading, db-layer)
- **DEFER** : 2 (student, fantome)
- **GO a rattachement secondaire** : 1 (RESEAU_SSH -> admin-trading, db-layer)
- **GO a ne pas deplacer** : 8
- **GO a revoir** : 0

## RISKS

- À qualifier.
