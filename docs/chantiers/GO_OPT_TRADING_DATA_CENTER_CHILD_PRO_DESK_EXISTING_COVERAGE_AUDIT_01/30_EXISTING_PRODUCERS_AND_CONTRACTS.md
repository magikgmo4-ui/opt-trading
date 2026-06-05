---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_EXISTING_PRODUCERS_AND_CONTRACTS
doc_type: audit
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# 30_EXISTING_PRODUCERS_AND_CONTRACTS

## Objet

Mapping complet producer → contract → output path → consumers downstream. Verifier la regle `producer <> view <> consumer`.

## 1. Mapping producer → contract

| Producer ID | Family | Contract class | Output path root | Path convention |
|---|---|---|---|---|
| derivatives_collector__bitget | derivatives | market_metrics.v1 | data/data_center/derivatives/derivatives_collector__bitget/ | OK |
| derivatives_collector__binance | derivatives | market_metrics.v1 | data/data_center/derivatives/derivatives_collector__binance/ | OK |
| collector_binance_spot | spot | pair_market_snapshot.v1 | data/data_center/spot/collector_binance_spot/ | OK |
| bot_vision_headless | vision | vision_analysis.v1 | data/data_center/views/vision_analysis/ | VIOLATION |
| bot_vision_headless__coinglass | vision | vision_context.coinglass.v1 | data/data_center/views/vision_context/coinglass/ | VIOLATION |
| bot_vision_headless__screener | vision | vision_context.screener.v1 | data/data_center/views/vision_context/screener/ | VIOLATION |
| bot_vision_headless__news_sentiment | vision | vision_context.news_sentiment.v1 | data/data_center/views/vision_context/news_sentiment/ | VIOLATION |

### Violations de convention

La regle canonique est :

```text
data/data_center/<family>/<producer_id>/   → ecriture producteur (source d'audit)
data/data_center/views/<contract_class>/   → lecture consumer (surface neutre)
```

Les 4 producers `bot_vision_headless*` ecrivent directement dans `views/` au lieu de `vision/<producer_id>/`. Cela melange la surface d'ecriture producteur (auditable) avec la surface de lecture consumer (neutre). Un consumer qui lit `views/vision_analysis/` lit directement le producer path sans passer par une view neutre.

## 2. Mapping contract → producers (multi-source potentiel)

| Contract class | Producers | Multi-source possible | Source scoring needed |
|---|---|---|---|
| market_metrics.v1 | bitget, binance | OUI (2 sources) | OUI |
| pair_market_snapshot.v1 | binance_spot | NON (1 source) | NON (actuellement) |
| vision_analysis.v1 | bot_vision_headless | NON (1 source) | NON (actuellement) |
| vision_context.coinglass.v1 | bot_vision_headless__coinglass | NON (1 source) | NON (actuellement) |
| vision_context.screener.v1 | bot_vision_headless__screener | NON (1 source) | NON (actuellement) |
| vision_context.news_sentiment.v1 | bot_vision_headless__news_sentiment | NON (1 source) | NON (actuellement) |

> **Note :** `market_metrics.v1` a 2 producers (bitget + binance) qui produisent les memes metriques. C'est le seul contract ou un source scoring / best-value resolver serait immediatement pertinent.

## 3. Mapping contract → consumers

| Contract class | Consumers | Total |
|---|---|---|
| market_metrics.v1 | desk_pro, strategy, perf, telegram, sheets, localcms | 6 |
| pair_market_snapshot.v1 | desk_pro | 1 |
| vision_analysis.v1 | desk_pro, dashboards | 2 |
| vision_context.coinglass.v1 | desk_pro, dashboards | 2 |
| vision_context.screener.v1 | desk_pro, dashboards | 2 |
| vision_context.news_sentiment.v1 | desk_pro, dashboards | 2 |

## 4. Chaine complete par contract

### 4.1 market_metrics.v1

