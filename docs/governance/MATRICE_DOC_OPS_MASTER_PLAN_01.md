---
doc_id: OPT_TRADING_MATRICE_DOC_OPS_MASTER_PLAN_01
doc_type: governance_master_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - matrice_doc_ops
  - governance
  - master_plan
  - continuity
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md
point_de_reprise: "Section 17. RESUME_POINT"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/DOC_LAYERS.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md
---

# MATRICE_DOC_OPS_MASTER_PLAN_01

## 1. Objet

Ancrer comme document canonique le plan complet du chantier parent `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`.

Ce document n'est pas encore la matrice maître finale.
Il fixe :
- la vraie cible
- les blocs obligatoires
- les décisions de lecture
- le gap restant
- la forme correcte du livrable final

Il doit empêcher que le prochain lot reparte d'une synthèse latérale au lieu d'une matrice gouvernante unique.

---

## 2. MASTER_TARGET

La matrice maître doit empêcher qu'on perde :
- le pourquoi produit
- le plan macro validé
- les plans de travail rattachés aux GO
- la lecture parent / sous-GO / GO simple
- le statut Git réel
- la suite logique globale

Même si des lots techniques s'enchaînent.

---

## 3. Cible de sortie du parent

Le parent `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` doit produire à terme une surface unique, gouvernante et opposable.

Cette surface unique devra :
- repartir du produit
- descendre vers le parent
- descendre ensuite vers le GO
- ne traiter Git qu'après la structure documentaire et produit

Le livrable final visé n'est donc pas :
- une nouvelle synthèse latérale
- un audit additionnel isolé
- une collection de notes parallèles

Le livrable final visé est :
- une matrice maîtresse unique, crossée avec l'existant réel du repo

---

## 4. MASTER_PROJECT_PLAN

La matrice unique à construire doit fusionner au minimum 6 blocs.

### Bloc A - Continuité produit globale

