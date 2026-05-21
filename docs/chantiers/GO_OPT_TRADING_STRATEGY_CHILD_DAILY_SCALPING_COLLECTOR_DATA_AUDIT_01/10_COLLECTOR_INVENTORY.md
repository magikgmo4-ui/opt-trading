---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_COLLECTOR_INVENTORY
doc_type: inventory
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: closed
audited_at: 2026-05-20
---

# 10_COLLECTOR_INVENTORY

Inventaire complet des collectors actifs dans le repo au 2026-05-20.

## Tableau synthétique

| Collector | Rôle | Symboles | Granularité | Output | Classification |
|---|---|---|---|---|---|
| `collector_binance_spot` | OHLCV snapshot | BTC/ETH (crypto) | 24h seulement | JSON fichier | NOT_RELEVANT |
| `collector_coingecko` | Prix snapshot | bitcoin/ethereum | Snapshot | JSON fichier | NOT_RELEVANT |
| `derivatives_collector` | Dérivatives | BTCUSDT/ETHUSDT | Snapshot | CSV/JSON | CONTEXT_ONLY |
| `simex_bitget_bridge` | OHLCV klines | **XAUUSDT** (configurable) | **M5+ configurable** | HTTP push | PRIMARY_WITH_GAPS |

---

## 1 — collector_binance_spot

**Chemin :** `modules/collector_binance_spot/`

| Propriété | Valeur |
|---|---|
| API | Binance `/api/v3/ticker/24hr` |
| Symboles | BTCUSDT, ETHUSDT (hardcodés dans defaults.toml) |
| Champs | open_price_24h, high_price_24h, low_price_24h, last_price, volume_base_24h, weighted_avg_price |
| Granularité | 24h snapshot uniquement |
| Output | `modules/collector_binance_spot/outputs/normalized/pair_market_snapshot_<run_id>.json` |
| bid/ask/spread | absent |
| XAUUSD | non supporté |

**Classification : `NOT_RELEVANT`**
Raison : crypto seulement, granularité 24h, pas de klines M5/M15, pas de XAUUSD.

---

## 2 — collector_coingecko

**Chemin :** `modules/collector_coingecko/`

| Propriété | Valeur |
|---|---|
| API | CoinGecko `/coins/markets` |
| Symboles | bitcoin, ethereum (coin_ids) |
| Champs | current_price, high_24h, low_24h, market_cap, volume, price_change_24h |
| Granularité | Snapshot par run |
| Output | `modules/collector_coingecko/outputs/normalized/market_snapshot_<run_id>.json` |
| bid/ask/spread | non applicable |
| XAUUSD | non applicable (crypto seulement) |

**Classification : `NOT_RELEVANT`**
Raison : crypto seulement, pas de forex/métaux, pas de granularité M5.

---

## 3 — derivatives_collector

**Chemin :** `modules/derivatives_collector/`

| Propriété | Valeur |
|---|---|
| API | Binance Futures / Bybit (configurable) |
| Symboles | BTCUSDT, ETHUSDT (configurable) |
| Champs | open_interest, funding_rate, liquidations_long, liquidations_short, long_short_ratio, volume_futures |
| Granularité | Snapshot par run |
| Output | `data/derivatives/` CSV/JSON |
| bid/ask/spread | non applicable (pas de prix OHLCV) |
| XAUUSD | non applicable — pas un collector OHLCV |

**Classification : `CONTEXT_ONLY`**
Raison : fournit des métriques de sentiment/microstructure dérivatives. Rôle = filtre contextuel de qualité pour les setups, jamais source OHLCV.

---

## 4 — simex_bitget_bridge

**Chemin :** `modules/simex_bitget_bridge/`

| Propriété | Valeur |
|---|---|
| API | Bitget `/api/v2/mix/market/candles` (USDT-FUTURES) |
| Symboles | **XAUUSDT** (via `SIMEX_SYMBOL` env, configurable) |
| Champs | timestamp, open, high, low, close, baseVolume, quoteVolume |
| Granularité | **M5 par défaut** (`SIMEX_GRANULARITY_SEC=300`), configurable |
| Output | **HTTP push** vers `PERF_EVENT` endpoint (http://127.0.0.1:8010/perf/event) |
| bid/ask/spread | absent |
| XAUUSD | XAUUSDT (futures Bitget, pas spot XAUUSD broker) |
| Pattern famille | ne suit pas le pattern collector famille (pas de manifest/status/events artifacts) |

**Classification : `PRIMARY_WITH_GAPS`**
Raison : le seul collector du repo qui fetch des klines OHLCV M5 sur un instrument gold (XAUUSDT). Gaps significatifs : output HTTP push seulement (pas fichier), pas de bid/ask/spread, XAUUSDT ≠ XAUUSD spot, pas de profondeur historique documentée, pas de pattern collector famille.

Voir `20_XAUUSD_OHLCV_CAPABILITY_CHECK.md` pour l'analyse détaillée.

---

## Données XAUUSD existantes dans le repo

**Chemin :** `data/market/`

| Fichier | Barres | Période | Champs |
|---|---|---|---|
| xauusd_m5.csv | 13 656 | 2026-03-11 → 2026-05-21 | timestamp, open, high, low, close, volume |
| xauusd_m15.csv | 4 562 | 2026-03-11 → 2026-05-21 | timestamp, open, high, low, close, volume |

Source actuelle : Yahoo Finance GC=F (smoke). Fenêtre : 60 jours. Champs manquants : bid, ask, spread, source.
