---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_DUKASCOPY_M1_COLLECTOR_01
doc_type: audit
---

# Source Access Audit

## Endpoint Dukascopy

```
https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YEAR}/{MONTH_0INDEXED:02d}/{DAY:02d}/BID_candles_min_1.bi5
```

Exemple : `https://datafeed.dukascopy.com/datafeed/XAUUSD/2026/03/07/BID_candles_min_1.bi5`
- Note : le mois est **0-indexé** (avril = `03`, pas `04`)

## Résultat du test (2026-04-07)

```
HTTP 200  size=17760 bytes compressed
Décompressé : 34560 bytes = 1440 records × 24 bytes (full day)
```

**Verdict : SOURCE_ACCESSIBLE**

## Format bi5

| Champ | Type | Notes |
|---|---|---|
| time_s | uint32 (big-endian) | secondes depuis minuit UTC du jour |
| open   | uint32 | prix × 1000 pour XAUUSD |
| close  | uint32 | prix × 1000 |
| low    | uint32 | prix × 1000 |
| high   | uint32 | prix × 1000 |
| volume | float32 | en lots |

- Compression : LZMA
- Endianness : big-endian (`>`)
- Ordre des champs de prix : **open, close, low, high** (pas OHLC standard)
- Diviseur XAUUSD : **1000** (confirmé empiriquement : 4659155 / 1000 = 4659.155)

## Prix BID vs ASK

Seuls les prix BID sont collectés. Pour la stratégie `xau_session_open_v1` en mode observation, les prix BID sont suffisants. L'écart bid/ask moyen XAUUSD est ~0.3–0.5 pts.

## Limitations

- Données historiques jusqu'au jour précédent (pas temps réel)
- Weekends : données présentes mais avec gaps (marché fermé)
- Aucune garantie de disponibilité des données futures (service public non documenté)
