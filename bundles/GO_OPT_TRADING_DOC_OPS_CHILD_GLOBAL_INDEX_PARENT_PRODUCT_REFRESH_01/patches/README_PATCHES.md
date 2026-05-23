# README_PATCHES — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

## État

Ce transport ne contient pas encore de patch applicatif final.

## Raison

La réécriture des index globaux doit être produite après lecture locale du repo réel, parce que les index doivent refléter l'état courant exact de `sot/mainline`.

## Patch attendu

Après modification et validation locale, générer :

```text
bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/<YYYYMMDD>_GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01_global_index_parent_product_refresh.patch
```

## Commande suggérée

```bash
mkdir -p bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches
git diff -- docs/index bundles/BUNDLE_TARGET_INDEX.md docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01 bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01 > bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/$(date +%Y%m%d)_GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01_global_index_parent_product_refresh.patch
```

## Interdits

- ne pas committer de `.patch` à la racine ;
- ne pas appliquer un patch sans `git apply --check` ;
- ne pas inclure runtime ;
- ne pas faire de cleanup branches dans ce GO.
