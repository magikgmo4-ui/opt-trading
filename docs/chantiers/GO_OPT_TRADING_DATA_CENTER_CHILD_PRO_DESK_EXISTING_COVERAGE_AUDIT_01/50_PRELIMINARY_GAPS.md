---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_PRELIMINARY_GAPS
doc_type: audit
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
---

# 50_PRELIMINARY_GAPS

## Objet

Gap matrix preliminaire : croiser l'inventaire P0-P21 du parent avec l'existant audite. Identifier les categories couvertes, partiellement couvertes, absentes, et les gaps d'infrastructure.

## 1. Gap matrix P0-P21

| P | Bloc data desk pro | Coverage | Detail |
|---|---|---|---|
| P0 | instrument_master | ABSENT | Aucun producer/contract/consumer pour l'identification des instruments |
| P1 | market_quote, market_trade, ohlcv_bar, order_book | PARTIEL | `pair_market_snapshot.v1` couvre prix spot snapshot uniquement. Pas d'OHLCV bars, pas de order book, pas de market trades |
| P2 | position_state, risk_state, capital_state | ABSENT | Aucun producer/contract/consumer pour les etats position/risque/capital |
| P3 | order_state, fill_event, execution_quality | ABSENT | Aucun producer/contract/consumer pour execution/TCA |
| P4 | liquidity_microstructure | PARTIEL | `vision_context.coinglass.v1` detecte liquidations mais pas spread/profondeur/imbalance/impact |
| P5 | options_surface, volatility_surface, derivatives_state | ABSENT | Aucun producer pour vol surface, greeks, OI options |
| P6 | rates_credit_funding | ABSENT | Aucun producer pour taux/credit/repo |
| P7 | macro_event | ABSENT | Aucun producer pour CPI/NFP/FOMC/releases |
| P8 | fundamental_snapshot, earnings_event, filing_event | ABSENT | Aucun producer pour fondamentaux |
| P9 | news_event, catalyst_event, sentiment_context | PARTIEL | `vision_context.news_sentiment.v1` couvre sentiment (score uniquement). Pas de news events structures, pas de catalysts |
| P10 | flow_positioning | PARTIEL | `market_metrics.v1` (bitget/binance) couvre OI, funding, liquidations, L/S ratio. Manque : COT, ETF flows, borrow rate |
| P11 | technical_context | PARTIEL | `vision_analysis.v1` (bot_vision_headless) couvre support/resistance/trend/key levels. Pas de structure technique derivee automatisee |
| P12 | model_signal, research_note | ABSENT | Aucun producer pour alpha interne/backtests/hypotheses |
| P13 | alternative_data | ABSENT | Aucun producer pour web/satellite/app/shipping/social alt data |
| P14 | crypto_derivatives_state, onchain_flow | PARTIEL | `market_metrics.v1` + `vision_context.coinglass.v1` couvrent OI, funding, liquidations. Manque : onchain wallets/flows |
| P15 | commodity_inventory | ABSENT | Aucun producer pour stocks/meteo/production/OPEC/EIA |
| P16 | fx_context | ABSENT | Aucun producer pour forwards/carry/reserves/CB expectations |
| P17 | equity_context | PARTIEL | `vision_context.screener.v1` couvre screening equities basique. Manque : float, short interest, ownership, buybacks |
| P18 | compliance_state | ABSENT | Aucun producer pour restrictions/audit/best execution/abuse flags |
| P19 | ops_settlement_state | ABSENT | Aucun producer pour clearing/allocation/settlement/reconciliation |
| P20 | desk_memory | ABSENT | Aucun producer pour notes/thesis/handover/post-trade reviews |
| P21 | data_quality_state, source_score | ABSENT | Aucun source_score.v1, source_evidence.v1, canonical_value.v1, resolver_decision.v1 |

## 2. Synthese

```text
COUVERT        : 0/22
PARTIEL        : 6/22 (P1, P4, P9, P10, P11, P14, P17)
ABSENT         : 15/22
```

## 3. Gaps d'infrastructure

### 3.1 Views manquantes

