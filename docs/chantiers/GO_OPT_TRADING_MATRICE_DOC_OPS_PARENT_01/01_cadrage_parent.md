---
doc_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - matrice_doc_ops
  - governance
  - master_matrix
  - parent_chantier
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Next GO"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01

## Classification

gouvernance + chantier parent + doc-only + fusion maître de structure documentaire et opératoire

## Rôle recommandé

architecte de gouvernance repo + mainteneur continuité + lecteur produit-first

## Besoin initial

Le repo dispose déjà :
- d'un socle gouvernant
- d'une doctrine de dérivation
- d'une hiérarchie produit
- d'index opératoires
- d'une lecture branches

Mais ces règles restent dispersées.

Il manque encore une matrice maîtresse unique capable d'empêcher qu'on reperde :
- le pourquoi produit
- le plan macro validé
- les plans de travail rattachés aux GO
- la lecture parent / sous-GO / GO simple
- le statut Git réel
- la suite logique globale

## Cible finale

Produire une matrice maîtresse unique, gouvernante et canonique qui fusionne :
- produit
- familles
- plans de travail
- rattachement des GO
- nommage
- frontmatter
- placement / indexation
- branches
- règles d'ouverture / fermeture / propagation

## ETABLI

- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` existe desormais comme matrice maitre finale unique de gouvernance
- `docs/governance/MATRICE_GOUVERNANTE_V2.md` fixe déjà le socle structurel
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md` fixe déjà la sous-couche de dérivation
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md` et `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md` portent déjà la continuité produit
- `docs/index/GO_INDEX.md`, `docs/index/ACTIVE_STREAMS.md`, `docs/index/NEXT_GO_CANDIDATES.md` et `docs/index/REPRISE.md` portent déjà une partie de la lecture opératoire
- `docs/index/BRANCH_STATE.md` et `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md` portent déjà une partie du statut Git réel
- les surfaces de nommage existent mais ne sont pas encore fusionnées proprement dans le canon maître

## Gap restant

- l'alignement / deduplication / reclassement des surfaces proches n'est pas encore execute
- certaines surfaces utiles restent encore annexes, derivees ou non souveraines et doivent etre recalees a partir de la matrice maitre
- le parent doit encore propager cette reference sans ouvrir de chantier concurrent

## Plan validé

### Axe 1 - Ancrage du plan maître
- poser le plan complet comme document canonique
- rattacher ce plan à un parent chantier explicite

### Axe 2 - Recroisement canonique
- relire les surfaces déjà publiées
- extraire les règles réellement stables
- isoler ce qui relève du maître, de l'annexe, du dérivé et de l'opératoire

### Axe 3 - Fusion gouvernante
- produire un document maître unique
- éviter toute synthèse latérale concurrente

### Axe 4 - Stabilisation
- faire de la matrice maître la référence à respecter ensuite
- n'ouvrir des sous-GO que si le parent a besoin d'une exécution bornée supplémentaire

## Anti-cibles

- ne pas rouvrir un audit général du repo
- ne pas faire du parent un chantier de correction massive
- ne pas déporter la cible vers une simple note de synthèse
- ne pas ouvrir de sous-GO techniques avant que l'ossature maître soit réellement fixée

## Support Git retenu

- repo canonique : `opt-trading`
- base canonique : `origin/sot/mainline`
- support Git local du présent passage : `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`

## Effet attendu sur la trajectoire produit

Ce parent doit réancrer la lecture globale du repo.

Il doit permettre ensuite de repartir :
1. du produit
2. du parent
3. du GO
4. du Git

Et non l'inverse.

## Next GO

Aucun sous-GO imposé à ce stade.

La suite immédiate correcte est :
- lancer le lot d'alignement / deduplication / reclassement des surfaces proches a partir de la matrice maitre deja redigee

## PASS / FAIL

- PASS : le parent aboutit à une matrice unique réellement gouvernante
- FAIL : le parent se disperse en notes latérales, en parents concurrents ou en lots techniques non recroisés

## RISKS

- À qualifier.
