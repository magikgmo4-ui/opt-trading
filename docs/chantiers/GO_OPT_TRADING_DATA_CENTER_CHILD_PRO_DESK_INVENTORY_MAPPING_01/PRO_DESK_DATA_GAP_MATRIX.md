---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01_GAP_MATRIX
doc_type: gap_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/10_EXISTING_DATA_CENTER_SURFACES.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/20_EXISTING_DESKPRO_CONSUMERS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/30_EXISTING_PRODUCERS_AND_CONTRACTS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/40_EXISTING_VIEWS_AND_PATHS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/50_PRELIMINARY_GAPS.md
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# PRO_DESK_DATA_GAP_MATRIX

## Objet

Matrix canonique croisant chaque categorie P0-P21 avec toutes les surfaces existantes (producers, consumers, views, readers, legacy paths, anomalies). Reference unique pour les childs suivants (scoring, resolver, consumption map).

## Legende

| Symbole | Signification |
|---|---|
| OK | Present et operationnel |
| ~ | Partiel (existe mais incomplet) |
| X | Absent |
| L | Legacy (path non migre) |
| V | Violation (convention non respectee) |
| — | Non applicable |

## Matrix P0-P21 × Surfaces

### P0 — instrument_master

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer pour instrument_master |
| Consumer | X | Aucun consumer pour instrument_master |
| Contract | X | Aucun contract class defini |
| DC View | X | Aucune view |
| Reader DeskPro | X | Aucun reader |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P1 — market_quote / market_trade / ohlcv_bar / order_book

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `collector_binance_spot` → pair_market_snapshot.v1 (spot snapshot uniquement) |
| Consumer | ~ | `desk_pro__spot_snapshot` → latest_only |
| Contract | ~ | pair_market_snapshot.v1 (prix spot only, pas OHLCV/order_book) |
| DC View | X | `pair_market_snapshot/` directory ABSENTE |
| Reader DeskPro | ~ | `spot_snapshot_reader.py` → path DC view (mais view absente) |
| Legacy Path | — | |
| Anomalies | A03, B02, C02, D01, G01 | |
| Manque | OHLCV bars, market trades, order book depth, multi-timeframe | |
| Score | **PARTIEL** | |

### P2 — position_state / risk_state / capital_state

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P3 — order_state / fill_event / execution_quality

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P4 — liquidity_microstructure

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `bot_vision_headless__coinglass` → vision_context.coinglass.v1 (liquidations/heatmap) |
| Consumer | ~ | `desk_pro__vision_context_coinglass` → L (legacy path) |
|  |  | `dashboards__screener_history` → OK (DC view history) |
| Contract | ~ | vision_context.coinglass.v1 (liquidations only, no spread/profondeur/imbalance) |
| DC View | X | Aucune view neutre dediee |
| Reader DeskPro | L | `vision_context_reader.py` → path legacy |
|  | L | `vision_panel.py` → path legacy |
| Legacy Path | OK | `data/deskpro/inputs/vision_context/coinglass/latest.json` EXISTE |
| Anomalies | A04, C05, C06, D02, G03 | |
| Manque | Spread, order book depth, imbalance, impact cost, volume profile | |
| Score | **PARTIEL** | |

### P5 — options_surface / volatility_surface / derivatives_state

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P6 — rates_credit_funding

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P7 — macro_event

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P8 — fundamental_snapshot / earnings_event / filing_event

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P9 — news_event / catalyst_event / sentiment_context

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `bot_vision_headless__news_sentiment` → vision_context.news_sentiment.v1 (sentiment score only) |
| Consumer | ~ | `desk_pro__vision_context_news_sentiment` → L (legacy path) |
|  |  | `dashboards__news_sentiment_history` → OK (DC view history) |
| Contract | ~ | vision_context.news_sentiment.v1 (sentiment only, no news events/catalysts) |
| DC View | X | Aucune view neutre dediee |
| Reader DeskPro | L | `vision_context_reader.py` → path legacy |
|  | L | `vision_panel.py` → path legacy |
| Legacy Path | X | `data/deskpro/inputs/vision_context/news_sentiment/latest.json` ABSENT |
| Anomalies | A04, C05, D02, G03 | |
| Manque | News events structures, catalysts, headlines, calendrier | |
| Score | **PARTIEL** | |

