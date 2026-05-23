# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_DOC_OPS_CHILD_GLOBAL_INDEX_PARENT_PRODUCT_REFRESH_01

## Objectif

Réécrire les index globaux en mode parent-product-only — les index ne doivent contenir que des parents avec produit utilisable ou cible produit claire.

## Classification

Chaque entrée classée selon :
- `KEEP_PARENT_PRODUCT` — parent actif avec produit utilisable
- `MOVE_TO_CLOSED` — chantier terminé/PASS
- `DROP_FROM_GLOBAL_INDEX` — enfant, micro-GO, artefact support

## Cibles

- `GO_INDEX.md` → parent-product-only table (9 parents + 3 hors-pilotage)
- `ACTIVE_STREAMS.md` → parents vivants uniquement
- `NEXT_GO_CANDIDATES.md` → 1 parent → 1 target/next GO
- `REPRISE.md` → reprise courte et opératoire
- `GO_CLOSED_INDEX.md` → déplacement des COMPLETE entries
- `BUNDLE_TARGET_INDEX.md` → refresh bundle target

## Target

`TARGET_GLOBAL_INDEX_PARENT_PRODUCT_ONLY_01`

## Master target

`MASTER_TARGET_CONTINUITY_INDEX_CLEAN_PARENT_PRODUCT_STATE_01`
