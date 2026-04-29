---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - governance
  - method
  - avalider
  - arbitration
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/02_assignment_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md
  - docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01

## Classification

doc-only / sous-GO d'arbitrage / gouvernance-methode

## Role recommande

Arbitrer les 2 GO marques `A_VALIDER` dans le lot THREAD_ASSIGNMENT, avant de passer aux parents machine ou aux GO orphelins.

## Besoin initial

Le lot GOVERNANCE_METHOD_THREAD_ASSIGNMENT_01 a affecte 16 GO de gouvernance/methode a des fils de continuite. 2 GO restent en A_VALIDER :
- GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 : THREAD_ARCHIVE_REFERENCE ou THREAD_METHOD_WORKFLOW ?
- GO_GIT_PROGRESSIVE_MIGRATION_START_13 : THREAD_METHOD_WORKFLOW confirme ?

## Cible finale

Trancher pour chaque GO :
- le fil de continuite definitif
- la justification courte
- la confiance ETABLI

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI

- GO_INDEX.md est la verite de liste
- la matrice d'affectation du lot precedent couvre 16 GO
- 2 GO sont en A_VALIDER
- les criteres d'arbitrage sont definis dans le prompt du GO

## Plan valide

### Phase 1 - Revue des 2 GO A_VALIDER
Lire les dossiers chantier des 2 GO pour comprendre leur nature reelle.

### Phase 2 - Arbitrage
Trancher pour chaque GO selon les criteres :
- OBSOLETE_RECLASS_ARCHIVE_AUDIT : si classer/archiver/déclasser -> THREAD_ARCHIVE_REFERENCE ; si definir methode durable -> THREAD_METHOD_WORKFLOW
- GIT_PROGRESSIVE_MIGRATION : si organiser methode progressive migration -> THREAD_METHOD_WORKFLOW

### Phase 3 - Documentation
Documenter le verdict, le fil retenu et la justification.

## Anti-cibles

Ne pas faire :
- traiter les parents machine
- traiter les GO orphelins
- creer GO_PARENT_THREAD_MAP.md
- modifier GO_INDEX.md
- modifier BRANCH_STATE.md

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md`
