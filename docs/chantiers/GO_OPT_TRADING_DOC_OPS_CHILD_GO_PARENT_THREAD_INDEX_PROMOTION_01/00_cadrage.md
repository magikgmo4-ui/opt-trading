---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - parent_thread_map
  - index
  - promotion
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01/02_assignment_matrix.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01

## Classification

doc-only / sous-GO de promotion index / parent-thread-map

## Role recommande

Decider et, si valide par l'audit, creer l'index leve derive `docs/index/GO_PARENT_THREAD_MAP.md`.

## Besoin initial

5 lots ont ete merges pour cartographier parent canonique / fil de continuite / GO. Les donnees sont dispersees dans 5 dossiers chantier. Un index leve consolidant cette cartographie serait utile comme vue derivee rapide.

## Cible finale

Creer `docs/index/GO_PARENT_THREAD_MAP.md` comme vue derivee legere, subordonnee a `GO_INDEX.md`.

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Source de verite : `docs/index/GO_INDEX.md`

## ETABLI

- GO_INDEX.md est la verite de liste
- les 5 lots precedents ont couvert tous les GO
- GO_PARENT_THREAD_MAP.md serait une vue derivee, pas une verite concurrente

## Plan valide

### Phase 1 - Audit d'utilite
Verifier que l'index est utile et non concurrent.

### Phase 2 - Contrat
Definir le contrat de l'index.

### Phase 3 - Creation
Creer l'index si l'audit confirme.

## Anti-cibles

Ne pas faire :
- faire de GO_PARENT_THREAD_MAP.md une verite de liste concurrente
- modifier massivement GO_INDEX.md
- rouvrir Student / Fantome

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_INDEX_PROMOTION_01/02_index_contract.md`

## RISKS

- À qualifier.
