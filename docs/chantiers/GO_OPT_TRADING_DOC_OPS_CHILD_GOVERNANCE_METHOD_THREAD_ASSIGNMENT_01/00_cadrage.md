---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - method
  - thread_assignment
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/04_assignment_rules.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01

## Classification

doc-only / sous-GO d'affectation fil de continuite / gouvernance-methode

## Role recommande

Regler l'affectation des GO de gouvernance, matrice, methode de travail, continuite et index dans la cartographie parent / fil de continuite, avant toute suite machine ou orphelins.

## Besoin initial

Le GO_PARENT_THREAD_MAP a produit une cartographie draft de 27 GO. Mais les GO de gouvernance/methode n'ont pas encore ete affectes a des fils de continuite nommes. Sans cette affectation, la cartographie reste une liste plate sans structure de flux.

## Cible finale

Disposer pour chaque GO gouvernance/methode de :
- un parent canonique confirme
- un fil de continuite principal nomme (THREAD_*)
- une action confirme (KEEP, ASSIGN, REFERENCE_ONLY, DEFER, REVIEW)
- une justification courte

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Surface de liste : `docs/index/GO_INDEX.md`
- Matrice draft : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md`

## ETABLI

- GO_INDEX.md est la verite de liste
- MATRICE_DOC_OPS_MASTER_MATRIX_01.md gouverne la lecture
- la matrice draft du GO_PARENT_THREAD_MAP couvre 27 GO
- les GO machine ne sont pas dans le perimetre de ce lot
- les GO orphelins ne sont pas dans le perimetre de ce lot

## Plan valide

### Phase 1 - Inventaire gouvernance/methode
Liste des GO de gouvernance, matrice, methode, continuite et index observes dans GO_INDEX.

### Phase 2 - Affectation par fil
Pour chaque GO, determiner le fil de continuite principal parmi :
- THREAD_DOC_OPS
- THREAD_GOVERNANCE_METADATA
- THREAD_NAMING_CANON
- THREAD_CONTINUITY_INDEX
- THREAD_METHOD_WORKFLOW
- THREAD_ARCHIVE_REFERENCE

### Phase 3 - Matrice d'affectation
Matrice GO -> parent -> fil -> action -> justification.

### Phase 4 - Decisions
Decisions explicites pour les GO ambigus ou a revoir.

## Anti-cibles

Ne pas faire :
- traiter les GO machine
- traiter les GO orphelins
- creer docs/index/GO_PARENT_THREAD_MAP.md
- modifier GO_INDEX.md
- ouvrir de chantier machine
- ouvrir Student / Fantome

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md`

## RISKS

- À qualifier.
