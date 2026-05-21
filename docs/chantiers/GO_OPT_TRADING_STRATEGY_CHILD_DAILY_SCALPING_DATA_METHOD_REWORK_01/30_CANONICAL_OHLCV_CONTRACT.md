---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_CANONICAL_OHLCV_CONTRACT
doc_type: data_contract
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
updated_at: 2026-05-20
---

# 30_CANONICAL_OHLCV_CONTRACT

## Contrat XAUUSD_M5_CANONICAL

### Schéma CSV

```text
timestamp,open,high,low,close,volume,bid,ask,spread,source,symbol,timeframe
2024-01-02 08:00:00+00:00,2063.50,2065.10,2062.80,2064.30,1250,2063.48,2063.52,0.04,mt5_export,XAUUSD,M5
```

| Colonne | Type | Obligatoire | Description |
|---|---|---|---|
| `timestamp` | ISO 8601 UTC | oui | Ouverture de la bougie, timezone UTC explicite |
| `open` | float | oui | Prix open (mid ou ask selon broker) |
| `high` | float | oui | Plus haut |
| `low` | float | oui | Plus bas |
| `close` | float | oui | Prix close |
| `volume` | int | oui | Volume (ticks ou lots selon broker, 0 si FX spot) |
| `bid` | float | oui | Bid close de la bougie |
| `ask` | float | oui | Ask close de la bougie |
| `spread` | float | oui | Ask - Bid en points (ex: 0.04 = 4 points) |
| `source` | string | oui | `mt5_export`, `dukascopy`, `prod_collector`, `smoke_yfinance` |
| `symbol` | string | oui | `XAUUSD` |
| `timeframe` | string | oui | `M5`, `M15` |

### Règles de validation

```python
# À implémenter dans load_data.py — couche canonique
REQUIRED_COLS = ["timestamp", "open", "high", "low", "close", "volume", "bid", "ask", "spread", "source"]

def validate_canonical(df):
    assert all(c in df.columns for c in REQUIRED_COLS), "colonnes manquantes"
    assert (df["spread"] >= 0).all(), "spread négatif"
    assert (df["ask"] >= df["bid"]).all(), "ask < bid"
    assert (df["high"] >= df["low"]).all(), "high < low"
    assert df.index.tz is not None, "timezone manquante"
    if df["source"].eq("smoke_yfinance").any():
        raise ValueError("source smoke_yfinance interdite pour verdict — utiliser source niveau 1")
```

### Différences avec le contrat smoke PR #658

| Propriété | PR #658 (smoke) | Canonical |
|---|---|---|
| bid | absent | obligatoire |
| ask | absent | obligatoire |
| spread | hardcodé config | issu du feed |
| source | implicite | explicite dans chaque ligne |
| validation | aucune | bloquante si source=smoke |

## Contrat XAUUSD_M15_CANONICAL

Même schéma. `timeframe` = `M15`. Utilisé comme contexte HTF dans `merge_timeframes()`.

## Gestion du spread dans le simulateur

Quand le contrat canonique est utilisé, le simulateur lit le spread par bar depuis la colonne `spread` plutôt que depuis `config.yaml`. La valeur config devient un fallback si le spread est manquant ou nul.

```python
# simulator.py — à implémenter lors du rework
spread_pts = row.get("spread", config_spread)
entry_with_spread = entry_price + spread_pts  # long
entry_with_spread = entry_price - spread_pts  # short
```

## Sources acceptées et process d'import

### MetaTrader 5 export

```
MT5 → History Center → XAUUSD → M5 → Export CSV
→ colonnes: time, open, high, low, close, tick_volume, spread, real_volume
→ renommer columns → ajouter bid/ask depuis spread/2 si tick précision disponible
→ sauvegarder data/market/xauusd_m5_canonical.csv avec source=mt5_export
```

### Dukascopy tick data

```
dukascopy.com/datafeed → XAUUSD → tick CSV
→ resample en M5 avec OHLC(bid) + OHLC(ask)
→ spread = ask_close - bid_close par bar
→ sauvegarder avec source=dukascopy
```

### Prod collector (futur)

```
prod_api_collector → XAUUSD endpoint → streaming OHLCV + bid/ask
→ normalisation UTC
→ sauvegarder avec source=prod_collector
```
