# TARGETS — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

## 1_MASTER_TARGET

`MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01`

Avoir des index globaux lisibles, actuels et exploitables qui reflètent seulement les chantiers parents portant un produit fini utilisable ou un produit cible utilisable.

## 6_FINAL_TARGET

`TARGET_GLOBAL_INDEX_PARENT_PRODUCT_ONLY_01`

Réécrire les index globaux en mode parent-only / product-only.

## Critères de réussite

- `GO_INDEX.md` ne contient plus de micro-GO, enfants techniques, branches, bundles ou références historiques comme entrées actives.
- `ACTIVE_STREAMS.md` contient uniquement les parents vivants avec produit utilisable, gap et prochain target.
- `NEXT_GO_CANDIDATES.md` applique la règle : 1 parent produit -> 1 target ou 1 next GO primaire.
- `REPRISE.md` fournit un point de reprise court : parent produit actif, target courant, prochaine action forte.
- `GO_CLOSED_INDEX.md` reçoit les éléments clos/PASS si déplacement nécessaire.
- Les détails restent dans `docs/chantiers/`, `docs/index/inbox/`, `bundles/`, ou `BRANCH_STATE.md`.
- Aucun runtime modifié.
- Aucun cleanup branches.
- Patch canonique produit et archivé sous `bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/`.
