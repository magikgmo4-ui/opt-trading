# 02_go_map - GO_OPT_TRADING_PARENT_NAMING_CANON_01

## Parent
- `GO_OPT_TRADING_PARENT_NAMING_CANON_01`

## Sous-chantiers proposes au demarrage
- `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01`
- `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01`

## Sous-chantiers futurs possibles
- `GO_OPT_TRADING_CHILD_NAMING_APPLY_BATCH_01`
- `GO_OPT_TRADING_CHILD_BRANCH_NAMING_REALIGNMENT_01`

## Ordre recommande
1. politique
2. inventaire
3. module audit-only
4. exceptions
5. apply borne si reellement utile

## Invariant
Aucun apply avant l'inventaire reel et la qualification explicite des exceptions.
