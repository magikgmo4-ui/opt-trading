# 03_decisions - GO_OPT_TRADING_PARENT_NAMING_CANON_01

## DECISION_01
Le canon GO du repo prime.

## DECISION_02
La politique transverse par surface est conservee mais reste subordonnee au canon GO.

## DECISION_03
Le chantier demarre en audit-only.

## DECISION_04
Le module durable retenu s'appelle `naming_normalizer`.

## DECISION_05
Le renommage reel de l'existant est hors du parent initial et doit passer par un GO separe.

## DECISION_06
Les trois noms de GO proposes sont conserves apres relecture finale :
- `GO_OPT_TRADING_PARENT_NAMING_CANON_01`
- `GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01`
- `GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01`

## DECISION_07
La granularite regex GO retenue pour l'outillage est :
- `<SCOPE>` = 1 token
- `<PRODUCT_OR_SURFACE>` = 1 a n tokens
- `<ROLE>` = `PARENT` ou `CHILD`
- `<OBJECT>` = 1 a n tokens
- `<NN>` = 2 chiffres minimum

## DECISION_08
Un lot separe reste necessaire avant tout depot repo eventuel.

## RISKS

- À qualifier.
