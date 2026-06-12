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
  - docs/governance/NAMING_CANON_POLICY_01.md
---

# GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01

## Classification
gouvernance + chantier parent + orchestration de reprise repo-first avant structuration projet / machine

## Role recommande
architecte de continuite repo-first + arbitre de reprise des flux ouverts + preparateur des futurs parents structurants

## Besoin initial
Ne plus dependre de la session pour repartir du bon pied apres canonisation de la matrice. Geler un plan unique qui commence par controler tout ce qui reste ouvert ou non termine, gerer proprement les branches encore actives ou residuelles, puis seulement ensuite preparer l'ouverture future de parents specialises par projet ou par machine.

## Cible finale
Disposer d'un parent canonique unique qui fixe sans ambiguite :
- l'ordre de reprise reel apres la matrice
- la gestion propre des branches et chantiers encore ouverts
- la regle "un seul flux principal a la fois"
- le fait que l'ouverture future de 5 parents specialises ne vient qu'apres controle des ouverts / non termines
- la verification finale que les futurs parents respecteront la matrice maitre sur le nommage, le frontmatter, le rattachement produit, les surfaces de continuite et le support Git

## Source canonique
- Repo canonique : `opt-trading`
- Branche canonique : `sot/mainline`

## ETABLI
- la matrice maitre est maintenant la surface souveraine de gouvernance
- `GO_INDEX.md` reste la verite de liste
- `NEXT_GO_CANDIDATES.md` reste la matrice parent actif -> next GO primaire
- `ACTIVE_STREAMS.md` et `REPRISE.md` restent operatoires et non souverains pour la liste
- les branches sont des supports Git et non des substituts a la trajectoire produit
- le prochain risque n'est plus doctrinal ; il porte sur la gestion propre des branches / chantiers ouverts et sur la reprise sans conflit des flux encore actifs
- l'ouverture de 5 parents specialises par projet / machine n'est pas l'etape immediate ; elle vient seulement apres controle de tout ce qui reste ouvert ou non termine

## Plan valide

### Axe 1 - Hygiene Git immediate
Qualifier les branches encore ouvertes, merged ou de reference, supprimer les branches merged sans utilite, et repartir depuis `sot/mainline` propre.

### Axe 2 - Controle des chantiers ouverts / non termines
Relire les surfaces actives (`GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md`) pour figer :
- ce qui est encore ouvert / actif / non termine
- ce qui reste vraiment prioritaire
- ce qui peut rester en reference ou hors execution courante
- quel parent devient le point de depart operatoire reel

### Axe 3 - Reprise d'un seul flux principal
Repartir ensuite sur un seul flux principal a la fois, au lieu de relancer plusieurs chantiers en parallele. La recommandation actuelle issue de la session est de repartir d'abord par la continuite active / index si aucun autre arbitrage reel ne s'impose.

### Axe 4 - Structuration future projet / machine
Seulement apres les axes 1 a 3, figer la carte cible d'ouverture de 5 parents specialises, repartis entre lecture projet et lecture machine, puis les ouvrir proprement sans conflit.

### Axe 5 - Validation finale de conformite
Verifier pour chaque parent ouvert :
- lecture produit -> parent -> GO -> Git
- absence de parent ou sous-GO decoratif
- respect du `PRODUCT_OR_SURFACE`
- respect des regles d'ouverture / fermeture / propagation
- absence de conflit entre les plans de travail paralleles

## Anti-cibles
Ne pas faire :
- ouverture immediate des 5 parents specialises sans avoir d'abord controle les ouverts / non termines
- multiplication de branches sans besoin d'isolement reel
- creation de parents decoratifs pour imiter une structure non prouvee
- confusion entre parents produit, parents machine et support Git
- reouverture de la doctrine au lieu de repartir operatoirement depuis les surfaces canoniques
- reprise simultanee de plusieurs flux principaux sans arbitrage explicite

## Gap restant
Il reste a produire :
1. l'inventaire qualifie des branches ouvertes / merged / de reference
2. le controle explicite des chantiers encore ouverts ou non termines
3. le choix du point de depart operatoire principal
4. la carte cible future des 5 parents a ouvrir
5. l'ouverture canonique de ces parents et l'audit final de conformite

## GO suivants proposes

### GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01
Inventaire et arbitrage des branches ouvertes / merged / de reference.

### GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01
Controle repo-first de tout ce qui reste ouvert / non termine dans les surfaces actives.

### GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01
Formalisation du point de depart operatoire principal et de l'ordre de reprise effectif.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_TARGET_MAP_01
Carte cible future des 5 parents projet / machine a ouvrir, seulement apres les etapes precedentes.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_OPENING_BATCH_01
Ouverture canonique des 5 parents specialises, un par un, avec propagation complete.

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01
Verification finale que les parents ouverts respectent la matrice.

## TODO
- qualifier les branches ouvertes restantes
- controler tout ce qui reste ouvert / non termine
- choisir un seul flux principal de reprise
- seulement ensuite figer la carte cible des 5 parents
- ouvrir les futurs parents specialises
- verifier leur conformite a la matrice

## REPRISE
Point de reprise recommande :
`GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`

Sequence :
branches ouvertes / merged / reference -> controle des ouverts / non termines -> point de depart principal -> carte cible future des 5 parents -> ouverture canonique -> audit de conformite

## RISKS

- À qualifier.
