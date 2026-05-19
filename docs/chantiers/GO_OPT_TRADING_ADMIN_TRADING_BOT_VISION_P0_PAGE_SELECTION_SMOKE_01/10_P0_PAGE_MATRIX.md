---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
surface: ADMIN_TRADING
source_kind: page_matrix
updated_at: 2026-05-19
---

# 10_P0_PAGE_MATRIX

## Objectif

Tester trois pages P0 sans modifier le profil runtime actif.

## Pages P0 testees

| Page ID | Source | Symbol | Timeframe | URL smoke | Statut |
| --- | --- | --- | --- | --- | --- |
| `tv_btc_h1` | `tradingview` | `BTCUSDT.P` | `H1` | `https://www.tradingview.com/chart/?symbol=BTCUSDT.P` | PASS capture |
| `tv_xau_h1` | `tradingview` | `XAUUSD` | `H1` | `https://www.tradingview.com/chart/?symbol=OANDA:XAUUSD` | BLOCKED timeout |
| `cg_btc_flow` | `coinglass` | `BTCUSDT.P` | `FLOW` | `https://www.coinglass.com/pro/futures/LiquidationHeatMap?coin=BTC&type=symbol` | BLOCKED timeout |

## Raison des choix

- `tv_btc_h1` reprend la page deja validee par le smoke de reparation Playwright.
- `tv_xau_h1` utilise `OANDA:XAUUSD` dans l'URL TradingView, tout en gardant `symbol: XAUUSD` pour le nommage attendu.
- `cg_btc_flow` utilise une page publique Coinglass Liquidation HeatMap BTC comme proxy initial du flow BTC.

## Decision

La matrice P0 ne doit pas etre promue vers `profiles.example.json` tant que `tv_xau_h1` et `cg_btc_flow` ne produisent pas au minimum PNG + JSON sidecar.
