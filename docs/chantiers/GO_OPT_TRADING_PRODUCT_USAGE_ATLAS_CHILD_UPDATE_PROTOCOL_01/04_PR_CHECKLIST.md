---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01_PR_CHECKLIST
doc_type: pr_checklist
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01
status: draft_for_review
lifecycle_stage: child_pr_checklist
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - pr
  - checklist
  - maintenance
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/04_PR_CHECKLIST.md
point_de_reprise: "Checklist actionnable après chaque PR significative pour maintenir les couches produit."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/01_UPDATE_MATRIX_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/02_STATUS_PROMOTION_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# 04_PR_CHECKLIST

## 1_OBJECTIF

Checklist actionnable à exécuter après chaque PR mergée qui impacte un produit de l'Atlas. Cette checklist est conçue pour pouvoir être exécutée par un opérateur humain ou par un agent (OpenClaw) sous supervision.

## 2_DECISION_TREE — La PR nécessite-t-elle une maintenance ?

```text
Étape 0 — DÉTECTION
La PR mergée modifie-t-elle au moins un de ces éléments ?
  □ Un fichier dans docs/chantiers/GO_OPT_TRADING_*
  □ Un module dans modules/
  □ Un script dans scripts/
  □ Un package dans packages/
  □ Un fichier de config ou registry
  □ Un guide dans docs/product/guides/
  □ Un fichier de preuve (log, test, capture)

Si NON → pas de maintenance produit requise. Stop.
Si OUI → continuer à l'étape 1.
```

## 3_CHECKLIST — 8 étapes

### Étape 1 — LIRE LE CLOSEOUT

```text
□ Lire le closeout du chantier (90_CLOSEOUT.md ou équivalent).
□ Identifier le verdict (PASS / PATCH_REQUIRED / FAIL).
□ Noter le GO_ID, le produit cible, le bucket avant/après.
□ Vérifier la présence d'une section remaining_gaps.
□ Vérifier la présence d'un NEXT_GO.
```

### Étape 2 — IDENTIFIER LES PRODUITS AFFECTÉS

```text
□ Lister les produits impactés par la PR.
□ Pour chaque produit :
  □ Vérifier s'il est déjà dans l'Atlas.
  □ S'il est nouveau → classification + décision ADD_TO_ATLAS / KEEP_CANDIDATE / DO_NOT_PROMOTE.
  □ S'il existe déjà → recalculer son bucket et sous-type.
```

### Étape 3 — RECALCULER LE BUCKET

```text
□ Appliquer la précédence prudente :
    FORBIDDEN_LIVE > SIMULATED_ONLY > DOC_ONLY > USABLE_LIMITED > USABLE_NOW

□ Pour chaque produit affecté :
  □ Déterminer si le produit a des preuves d'usage réel.
  □ Déterminer si le produit a des tests simulés PASS.
  □ Déterminer si le produit a une documentation complète.
  □ Déterminer si le produit a un flag FORBIDDEN_LIVE.

□ Attribuer le bucket le plus prudent applicable.
□ Attribuer le sous-type (référence, implémentation, backtest, contraint, etc.).
```

### Étape 4 — METTRE À JOUR PRODUCT_USAGE_MATRIX.md

```text
□ Mettre à jour la ligne du produit (ou l'ajouter).
□ Vérifier la colonne bucket.
□ Vérifier la colonne usage_mode.
□ Vérifier la colonne user_guide.
□ Vérifier la colonne next_go.
□ Commiter avec : "docs: update PRODUCT_USAGE_MATRIX after PR #NNN"
```

### Étape 5 — METTRE À JOUR PRODUCT_USAGE_ATLAS.md

```text
□ Si le produit est nouveau → créer sa fiche complète.
□ Si le produit existe → mettre à jour les champs modifiés :
  □ current_state
  □ usable_now
  □ usage_mode
  □ remaining_gaps (ajouter/retirer)
  □ next_go
  □ do_not_use_notes (si applicable)
□ Vérifier que canonical_sources pointe vers des fichiers existants.
□ Commiter avec : "docs: update PRODUCT_USAGE_ATLAS after PR #NNN"
```

### Étape 6 — METTRE À JOUR FINAL_TARGET_GAPS.md

```text
□ Pour chaque gap fermé par cette PR → marquer CLOSED.
□ Pour chaque nouveau gap → ajouter avec :
  □ description
  □ sévérité (BLOCKING / MAJOR / MINOR)
  □ NEXT_GO
□ Commiter avec : "docs: update FINAL_TARGET_GAPS after PR #NNN"
```

### Étape 7 — METTRE À JOUR LE GUIDE (si applicable)

