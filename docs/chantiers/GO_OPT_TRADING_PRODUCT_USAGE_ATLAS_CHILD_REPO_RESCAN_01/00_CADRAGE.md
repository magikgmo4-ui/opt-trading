---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/90_CLOSEOUT.md
  - docs/product/PROJECT_PRESENTATION.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/PRODUCT_USAGE_GRAPH.mmd
---

# 00_CADRAGE - GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01

## 1_MASTER_TARGET

Rescanner la couche Product Usage Atlas apres les mergees posterieures au 2026-05-07 afin de rattraper uniquement les deltas produits prouvables dans le repo reel.

## 2_INITIAL_PROJECT_DOC

Ce fichier ouvre un child de refresh cible.

Le parent, l'inventaire repo et le child d'application sont deja `PASS`. Le besoin ici n'est pas de rejouer tout l'inventaire, mais de verifier si des preuves nouvelles imposent un patch doc-only de `docs/product/*`.

## 3_INITIAL_NEED

Le clean clone `origin/sot/mainline` contient deja :

- le parent Product Usage Atlas ;
- le child `REPO_INVENTORY_01` ;
- le child `APPLY_REPO_INVENTORY_01`.

En revanche, les fichiers `docs/product/*` sont encore dates du `2026-05-07` alors que plusieurs closeouts ulterieurs ont modifie la preuve disponible sur certaines surfaces.

## 4_MASTER_PROJECT_PLAN

1. Repartir du clean clone et ignorer le repo local corrompu.
2. Relire l'etat courant de `docs/product/*`.
3. Scanner seulement les preuves posterieures au `2026-05-07` qui peuvent changer une lecture produit.
4. Promouvoir ou rafraichir uniquement les surfaces prouvees.
5. Fermer avec un closeout doc-only et sans changement runtime.

## 6_FINAL_TARGET

Produire une mise a jour prudente de la couche produit avec :

- une presentation projet synchronisee avec l'Atlas reel ;
- au moins une reevaluation post-inventaire si la preuve est suffisante ;
- des `NEXT_GO` et gaps moins perimes pour les surfaces touchees.

## 7_CANONICAL_STATE

- `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01` = `PASS`.
- `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_APPLY_REPO_INVENTORY_01` = `PASS`.
- L'Atlas suit deja 13 produits.
- `Deepseek Student` etait reste `KEEP_CANDIDATE` dans l'inventaire initial.
- `Bot Vision` et `derivatives_collector` disposent maintenant de preuves plus recentes que la couche produit n'a pas encore reprises.
- Le clean clone sain de travail est : `/home/fantome/opt-trading-clean`.

## 8_VALIDATED_PLAN

Plan valide pour ce child :

1. ne pas relancer un inventaire complet ;
2. ne pas promouvoir les surfaces encore ambigues (`PERF`, `marketdata`, `Simex`, etc.) ;
3. ajouter seulement les deltas qui ont une preuve repo plus forte que le lot du `2026-05-07`.

## 11_KEY_DECISIONS

- Le repo corrompu historique reste hors scope.
- Le child courant travaille uniquement depuis le clean clone.
- `Deepseek Student` peut etre requalifie seulement s'il reste `USABLE_LIMITED` et explicitement non autonome.
- `Bot Vision` et `derivatives_collector` peuvent etre rafraichis sans changer leur bucket.
- `PERF` reste hors Atlas dans ce lot, faute de preuve produit assez stable et assez lisible pour un operateur.

## 12_INVARIANTS

- Doc-only uniquement.
- Aucun runtime modifie.
- Aucun secret.
- Aucun bucket nouveau.
- Aucune promotion directe vers `USABLE_NOW` sans preuve operatoire nette.
- Aucun guide live ajoute pour une surface non validee.
- Le repo reste la source canonique ; l'Atlas reste une couche de lecture.

## 13_ESTABLISHED

- `/home/fantome/opt-trading-clean` est sain et sur `sot/mainline`.
- Les enfants `REPO_INVENTORY_01` et `APPLY_REPO_INVENTORY_01` sont deja merges.
- Les deltas post-`2026-05-07` sont reels, mais cibles.

## 15_REMAINING_GAP

- `PROJECT_PRESENTATION.md` ne reflete pas encore tout l'Atlas deja applique.
- `Deepseek Student` n'apparait pas encore dans l'Atlas malgre des preuves supplementaires.
- `Bot Vision` et `derivatives_collector` portent encore des gaps / `NEXT_GO` plus anciens que les closeouts recents.

## 16_TODO

1. Creer `01_DELTA_SCAN.md`.
2. Creer `02_ATLAS_PATCH.md`.
3. Mettre a jour `docs/product/PROJECT_PRESENTATION.md`.
4. Mettre a jour `docs/product/PRODUCT_USAGE_MATRIX.md`.
5. Mettre a jour `docs/product/PRODUCT_USAGE_ATLAS.md`.
6. Mettre a jour `docs/product/FINAL_TARGET_GAPS.md`.
7. Mettre a jour `docs/product/PRODUCT_USAGE_GRAPH.mmd`.
8. Creer `90_CLOSEOUT.md` et l'entree inbox associee.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01/01_DELTA_SCAN.md
```

Puis appliquer les deltas valides dans :

```text
docs/product/PROJECT_PRESENTATION.md
docs/product/PRODUCT_USAGE_MATRIX.md
docs/product/PRODUCT_USAGE_ATLAS.md
docs/product/FINAL_TARGET_GAPS.md
docs/product/PRODUCT_USAGE_GRAPH.mmd
```
