# PRO_DESK_DATA_GAP_MATRIX — P0-P21 vs Existant Data Center

## Légende

| Status | Description |
|---|---|
| ✅ PROVEN | Producer + contrat + consumer + view existent |
| 🟡 PARTIAL | Producer existe mais contrat/view incomplet |
| 🔶 DECLARED | Déclaré dans registry mais pas implémenté |
| ❌ MISSING | Aucun producer, contrat, ni consumer |
| ⏳ FUTURE | Hors scope immédiat, candidat identifié |

## Gap Matrix

| P | Bloc | Contrat cible | Producer existant | Consumer DeskPro | View DC | Status |
|---|---|---|---|---|---|---|
| P0 | Instrument master | `instrument_master.v1` | ❌ | ❌ | ❌ | ❌ MISSING (vendor payant) |
| P1 | Market quote/price | `market_metrics.v1` | ✅ coingecko | ✅ desk_pro__market_metrics | ✅ | ✅ PROVEN |
| P1 | OHLCV snapshot | `pair_market_snapshot.v1` | ✅ coingecko | ✅ desk_pro__spot_snapshot | ✅ | ✅ PROVEN |
| P1 | OHLCV history | `market_klines.v1` | ✅ coingecko/binance | ❌ | 🟡 | 🟡 PARTIAL |
| P2 | Position state | `position_state.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P2 | Risk state | `risk_state.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P2 | PnL / capital | `pnl_state.v1` | 🟡 perf_app (SQLite) | ❌ | ❌ | 🔶 DECLARED |
| P3 | Order state | `order_state.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P3 | Fill events | `fill_event.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P4 | OI / funding / liq | `market_metrics.v1` | ✅ bitget/binance derivatives | ✅ | 🟡 | 🟡 PARTIAL |
| P4 | Liquidity heatmap | `vision_context.coinglass.v1` | ✅ coinglass headless | ✅ | ✅ | ✅ PROVEN |
| P5 | Options surface | `options_surface.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P6 | Rates / credit | `rates_context.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P7 | Macro events | `macro_event.v1` | ✅ FRED + 🟡 bot_vision | ❌ | ✅ | ✅ PROVEN |
| P8 | Fundamentals | `fundamental_snapshot.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P9 | News / sentiment | `news_event.v1` | ✅ finnhub + 🟡 bot_vision | ✅ | ✅ | ✅ PROVEN |
| P10 | Flows / positioning | `flow_positioning.v1` | 🟡 data_center_aggregator + 🟡 bot_vision | ❌ | ✅ | 🟡 PARTIAL |
| P11 | Technical analysis | `vision_analysis.v1` | ✅ bot_vision | ✅ | ✅ | ✅ PROVEN |
| P12 | Model signals | `telegram_signal.v1` | ✅ telegram_screener | 🟡 telegram_claim | ✅ | 🟡 PARTIAL |
| P13 | Alternative data | `alternative_data.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P14 | Crypto derivatives | `crypto_derivatives_state.v1` | 🟡 OI/funding/liq | ❌ | ❌ | 🔶 DECLARED |
| P15 | Commodities | `commodity_inventory.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P16 | FX context | `fx_context.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P17 | Equity screener | `vision_context.screener.v1` | ✅ bot_vision | ✅ | ✅ | ✅ PROVEN |
| P18 | Compliance | `compliance_state.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P19 | Ops / settlement | `ops_state.v1` | ❌ | ❌ | ❌ | ❌ MISSING |
| P20 | Desk memory | `desk_memory.v1` | ❌ | ❌ | ❌ | ⏳ FUTURE |
| P21 | Data quality | `source_score.v1` | 🟡 schema prêt | ❌ | ❌ | 🔶 DECLARED |
| — | Signal events | `signal_event.v1` | ✅ webhook | ❌ | ✅ | ✅ PROVEN |
| — | Telegram raw | `telegram_raw.v1` | ✅ collector | ❌ | ✅ | ✅ PROVEN |
| — | Runtime health | `runtime_health.v1` | ✅ runtime_health | ❌ | ✅ | ✅ PROVEN |
| — | Telegram context | `telegram_context.v1` | ✅ bridge | ❌ | ✅ | ✅ PROVEN |
| — | Channel stats | `telegram_channel_stats.v1` | ✅ bridge | ❌ | ✅ | ✅ PROVEN |

## Résumé

| Statut | Count |
|---|---|
| ✅ PROVEN | 13 |
| 🟡 PARTIAL | 4 |
| 🔶 DECLARED | 4 |
| ❌ MISSING | 14 |
| ⏳ FUTURE | 1 |

**Total: 36 data items across P0-P21 + extensions**

## Prochains GO candidats

| Priorité | GO | Gap | Effort |
|---|---|---|---|
| P0 | `BEST_VALUE_RESOLVER_02` | Brancher resolver sur market_metrics + coinglass | 2h |
| P1 | `SOURCE_SCORING_01` | Implémenter source_score.v1 avec scores réels | 3h |
| P1 | `POSITION_RISK_DC_WRITER` | Router position/risk state → DC views | 2h |
| P1 | `PNL_DC_WRITER` | Exporter perf.db → DC views | 2h |
| P2 | `OHLCV_HISTORY_CONSUMER` | Consommer klines dans DeskPro/backtest | 2h |
| P2 | `CRYPTO_DERIVATIVES_VIEW` | Consolider OI/funding/liq → crypto_derivatives_state.v1 | 2h |
| P2 | `FLOW_POSITIONING_VIEW` | Agréger OI + liquidations + whale → flow_positioning.v1 | 2h |
