---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: implementation_plan
updated_at: 2026-05-19
---

# 30_IMPLEMENTATION_PLAN

## Changements code

Fichier modifie :

`modules/bot_vision/headless_capture/capture_headless.js`

Changements :

- ajout des defaults `POST_LOAD_WAIT_MS`, `WAIT_UNTIL`, `SCREENSHOT_MODE` ;
- validation de `wait_until` via `networkidle | domcontentloaded | load` ;
- validation de `screenshot_mode` via `viewport` ;
- parsing numerique de `timeout_ms` et `post_load_wait_ms` ;
- `page.setDefaultTimeout()` utilise le timeout de profil ;
- `page.goto()` utilise `wait_until` et `timeout_ms` du profil ;
- attente post-load configurable ;
- sidecar enrichi avec `page_id` et options de chargement.

## Profil smoke dynamique

Fichier cree :

`modules/bot_vision/headless_capture/profiles.p0.dynamic.smoke.local.json`

Profil courant :

```json
[
  {
    "page_id": "tv_btc_h1",
    "source": "tradingview",
    "symbol": "BTCUSDT.P",
    "timeframe": "H1",
    "url": "https://www.tradingview.com/chart/?symbol=BTCUSDT.P",
    "wait_until": "networkidle",
    "post_load_wait_ms": 3000,
    "timeout_ms": 30000,
    "screenshot_mode": "viewport"
  },
  {
    "page_id": "tv_xau_h1",
    "source": "tradingview",
    "symbol": "XAUUSD",
    "timeframe": "H1",
    "url": "https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD",
    "wait_until": "domcontentloaded",
    "post_load_wait_ms": 30000,
    "timeout_ms": 60000,
    "screenshot_mode": "viewport"
  },
  {
    "page_id": "cg_btc_flow",
    "source": "coinglass",
    "symbol": "BTCUSDT.P",
    "timeframe": "FLOW",
    "url": "https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC",
    "wait_until": "domcontentloaded",
    "post_load_wait_ms": 20000,
    "timeout_ms": 60000,
    "screenshot_mode": "viewport"
  }
]
```

## Checks

- `node --check modules/bot_vision/headless_capture/capture_headless.js` : OK.
- `python3 -m json.tool profiles.p0.dynamic.smoke.local.json` : OK.
- `npm run check` : `playwright:OK`.
- `profiles.example.json` : aucun diff.
