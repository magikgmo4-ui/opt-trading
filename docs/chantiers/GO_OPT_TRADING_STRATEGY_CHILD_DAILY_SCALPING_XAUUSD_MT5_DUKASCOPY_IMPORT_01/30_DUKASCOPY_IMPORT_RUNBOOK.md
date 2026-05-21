---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_DUKASCOPY_IMPORT_RUNBOOK
doc_type: runbook
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
status: open
updated_at: 2026-05-20
---

# 30_DUKASCOPY_IMPORT_RUNBOOK

## Pourquoi Dukascopy

Dukascopy Bank fournit gratuitement des données tick XAUUSD (bid + ask) depuis 2003, via leur plateforme JForex ou leur API publique. Pas de compte réel requis.

## Accès

URL : https://www.dukascopy.com/trading-tools/widgets/quotes/historical_data_feed/

Ou via le téléchargeur offline :
- Installer JForex (gratuit) → History Data → XAUUSD → Tick
- Sélectionner la période et exporter en CSV

## Format Dukascopy tick CSV

```text
Timestamp,Ask,Bid,AskVolume,BidVolume
01.01.2024 00:00:00.123,2062.500,2062.400,1.0,1.0
```

Champs :
- `Timestamp` : `DD.MM.YYYY HH:MM:SS.mmm` en UTC
- `Ask` / `Bid` : prix float
- `AskVolume` / `BidVolume` : volume (unités Dukascopy)

## Étape 1 — Télécharger les ticks

```
JForex → History Data Manager → XAUUSD
  → Timeframe : Tick
  → Date début : 2024-01-01
  → Date fin   : 2025-12-31
  → Export CSV (bi-mensuel ou annuel selon la limite du téléchargeur)
→ xauusd_tick_2024.csv
→ xauusd_tick_2025.csv
```

Alternative via API publique Dukascopy (sans JForex, en Python) :
```
https://datafeed.dukascopy.com/datafeed/XAUUSD/YYYY/MM/DD/BID_candles_minute_1.bi5
```
Format .bi5 (binaire LZW) → décompressable avec la lib dukascopy-python.

## Étape 2 — Normaliser avec normalize_dukascopy.py

```bash
python tools/strategy/daily_scalping/normalize_dukascopy.py \
    --input data/market/raw/xauusd_tick_2024.csv data/market/raw/xauusd_tick_2025.csv \
    --output-m5 data/market/xauusd_m5_canonical.csv \
    --output-m15 data/market/xauusd_m15_canonical.csv
```

Le script effectue :
1. Merge des fichiers tick si plusieurs
2. Resample en M5 : open/high/low/close sur bid ou mid (configuré)
3. Calcul spread par bar = `ask_close - bid_close`
4. Ajout colonnes source, symbol, timeframe

## Resample M5 depuis tick

```python
# Logique de normalize_dukascopy.py
df_tick["mid"] = (df_tick["Ask"] + df_tick["Bid"]) / 2
df_tick["spread_pt"] = df_tick["Ask"] - df_tick["Bid"]

df_m5 = df_tick.resample("5min").agg({
    "mid": ["first", "max", "min", "last"],
    "spread_pt": "mean",
    "AskVolume": "sum",
}).dropna()

df_m5.columns = ["open", "high", "low", "close", "spread", "volume"]
# bid/ask approximé depuis close mid ± spread/2
df_m5["bid"] = df_m5["close"] - df_m5["spread"] / 2
df_m5["ask"] = df_m5["close"] + df_m5["spread"] / 2
df_m5["source"] = "dukascopy"
df_m5["symbol"] = "XAUUSD"
df_m5["timeframe"] = "M5"
```

## Avantage Dukascopy vs MT5

- Spread interbank par tick → moyenne de spread par bar M5 (plus précis que colonne `spread` MT5)
- Historique depuis 2003 (vs ouverture compte MT5)
- Source institutionnelle reconnue
- Gratuit sans compte réel

## Inconvénient

- Spread interbank ≠ spread broker retail (Dukascopy est tighter)
- Le resample tick → M5 prend plus de temps (~10 min pour 2 ans)
- Format .bi5 nécessite une lib de décompression si téléchargement API
