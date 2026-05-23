---
doc_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
parent_go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: open
lifecycle_stage: governance_alignment
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - governance
  - product_final_surface
  - master_target
  - global_indexes
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Créer le registre canonique des produits/surfaces finales visés par opt-trading et aligner la matrice + les index globaux pour éviter de fermer un chantier sans produit final utilisable.

## 2_INITIAL_NEED

La lecture actuelle du projet est trop étroite si elle ne voit que quelques centres de gravité. La mémoire projet et les chantiers umbrella montrent des surfaces finales additionnelles : Signal Chain Product, Telegram Screener, runtime opérateur distant, OpenClaw/OpenCode operator, LocalCMS cockpit, Strategy/Perf/Lab, Sheets consumer, strict workers, collectors et gouvernance transport.

## 4_MASTER_PROJECT_PLAN

1. Créer `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
2. Aligner `MATRICE_DOC_OPS_MASTER_MATRIX_01.md` pour pointer vers ce registre.
3. Mettre à jour les index globaux : `GO_INDEX`, `NEXT_GO_CANDIDATES`, `ACTIVE_STREAMS`, `REPRISE`.
4. Produire bundle déportable + `.patch` canonique.
5. Garder les surfaces support séparées des produits finaux utilisables.

## 6_FINAL_TARGET

Registre produit/surfaces finales disponible et index globaux alignés sur une lecture où `MASTER_TARGET = produit final utilisable`, non PR, non patch, non bundle.

## 8_VALIDATED_PLAN

Plan validé par l’utilisateur :

```text
oui plan valide, plus alignement matrice + mise a jours index globaux
patch
```

## 11_KEY_DECISIONS

- Les index globaux peuvent être modifiés dans ce lot, exception explicite à la règle locale de non-propagation systématique.
- Le `.patch` est un livrable obligatoire du bundle.
- La correction est subjective et vise à corriger le canon, pas à répéter l’état canonique existant.

## 12_INVARIANTS

- Produit final utilisable ≠ patch.
- Produit final utilisable ≠ bundle.
- Produit final utilisable ≠ PR mergée.
- Surface support ≠ produit final sans décision explicite.
- Les GOs doivent rattacher leur `PRODUCT_OR_SURFACE` à un `PF_*` ou à une surface support identifiée.

## 16_TODO

- Mettre à jour matrice.
- Mettre à jour index globaux.
- Produire bundle + patch.
- Ouvrir PR.

## 17_RESUME_POINT

Reprendre depuis `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`, puis vérifier les entrées globales dans `docs/index/*`.
