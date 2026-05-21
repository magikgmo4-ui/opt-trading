---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01_IMPLEMENTATION_PLAN
doc_type: implementation_plan
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01
status: closed
updated_at: 2026-05-20
---

# 10_IMPLEMENTATION_PLAN

## Script cible

`tools/strategy/daily_scalping/fetch_bitget.py`

Standalone, ne modifie pas simex_bitget_bridge.

## API Bitget utilisée

```
GET https://api.bitget.com/api/v2/mix/market/candles
  params: symbol=XAUUSDT, productType=USDT-FUTURES, granularity=300, limit=200
          startTime=<ms>, endTime=<ms>
  response: [[ts_ms, open, high, low, close, baseVol, quoteVol], ...]

GET https://api.bitget.com/api/v2/mix/market/ticker
  params: symbol=XAUUSDT, productType=USDT-FUTURES
  response: {data: [{bidPr, askPr, lastPr, ...}]}
```

## Pagination

Bitget limite à 200 bougies par requête. Pour couvrir 30 jours de M5 :
- 30 jours × 24h × 12 bougies/h = 8 640 bougies = 44 requêtes minimum
- Boucle : `end_time = start_time + 200 × granularity_sec × 1000` puis avancer

## Spread

Le spread historique par bar n'est pas disponible via l'API candles. Deux approches :
1. Snapshot ticker au moment du fetch → `spread_snapshot = ask - bid`
2. Appliquer ce spread_snapshot uniformément à toutes les bougies historiques

Pour XAUUSDT Bitget : spread observé = 0.01 USD (1 cent sur $4500+). À documenter.

## Schéma CSV produit

```text
timestamp,open,high,low,close,volume,bid,ask,spread,source,symbol,timeframe
2026-04-21 01:55:00+00:00,4484.91,4486.99,4483.77,4486.79,72.43,4560.69,4560.70,0.01,bitget_xauusdt_futures_approx,XAUUSDT,M5
```

Note : bid/ask = snapshot au moment du fetch (pas valeurs historiques per-bar). `spread` = ask - bid au moment du fetch.

## Paramètres CLI

```bash
python tools/strategy/daily_scalping/fetch_bitget.py \
    --out data/market \
    --days 30 \
    --symbol XAUUSDT \
    --product-type USDT-FUTURES
```

## Fichiers produits

```
data/market/xauusdt_m5_bitget.csv
data/market/xauusdt_m15_bitget.csv
```

Nommage distinct de `xauusd_m5.csv` (Yahoo/GC=F smoke) pour éviter toute confusion.
