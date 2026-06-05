---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_DATA_CLASSES_P0_P21
doc_type: inventory
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 20_PRO_DESK_DATA_CLASSES_P0_P21

## Canonical data classes

| Priority | Canonical data class | Role | Candidate contracts |
|---|---|---|---|
| P0 | `instrument_master` | Instrument identity, specs, calendars | `instrument_master.v1`, `contract_specs.v1`, `trading_calendar.v1` |
| P1 | `market_state` | Tradable prices and market state | `market_quote.v1`, `market_trade.v1`, `ohlcv_bar.v1`, `order_book.v1`, `pair_market_snapshot.v1` |
| P2 | `risk_and_position_state` | Internal risk, PnL, exposure | `position_state.v1`, `risk_state.v1`, `capital_state.v1`, `exposure_state.v1` |
| P3 | `execution_state` | Orders, fills, routing, TCA | `order_state.v1`, `fill_event.v1`, `execution_quality.v1`, `routing_state.v1` |
| P4 | `liquidity_microstructure` | Depth, imbalance, spread, impact | `liquidity_microstructure.v1`, `order_flow.v1`, `auction_imbalance.v1` |
| P5 | `options_vol_derivatives` | Vol surface, greeks, expiry, options OI | `options_surface.v1`, `volatility_surface.v1`, `greeks_state.v1`, `derivatives_state.v1` |
| P6 | `rates_credit_funding` | Rates, curves, repo, credit, funding | `rates_curve.v1`, `credit_spread.v1`, `funding_context.v1`, `bond_snapshot.v1` |
| P7 | `macro_context` | Calendar and macro releases | `macro_event.v1`, `economic_release.v1`, `central_bank_event.v1` |
| P8 | `fundamental_context` | Company fundamentals and filings | `fundamental_snapshot.v1`, `earnings_event.v1`, `filing_event.v1`, `estimate_revision.v1` |
| P9 | `news_event_context` | News, catalysts, sentiment | `news_event.v1`, `catalyst_event.v1`, `sentiment_context.v1` |
| P10 | `flow_positioning` | OI, ETF flows, COT, borrow, liquidations | `flow_positioning.v1`, `market_metrics.v1`, `borrow_state.v1`, `liquidation_state.v1` |
| P11 | `technical_context` | Technical structure and vision-derived levels | `technical_context.v1`, `vision_analysis.v1` |
| P12 | `model_research_signal` | Internal model outputs and research | `model_signal.v1`, `research_note.v1`, `signal_event.v1`, `strategy_eval.v1` |
| P13 | `alternative_data` | Non-market external data | `alternative_data.v1`, `web_traffic.v1`, `shipping_flow.v1`, `weather_context.v1` |
| P14 | `crypto_specific_context` | Crypto derivatives and on-chain | `crypto_derivatives_state.v1`, `onchain_flow.v1`, `stablecoin_flow.v1`, `token_unlock.v1` |
| P15 | `commodity_specific_context` | Inventories, production, weather | `commodity_inventory.v1`, `energy_supply.v1`, `metals_inventory.v1`, `agri_report.v1` |
| P16 | `fx_specific_context` | FX rates, forwards, carry, reserves | `fx_context.v1`, `fx_forward_curve.v1`, `carry_context.v1`, `reserve_flow.v1` |
| P17 | `equity_specific_context` | Equity float, borrow, ownership, events | `equity_context.v1`, `short_interest.v1`, `ownership_state.v1`, `corporate_action.v1` |
| P18 | `compliance_restriction_state` | Restricted lists, abuse, audit constraints | `compliance_state.v1`, `restricted_list.v1`, `best_execution_evidence.v1` |
| P19 | `ops_settlement_state` | Settlement, clearing, allocation, reconciliation | `settlement_state.v1`, `allocation_state.v1`, `reconciliation_break.v1` |
| P20 | `desk_memory` | Notes, thesis, handover, review | `desk_note.v1`, `trade_thesis.v1`, `handover_note.v1`, `post_trade_review.v1` |
| P21 | `data_quality_lineage` | Freshness, source, score, lineage, entitlement | `data_quality_state.v1`, `source_score.v1`, `source_evidence.v1`, `resolver_decision.v1`, `canonical_value.v1` |

## Current coverage flags from previous child summary

| Priority group | Coverage declared by audit summary |
|---|---|
| Complete | 0/22 |
| Partial | 7/22 |
| Absent | 15/22 |

## Partial coverage candidates to validate in mapping child

- P1 via `pair_market_snapshot.v1`.
- P9 via `vision_context.news_sentiment.v1`.
- P10 via `market_metrics.v1` and `vision_context.coinglass.v1`.
- P11 via `vision_analysis.v1`.
- P14 via derivatives and Coinglass context.
- P17 via `vision_context.screener.v1`.
- P21 partially implicit through registry metadata, but no dedicated source scoring yet.

## Rule

Coverage remains `partial` unless fields, sources, freshness, view path, consumer path and validation rules are all documented.
