---
bundle_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
created_at: 2026-05-23
---

# README_BUNDLE — Product surface final registry

## But

Bundle déportable pour appliquer la correction canonique suivante :

- créer `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` ;
- ajouter l’addendum d’alignement matrice ;
- ouvrir le chantier ;
- créer l’entrée inbox ;
- mettre à jour `GO_INDEX`, `NEXT_GO_CANDIDATES`, `ACTIVE_STREAMS`, `REPRISE` ;
- archiver le `.patch` canonique dans `patches/`.

## Application IDE

Depuis la racine du repo :

```bash
git apply --check bundles/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01/patches/20260523_GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01_product_surface_registry.patch
git apply bundles/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01/patches/20260523_GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01_product_surface_registry.patch
```

## Invariant

Le `.patch` est le transport canonique. Un `.zip` peut transporter le bundle, mais ne remplace jamais le contenu source de `bundles/<GO_ID>/`.

## Reprise

Après application : lire `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`, puis ouvrir le NEXT_GO d’audit close gate.
