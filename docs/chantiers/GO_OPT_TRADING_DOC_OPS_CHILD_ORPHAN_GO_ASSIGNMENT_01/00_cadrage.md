---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - orphan
  - go_assignment
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01

## Classification

doc-only / sous-GO d'affectation / GO orphelins

## Role recommande

Traiter les GO restant a clarifier apres les lots gouvernance/methode et machine : orphelins, REFERENCE_ONLY, mal rattaches, autonomes.

## Besoin initial

Les lots precedents ont couvert :
- 16 GO gouvernance/methode (tous ETABLI)
- 4 parents machine (2 KEEP, 2 DEFER)
- 1 GO ASSIGN (LOCALCMS_FORMS -> parent UI)

Il reste des GO dans GO_INDEX qui n'ont pas ete explicitement affectes a un fil de continuite.

## Cible finale

Disposer pour chaque GO restant de :
- un parent canonique confirme
- un fil de continuite propose ou "autonome"
- une action confirme
- une justification courte

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI

- GO_INDEX.md est la verite de liste
- les lots precedents ont couvert gouvernance/methode et machine
- les GO restants sont : transversaux, projet, runtime, ou autonomes

## Plan valide

### Phase 1 - Inventaire des GO non couverts
Identifier les GO de GO_INDEX non couverts par les lots precedents.

### Phase 2 - Affectation
Pour chaque GO, determiner le parent et le fil.

### Phase 3 - Decisions
Decisions explicites.

## Anti-cibles

Ne pas faire :
- recreer un parent LocalCMS deja fusionne
- absorber les GO transversaux par les parents machine
- modifier GO_INDEX.md
- creer GO_PARENT_THREAD_MAP.md

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_ORPHAN_GO_ASSIGNMENT_01/02_assignment_matrix.md`

## RISKS

- À qualifier.
