---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01_CONTRACT
doc_type: contrat
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - parent_thread_map
  - index
  - contract
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Contrat"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
---

# 02_index_contract — Contrat de GO_PARENT_THREAD_MAP.md

## Contrat

### 1. Frontmatter

- `doc_id: OPT_TRADING_GO_PARENT_THREAD_MAP`
- `doc_type: index`
- `repo: opt-trading`
- `status: reference`
- `lifecycle_stage: continuity`
- `surface: continuity`
- `source_kind: derived`
- `reference_canonique_principale: docs/index/GO_INDEX.md`

### 2. Regle de priorite

- `GO_INDEX.md` reste verite de liste
- `GO_PARENT_THREAD_MAP.md` est une vue derivee parent/thread
- les divergences sont a resoudre contre `GO_INDEX.md` et les dossiers chantier
- `GO_PARENT_THREAD_MAP.md` ne gouverne pas la structure parent/GO

### 3. Contenu

Une table unique :

| GO | statut | parent canonique | fil principal | fils secondaires | action | confiance | source |

### 4. Groupes

- gouvernance / methode
- machine
- orphelins / transversaux / runtime / projet
- reference-only

### 5. Source des donnees

Les donnees proviennent de :
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01/02_assignment_matrix.md`

### 6. Regles de priorite entre index

| Index | Role | Priorite |
| --- | --- | --- |
| GO_INDEX.md | verite de liste des parents et GO | souveraine |
| GO_PARENT_THREAD_MAP.md | vue derivee parent/thread | derivee, subordonnee |
| REPRISE.md | support de pilotage operatoire | operatoire, non souveraine |
| ACTIVE_STREAMS.md | flux actifs ou bloques | operatoire, non souveraine |
| NEXT_GO_CANDIDATES.md | next GO par parent actif | operatoire, non souveraine |
| BRANCH_STATE.md | surface branche uniquement | branche, non souveraine |

## RISKS

- À qualifier.
