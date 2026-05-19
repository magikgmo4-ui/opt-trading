# 10_SOURCE_MATRIX

## Matrice initiale

| Page | URL initiale | Problème initial | Résolution |
| --- | --- | --- | --- |
| `tv_btc_h1` | `https://www.tradingview.com/chart/?symbol=BTCUSDT.P` | timeout Playwright malgré HTML reachable | UA Chrome réaliste + flags Chromium WebGL + stratégie `domcontentloaded` |
| `tv_xau_h1` | `https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD` | spinner / `possible_spinner` | mêmes fixes moteur + check visuel SPA moins strict |
| `cg_btc_flow` | `https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC` | timeout persistant | abandon route pro, adoption route publique `LiquidationData?coin=BTC` |

## Causes racines confirmées

### TradingView BTC

- Le `userAgent` initial était trop générique.
- Le moteur Chromium headless sans WebGL suffisait à provoquer des timeouts de `page.goto()`.
- Avec ces réglages, une page HTML partiellement chargée restait bloquée du point de vue Playwright.

Fixes confirmés :

1. `userAgent` complet type Chrome 125
2. flags Chromium : `--enable-webgl`, `--disable-web-security`
3. stratégie `domcontentloaded` + `post_load_wait_ms`

### TradingView XAU

- Le problème n’était pas seulement l’URL/symbole, mais surtout le rendu SPA headless.
- Une fois le moteur stabilisé, la route `OANDA:XAUUSD` est devenue exploitable.

### Coinglass

- Les routes `pro/futures/LiquidationHeatMap` et `futures/LiquidationHeatMap` restent instables / timeout.
- La route `LiquidationHeatMap?coin=BTC` non-pro a produit un faux positif : capture `ready` visuellement, mais contenu fonctionnel `/404`.
- La route publique valide retenue est `https://www.coinglass.com/LiquidationData?coin=BTC`.
