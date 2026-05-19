---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - go_parent_thread_map
  - parent_canonical
  - continuity
  - governance
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
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01

## Classification

doc-only / sous-GO d'audit / cartographie parent -> fil -> GO

## Role recommande

Produire une cartographie canonique audit-first : parent canonique -> fil de continuite -> GO.

## Besoin initial

Apres la matrice maitre, l'ouverture des parents machine et l'audit de conformite, il manque une cartographie unique qui relie chaque GO a son parent canonique et a son fil de continuite principal. Sans cette cartographie, les rattachements restent implicites ou disperses entre plusieurs surfaces.

## Cible finale

Disposer d'une matrice canonique draft qui :
- liste tous les parents existants observes dans `GO_INDEX.md`
- liste separement les parents machine
- liste tous les GO connus avec leur parent canonique propose et leur fil de continuite principal
- documente les regles d'affectation
- identifie les GO ambigus, les GO a ne pas deplacer, et les GO deja clairement assignes

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`
- Surface de liste : `docs/index/GO_INDEX.md`

## ETABLI

- `GO_INDEX.md` est la verite de liste des parents et GO
- `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la lecture parent / GO / Git
- les parents machine `admin-trading` et `db-layer` sont ouverts et conformes
- `student` et `fantome` restent differes
- `localcms` reste fusionne avec le parent UI existant
- `BRANCH_STATE.md` reste surface branche uniquement
- `REPRISE.md` ne devient pas verite de liste

## Plan valide

### Phase 1 - Inventaire des parents
Liste de tous les parents observes dans `GO_INDEX.md` avec type, statut, dossier present, source canonique et fil de continuite propose.

### Phase 2 - Inventaire des parents machine
Traitement separe des 4 parents machine (admin-trading, db-layer, student, fantome).

### Phase 3 - Inventaire des GO
Liste de tous les GO connus avec parent actuel, parent canonique propose, fil principal, confiance et action.

### Phase 4 - Regles d'affectation
Documentation des regles canoniques de rattachement.

### Phase 5 - Draft de mapping
Matrice draft dans le dossier chantier.

## Anti-cibles

Ne pas faire :
- creer `docs/index/GO_PARENT_THREAD_MAP.md` dans ce lot sauf necessite prouvee
- deplacer des GO sans preuve
- ouvrir `STUDENT` ou `FANTOME`
- creer un clone LocalCMS
- modifier `BRANCH_STATE.md` sauf incoherence prouvee
- fermer `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`
- ouvrir un nouveau parent machine

## Gap restant

Il reste a produire :
1. la liste des parents existants
2. la liste separee des parents machine
3. la liste des GO avec rattachement propose
4. les regles d'affectation
5. la matrice draft

## Point de reprise

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GO_PARENT_THREAD_MAP_01/05_parent_thread_map_draft.md`
