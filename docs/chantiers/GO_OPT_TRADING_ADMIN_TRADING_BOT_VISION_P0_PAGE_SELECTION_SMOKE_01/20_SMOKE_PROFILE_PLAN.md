---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
surface: ADMIN_TRADING
source_kind: profile_plan
updated_at: 2026-05-19
---

# 20_SMOKE_PROFILE_PLAN

## Profil smoke separe

Fichier cree :

`modules/bot_vision/headless_capture/profiles.p0.smoke.local.json`

Ce fichier n'est pas reference par le timer systemd et ne remplace pas `profiles.example.json`.

## Contenu

```json
[
  {
    "page_id": "tv_btc_h1",
    "source": "tradingview",
    "symbol": "BTCUSDT.P",
    "timeframe": "H1",
    "url": "https://www.tradingview.com/chart/?symbol=BTCUSDT.P"
  },
  {
    "page_id": "tv_xau_h1",
    "source": "tradingview",
    "symbol": "XAUUSD",
    "timeframe": "H1",
    "url": "https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD"
  },
  {
    "page_id": "cg_btc_flow",
    "source": "coinglass",
    "symbol": "BTCUSDT.P",
    "timeframe": "FLOW",
    "url": "https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC&type=symbol"
  }
]
```

## Validation syntaxe

Validation Node executee :

```text
PROFILE_OK tv_btc_h1,tv_xau_h1,cg_btc_flow
```

## Statut Git

`profiles.p0.smoke.local.json` n'est pas ignore par `.gitignore`, ne contient pas de secret et peut etre committe comme profil smoke reproductible.

## Commande smoke

```bash
cd /opt/trading/modules/bot_vision/headless_capture
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox \
  npm run capture -- --profile profiles.p0.smoke.local.json --once
```
