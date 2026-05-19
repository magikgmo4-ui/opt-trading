---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 10_PAGE_SELECTION_MATRIX

## Objectif

Definir les pages candidates sans modifier encore le profil runtime.

## P0 - Fenetre pilote 24-48h

| Page ID | Page | Symbol | Timeframe | Role | Conservation cible | Statut |
| --- | --- | --- | --- | --- | ---: | --- |
| `tv_btc_h1` | TradingView BTC H1 | `BTCUSDT.P` | `H1` | prix / structure marche | 1-2/jour | candidat P0 |
| `tv_xau_h1` | TradingView XAU H1 | `XAUUSD` ou symbole broker a confirmer | `H1` | gold / session macro | 1-2/jour | candidat P0, URL a valider |
| `cg_btc_flow` | Coinglass BTC liquidation/OI/funding | `BTCUSDT.P` | `FLOW` | orderflow / levier / funding | 1-2/jour | candidat P0, URL a valider |

## Extensions apres validation humaine

| Page ID | Page | Symbol | Timeframe | Role | Conservation cible |
| --- | --- | --- | --- | --- | ---: |
| `tv_sol_h1` | TradingView SOL H1 | `SOLUSDT.P` | `H1` | crypto alt beta | 1/jour |
| `tv_eth_h1` | TradingView ETH H1 | `ETHUSDT.P` | `H1` | crypto major beta | 1/jour |
| `screener_crypto_global` | Screener global crypto ou watchlist | `CRYPTO` | `SCREENER` | breadth / alertes | 1/jour |
| `deskpro_latest` | Desk Pro latest dashboard | `DESKPRO` | `LATEST` | verification consumer final | 1/jour |

## Decision pratique

Ne pas appliquer cette matrice directement a `profiles.example.json` tant que :

1. le service capture reste failed ;
2. Playwright est absent ;
3. le flux ne produit pas de PNG ;
4. la validation humaine n'a pas approuve le passage 3 pages.

## Profil cible apres PASS humain

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
    "url": "URL_A_VALIDER_HUMAINEMENT"
  },
  {
    "page_id": "cg_btc_flow",
    "source": "coinglass",
    "symbol": "BTCUSDT.P",
    "timeframe": "FLOW",
    "url": "URL_A_VALIDER_HUMAINEMENT"
  }
]
```

