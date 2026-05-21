---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_NORMALIZATION_CONTRACT
doc_type: data_contract
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
status: open
updated_at: 2026-05-20
---

# 40_NORMALIZATION_CONTRACT

## Scripts à créer

### normalize_mt5.py

**Chemin :** `tools/strategy/daily_scalping/normalize_mt5.py`

```bash
python tools/strategy/daily_scalping/normalize_mt5.py \
    --input <path_raw_mt5.csv> \
    --output <path_canonical.csv> \
    --timeframe M5|M15 \
    --broker-tz UTC+2
```

**Transformations :**

| Colonne MT5 | Transformation | Colonne canonique |
|---|---|---|
| `<DATE> <TIME>` | parse + localize broker-tz + convert UTC | `timestamp` |
| `<OPEN>` | float | `open` |
| `<HIGH>` | float | `high` |
| `<LOW>` | float | `low` |
| `<CLOSE>` | float | `close` |
| `<TICKVOL>` | int | `volume` |
| `<SPREAD>` | points → USD (÷100 si 2 décimales) | `spread` |
| `spread/2` estimé | bid = close - spread/2 | `bid` |
| `spread/2` estimé | ask = close + spread/2 | `ask` |
| constante | `mt5_export` | `source` |
| constante | `XAUUSD` | `symbol` |
| paramètre | `M5` ou `M15` | `timeframe` |

**Notes sur le spread MT5 :**
- MT5 exporte `<SPREAD>` en points (ex: `15` = 15 points = 0.15 USD pour XAUUSD à 2 décimales)
- Conversion : `spread_usd = spread_points * point_size` où `point_size = 0.01` pour XAUUSD
- bid/ask par bar sont estimés à ± spread/2 autour du close — acceptable pour backtest

### normalize_dukascopy.py

**Chemin :** `tools/strategy/daily_scalping/normalize_dukascopy.py`

```bash
python tools/strategy/daily_scalping/normalize_dukascopy.py \
    --input data/market/raw/xauusd_tick_*.csv \
    --output-m5 data/market/xauusd_m5_canonical.csv \
    --output-m15 data/market/xauusd_m15_canonical.csv
```

**Transformations :**

| Champ Dukascopy | Transformation | Colonne canonique |
|---|---|---|
| `Timestamp` | parse UTC DD.MM.YYYY + ms → ISO UTC | `timestamp` |
| `(Ask+Bid)/2` open | resample first | `open` |
| `(Ask+Bid)/2` max | resample max | `high` |
| `(Ask+Bid)/2` min | resample min | `low` |
| `(Ask+Bid)/2` close | resample last | `close` |
| `AskVolume` | sum | `volume` |
| `Ask_close - Bid_close` | par bar resampleé | `spread` |
| `close - spread/2` | | `bid` |
| `close + spread/2` | | `ask` |
| constante | `dukascopy` | `source` |
| constante | `XAUUSD` | `symbol` |
| paramètre | `M5` ou `M15` | `timeframe` |

## Schéma CSV canonique résultant

```text
timestamp,open,high,low,close,volume,bid,ask,spread,source,symbol,timeframe
2024-01-02 08:00:00+00:00,2063.50,2065.10,2062.80,2064.30,1250,2064.22,2064.37,0.15,mt5_export,XAUUSD,M5
```

## Validation post-normalisation

```python
REQUIRED_COLS = ["timestamp","open","high","low","close","volume","bid","ask","spread","source","symbol","timeframe"]

def validate_canonical(df):
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    assert not missing, f"Colonnes manquantes: {missing}"
    assert (df["spread"] >= 0).all(), "spread négatif détecté"
    assert (df["ask"] >= df["bid"]).all(), "ask < bid"
    assert (df["high"] >= df["low"]).all(), "high < low"
    assert (df["high"] >= df["close"]).all(), "high < close"
    assert (df["low"] <= df["close"]).all(), "low > close"
    assert df["source"].isin(["mt5_export", "dukascopy"]).all(), "source invalide"
    n_rows = len(df)
    assert n_rows >= 50_000, f"Trop peu de lignes: {n_rows} (min 50 000 pour 180j M5)"
    print(f"✅ Validation OK — {n_rows} barres, période: {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")
```

## Fichiers de destination

```
data/market/xauusd_m5_canonical.csv    ← source primaire backtest
data/market/xauusd_m15_canonical.csv   ← contexte HTF
data/market/raw/                        ← fichiers bruts (ignorés par git)
```

Les fichiers `*_canonical.csv` sont ignorés par `.gitignore` (données trop lourdes pour le repo). Seuls les scripts de normalisation sont versionnés.
