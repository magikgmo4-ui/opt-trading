# SimEx Bitget Bridge

Module durable pour le runner SimEx Bitget.

## Contrat runtime

Variables d'environnement conservees :

- `SIMEX_SYMBOL`
- `SIMEX_PRODUCT_TYPE`
- `SIMEX_GRANULARITY`
- `SIMEX_LIMIT`
- `SIMEX_TOL`
- `SIMEX_PERF_EVENT`
- `SIMEX_ENGINE`

## Entry points

- `cmd.sh`
- `menu.sh`
- `sanity.sh`
- `app/simex_bitget_bridge.py`

## Compatibilite

Les wrappers operateur historiques sous `scripts/` et le shim `bitget_bridge.py` restent disponibles.
