# marketdata

Facade module minimale pour l'exploration et les wrappers autour de la surface market data.

## Role
- fournir un point d'entree standard `cmd/menu/sanity` pour la surface `marketdata`
- exposer une enveloppe legere de navigation tant que la logique metier reste diffusee ailleurs

## Contenu
- `__init__.py` : module Python minimal
- `scripts/cmd.sh` : commandes generiques `info`, `readme`, `ls`, `grep`, `menu`
- `scripts/menu.sh`, `scripts/install_shortcuts.sh`, `scripts/sanity_check.sh`

## Integration
- surface legerement outillee, sans noyau Python riche dans ce module a ce stade
- a lire avec les collectors et modules de donnees de marche :
  - `collector_binance_spot`
  - `collector_coingecko`
  - `market_scanner`
  - `derivatives_collector`

## Statut
- actif mais leger
- facade de navigation / wrapper plus que centre de gravite fonctionnel

## Notes de consolidation
- a clarifier dans les lots suivants :
  - soit rester module facade de navigation
  - soit etre absorbe par une suite `collectors / market intelligence`
- pas de move physique avant audit des callers et des usages operatoires
