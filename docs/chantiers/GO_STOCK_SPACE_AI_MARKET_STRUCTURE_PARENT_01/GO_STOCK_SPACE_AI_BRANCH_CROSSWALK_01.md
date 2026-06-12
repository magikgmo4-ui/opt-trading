# GO_STOCK_SPACE_AI_BRANCH_CROSSWALK_01

## 1_MASTER_TARGET

Recroiser uniquement les deux branches :
- go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01
- go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01

## 7_CANONICAL_STATE

AI_SPACE_WATCHLIST porte le dataset canonique IA + spatial + défense.
MARKET_STRUCTURE porte la thèse sectorielle SpaceX / effets indirects / structure de marché.

## 13_ESTABLISHED

LUNR est déjà présent dans AI_SPACE_WATCHLIST.
LUNR manque dans MARKET_STRUCTURE.
FLY est présent dans MARKET_STRUCTURE mais absent du dataset watchlist V1.

## 16_TODO

- Ajouter LUNR à MARKET_STRUCTURE.
- Décider si FLY doit être intégré à AI_SPACE_WATCHLIST.
- Garder les index globaux inchangés.

## RISKS

- À qualifier.