### P10 — flow_positioning

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `derivatives_collector__bitget` → market_metrics.v1 (OI, funding, liquidations, L/S) |
|  |  | `derivatives_collector__binance` → market_metrics.v1 (memes metriques) |
|  |  | `bot_vision_headless__coinglass` → vision_context.coinglass.v1 (liquidations, OI, funding) |
| Consumer | ~ | `desk_pro__market_metrics` → OK (latest_only) |
|  |  | `strategy_framework__market_context` → OK (by_symbol) |
|  |  | `perf_engine__replay_context` → OK (full_history) |
|  |  | `telegram_screener__signal_context` → OK (latest_only) |
|  |  | `google_sheets__market_reporting` → OK (latest_only) |
| Contract | ~ | market_metrics.v1 (OI, funding, liquidations, L/S — manque COT/ETF flows/borrow) |
| DC View | OK | `market_metrics/` (latest.json + by_symbol/) |
| Reader DeskPro | OK | `market_metrics_reader.py` → DC view primary + legacy fallback |
| Legacy Path | — | |
| Anomalies | A01, A02, C03, G06, G07 | |
| Manque | COT report, ETF flows, borrow rate, exchange reserves, whale alerts | |
| Score | **PARTIEL** | |

### P11 — technical_context

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `bot_vision_headless` → vision_analysis.v1 (support/resistance/trend/key levels visuels) |
| Consumer | ~ | `desk_pro__vision_analysis` → L (legacy path) |
|  |  | `dashboards__vision_analysis_history` → ~ (lit history/ mais seuls by_symbol/ existent) |
| Contract | ~ | vision_analysis.v1 (analyse visuelle, pas de structure technique automatisee) |
| DC View | ~ | `vision_analysis/by_symbol/` (20 symboles) |
|  |  | `vision_analysis/history/` ABSENT (reference par dashboards) |
| Reader DeskPro | L | `vision_analysis_reader.py` → path legacy |
| Legacy Path | X | `data/deskpro/inputs/vision_analysis/latest.json` ABSENT |
| Anomalies | A02, B01, C01, C04, D02, D04, G02 | |
| Manque | Indicateurs techniques derives, patterns automatises, multi-timeframe | |
| Score | **PARTIEL** | |

