# GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

## Type

Transport bundle / IDE handoff / doc-ops index refresh.

## Target

`TARGET_GLOBAL_INDEX_PARENT_PRODUCT_ONLY_01`

## Master target

`MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01`

## Objet

Préparer le transport d'exécution pour mettre à jour les index globaux afin qu'ils reflètent l'état actuel uniquement au niveau des chantiers parents avec produit fini utilisable ou produit cible utilisable.

## Principe

Ce bundle ne contient pas encore de patch applicatif final, parce que la réécriture des index doit être produite après lecture locale du repo réel et validation des entrées.

Il transporte :

- le contexte canonique ;
- le target ;
- la règle de classification ;
- le prompt IDE ;
- la checklist ;
- les sorties attendues ;
- le protocole de génération du `.patch` canonique.

## Surfaces cibles

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`
- `docs/index/GO_CLOSED_INDEX.md` si déplacement nécessaire
- `bundles/BUNDLE_TARGET_INDEX.md` si le suivi bundle/target doit être rafraîchi

## Hors scope

- runtime ;
- cleanup branches ;
- modification de `BRANCH_STATE.md` sauf note de stale/recount si strictement nécessaire ;
- ajout de micro-GO dans les index globaux ;
- modification produit non documentaire.

## Règle transport

Le patch final devra être généré par l'IDE après validation locale :

`bundles/GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01/patches/<YYYYMMDD>_GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01_global_index_parent_product_refresh.patch`

Aucun `.patch` racine ne doit être committé.
