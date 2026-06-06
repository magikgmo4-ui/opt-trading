---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_EXISTING_DESKPRO_CONSUMERS
doc_type: audit
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - modules/data_center/registry/consumers.json
  - modules/desk_pro/service/market_metrics_reader.py
  - modules/desk_pro/service/spot_snapshot_reader.py
  - modules/desk_pro/service/vision_analysis_reader.py
  - modules/desk_pro/service/vision_context_reader.py
  - modules/desk_pro/service/telegram_claim_reader.py
  - modules/desk_pro/service/vision_panel.py
  - modules/desk_pro/service/aggregator.py
---

# 20_EXISTING_DESKPRO_CONSUMERS

## Objet

Cartographier les consumers DeskPro reels : paths effectifs, migration status, readers correspondants. Comparer les entrees registry avec le code effectif.

## 1. Consumers DeskPro enregistres dans le registry

### 1.1 desk_pro__market_metrics

| Field | Value |
|---|---|
| Contract | market_metrics.v1 |
| **Registry read_path** | data/data_center/views/market_metrics/latest.json |
| **Reader path effectif** | data/data_center/views/market_metrics/latest.json (primary) |
| **Fallback** | data/deskpro/inputs/market_metrics/latest.json |
| Migrated | OUI |
| Access pattern | latest_only |

### 1.2 desk_pro__spot_snapshot

| Field | Value |
|---|---|
| Contract | pair_market_snapshot.v1 |
| **Registry read_path** | data/data_center/views/pair_market_snapshot/latest.json |
| **Reader path effectif** | data/data_center/views/pair_market_snapshot/latest.json |
| Migrated | OUI (registry) |
| Access pattern | latest_only |

> **Gap:** La view directory `pair_market_snapshot/` n'existe pas. Le consumer est migre au niveau registry mais le path est orphelin.

### 1.3 desk_pro__vision_analysis

| Field | Value |
|---|---|
| Contract | vision_analysis.v1 |
| **Registry read_path** | data/deskpro/inputs/vision_analysis/latest.json |
| **Reader path effectif** | data/deskpro/inputs/vision_analysis/latest.json |
| Migrated | NON (legacy) |
| Access pattern | latest_only |

### 1.4 desk_pro__vision_context_coinglass

| Field | Value |
|---|---|
| Contract | vision_context.coinglass.v1 |
| **Registry read_path** | data/deskpro/inputs/vision_context/coinglass/latest.json |
| **Reader path effectif** | data/deskpro/inputs/vision_context/coinglass/latest.json |
| Migrated | NON (legacy) |
| Access pattern | latest_only |

### 1.5 desk_pro__vision_context_screener

| Field | Value |
|---|---|
| Contract | vision_context.screener.v1 |
| **Registry read_path** | data/deskpro/inputs/vision_context/screener/latest.json |
| **Reader path effectif** | data/deskpro/inputs/vision_context/screener/latest.json |
| Migrated | NON (legacy) |
| Access pattern | latest_only |

### 1.6 desk_pro__vision_context_news_sentiment

| Field | Value |
|---|---|
| Contract | vision_context.news_sentiment.v1 |
| **Registry read_path** | data/deskpro/inputs/vision_context/news_sentiment/latest.json |
| **Reader path effectif** | data/deskpro/inputs/vision_context/news_sentiment/latest.json |
| Migrated | NON (legacy) |
| Access pattern | latest_only |

## 2. Consumers non-DeskPro (pour contexte)

| Consumer ID | Surface | Contract | Path | Migrated |
|---|---|---|---|---|
| strategy_framework__market_context | PF_STRATEGY | market_metrics.v1 | DC view by_symbol | OUI |
| perf_engine__replay_context | PF_PERF | market_metrics.v1 | DC view history | OUI |
| telegram_screener__signal_context | PF_TELEGRAM | market_metrics.v1 | DC view latest | OUI |
| google_sheets__market_reporting | PF_SHEETS | market_metrics.v1 | DC view latest | OUI |
| localcms__data_center_health | PF_LOCALCMS | null (status_only) | registry producers.json | OUI |
| dashboards__vision_analysis_history | PF_DASHBOARDS | vision_analysis.v1 | DC view history | OUI |
| dashboards__screener_history | PF_DASHBOARDS | vision_context.screener.v1 | DC view history | OUI |
| dashboards__news_sentiment_history | PF_DASHBOARDS | vision_context.news_sentiment.v1 | DC view history | OUI |

## 3. Readers DeskPro : correspondance path effectif vs registry

| Reader | Default path | Type de path | Registry match |
|---|---|---|---|
| `market_metrics_reader.py` | DC view (+ legacy fallback) | DC view primary | OUI |
| `spot_snapshot_reader.py` | DC view | DC view only | OUI (mais view absente) |
| `vision_analysis_reader.py` | deskpro/inputs/ | LEGACY | OUI (registry dit legacy) |
| `vision_context_reader.py` (coinglass) | deskpro/inputs/ | LEGACY | OUI (registry dit legacy) |
| `vision_context_reader.py` (news_sentiment) | deskpro/inputs/ | LEGACY | OUI (registry dit legacy) |
| `vision_context_reader.py` (screener) | deskpro/inputs/ | LEGACY | OUI (registry dit legacy) |
| `telegram_claim_reader.py` | deskpro/inputs/ | LEGACY | NON (pas dans consumers.json) |
| `vision_panel.py` (coinglass) | deskpro/inputs/ | LEGACY | — (panel, pas consumer) |
| `vision_panel.py` (news) | deskpro/inputs/ | LEGACY | — (panel, pas consumer) |
| `vision_panel.py` (screener) | deskpro/inputs/ | LEGACY | — (panel, pas consumer) |
| `vision_panel.py` (telegram_claim) | deskpro/inputs/ | LEGACY | — (panel, pas consumer) |
| `aggregator.py` | mix (DC + legacy) | HYBRID | — |

## 4. Bilan migration DeskPro

```text
MIGRES   : 2/6 (market_metrics, spot_snapshot)
LEGACY   : 4/6 (vision_analysis, vision_context x3)
ORPHELIN : 1 (spot_snapshot : view directory absente)
MANQUANT : 1 (telegram_claim non enregistre dans consumers.json)
```

## 5. Anomalies

| ID | Gravite | Description |
|---|---|---|
| B01 | HIGH | 4 consumers DeskPro lisent des paths legacy (non migres vers DC views) |
| B02 | HIGH | `pair_market_snapshot` view directory absente — consumer orphelin |
| B03 | MEDIUM | `telegram_claim_reader.py` existe mais aucun consumer `telegram_claim` dans le registry |
| B04 | MEDIUM | `aggregator.py` utilise vision_context_coinglass via path legacy (lecture directe du reader, pas de la view) |
| B05 | LOW | `vision_panel.py` et `vision_context_reader.py` dupliquent la logique de lecture coinglass |
| B06 | LOW | `vision_panel.py` lit 4 paths legacy sans consumer registry correspondant |
