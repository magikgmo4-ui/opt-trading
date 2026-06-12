---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - parent
  - closeout
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
---

# GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01

## Classification

doc-only / sous-GO de closeout / parent doc-ops

## Role recommande

Fermer proprement le parent GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01, sauf si un ecart reel impose de le garder ouvert.

## Besoin initial

Le parent GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 a ete ouvert pour orchestrer la reprise repo-first apres la matrice. Sa sequence de 6 etapes est consommee. Des enfants supplementaires ont ete ouverts et clos. Il faut verifier si le parent peut passer en CLOSED/PASS.

## Cible finale

Verifier et documenter :
- la sequence enfant complete est-elle consommee ?
- les parents machine sont-ils ouverts et conformes ?
- STUDENT et FANTOME sont-ils bien differes ?
- LOCALCMS est-il bien fusionne ?
- GO_PARENT_THREAD_MAP.md existe-t-il ?
- les index pointent-ils vers un etat coherent ?
- reste-t-il un lot complementaire reel ?

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI

- la matrice maitre est la surface souveraine
- GO_INDEX.md reste la verite de liste
- GO_PARENT_THREAD_MAP.md existe comme index derive

## Plan valide

### Phase 1 - Revue du parent
Lire les dossiers du parent et de tous les enfants.

### Phase 2 - Verification des criteres
Verifier chaque critere de closeout.

### Phase 3 - Decision
Decider CLOSE ou KEEP_OPEN.

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/02_final_state.md`

## RISKS

- À qualifier.
