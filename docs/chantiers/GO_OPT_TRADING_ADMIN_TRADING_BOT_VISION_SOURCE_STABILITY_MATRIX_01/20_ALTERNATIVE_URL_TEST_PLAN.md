# 20_ALTERNATIVE_URL_TEST_PLAN

## Profils créés

- `modules/bot_vision/headless_capture/profiles.source.stability.smoke.local.json`
- `modules/bot_vision/headless_capture/profiles.source.stability.alt.smoke.local.json`

## Profil principal retenu

| Page ID | URL | wait_until | timeout_ms | post_load_wait_ms |
| --- | --- | --- | ---: | ---: |
| `tv_btc_h1_strat_a` | `https://www.tradingview.com/chart/?symbol=BTCUSDT.P` | `domcontentloaded` | 45000 | 10000 |
| `tv_btc_h1_strat_b` | `https://www.tradingview.com/chart/?symbol=BTCUSDT.P` | `load` | 60000 | 5000 |
| `tv_xau_h1_strat_a` | `https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD` | `domcontentloaded` | 60000 | 15000 |
| `cg_btc_flow_strat_a` | `https://www.coinglass.com/LiquidationData?coin=BTC` | `domcontentloaded` | 60000 | 15000 |

## Profil alt retenu

| Page ID | Rôle | URL |
| --- | --- | --- |
| `tv_btc_h1_alt_binance_spot` | fallback BTC | `https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT` |
| `tv_btc_h1_alt_binance_perp` | fallback BTC | `https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDTPERP` |
| `tv_btc_h1_alt_bybit_perp` | fallback BTC | `https://www.tradingview.com/chart/?symbol=BYBIT:BTCUSDT.P` |
| `tv_xau_h1_alt_oanda` | fallback XAU | `https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD` |
| `cg_btc_flow_alt_funding` | fallback flow | `https://www.coinglass.com/FundingRate/BITCOIN` |

## Variantes explicitement rejetées

| URL | Résultat | Raison |
| --- | --- | --- |
| `https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC` | `blocked` | timeout persistant |
| `https://www.coinglass.com/futures/LiquidationHeatMap?coin=BTC` | `blocked` | timeout persistant |
| `https://www.coinglass.com/LiquidationHeatMap?coin=BTC` | faux positif | page `/404` malgré capture visuellement riche |

## Ajustements moteur retenus

Dans `capture_headless.js` :

1. Chromium : `--enable-webgl`, `--disable-web-security`
2. `userAgent` Chrome complet
3. Le check `readyState !== complete` ne dégrade plus une capture SPA si le PNG est déjà suffisamment riche
