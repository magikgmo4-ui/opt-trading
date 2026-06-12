# Mapping d'execution sur db-layer

## Relation LocalCMS <-> db-layer
- `db-layer` est la machine d'execution reelle des surfaces `LocalCMS` relues dans ce cycle.
- `LocalCMS` reste un sujet projet/UI.
- La relation a conserver est :
  - `opt-trading` = producer canonique
  - `localcms` = consumer UI
  - `db-layer` = hote d'execution reel

## Chemins connus documentes
- Depot `LocalCMS` present sur `db-layer` : `/home/ghost/localcms`
- Runtime associe present : `/home/ghost/localcms_runtime`
- Surfaces opt-trading liees a la consommation UI sur `db-layer` :
  - `/opt/trading/docs/ui_indexation`
  - `/opt/trading/docs/ui_screenshots`
  - `/opt/trading/modules/ui_registry_msi`

## Ce qui releve de db-layer
- l'hebergement reel des repertoires de travail / runtime `LocalCMS`
- les surfaces machine/documentation qui prouvent l'execution locale
- le statut machine et les prerequis d'acces

## Ce qui releve de LocalCMS consumer
- la qualification des UI `producer-only` / `consumer-compatible` / `adapter` / `excluded`
- les contrats d'exposition documentes
- l'ordre d'adoption :
  - viewers read-only
  - dashboards / reporting
  - admin leger
  - consoles hybrides
  - exclusions runtime explicites

## Ce que `opt-trading` produit pour `localcms` si documente
- formats de contrat cibles deja poses dans le parent :
  - build exporte
  - manifest + assets
  - fragment HTML
  - JSON de config / schema UI
  - API + renderer cote `localcms`
  - proxy / embed / viewer

## Limites
- Aucun contrat n'est implemente ou rejoue ici.
- Aucun runtime `LocalCMS` n'est modifie.
- `db-layer` ne devient pas le parent projet `LocalCMS`.

## RISKS

- À qualifier.
