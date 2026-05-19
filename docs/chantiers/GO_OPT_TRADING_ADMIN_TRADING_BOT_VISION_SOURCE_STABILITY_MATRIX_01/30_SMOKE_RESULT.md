# 30_SMOKE_RESULT

Verdict : `PASS_SOURCE_STABILITY_MATRIX`

## Captures retenues

| Page | URL | status | visual_status | png_created | ingestion | extraction | human_readability |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | `https://www.tradingview.com/chart/?symbol=BTCUSDT.P` | `ready` | `pass` | oui (`173186 B`) | oui (`vision_processed`) | oui (`vision_outbox`, OCR bruité mais utile) | oui |
| XAU | `https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD` | `ready` | `pass` | oui (`179245 B`) | oui (`vision_processed`) | oui (`vision_outbox`, OCR bruité mais utile) | oui |
| BTC flow | `https://www.coinglass.com/LiquidationData?coin=BTC` | `ready` | `pass` | oui (`333592 B`) | oui (`vision_processed`) | oui (`vision_outbox`) | oui |

## Résultats détaillés

### BTC TradingView

- sidecar : `status=ready`, `visual_status=pass`
- DOM text observé : `Bitcoin / TetherUS PERPETUAL CONTRACT`, OHLC, watchlist, indices
- variantes fallback validées : `BINANCE:BTCUSDT`, `BINANCE:BTCUSDTPERP`, `BYBIT:BTCUSDT.P`

### XAU TradingView

- sidecar : `status=ready`, `visual_status=pass`
- DOM text observé : `Gold Spot / U.S. Dollar`, OANDA, OHLC, watchlist

### Coinglass flow

- route retenue : `LiquidationData?coin=BTC`
- sidecar : `status=ready`, `visual_status=pass`
- OCR outbox présent
- route root `LiquidationHeatMap?coin=BTC` rejetée car elle rendait une page `/404`

## Extraits d’extraction

### BTC

```text
Bitcoin / TetherUS PERPETUAL CONTRACT - 1D - Binance
O 76,963.2 H 77,384.6 L 76,451.3 C 76,992.6
```

### XAU

```text
Gold Spot / U.S. Dollar - 1D OANDA
O 4,570.260 H 4,589.580 L 4,525.680
```

### Coinglass

```text
24h Volume
Open Interest
24h Liquidation
Liquidation Data
```
