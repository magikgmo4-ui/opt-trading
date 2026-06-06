---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_EXISTING_DATA_CENTER_SURFACES
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

# 10_EXISTING_DATA_CENTER_SURFACES

## Objet

Inventaire factuel des surfaces Data Center existantes : registres, producers, consumers, contracts actifs. Base de reference avant toute extension.

## 1. Registres

### Registry files

| File | Version | Entries |
|---|---|---|
| `modules/data_center/registry/producers.json` | v1 | 7 producers |
| `modules/data_center/registry/consumers.json` | v1 | 14 consumers |

### Registry metadata

```text
registry_version: v1
updated_at:        2026-05-30T12:00:00Z
```

## 2. Producers

### 2.1 derivatives_collector__bitget

| Field | Value |
|---|---|
| Family | derivatives |
| Contract | market_metrics.v1 |
| Output path root | data/data_center/derivatives/derivatives_collector__bitget/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | open_interest, funding_rate, volume_futures, long_short_ratio, liquidations_long, liquidations_short |
| Coverage | full |
| Validated | 2026-05-23 |
| Last write | null |

### 2.2 derivatives_collector__binance

| Field | Value |
|---|---|
| Family | derivatives |
| Contract | market_metrics.v1 |
| Output path root | data/data_center/derivatives/derivatives_collector__binance/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | open_interest, funding_rate, volume_futures, long_short_ratio, liquidations_long, liquidations_short |
| Coverage | full |
| Validated | 2026-05-23 |
| Last write | null |

### 2.3 collector_binance_spot

| Field | Value |
|---|---|
| Family | spot |
| Contract | pair_market_snapshot.v1 |
| Output path root | data/data_center/spot/collector_binance_spot/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | last_price, open_price_24h, high_price_24h, low_price_24h, volume_24h, quote_volume_24h, price_change_24h, price_change_pct_24h, trading_status |
| Coverage | full |
| Validated | null |
| Last write | null |

### 2.4 bot_vision_headless

| Field | Value |
|---|---|
| Family | vision |
| Contract | vision_analysis.v1 |
| Output path root | data/data_center/views/vision_analysis/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | support_level, resistance_level, trend_direction, key_level, invalidation_level, price_target |
| Coverage | full |
| Validated | 2026-05-30 |
| Last write | null |

> **Observation :** Le path root `data/data_center/views/vision_analysis/` ne suit pas la convention canonique `data/data_center/<family>/<producer_id>/`. Il ecrit directement dans le dossier views, ce qui melange producer path et view path.

### 2.5 bot_vision_headless__coinglass

| Field | Value |
|---|---|
| Family | vision |
| Contract | vision_context.coinglass.v1 |
| Output path root | data/data_center/views/vision_context/coinglass/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | liquidations_long, liquidations_short, liquidation_heatmap_level, funding_rate, open_interest, open_interest_change_24h, long_short_ratio |
| Coverage | full |
| Validated | 2026-05-30 |
| Last write | null |

> **Observation :** Idem — path root ecrit dans `views/` au lieu de `<family>/<producer_id>/`.

### 2.6 bot_vision_headless__screener

| Field | Value |
|---|---|
| Family | vision |
| Contract | vision_context.screener.v1 |
| Output path root | data/data_center/views/vision_context/screener/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | stock_price, stock_change_pct, stock_volume |
| Coverage | full |
| Validated | 2026-05-30 |
| Last write | null |

### 2.7 bot_vision_headless__news_sentiment

| Field | Value |
|---|---|
| Family | vision |
| Contract | vision_context.news_sentiment.v1 |
| Output path root | data/data_center/views/vision_context/news_sentiment/ |
| Write mode | atomic |
| Latency | oneshot |
| Metrics collectable | sentiment_score, article_count, positive_count, negative_count, neutral_count |
| Coverage | full |
| Validated | 2026-05-30 |
| Last write | null |

## 3. Contracts actifs

| Contract class | Producers | Consumers | Views existantes |
|---|---|---|---|
| market_metrics.v1 | 2 (bitget, binance) | 6 (desk_pro, strategy, perf, telegram, sheets, localcms) | market_metrics/ (latest.json + by_symbol/) |
| pair_market_snapshot.v1 | 1 (binance_spot) | 1 (desk_pro) | NON (directory absent) |
| vision_analysis.v1 | 1 (bot_vision) | 2 (desk_pro, dashboards) | vision_analysis/ (by_symbol/) |
| vision_context.coinglass.v1 | 1 (bot_vision__coinglass) | 2 (desk_pro, dashboards) | NON (view directory absent, legacy only) |
| vision_context.screener.v1 | 1 (bot_vision__screener) | 2 (desk_pro, dashboards) | NON (view directory absent, legacy only) |
| vision_context.news_sentiment.v1 | 1 (bot_vision__news_sentiment) | 2 (desk_pro, dashboards) | NON (view directory absent, legacy only) |

## 4. Vue d'ensemble

```text
PRODUCERS  : 7 enregistres — 7 avec last_write = null (jamais executes)
CONSUMERS  : 14 enregistres — 10 migres DC views, 4 legacy DeskPro paths
CONTRACTS  : 6 contracts actifs — 2 avec view DC, 4 sans view DC dediee
VIEWS      : market_metrics + vision_analysis existantes / pair_market_snapshot + vision_context absentes
```

## 5. Anomalies detectees

| ID | Gravite | Description |
|---|---|---|
| A01 | HIGH | Tous les producers ont `last_write: null` — aucune execution confirmee |
| A02 | HIGH | 4 bot_vision producers ecrivent dans `views/` au lieu de `<family>/<producer_id>/` |
| A03 | MEDIUM | `pair_market_snapshot` view directory absente (consumer registered, infrastructure missing) |
| A04 | MEDIUM | 3 vision_context contracts sans view directory dediee |
| A05 | LOW | `collector_binance_spot` a `validated_at: null` |
