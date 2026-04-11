# SimEx presets (Bitget bridge -> Perf)

## Prérequis
- Perf up : `cmd-simex perf-start` (dev) ou service runtime
- Vérif : `cmd-simex sanity`

## Presets

### XAUUSDT — 5m (default)
```bash
cmd-simex bitget-run
```

### BTCUSDT — 5m (tol absolue 0.6)
```bash
SIMEX_SYMBOL=BTCUSDT SIMEX_TOL_PRICE_ABS=0.6 cmd-simex bitget-run
```

### XAUUSDT — 15m
```bash
SIMEX_GRANULARITY_SEC=900 SIMEX_LIMIT=5 cmd-simex bitget-run
```

### Contrat risque / offsets explicites
```bash
SIMEX_STOP_OFFSET_PRICE_ABS=5.0 \
SIMEX_TARGET_OFFSET_PRICE_ABS=2.0 \
SIMEX_QTY_UNITS=0.1 \
SIMEX_RISK_USD=0.5 \
cmd-simex bitget-run
```

### Engine tag explicite
```bash
SIMEX_ENGINE="SIMEX_BITGET_PILOT" cmd-simex bitget-run
```

## Variables ENV

### Canonique (`SIMEX_UNITS_V1`)
- `SIMEX_SYMBOL` (ex: XAUUSDT, BTCUSDT)
- `SIMEX_PRODUCT_TYPE` (default `USDT-FUTURES`)
- `SIMEX_GRANULARITY_SEC` (seconds: 60, 300, 900, 3600...)
- `SIMEX_LIMIT` (candles count; default 3)
- `SIMEX_TOL_PRICE_ABS` (float; delta absolu de prix)
- `SIMEX_STOP_OFFSET_PRICE_ABS` (float; delta absolu de prix)
- `SIMEX_TARGET_OFFSET_PRICE_ABS` (float; delta absolu de prix)
- `SIMEX_QTY_UNITS` (float; quantité scalaire transmise à Perf)
- `SIMEX_RISK_USD` (float; risque nominal USD)
- `SIMEX_PERF_EVENT` (default `http://127.0.0.1:8010/perf/event`)
- `SIMEX_ENGINE` (default `BITGET_SM_LITE`)

### Compat legacy
- `SIMEX_GRANULARITY` -> alias de `SIMEX_GRANULARITY_SEC`
- `SIMEX_TOL` -> alias de `SIMEX_TOL_PRICE_ABS`

## Observabilité
- Perf UI: http://127.0.0.1:8010/perf/ui
- Trades:
```bash
curl -fsS "http://127.0.0.1:8010/perf/trades?limit=50" | head
```
