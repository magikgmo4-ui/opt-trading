---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01_CONTRACT
doc_type: data_contract
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_BROKER_DATA_LAB_ACTIVATION_01
---

# 20 — Contrat CSV broker minimal

## Format canonique

```csv
timestamp,open,high,low,close,volume
2026-04-07T18:00:00-04:00,3248.0,3250.5,3246.5,3249.5,120
```

## Règles de format

| Champ | Type | Règle |
|---|---|---|
| `timestamp` | ISO 8601 | Obligatoire. Avec timezone explicite (ex: `-04:00`). Pas de `Z`. |
| `open` | float | OHLC: high >= open et close, low <= open et close, high >= low |
| `high` | float | Voir ci-dessus |
| `low` | float | Voir ci-dessus |
| `close` | float | Voir ci-dessus |
| `volume` | float | Peut être 0.0 si non disponible. Non utilisé pour la détection. |

## Timezone

`trading_lab_v1` utilise `America/Montreal` (UTC-4 en EDT, UTC-5 en EST).

- EDT (été): offset `-04:00` → du 2e dimanche de mars au 1er dimanche de novembre
- EST (hiver): offset `-05:00`

La session `gold_open_18h` déclenche sur 18:00–18:10 heure locale Montreal.
La session `midnight_00h` déclenche sur 00:00–00:10 heure locale Montreal.

## Couverture minimale pour mesure réelle

Pour que `perf_status` puisse être mis à jour vers `MEASURED`:

```text
≥ 20 trades closés (result ∈ {win, loss, breakeven})
≥ 30 jours calendaires de sessions
Source: broker réel (Dukascopy, MT4/MT5, Interactive Brokers)
Format: M1 XAUUSD avec timestamps timezone-aware
```

## Sources broker compatibles

| Source | Format export | Compatible |
|---|---|---|
| Dukascopy JForex | CSV OHLCV avec timestamps UTC | Oui — convertir UTC vers Montreal |
| MT4/MT5 History Export | CSV OHLCV | Oui — vérifier timezone |
| Interactive Brokers TWS | CSV OHLCV | Oui |
| TradingView Export | CSV OHLCV | Oui |
| Yahoo Finance (GC=F) | CSV OHLCV | Smoke only — non validé pour décisions réelles |

## Conversion Dukascopy (exemple)

```python
import pandas as pd
from zoneinfo import ZoneInfo

# Charger export Dukascopy (timestamps en UTC)
df = pd.read_csv("dukascopy_xauusd_m1.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df["timestamp"] = df["timestamp"].dt.tz_convert("America/Montreal")
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S%z")
# Formater offset: +0000 → +00:00 si nécessaire
df.to_csv("xauusd_m1_montreal.csv", index=False)
```
