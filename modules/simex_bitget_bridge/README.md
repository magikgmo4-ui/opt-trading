# SimEx Bitget Bridge

Module durable pour le runner SimEx Bitget.

## Contrat runtime

### Contrat d'unités canonique (`SIMEX_UNITS_V1`)

Variables d'environnement explicites :

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

### Compat legacy conservée

Aliases encore acceptés :

- `SIMEX_GRANULARITY` -> `SIMEX_GRANULARITY_SEC`
- `SIMEX_TOL` -> `SIMEX_TOL_PRICE_ABS`

## Sémantique minimale

- `*_SEC` : secondes
- `*_PRICE_ABS` : delta absolu de prix
- `SIMEX_QTY_UNITS` : quantité scalaire transmise à Perf
- `SIMEX_RISK_USD` : risque nominal USD transmis à Perf

## Entry points

- `cmd.sh`
- `menu.sh`
- `sanity.sh`
- `app/simex_bitget_bridge.py`

## Compatibilité

Les wrappers opérateur historiques sous `scripts/` et le shim `bitget_bridge.py` restent disponibles.
