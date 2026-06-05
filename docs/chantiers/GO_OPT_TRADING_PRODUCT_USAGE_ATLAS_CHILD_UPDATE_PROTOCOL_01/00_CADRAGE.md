---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - update-protocol
  - governance
  - maintenance
  - openclaw
  - worker
  - orchestration
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/00_CADRAGE.md
point_de_reprise: "Fixer la méthode de maintenance durable pour tous les produits, apps, workers, OpenClaw, parents et children."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/04_UPDATE_PROTOCOL_AFTER_PR.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
  - docs/product/FINAL_TARGET_GAPS.md
  - docs/product/UPDATE_PROTOCOL.md
  - docs/product/guides/README.md
---

# 00_CADRAGE — UPDATE_PROTOCOL_01

## 1_MASTER_TARGET

Transformer la logique `Product Usage Atlas` + `User Guides` en **protocole durable de maintenance** applicable après chaque PR significative, pour tous les produits, apps, workers, OpenClaw, parents et children.

## 2_INITIAL_PROJECT_DOC

Ce document est le cadrage du child `UPDATE_PROTOCOL_01`.

Règle : aucun runtime, aucun secret, aucune connexion externe. Ce child est purement documentaire et gouvernance.

## 3_INITIAL_NEED

Problème actuel :

```text
PR #237-242 ont construit une couche Product Usage Atlas opérationnelle,
mais la méthode de maintenance future n'est pas encore canonisée.

UPDATE_PROTOCOL.md existe mais reste squelettique (78 lignes).
Il manque :
- le traitement explicite des sous-types DOC_ONLY / SIMULATED_ONLY raffinés par PR #242
- le statut d'OpenClaw / workers / orchestration dans la chaîne canonique
- une checklist actionnable par PR
- des règles anti-promotion implicite
- la distinction DOC_ONLY_REFERENCE vs DOC_ONLY_INITIAL_PROJECT vs DOC_ONLY_IMPLEMENTATION_READY
```

Éléments déjà en place :

```text
- taxonomy produit (01_PRODUCT_STATUS_TAXONOMY.md)
- buckets d'usage (01_USAGE_VIEW.md)
- inventaire repo (REPO_INVENTORY_01)
- 13 produits dans l'Atlas
- guides enrichis avec MASTER_TARGET, IMPLEMENTATION_PATH, CONTINUITY_STATE
- UPDATE_PROTOCOL.md (base 9 étapes)
```

## 4_MASTER_PROJECT_PLAN

1. Lire l'existant : UPDATE_PROTOCOL.md, taxonomy, usage view, guides, atlas, gaps.
2. Documenter les règles de mise à jour de chaque couche (Matrice, Atlas, Gaps, Graph, Guides).
3. Définir tous les sous-types de statut avec leurs conditions de promotion.
4. Traiter OpenClaw / workers / orchestration comme couches de projection, pas sources canoniques.
5. Produire une checklist actionnable après chaque PR.
6. Mettre à jour `UPDATE_PROTOCOL.md` canonique.
7. Produire closeout et verdict PASS.

## 6_FINAL_TARGET

Livrables attendus :

```text
docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/
├── 00_CADRAGE.md                              ← présent document
├── 01_UPDATE_MATRIX_RULES.md                  ← quand et comment mettre à jour chaque couche
├── 02_STATUS_PROMOTION_RULES.md               ← tous les sous-types + conditions de promotion
├── 03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md  ← règles pour les couches externes
├── 04_PR_CHECKLIST.md                         ← checklist actionnable après chaque PR
└── 90_CLOSEOUT.md                             ← closeout + verdict

+ inbox :
  docs/index/inbox/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01.md

+ mise à jour :
  docs/product/UPDATE_PROTOCOL.md
```

## 7_CANONICAL_STATE

```text
Couche Product Usage Atlas construite par séquence :
  PR #237 (PARENT) → PR #238 (USAGE_VIEW) → PR #240 (REPO_INVENTORY)
  → PR #242 (APPLY_REPO_INVENTORY) → PR #242 (USER_GUIDES en cours)

Chaque PR a enrichi la méthode.
UPDATE_PROTOCOL_01 fige la méthode pour tous les prochains changements.
```

## 8_VALIDATED_PLAN

```text
1. Valider 00_CADRAGE.md.
2. Créer 01_UPDATE_MATRIX_RULES.md.
3. Créer 02_STATUS_PROMOTION_RULES.md.
4. Créer 03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md.
5. Créer 04_PR_CHECKLIST.md.
6. Mettre à jour docs/product/UPDATE_PROTOCOL.md.
7. Produire 90_CLOSEOUT.md.
8. Verdict PASS / PATCH_REQUIRED.
```

## 12_INVARIANTS

```text
- Repo = source canonique unique.
- Product Usage Atlas = lecture opérateur, pas source de vérité indépendante.
- OpenClaw = couche de projection/orchestration/agent, pas source canonique.
- Worker = composant d'exécution, pas produit fini sans closeout + preuve.
- Apps externes (ClickUp, Telegram, Airtable) = interfaces d'usage, pas preuves souveraines.
- Ne pas fermer un produit sans NEXT_GO ou condition de reprise.
- Ne pas promouvoir DOC_ONLY ou SIMULATED_ONLY sans preuve d'usage réel.
- Aucun runtime dans ce child.
- Aucun secret dans ce child.
- Tout changement production doit toucher la couche Product Usage Atlas.
```

## 15_REMAINING_GAP

```text
- La méthode ne sera prouvée durable qu'après son application à 3+ PRs futures.
- Les guides des 7 nouveaux produits (NEXT_GO USER_GUIDES_01) devront suivre ce protocole.
- L'audit des 10 modules orphelins devra être intégré dans le flux.
```

## 16_TODO

```text
1. Validation du cadrage.
2. Création des 4 documents de règles.
3. Mise à jour d'UPDATE_PROTOCOL.md canonique.
4. Closeout + verdict.
5. Commit + push + PR.
```

## 17_RESUME_POINT

```text
UPDATE_PROTOCOL_01 = child ouvert pour figer la méthode de maintenance durable.
Tous les futurs changements produit devront suivre ce protocole.
0 runtime, 0 secret, 0 connexion externe.
Prochaine action : validation cadrage → création des règles → closeout.
```

## RISKS

- À qualifier.