```text
derivatives_collector__bitget ──→ data/data_center/derivatives/derivatives_collector__bitget/ ──→ (view builder) ──→ data/data_center/views/market_metrics/
derivatives_collector__binance ─→ data/data_center/derivatives/derivatives_collector__binance/ ──→ (view builder) ──→ data/data_center/views/market_metrics/
                                                                                                     │
                                                                                                     ├── desk_pro__market_metrics        (latest_only)
                                                                                                     ├── strategy_framework__market      (by_symbol)
                                                                                                     ├── perf_engine__replay             (full_history)
                                                                                                     ├── telegram_screener__signal       (latest_only)
                                                                                                     ├── google_sheets__market           (latest_only)
                                                                                                     └── localcms__data_center_health    (status_only)
```

**Status :** Chaine complete. View presente. Consumers migres. Multi-source non resolu (pas de source scoring).

### 4.2 pair_market_snapshot.v1

```text
collector_binance_spot ──→ data/data_center/spot/collector_binance_spot/ ──→ (view builder manquant) ──→ data/data_center/views/pair_market_snapshot/ ABSENTE
                                                                                   │
                                                                                   └── desk_pro__spot_snapshot (orphelin)
```

**Status :** Chaine cassee. View directory absente. Consumer orphelin.

### 4.3 vision_analysis.v1

```text
bot_vision_headless ──→ data/data_center/views/vision_analysis/ (path melange producer/view)
                            │
                            ├── desk_pro__vision_analysis    → lit data/deskpro/inputs/vision_analysis/ (LEGACY)
                            └── dashboards__vision_analysis  → lit data/data_center/views/vision_analysis/history/ (OK)
```

**Status :** Producer ecrit dans views/. DeskPro consumer lit un path legacy different. Dashboards consumer lit la view correctement.

### 4.4 vision_context.coinglass.v1

```text
bot_vision_headless__coinglass ──→ data/data_center/views/vision_context/coinglass/ (path melange)
                                       │
                                       ├── desk_pro__vision_context_coinglass  → lit data/deskpro/inputs/vision_context/coinglass/ (LEGACY)
                                       └── ?? (pas de consumer dashboards pour coinglass specifiquement)
```

**Status :** Producer ecrit dans views/. DeskPro consumer lit un path legacy different. Aucune view neutre dediee.

### 4.5 vision_context.screener.v1

```text
bot_vision_headless__screener ──→ data/data_center/views/vision_context/screener/ (path melange)
                                      │
                                      ├── desk_pro__vision_context_screener  → lit data/deskpro/inputs/vision_context/screener/ (LEGACY)
                                      └── dashboards__screener_history       → lit data/data_center/views/vision_context/screener/history/ (OK)
```

**Status :** Producer ecrit dans views/. DeskPro consumer lit path legacy. Dashboards consumer lit la view.

### 4.6 vision_context.news_sentiment.v1

```text
bot_vision_headless__news_sentiment ──→ data/data_center/views/vision_context/news_sentiment/ (path melange)
                                           │
                                           ├── desk_pro__vision_context_news_sentiment → lit data/deskpro/inputs/vision_context/news_sentiment/ (LEGACY)
                                           └── dashboards__news_sentiment_history       → lit data/data_center/views/vision_context/news_sentiment/history/ (OK)
```

**Status :** Producer ecrit dans views/. DeskPro consumer lit path legacy. Dashboards consumer lit la view.

## 5. Anomalies

| ID | Gravite | Description |
|---|---|---|
| C01 | HIGH | 4 producers vision violent la convention `<family>/<producer_id>/` en ecrivant dans `views/` |
| C02 | HIGH | `pair_market_snapshot` chaine cassee : view absente, consumer orphelin |
| C03 | HIGH | `market_metrics.v1` a 2 producers mais aucun source scoring / best-value resolver |
| C04 | MEDIUM | `desk_pro__vision_analysis` lit un path legacy different du producer output path |
| C05 | MEDIUM | `desk_pro__vision_context_coinglass` lit un path legacy different du producer output path |
| C06 | MEDIUM | `bot_vision_headless__coinglass` ecrit dans views/mais le consumer desk_pro lit un path deskpro/inputs/ — disconnect total |
