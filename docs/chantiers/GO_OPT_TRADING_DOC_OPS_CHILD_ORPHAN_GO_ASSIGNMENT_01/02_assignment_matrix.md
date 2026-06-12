---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01_MATRIX
doc_type: matrice_affectation
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - orphan
  - go_assignment
  - matrix
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/index/GO_INDEX.md
point_de_reprise: "Section Matrice d'affectation"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01/01_orphan_go_inventory.md
---

# 02_assignment_matrix — Matrice d'affectation orphelins

## Matrice d'affectation

| go_id | statut | parent_canonical_propose | fil_propose | action | confiance | justification |
| --- | --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 | OPEN | self | THREAD_GOVERNANCE_AUTONOME | KEEP | ETABLI | parent gouvernance multi-agents, deja dans GO_INDEX, pas de parent superieur prouve |
| GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 | OPEN | self | THREAD_TRANSVERSE_MODULES | KEEP | ETABLI | GO transverse consolidation modules, traverse 4 machines, pas absorbable par un parent machine |
| GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 | OPEN | RESEAU_SSH_CONSOLIDATION_03 | THREAD_TRANSVERSE_MODULES | KEEP | ETABLI | sous-GO de RESEAU_SSH_CONSOLIDATION_03 |
| GO_TMUX_IDE_OPT_TRADING_CADRAGE_01 | ACTIVE | self | THREAD_OUTILLAGE | KEEP | ETABLI | GO outillage tmux-ide, autonome |
| GO_LOCALCMS_FORMS_INTEGRATION_DOC_01 | OPEN | GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | THREAD_PROJET_UI | ASSIGN | ETABLI | integration forms compatible localcms, rattache au parent UI |
| GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 | OPEN | self | THREAD_PROJET_UI | KEEP | ETABLI | parent UI producer/consumer, autonome |
| GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 | OPEN | self | THREAD_GOVERNANCE_AUTONOME | KEEP | ETABLI | parent gouvernance architecture equipe agents, autonome |
| GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 | ACTIVE | self | THREAD_RUNTIME | KEEP | ETABLI | parent runtime openclaw, autonome, sous-GO deja REFERENCE |
| GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01 | ACTIVE | self | THREAD_GOVERNANCE_RUNTIME | KEEP | ETABLI | gouvernance familles mixtes runtime-exception |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | ACTIVE | self | THREAD_GOVERNANCE_REGISTRY | KEEP | ETABLI | gouvernance scope registry |

## Fils proposes pour les GO non couverts

| thread_id | objet | GO |
| --- | --- | --- |
| THREAD_GOVERNANCE_AUTONOME | parents gouvernance autonomes sans fil existant | MULTI_AGENTS_CANON_PARENT, AI_TEAM_ARCHITECTURE_PARENT |
| THREAD_TRANSVERSE_MODULES | modules transversaux multi-machines | RESEAU_SSH_CONSOLIDATION_03, RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01 |
| THREAD_OUTILLAGE | outillage IDE/terminal | TMUX_IDE_OPT_TRADING_CADRAGE_01 |
| THREAD_PROJET_UI | projet UI producer/consumer | UI_LOCALCMS_CONSUMER_PARENT, LOCALCMS_FORMS_INTEGRATION_DOC |
| THREAD_RUNTIME | runtime openclaw | TMUX_OPENCODE_OPENCLAW_RUNTIME_01 |
| THREAD_GOVERNANCE_RUNTIME | gouvernance runtime/familles | RUNTIME_EXCEPTION_FAMILIES_01 |
| THREAD_GOVERNANCE_REGISTRY | gouvernance registry | REGISTRY_SCOPE_REALIGNMENT_01 |

## Synthese

- **GO non couverts** : 10
- **KEEP** : 9
- **ASSIGN** : 1 (LOCALCMS_FORMS -> parent UI)
- **GO autonomes confirmes** : 7 (MULTI_AGENTS, RESEAU_SSH x2, TMUX_IDE, UI_LOCALCMS, AI_TEAM, TMUX_RUNTIME)
- **GO a rattachement propose** : 3 (LOCALCMS_FORMS, RUNTIME_EXCEPTION, REGISTRY_SCOPE)
- **GO a revoir** : 0

## Sous-GO REFERENCE non traites individuellement

Les sous-GO REFERENCE suivants restent rattaches a leur parent et ne necessitent pas de traitement individuel :
- UI_LOCALCMS_INVENTORY, UI_LOCALCMS_MATRIX, UI_LOCALCMS_CONTRACTS, UI_LOCALCMS_PILOT_READONLY (parent: UI_LOCALCMS_CONSUMER_PARENT)
- TMUX_RUNTIME_CONVENTIONS, OPENCLAW_COMMAND_SCOPE, TMUX_RUNTIME_CONTRACT, OPENCLAW_MODES, GUARDRAILS (parent: TMUX_OPENCODE_OPENCLAW_RUNTIME)

## RISKS

- À qualifier.