Cette partie doit garder visible :
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`
- `plan_macro_valide`
- `jalons_clos`
- `etat_global_courant`
- `gap_global_restant`
- `suite_logique`

### Bloc B - Produits / groupes / familles

Le projet global doit rester lu comme :

Centres de gravité produit :
- Desk Pro
- Trading Dual Stack V1
- Bot Vision

Familles de soutien :
- webhook
- perf
- quant
- collectors
- LocalCMS
- openclaw / agents / prompt factory
- satellites machines

### Bloc C - Plans de travail / chantiers / GO

La matrice doit dire clairement :
- parent prouvé ou GO simple
- sous-GO prouvé ou non
- objectif local
- cible locale
- rattachement au parent
- effet attendu sur la trajectoire produit
- propagation à la fermeture

La doc actuelle porte déjà beaucoup de règles, mais elles sont dispersées entre :
- `docs/index/GO_INDEX.md`
- `docs/index/REPRISE.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/governance/SESSION_DOCUMENTATION_GATE.md`
- la gouvernance branches

### Bloc D - Nommage + frontmatter

La matrice maître doit intégrer explicitement :
- la règle de nommage `GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`
- le rôle structurel réel de `PARENT` / `CHILD`
- le noyau frontmatter
- le frontmatter enrichi pour parent / sous-GO
- l'alignement entre :
  - nom du GO
  - frontmatter
  - ligne `GO_INDEX`
  - branche
  - structure réelle

### Bloc E - Placement / indexation / surfaces

La matrice doit gouverner :
- où vit chaque objet
- quelle indexation minimale il doit avoir
- la frontière entre :
  - `docs/governance/`
  - `docs/architecture/`
  - `docs/index/`
  - `docs/chantiers/`
  - `registry/*`
  - `journal*`
  - la racine repo

### Bloc F - GO ↔ branches ↔ ouverture / fermeture

C'est un manque réel actuel.

La matrice unique doit trancher :
- parent sur trunk ou branche dédiée
- sous-GO sur branche parent ou branche enfant
- quand une branche enfant est autorisée
- comment fermer un sous-GO sans fermer le parent
- comment fermer le parent et la branche

La synthèse d'archive dit explicitement que cette matrice unique manque encore.

---

## 5. Recroisement canonique minimal

Le présent plan s'appuie d'abord sur les surfaces canoniques déjà publiées :
- `docs/governance/MATRICE_GOUVERNANTE_V2.md`
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`
- `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`
- `docs/governance/SESSION_DOCUMENTATION_GATE.md`
- `docs/governance/DOC_LAYERS.md`
- `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`
- `docs/index/BRANCH_STATE.md`
- `docs/architecture/REPO_SURFACES_MAP.md`

Des surfaces locales de nommage existent aussi, mais elles ne doivent pas concurrencer le canon publié tant qu'elles ne sont pas promues proprement.

---

## 6. Lecture de construction retenue

La bonne méthode de construction est :
1. repartir du produit global
2. figer les centres de gravité et familles
3. rattacher les parents / sous-GO / GO simples à la trajectoire produit
4. fixer ensuite nommage et frontmatter
5. fixer ensuite placement / indexation / surfaces
6. trancher enfin la doctrine Git du flux

Interdit :
- partir de la branche pour reconstruire le chantier
- partir du tag pour reconstruire la structure
- partir d'un index opératoire pour remplacer la gouvernance maître

---

## 7. Hiérarchie cible

La matrice maître finale devra rendre explicite la hiérarchie suivante :
- canon maître
- canon stable annexe
- dérivé
- opératoire

Lecture attendue :
- le canon maître gouverne
- les annexes stabilisent ou explicitent
- les dérivés recroisent sans devenir souverains
- l'opératoire aide à agir sans remplacer le canon

---

## 8. Livrable final attendu

La forme correcte du prochain livrable final est :
- une matrice maître unique
- pas une nouvelle synthèse latérale

Cette matrice maître devra contenir :
- Partie 1 : autorité / couches / hiérarchie
- Partie 2 : continuité produit globale
- Partie 3 : parent / sous-GO / GO simple
- Partie 4 : plans de travail et rattachement des chantiers
- Partie 5 : nommage canonique
- Partie 6 : frontmatter noyau + enrichi
- Partie 7 : placement / indexation / docs vs registry
- Partie 8 : trunk / branche parent / branche enfant / exceptions
- Partie 9 : ouverture / fermeture / propagation / closeout
- Partie 10 : invariants / interdits / conditions de réouverture

---

## 9. SELECTED_SOLUTION

La lecture correcte de l'existant est :
- la matrice V2 promue = socle
- la doctrine de dérivation = sous-couche
- la matrice maître finale = fusion gouvernante de toutes les dimensions utiles

La solution retenue n'est donc pas :
- refaire un audit isolé
- réécrire une synthèse produit seule
- réécrire une doctrine Git seule

La solution retenue est :
- produire une seule matrice maître unique
- l'ancrer comme référence canonique à respecter ensuite

---

## 10. KEY_DECISIONS

Les décisions de lecture retenues sont :
- chaque synthèse passée a apporté une pièce manquante
- aucune synthèse passée n'était la matrice finale
- la PR 154 a seulement ancré un socle
- la prochaine vraie cible est bien une matrice gouvernante unique, maîtresse, recroisée avec l'existant réel du repo

Conséquence :
- aucune surface actuelle ne suffit seule
- le parent `MATRICE_DOC_OPS` existe pour fusionner proprement sans casser le canon existant

---

## 11. REMAINING_GAP

Ce qui manque encore pour atteindre la vraie cible :
- une surface unique qui rassemble dans un seul document gouvernant :
  - produit global
  - plans de travail
  - rattachement des GO
  - nommage
  - frontmatter
  - indexation
  - branches
  - règles d'ouverture / fermeture
  - propagation / reprise
- une hiérarchie claire entre :
  - ce qui est canon maître
  - ce qui est annexe
  - ce qui est dérivé
  - ce qui est opératoire
- une lecture qui permette de repartir du produit, puis du parent, puis du GO, puis du Git

---

## 12. Garde de construction

Pendant la construction de la matrice maître :
- ne pas ouvrir une taxonomie parallèle
- ne pas inventer un parent non prouvé
- ne pas faire de `REPRISE.md` une source souveraine
- ne pas faire de `BRANCH_STATE.md` une doctrine complète à lui seul
- ne pas laisser les surfaces locales de naming redéfinir le canon sans promotion explicite
- ne pas faire précéder la structure par les tags, les dérivés ou Git

---

## 13. Conditions de validité du parent

Le parent `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` sera sur la bonne trajectoire si :
- il garde une seule cible finale
- il recroise le canon déjà publié avant d'ajouter de nouvelles règles
- il n'ouvre pas de sous-GO artificiel avant d'avoir posé l'ossature maître
- il produit un document final réellement gouvernant, pas une synthèse latérale de plus

Le parent dérive si :
- il ouvre trop tôt des sous-lots techniques
- il tente de corriger le repo entier avant de fixer la matrice maître
- il substitue l'opératoire au canon

---

## 14. TODO

Le prochain geste juste est :
1. repartir de tout ce qui a été synthétisé
2. recroiser avec l'existant réel du repo
3. produire un seul document maître
4. faire de ce document la référence à respecter à l'avenir

Dans le présent passage, seule l'ancre de plan complète est posée.

---

## 15. Effet attendu sur la trajectoire produit

Le parent `MATRICE_DOC_OPS` doit empêcher la perte de lecture globale quand le repo enchaîne :
- des lots techniques
- des lots d'indexation
- des lots Git
- des lots de normalisation documentaire

Effet attendu :
- la trajectoire produit reste lisible
- les GO restent rattachés à une logique plus haute
- Git reste une couche de support et non l'origine de la lecture

---

## 16. Point de sortie prévu

Le point de sortie correct du parent n'est pas :
- un closeout de synthèse
- un bundle latéral
- une simple collection d'ajustements d'index

Le point de sortie correct est :
- une matrice maître unique, publiée comme surface canonique gouvernante

---

## 17. RESUME_POINT

La matrice maître visée est bien :
- unique
- gouvernante
- complète
- orientée produit d'abord

Les synthèses précédentes restent des entrées.
La matrice V2 reste le socle.
La doctrine de dérivation reste la sous-couche.

Mais l'objectif final demeure :
- une matrice unique qui évite qu'on reperde le produit
- une matrice unique qui évite qu'on reperde les chantiers
- une matrice unique qui évite qu'on reperde le nommage
- une matrice unique qui évite qu'on reperde les branches
- une matrice unique qui évite qu'on reperde la suite logique
