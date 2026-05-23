---
doc_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01
parent_go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: open
lifecycle_stage: governance_alignment
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - product_final_surface
  - master_target
  - master_project_plan
  - gap_remediation
---

# GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01

## 1_MASTER_TARGET

Registre des produits/surfaces finales remédié, lisible et utilisable pour rattacher chaque parent produit à un `PF_*`, à un `1_MASTER_TARGET` et à un `4_MASTER_PROJECT_PLAN` avant fermeture.

## 2_INITIAL_PROJECT_DOC

Ce document transporte le plan initial validé pour la remédiation des surfaces finales.

## 3_INITIAL_NEED

Le canon produit était encore trop étroit ou ambigu. Il distinguait insuffisamment les produits finaux utilisables, les chaînes produit complètes, les surfaces opérables, les supports critiques et les surfaces de gouvernance/transport.

## 4_MASTER_PROJECT_PLAN

1. Mettre à jour `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` avec les surfaces finales validées.
2. Ajouter `PF_DATA_CENTER` comme produit transverse de normalisation data.
3. Distinguer `PF_TELEGRAM_SCREENER` et `PF_TELEGRAM_INGESTION`.
4. Clarifier `PF_OPENCLAW_ORCHESTRATOR_FULL` et `PF_OPERATOR_RUNTIME`.
5. Renommer ou préciser `PF_STRATEGY_FRAMEWORK_REGISTRY`.
6. Clarifier les supports critiques non promus automatiquement.
7. Rappeler la chaîne `PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> 6_FINAL_TARGET -> BUNDLE_TARGET -> GO_ID`.
8. Archiver un bundle et un `.patch` canonique.

## 6_FINAL_TARGET

Appliquer la remédiation documentaire validée au registre produit/surface, sans fermer de parent et sans modifier les index globaux sauf entrée inbox atomique.

## 8_VALIDATED_PLAN

Plan validé par l'utilisateur comme `matrix_plan_target` de `master_plan_target`.

## 12_INVARIANTS

- Un `PF_*` est une surface ou chaîne finale utilisable/testable.
- Un `1_MASTER_TARGET` doit viser un produit final utilisable.
- Un `4_MASTER_PROJECT_PLAN` est requis pour fermer un parent.
- Un `BUNDLE_TARGET` ne ferme jamais un parent.
- Une PR, un patch, un bundle ou un commit ne prouvent pas que le produit final est atteint.
- Les supports critiques restent des dépendances ou surfaces de plan, sauf promotion explicite.

## 16_TODO

- Créer la PR de remédiation.
- Vérifier le diff du registre.
- Archiver le `.patch` canonique sous le bundle.
- Merger uniquement si le registre reste cohérent et sans fermeture parent.

## 17_RESUME_POINT

Reprendre depuis `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` et vérifier que chaque surface finale promue dispose d'un `PF_*`, d'un rattachement master target et d'un usage vérifiable.
