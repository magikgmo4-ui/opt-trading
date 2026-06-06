---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_EXISTING_SURFACES_TO_REUSE
doc_type: inventory
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 20_EXISTING_SURFACES_TO_REUSE

## Objet

Lister les surfaces existantes a reprendre avant toute extension, pour eviter doublon DeskPro ou Data Center.

## Data Center — registres existants

A lire en priorite :

```text
modules/data_center/registry/producers.json
modules/data_center/registry/consumers.json
```

## Producers existants a recroiser

| Producer | Famille | Contract | Couverture pro desk |
|---|---|---|---|
| `derivatives_collector__bitget` | derivatives | `market_metrics.v1` | P10/P14 flows, OI, funding, liquidations |
| `derivatives_collector__binance` | derivatives | `market_metrics.v1` | P10/P14 flows, OI, funding, liquidations |
| `collector_binance_spot` | spot | `pair_market_snapshot.v1` | P1 prix spot / snapshot |
| `bot_vision_headless` | vision | `vision_analysis.v1` | P11 technical context |
| `bot_vision_headless__coinglass` | vision | `vision_context.coinglass.v1` | P4/P10/P14 liquidations/funding/OI context |
| `bot_vision_headless__screener` | vision | `vision_context.screener.v1` | P17 screener equities |
| `bot_vision_headless__news_sentiment` | vision | `vision_context.news_sentiment.v1` | P9 news/sentiment context |

## Consumers DeskPro existants a reprendre

| Consumer | Contract | Role |
|---|---|---|
| `desk_pro__market_metrics` | `market_metrics.v1` | contexte marche derives |
| `desk_pro__spot_snapshot` | `pair_market_snapshot.v1` | snapshot spot |
| `desk_pro__vision_analysis` | `vision_analysis.v1` | analyse visuelle structuree |
| `desk_pro__vision_context_coinglass` | `vision_context.coinglass.v1` | contexte liquidations/funding/OI |
| `desk_pro__vision_context_screener` | `vision_context.screener.v1` | contexte screener equities |
| `desk_pro__vision_context_news_sentiment` | `vision_context.news_sentiment.v1` | contexte news/sentiment |

## Regles de reprise

- Un consumer existant est repris avant d'en creer un nouveau.
- Un producer existant est mappe avant d'ajouter une nouvelle source.
- Les paths `data/deskpro/inputs/*` sont legacy ou transit si une view Data Center existe.
- Les consumers doivent lire les views Data Center, sauf exception documentee.

## Gaps a mesurer dans le premier child

- Contrats presents mais non couverts par scoring source.
- Producers avec `last_write: null`.
- Views existantes vs paths legacy.
- Readers DeskPro reels vs entries registry.
- Donnees pro P0-P21 absentes de l'existant.
