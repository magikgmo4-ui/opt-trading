---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - machine
  - parent
  - thread_assignment
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/04_assignment_rules.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GOVERNANCE_METHOD_AVALIDER_ARBITRATION_01/02_final_assignment.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01

## Classification

doc-only / sous-GO d'affectation / parents machine

## Role recommande

Traiter les parents machine et les GO lies aux machines dans la cartographie parent / fil de continuite.

## Besoin initial

Les GO gouvernance/methode sont tous arbitres (16 GO, tous ETABLI). Il reste a traiter les parents machine :
- GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)
- GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01 (OPEN)
- GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 (DEFERRED)
- GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 (DEFERRED)

## Cible finale

Disposer pour chaque parent machine de :
- un statut confirme
- un fil de continuite principal nomme
- les GO directement rattaches
- les GO candidats a rattachement secondaire
- les GO a ne pas deplacer

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI

- admin-trading et db-layer sont ouverts et conformes (audit PASS)
- student et fantome restent differes
- les GO transversaux (RESEAU_SSH, TMUX_IDE, RUNTIME, MULTI_AGENTS) ne doivent pas etre absorbes sans preuve

## Plan valide

### Phase 1 - Revue des parents machine
Lire les dossiers chantier des 4 parents machine.

### Phase 2 - Identification des GO lies
Identifier les GO qui ont un lien machine, meme secondaire.

### Phase 3 - Affectation par fil
Affecter chaque parent machine a un fil THREAD_MACHINE_*.

### Phase 4 - Decisions
Decisions explicites pour les GO transversaux.

## Anti-cibles

Ne pas faire :
- deplacer un GO vers un parent machine sans preuve
- absorber RESEAU_SSH, TMUX_IDE, RUNTIME dans un parent machine
- ouvrir STUDENT ou FANTOME
- creer GO_PARENT_THREAD_MAP.md

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_MACHINE_PARENT_THREAD_ASSIGNMENT_01/02_machine_go_assignment_matrix.md`