```text
□ Si le mode d'usage a changé → mettre à jour le guide.
□ Si des prérequis ont changé → mettre à jour le guide.
□ Si des limites ont été levées → mettre à jour le guide.
□ Mettre à jour CONTINUITY_STATE et REPRISE_POINT.
□ Commiter avec : "docs: update guide {PRODUIT} after PR #NNN"
```

### Étape 8 — METTRE À JOUR LE GRAPHE (si applicable)

```text
□ Si la topologie a changé → mettre à jour PRODUCT_USAGE_GRAPH.mmd.
□ Vérifier que le graphe compile (mermaid).
□ Commiter avec : "docs: update PRODUCT_USAGE_GRAPH after PR #NNN"
```

## 4_VERIFICATIONS_FINALES

Avant de considérer la maintenance terminée :

```text
□ Vérifier qu'aucune promotion implicite n'a eu lieu (anti-règles A1-A10).
□ Vérifier que la somme des produits par bucket dans MATRIX est cohérente.
□ Vérifier que chaque produit dans l'Atlas a un NEXT_GO (même "none").
□ Vérifier que chaque produit FORBIDDEN_LIVE a un do_not_use_notes.
□ Vérifier que chaque produit DOC_ONLY a un remaining_gap documenté.
□ Vérifier que chaque guide pointe vers sa source canonique.
□ Vérifier que le UPDATE_PROTOCOL.md lui-même n'a pas besoin de mise à jour.
□ Vérifier que le commit message référence la PR source.
```

## 5_CHECKLIST_RAPIDE_POUR_PR_MINEURE

Pour les PRs mineures (fix de typo, ajustement de doc sans changement d'état) :

```text
□ Lire le diff.
□ Confirmer qu'aucun produit ne change d'état.
□ Pas de mise à jour requise.
□ Optionnel : noter dans le closeout "no product state change".
```

## 6_CHECKLIST_POUR_NOUVEAU_PRODUIT

Pour l'ajout d'un nouveau produit dans l'Atlas :

```text
□ Classification initiale (bucket + sous-type).
□ Décision ADD_TO_ATLAS (vs KEEP_CANDIDATE, DO_NOT_PROMOTE).
□ Création de la fiche dans PRODUCT_USAGE_ATLAS.md.
□ Ajout dans PRODUCT_USAGE_MATRIX.md.
□ Ajout des gaps dans FINAL_TARGET_GAPS.md.
□ Création du guide dans docs/product/guides/ (si applicable).
□ Mise à jour de guides/README.md.
□ Mise à jour du PRODUCT_USAGE_GRAPH.mmd (si dépendances).
□ Commits séparés ou groupés selon l'ampleur.
```

## 7_EXEMPLE_COMPLET

Exemple : PR #243 (FORMULAS_SOURCE_LOCK_01) mergée.

```text
Étape 0 : PR modifie docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/ → OUI

Étape 1 : Lire closeout (formulas_source_lock.md §9-10).
         Verdict = PASS. GO_ID = SOURCE_LOCK_01.
         Produit = BTC COIN-M Accumulation Engine.

Étape 2 : Produit affecté = BTC COIN-M. Déjà dans l'Atlas (FORBIDDEN_LIVE).

Étape 3 : Recalcul bucket.
         - flag FORBIDDEN_LIVE toujours actif → FORBIDDEN_LIVE
         - sous-type = FORBIDDEN_LIVE_ACTIVE_DEVELOPMENT
         - pas de changement de bucket (la PR lève les UNKNOWN mais pas le flag LIVE)

Étape 4 : MATRIX → pas de changement de bucket, mais next_go change.
         next_go passe de SOURCE_LOCK_01 à BACKTEST_DATA_PREP_01.

Étape 5 : ATLAS → mettre à jour remaining_gaps (9 UNKNOWN → 0, BACKTEST_DATA_PREP autorisé).
         next_go = BACKTEST_DATA_PREP_01.

Étape 6 : GAPS → retirer "9 UNKNOWN formulas" des gaps BTC COIN-M.
         Ajouter "RUNTIME bloqué (PAPER_LOCKED < API_VERIFIED)".

Étape 7 : Guide → pas de guide pour BTC COIN-M (FORBIDDEN_LIVE).

Étape 8 : GRAPH → pas de changement topologique.

Vérifications finales :
  □ Pas de promotion implicite ✓
  □ Produit reste FORBIDDEN_LIVE ✓
  □ NEXT_GO à jour ✓
```

## 17_RESUME_POINT

```text
Checklist en 8 étapes, exécutable par humain ou agent.
Arbre de décision initial pour filtrer les PRs non concernées.
Variantes pour PR mineure et pour nouveau produit.
Exemple complet fourni (PR #243).
```
