# 10_SCHEMA_SPEC

## Schémas canoniques

| Schéma | Type | Unités | Coverage |
|---|---|---|---|
| `market_metrics.v1` | OHLCV + volume | Quote currency | Spot + Derivatives |
| `oi.v1` | Open Interest | Base currency | Perpetual + Futures |
| `funding.v1` | Funding Rate | % (8h) | Perpetual |
| `liquidations.v1` | Liquidation | Base currency | All |
| `long_short.v1` | Long/Short Ratio | % | Perpetual |
| `signal.v1` | Trading signal | Direction + price | Screener |
| `event.v1` | Trading event | Entry/Exit/PnL | Perf |

## Format canonique

```json
{
  "schema": "string",
  "schema_version": "string",
  "producer": "string",
  "symbol": "string",
  "timestamp": "ISO8601",
  "data": {},
  "coverage": {
    "start": "ISO8601",
    "end": "ISO8601",
    "gap": "string | null"
  }
}
```

## Module structure

```text
modules/data_center/
  schemas/
    __init__.py
    registry.py
    market_metrics_v1.py
    oi_v1.py
    funding_v1.py
    liquidations_v1.py
    long_short_v1.py
    signal_v1.py
    event_v1.py
  tests/
    test_schemas.py
```
