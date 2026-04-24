---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - project_machine_split
  - continuity
  - governance
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01

## Classification
gouvernance + chantier parent + orchestration de reprise projet / machine

## Role recommande
architecte de continuite repo-first + arbitre d'ouverture des parents structurants

## Besoin initial
Repartir du bon pied apres canonisation de la matrice, gerer proprement les chantiers et branches encore ouverts, puis ouvrir sans conflit des parents structurants lisibles par projet et par machine.

## Cible finale
Disposer d'un plan canonique unique permettant :
- de qualifier les branches et chantiers encore ouverts
- de repartir d'une base propre `sot/mainline`
- d'ouvrir proprement 5 chantiers parents specialises, repartis entre lecture projet et lecture machine
- de verifier que chaque parent respecte la matrice maitre sur le nommage, le frontmatter, le rattachement produit, les surfaces de continuite et le support Git

## Source canonique
- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI
- la matrice maitre est maintenant la surface souveraine de gouvernance
- `GO_INDEX.md` reste la verite de liste
- `NEXT_GO_CANDIDATES.md` reste la matrice parent actif -> next GO primaire
- `ACTIVE_STREAMS.md` et `REPRISE.md` restent operatoires et non souverains pour la liste
- les branches sont des supports Git et non des substituts a la trajectoire produit
- le prochain risque n'est plus doctrinal ; il porte sur la gestion propre des branches / chantiers ouverts et sur l'ouverture sans conflit des futurs parents structurants

## Plan valide

### Axe 1 - Hygiene de reprise
Qualifier les branches et chantiers ouverts restants, supprimer les branches merged sans utilite, et repartir depuis `sot/mainline` propre.

### Axe 2 - Carte cible projet / machine
Figer la repartition cible des 5 parents a ouvrir, avec un rattachement principal explicite :
- centre de gravite produit
- famille de soutien
- ou couche methode / transmission
- machine cible si le parent est machine-first

### Axe 3 - Ouverture canonique des 5 parents
Ouvrir les 5 parents un par un avec :
- nom canonique stabilise
- dossier parent reel
- frontmatter noyau correct
- support Git justifie
- propagation dans `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` et `BRANCH_STATE.md` si necessaire

### Axe 4 - Validation de conformite
Verifier pour chaque parent :
- lecture produit -> parent -> GO -> Git
- absence de parent ou sous-GO decoratif
- respect du `PRODUCT_OR_SURFACE`
- respect des regles d'ouverture / fermeture / propagation
- absence de conflit entre les plans de travail paralleles

## Anti-cibles
Ne pas faire :
- ouverture simultanee opportuniste des 5 parents sans carte cible prealablement validee
- multiplication de branches sans besoin d'isolement reel
- creation de parents decoratifs pour imiter une structure non prouvee
- confusion entre parents produit, parents machine et support Git
- fermeture implicite ou suppression de branche sans propagation documentaire

## Gap restant
Il reste a produire :
1. l'inventaire qualifie des branches et chantiers ouverts restants
2. la carte cible des 5 parents a ouvrir
3. l'ouverture canonique des 5 parents specialises
4. la verification finale de conformite selon la matrice

## GO suivants proposes

### GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01
Inventaire et arbitrage des branches ouvertes / merged / de reference.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
Carte cible des 5 parents projet / machine a ouvrir.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
Ouverture canonique des 5 parents specialises, un par un, avec propagation complete.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01
Verification finale que chaque parent respecte la matrice.

## TODO
- qualifier les branches ouvertes restantes
- figer la carte cible projet / machine
- ouvrir les 5 parents specialises
- verifier leur conformite a la matrice
- reclore les branches de support devenues inutiles

## REPRISE
Point de reprise recommande :
`GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`

Sequence :
branches/chantiers ouverts -> carte cible des 5 parents -> ouverture canonique -> audit de conformite
