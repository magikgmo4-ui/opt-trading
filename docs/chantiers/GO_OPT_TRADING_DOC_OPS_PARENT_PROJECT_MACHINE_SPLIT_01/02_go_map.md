---
doc_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01_GO_MAP
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - doc_ops
  - project_machine_split
  - go_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Sequence canonique"
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# GO_MAP — GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01

## Objet
Cartographier la sequence canonique de reprise apres la matrice, sans dependre de la session et sans ouvrir trop tot les futurs parents specialises.

## Regle
Le present fichier ne canonise pas encore les 5 parents projet / machine.
Il fige d'abord la sequence de controle des branches et des chantiers encore ouverts, puis seulement la phase future de structuration.

## Sequence canonique

### Etape 1 - Hygiene Git / branches / supports ouverts
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`

But :
- qualifier les branches restantes
- distinguer `KEEP_ACTIVE`, `KEEP_REFERENCE`, `DROP_MERGED`
- remettre le systeme a plat sur `sot/mainline`

### Etape 2 - Controle des ouverts / non termines
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`

But :
- relire `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md`
- figer la liste de ce qui reste reellement ouvert ou non termine
- identifier ce qui reste executable, ce qui reste reference, et ce qui doit etre depriorise

### Etape 3 - Reprise d'un flux principal
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`

But :
- arbitrer le point de depart operatoire principal
- repartir sur un seul flux principal a la fois
- documenter explicitement pourquoi ce flux est retenu avant les autres

### Etape 4 - Carte cible future des 5 parents
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01`

But :
- fixer la liste exacte des 5 parents a ouvrir plus tard
- expliciter pour chacun : projet / machine / famille / rattachement principal / support Git vise
- verifier qu'aucun parent n'est decoratif

### Etape 5 - Ouverture canonique des 5 parents
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01`

But :
- ouvrir les 5 parents reellement valides
- propager leur ouverture dans `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` et `BRANCH_STATE.md` si necessaire

### Etape 6 - Audit de conformite final
GO de reprise propose :
- `GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01`

But :
- verifier que les 5 parents respectent la matrice maitre
- valider nommage, frontmatter, rattachement produit, support Git, propagation et non-concurrence

## Conditions de passage
On ne passe a l'etape suivante que si :
- l'etape precedente est documentee et propagee dans la continuite active
- aucun conflit structurel non arbitre ne subsiste
- le support Git retenu reste coherent avec la matrice
- aucun nouveau parent specialise n'est ouvert avant la fin explicite du controle des ouverts / non termines