### P12 — model_signal / research_note

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer dedie |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P13 — alternative_data

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P14 — crypto_derivatives_state / onchain_flow

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `derivatives_collector__bitget` → market_metrics.v1 (OI, funding, liquidations, L/S) |
|  |  | `derivatives_collector__binance` → market_metrics.v1 (memes metriques) |
|  |  | `bot_vision_headless__coinglass` → vision_context.coinglass.v1 (liquidations, OI, funding, heatmap, L/S) |
| Consumer | ~ | Memes consumers que P10 + `desk_pro__vision_context_coinglass` (L) |
| Contract | ~ | market_metrics.v1 + vision_context.coinglass.v1 (pas d'onchain) |
| DC View | ~ | market_metrics OK / vision_context absent |
| Reader DeskPro | ~ | market_metrics OK / vision_context L |
| Legacy Path | ~ | coinglass legacy existe / market_metrics legacy absent |
| Anomalies | A01, A02, C01, C03, C05, G02, G03, G06, G07 | |
| Manque | Onchain wallets, exchange flows, DeFi TVL, staking, open interest options | |
| Score | **PARTIEL** | |

### P15 — commodity_inventory

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P16 — fx_context

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P17 — equity_context

| Dimension | Statut | Detail |
|---|---|---|
| Producer | ~ | `bot_vision_headless__screener` → vision_context.screener.v1 (stock price/change/volume) |
| Consumer | ~ | `desk_pro__vision_context_screener` → L (legacy path) |
|  |  | `dashboards__screener_history` → OK (DC view history) |
| Contract | ~ | vision_context.screener.v1 (screening basique) |
| DC View | X | Aucune view neutre dediee |
| Reader DeskPro | L | `vision_context_reader.py` → path legacy |
|  | L | `vision_panel.py` → path legacy |
| Legacy Path | X | `data/deskpro/inputs/vision_context/screener/latest.json` ABSENT |
| Anomalies | A04, C05, D02, G03 | |
| Manque | Float, short interest, ownership, earnings dates, buybacks, sector | |
| Score | **PARTIEL** | |

### P18 — compliance_state

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P19 — ops_settlement_state

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P20 — desk_memory

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer |
| Consumer | X | Aucun consumer |
| Contract | X | Aucun contract |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

### P21 — data_quality_state / source_score

| Dimension | Statut | Detail |
|---|---|---|
| Producer | X | Aucun producer (schema source_score.v1 absent) |
| Consumer | X | Aucun consumer |
| Contract | X | source_score.v1 / source_evidence.v1 / canonical_value.v1 / resolver_decision.v1 absents |
| DC View | X | |
| Reader DeskPro | X | |
| Legacy Path | — | |
| Anomalies | G08 | |
| Score | **ABSENT** | |

## Synthese

```text
COUVERT (OK)   : 0/22
PARTIEL (~)    : 7/22  → P1, P4, P9, P10, P11, P14, P17
ABSENT  (X)    : 15/22 → P0, P2, P3, P5, P6, P7, P8, P12, P13, P15, P16, P18, P19, P20, P21
```

## Blocs de remediation

### Bloc 1 — Infrastructure (priorite HIGH)

| ID | Categorie | Action |
|---|---|---|
| R01 | P1 | Creer `data/data_center/views/pair_market_snapshot/` view directory |
| R02 | P11+P14 | Corriger 4 producer paths vision (views/ → vision/<producer_id>/) |
| R03 | P4+P9+P17 | Creer 3 vision_context view directories neutres |

### Bloc 2 — Migration DeskPro (priorite HIGH)

| ID | Categorie | Action |
|---|---|---|
| R04 | P11 | Migrer `vision_analysis_reader.py` → DC view |
| R05 | P4 | Migrer `vision_context_reader.py` (coinglass) → DC view |
| R06 | P9 | Migrer `vision_context_reader.py` (news_sentiment) → DC view |
| R07 | P17 | Migrer `vision_context_reader.py` (screener) → DC view |
| R08 | — | Enregistrer `telegram_claim` dans consumers.json + migrer reader |
| R09 | P4+P9+P17 | Migrer `vision_panel.py` (x4 paths) → DC views |
| R10 | P11+P4+P9+P17 | Supprimer les paths legacy devenus orphelins apres migration |

### Bloc 3 — Multi-source scoring (priorite MEDIUM, apres bloc 1+2)

| ID | Categorie | Action |
|---|---|---|
| R11 | P10+P14 | Implementer `source_score.v1` pour market_metrics (bitget vs binance) |
| R12 | P10+P14 | Implementer `best_value_resolver` pour market_metrics |
| R13 | Global | Specifier `source_score.v1`, `source_evidence.v1`, `canonical_value.v1`, `resolver_decision.v1` |

### Bloc 4 — Extension categories absentes (priorite LOW, futur)

| ID | Categorie | Action |
|---|---|---|
| R14-R20 | P0, P2, P3 | Nouveaux producers pour instrument_master, position/risk/capital, execution/TCA |
| R21 | P5 | Nouveau producer pour vol surface / options |
| R22 | P6 | Nouveau producer pour rates/credit/funding |
| R23 | P7 | Nouveau producer pour macro events |
| R24 | P8 | Nouveau producer pour fondamentaux/earnings |
| R25 | P12 | Nouveau producer pour model signals/research |
| R26 | P13 | Nouveau producer pour alternative data |
| R27 | P15 | Nouveau producer pour commodities |
| R28 | P16 | Nouveau producer pour FX context |
| R29 | P18 | Nouveau producer pour compliance |
| R30 | P19 | Nouveau producer pour ops settlement |
| R31 | P20 | Nouveau producer pour desk memory |
| R32 | P21 | Nouveau producer pour data quality / source scoring |

### Bloc 5 — Completion categories partielles (priorite LOW, futur)

| ID | Categorie | Manque a combler |
|---|---|---|
| R33 | P1 | Ajouter OHLCV bars, order book, market trades |
| R34 | P4 | Ajouter spread, depth, imbalance, impact cost |
| R35 | P9 | Ajouter news events structures, catalysts, calendrier |
| R36 | P10 | Ajouter COT, ETF flows, borrow rate |
| R37 | P11 | Ajouter indicateurs techniques derives automatises |
| R38 | P14 | Ajouter onchain wallets, DeFi TVL, exchange flows |
| R39 | P17 | Ajouter float, short interest, ownership, buybacks |

## Total anomalies referencees

| Audit doc | IDs |
|---|---|
| 10_EXISTING_DATA_CENTER_SURFACES | A01, A02, A03, A04, A05 |
| 20_EXISTING_DESKPRO_CONSUMERS | B01, B02, B03, B04, B05, B06 |
| 30_EXISTING_PRODUCERS_AND_CONTRACTS | C01, C02, C03, C04, C05, C06 |
| 40_EXISTING_VIEWS_AND_PATHS | D01, D02, D03, D04, D05, D06 |
| 50_PRELIMINARY_GAPS | G01, G02, G03, G04, G05, G06, G07, G08 |

Total : 24 anomalies → 5 blocs de remediation
