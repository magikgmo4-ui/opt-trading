# SimEx presets (Bitget bridge → Perf)

## Prérequis
- Perf up : `cmd-simex perf-start` (dev) ou service runtime
- Vérif : `cmd-simex sanity`

## Presets

### XAUUSDT — 5m (default)
```bash
cmd-simex bitget-run
```

### BTCUSDT — 5m (tol 0.6)
```bash
SIMEX_SYMBOL=BTCUSDT SIMEX_TOL=0.6 cmd-simex bitget-run
```

### XAUUSDT — 15m
```bash
SIMEX_GRANULARITY=900 SIMEX_LIMIT=5 cmd-simex bitget-run
```

### Engine tag explicite
```bash
SIMEX_ENGINE="SIMEX_BITGET_PILOT" cmd-simex bitget-run
```

## Variables ENV
- `SIMEX_SYMBOL` (ex: XAUUSDT, BTCUSDT)
- `SIMEX_PRODUCT_TYPE` (default `USDT-FUTURES`)
- `SIMEX_GRANULARITY` (seconds: 60, 300, 900, 3600…)
- `SIMEX_LIMIT` (candles count; default 3)
- `SIMEX_TOL` (float; default 0.5)
- `SIMEX_PERF_EVENT` (default `http://127.0.0.1:8010/perf/event`)
- `SIMEX_ENGINE` (default `BITGET_SM_LITE`)

## Observabilité
- Perf UI: http://127.0.0.1:8010/perf/ui
- Trades:
```bash
curl -fsS "http://127.0.0.1:8010/perf/trades?limit=50" | head
```
