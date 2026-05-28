# GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_SANITY_FIX_01

## Goal
Fix `collector_binance_spot.run_sanity()` so it initializes runtime directories without raising `NameError`.

## Scope
- `modules/collector_binance_spot/src/collector_binance_spot/run.py`
- this chantier documentation
- bundle metadata

## Expected Result
`run_sanity()` and `run_collection()` share the same minimal runtime directory initialization path.