| Gap | Impact |
|---|---|
| `pair_market_snapshot` view directory | Consumer desk_pro__spot_snapshot lit un path inexistant |
| `vision_context/coinglass` view neutre | Consumer desk_pro lit path legacy, pas de view |
| `vision_context/screener` view neutre | Consumer desk_pro lit path legacy, pas de view |
| `vision_context/news_sentiment` view neutre | Consumer desk_pro lit path legacy, pas de view |

### 3.2 Migration DeskPro incomplete

| Reader | Statut | Action |
|---|---|---|
| vision_analysis_reader.py | LEGACY | Migrer vers DC view |
| vision_context_reader.py (x3) | LEGACY | Migrer vers DC view (x3) |
| telegram_claim_reader.py | LEGACY | Ajouter au registry + migrer vers DC view |
| vision_panel.py (x4) | LEGACY | Migrer vers DC view (x4) |

### 3.3 Producer path convention violations

| Producer | Action |
|---|---|
| bot_vision_headless | Corriger output_path_root → `data/data_center/vision/bot_vision_headless/` |
| bot_vision_headless__coinglass | Corriger output_path_root → `data/data_center/vision/bot_vision_headless__coinglass/` |
| bot_vision_headless__screener | Corriger output_path_root → `data/data_center/vision/bot_vision_headless__screener/` |
| bot_vision_headless__news_sentiment | Corriger output_path_root → `data/data_center/vision/bot_vision_headless__news_sentiment/` |

### 3.4 Multi-source non resolu

| Contract | Sources | Action |
|---|---|---|
| market_metrics.v1 | bitget, binance | Implementer source scoring + best-value resolver |

### 3.5 Producers jamais executes

Les 7 producers ont `last_write: null`. Aucune donnee fraiche n'a ete produite par un producer enregistre. Ceci est potentiellement normal (collectors oneshot non actives) mais doit etre verifie.

### 3.6 Consumers orphelins ou non enregistres

| Consumer | Statut |
|---|---|
| desk_pro__spot_snapshot | View directory absente |
| telegram_claim (reader only) | Non enregistre dans consumers.json |
| vision_panel (x4 paths) | Non enregistres dans consumers.json |

## 4. Priorites de remediation

### Bloc 1 : Infrastructure (avant source scoring)

1. Creer `pair_market_snapshot` view directory.
2. Corriger les 4 producer paths vision (views/ → vision/<producer_id>/).
3. Creer les 3 vision_context view directories neutres.

### Bloc 2 : Migration DeskPro (avant source scoring)

4. Migrer `vision_analysis_reader.py` vers DC view.
5. Migrer `vision_context_reader.py` (x3) vers DC views.
6. Enregistrer `telegram_claim` dans consumers.json + migrer reader.
7. Migrer `vision_panel.py` (x4) vers DC views.
8. Supprimer les paths legacy restants apres migration.

### Bloc 3 : Multi-source (apres bloc 1+2)

9. Implementer `source_score.v1` pour market_metrics (bitget vs binance).
10. Implementer `best_value_resolver` pour market_metrics.

### Bloc 4 : Extension P0-P21 (futur)

11-26. Ajouter producers/contracts/views pour les categories P0, P2, P3, P5, P6, P7, P8, P12, P13, P15, P16, P18, P19, P20, P21 + completer P1, P4, P9, P10, P11, P14, P17.

## 5. Anomalies resume

| ID | Bloc | Description |
|---|---|---|
| G01 | Infrastructure | pair_market_snapshot view absente |
| G02 | Infrastructure | 4 producers vision ecrivent dans views/ (path convention violee) |
| G03 | Infrastructure | 3 vision_context views absentes |
| G04 | Migration | 4 readers DeskPro non migres vers DC views |
| G05 | Migration | telegram_claim non enregistre dans consumers.json |
| G06 | Multi-source | market_metrics 2 sources, pas de source scoring |
| G07 | Runtime | Tous les producers last_write = null |
| G08 | Extension | 15 categories P0-P21 absentes, 7 partielles |
