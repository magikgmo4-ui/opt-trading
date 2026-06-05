---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_INVENTORY_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 10_PRO_DESK_DATA_INVENTORY_PLAN

## Objet

Transformer l'inventaire complet des donnees utilisees par des desks professionnels en checklist canonique Data Center.

## P0-P21 — classes a conserver distinctes

| Priority | Bloc data desk pro | Role |
|---|---|---|
| P0 | `instrument_master` | Identifier quoi trader |
| P1 | `market_quote`, `market_trade`, `ohlcv_bar`, `order_book` | Etat prix tradable |
| P2 | `position_state`, `risk_state`, `capital_state` | Survivre au risque |
| P3 | `order_state`, `fill_event`, `execution_quality` | Execution, routing, TCA |
| P4 | `liquidity_microstructure` | Profondeur, spread, impact, imbalance |
| P5 | `options_surface`, `volatility_surface`, `derivatives_state` | Vol, greeks, OI options |
| P6 | `rates_credit_funding` | Taux, credit, repo, funding |
| P7 | `macro_event` | CPI, NFP, FOMC, releases |
| P8 | `fundamental_snapshot`, `earnings_event`, `filing_event` | Fondamentaux entreprises |
| P9 | `news_event`, `catalyst_event`, `sentiment_context` | Catalyseurs texte |
| P10 | `flow_positioning` | COT, ETF flows, OI, borrow, liquidations |
| P11 | `technical_context` | Structure technique derivee |
| P12 | `model_signal`, `research_note` | Alpha interne, hypotheses, backtests |
| P13 | `alternative_data` | Web, satellite, app, shipping, social |
| P14 | `crypto_derivatives_state`, `onchain_flow` | Funding, OI, liquidations, wallets |
| P15 | `commodity_inventory` | Stocks, meteo, production, OPEC, EIA |
| P16 | `fx_context` | Forwards, carry, reserves, CB expectations |
| P17 | `equity_context` | Float, short, ownership, earnings, buybacks |
| P18 | `compliance_state` | Restrictions, audit, best execution, abuse flags |
| P19 | `ops_settlement_state` | Clearing, allocation, settlement, reconciliation |
| P20 | `desk_memory` | Notes, thesis, handover, post-trade reviews |
| P21 | `data_quality_state`, `source_score` | Freshness, lineage, score, entitlements |

## Regle

Aucune categorie P0-P21 ne doit etre minimisee, fusionnee ou traitee comme equivalente a une autre sans decision explicite.

## Sorties attendues dans les child GO

- `PRO_DESK_DATA_INVENTORY_CANONICAL.md`
- `pro_desk_data_inventory.json`
- `pro_desk_data_fields.json`
- `PRO_DESK_DATA_GAP_MATRIX.md`
