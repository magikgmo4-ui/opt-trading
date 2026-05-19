# SIMEX units contract (`SIMEX_UNITS_V1`)

## Objectif
Rendre explicites les unités manipulées par le bridge SimEx Bitget afin d'éviter les ambiguïtés inter-symboles et de conserver une compatibilité ascendante minimale avec les anciens presets `SIMEX_*`.

## Variables canoniques

- `SIMEX_SYMBOL`
- `SIMEX_PRODUCT_TYPE`
- `SIMEX_GRANULARITY_SEC`
- `SIMEX_LIMIT`
- `SIMEX_TOL_PRICE_ABS`
- `SIMEX_STOP_OFFSET_PRICE_ABS`
- `SIMEX_TARGET_OFFSET_PRICE_ABS`
- `SIMEX_QTY_UNITS`
- `SIMEX_RISK_USD`
- `SIMEX_PERF_EVENT`
- `SIMEX_ENGINE`

## Sémantique

- `SIMEX_GRANULARITY_SEC`
  - unité : secondes
  - exemple : `300` = 5 minutes

- `SIMEX_TOL_PRICE_ABS`
  - unité : delta absolu de prix
  - usage : sweep tolérant `b_low <= a_low + tol`

- `SIMEX_STOP_OFFSET_PRICE_ABS`
  - unité : delta absolu de prix
  - usage : `stop = entry - offset`

- `SIMEX_TARGET_OFFSET_PRICE_ABS`
  - unité : delta absolu de prix
  - usage : `exit = entry + offset`

- `SIMEX_QTY_UNITS`
  - unité : quantité scalaire consommée par Perf
  - note : dans l'état actuel de `perf/perf_app.py`, le PnL est calculé par simple produit `delta_prix * qty`

- `SIMEX_RISK_USD`
  - unité : USD nominaux
  - note : transmis tel quel à Perf pour le calcul du `r_real`

## Compat legacy conservée

- `SIMEX_GRANULARITY` -> alias de `SIMEX_GRANULARITY_SEC`
- `SIMEX_TOL` -> alias de `SIMEX_TOL_PRICE_ABS`

## Non-objectifs de V1

- pas de normalisation instrument-aware par tick size
- pas de conversion lot/contrat
- pas d'inférence automatique par symbole
- pas de refonte du contrat Perf

## Meta runtime

Le bridge joint maintenant au payload SimEx :

- `contract_version = SIMEX_UNITS_V1`
- une section `units`
- une section `normalization`
- une section `legacy_env_bridge`

afin de rendre la sémantique visible côté traces et observabilité.
