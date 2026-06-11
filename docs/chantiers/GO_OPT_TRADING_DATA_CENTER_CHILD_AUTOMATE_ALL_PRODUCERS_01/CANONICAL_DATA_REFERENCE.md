# Data Center — Canonical Data Reference

## Naming Convention

```
{domain}_{type}.v{version}
Ex: market_metrics.v1, fx_context.v1, telegram_signal.v1
```

- `domain` = source domain (market, fx, telegram, vision, position...)
- `type` = data shape (metrics, context, signal, snapshot, state, event, score)
- `v1` = contract version

---

## 1. Market Data

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| M1 | `market_metrics.v1` | Métriques marché | coingecko_public_api | hourly | `{symbol, metrics: {price, change_24h_pct}}` | 0.85 | price, price_change_24h_pct |
| M2 | `pair_market_snapshot.v1` | Snapshot paire | coingecko_public_api | hourly | `{symbol, snapshot: {price, change_24h_pct}, freshness_state}` | 0.85 | price, change_24h_pct, freshness |
| M3 | `market_klines.v1` | Historique OHLCV | coingecko_public_api / twelvedata | daily | `{symbol, interval, klines: [{open_time_iso, open, high, low, close}]}` | 0.80 | open, high, low, close, volume |
| M4 | `fx_context.v1` | Contexte Forex | alphavantage | hourly (2 pairs) | `{symbol, rate, bid, ask, refresh_ts}` | 0.70 | rate, bid, ask |
| M5 | `rates_context.v1` | Contexte Taux | fred | daily | `{rates: {label: {value, date}}}` | 0.78 | Fed Funds, 10Y, 2Y, Spread |
| M6 | `macro_event.v1` | Événements Macro | fred | daily | `{indicators: {id: {label, value, unit, date}}}` | 0.78 | GDP, CPI, Unemployment, VIX |
| M7 | `commodity_inventory.v1` | Matières premières | eia | daily | `{commodities: {label: {last_value, unit}}}` | 0.55 | WTI, Brent, NatGas |
| M8 | `fundamental_snapshot.v1` | Fondamentaux | yahoo_finance | daily | `{tickers: {symbol: {price, currency}}}` | 0.45 | price, previous_close, currency |
| M9 | `options_surface.v1` | Surface options | deribit_public | daily | `{surfaces: {BTC/ETH: {total_options, sample}}}` | 0.60 | total_options, strikes |

---

## 2. Vision & Analysis

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| V1 | `vision_analysis.v1` | Analyse technique | bot_vision_headless | 10min | `{symbol, timeframe, signals: [{type, value, confidence}]}` | 0.90 | support, resistance, trend, invalidation |
| V2 | `vision_context.coinglass.v1` | Contexte Coinglass | bot_vision_headless__coinglass | 1h | `{symbol, detections: [{detected_metric_type, extracted_value}]}` | 0.85 | OI, liquidations_long, liquidations_short, long_short_ratio, heatmap |
| V3 | `vision_context.screener.v1` | Screener Stocks | bot_vision_headless__screener | 6h | `{screener_label, stocks: [{symbol, price, change_pct}]}` | 0.70 | symbol, price, change_pct, volume |
| V4 | `vision_context.news_sentiment.v1` | Sentiment News | bot_vision_headless__news_sentiment | 6h | `{sentiment_label, articles, avg_score}` | 0.70 | sentiment_label, avg_sentiment_score, article_count |

---

## 3. Telegram Signals

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| T1 | `telegram_signal.v1` | Signal Trade | telegram_screener_bridge | hourly | `{pair, direction, entry_price, sl, tp, channel, confidence}` | 0.88 | entry_price, sl, tp, direction, channel |
| T2 | `telegram_context.v1` | Contexte Telegram | telegram_screener_bridge | hourly | `{signal_type, asset, direction, amount, value_usd}` | 0.82 | whale flows, onchain alerts |
| T3 | `telegram_channel_stats.v1` | Stats Canaux | telegram_screener_bridge | hourly | `{channels: [{channel, total_messages, complete_setups, parse_rate}]}` | 0.80 | trade_setups, complete_setups, candidate_score |
| T4 | `telegram_raw.v1` | Messages Bruts | collector_telegram | hourly | `{channel, total_messages, messages: [{message_id, raw_text}]}` | 0.75 | raw_text, timestamp |

---

## 4. Trading Runtime

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| R1 | `signal_event.v1` | Événements Signal | webhook_server | hourly | `{symbol, total_events, events: [{engine, signal, price, sl, tp}]}` | 0.85 | engine, signal, price, tp, sl, qty |
| R2 | `position_state.v1` | État Positions | position_engine | hourly | `{positions: {symbol: {...}}}` | 0.50 | position data from state/positions.json |
| R3 | `compliance_state.v1` | État Conformité | risk_engine | hourly | `{risk_config, checks: {accounts_defined}}` | 0.45 | accounts, risk limits, allowed symbols |
| R4 | `runtime_health.v1` | Santé Runtime | runtime_health | hourly | `{services_status: {webhook, perf, localcms}}` | 0.75 | service status, uptime |

---

## 5. Derivatives & Flows

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| D1 | `crypto_derivatives_state.v1` | Dérivés Crypto | data_center_aggregator | hourly | `{metrics: {metric_type: {value, source}}}` | 0.55 | OI, funding, liquidations (aggregated) |
| D2 | `flow_positioning.v1` | Positionnement Flux | data_center_aggregator | hourly | `{sources: [{source, count}]}` | 0.50 | whale transfers, liquidation context |

---

## 6. Meta & Quality

| # | Contract | Label FR | Provider | Schedule | Format | Score | Fields |
|---|---|---|---|---|---|---|---|
| Q1 | `source_score.v1` | Score Fiabilité | source_scoring_engine | hourly | `{source_id, final_score, dimensions: {freshness, completeness, ...}}` | 0.85 | freshness, completeness, schema_validation, latency, consistency, uptime |
| Q2 | `canonical_value.v1` | Valeur Canonique | canonical_value_publisher | on-demand | `{contract_class, symbol, data_key, canonical_value, winning_producer_id}` | — | resolved value + metadata |
| Q3 | `resolver_decision.v1` | Décision Resolver | source_selector | on-demand | `{decision_id, selected_producer_id, selection_rule, candidates}` | — | which source won + why |

---

## 7. Backtest

| # | Contract | Label FR | Provider | Schedule | Format | Fields |
|---|---|---|---|---|---|---|
| B1 | `telegram_backtest.v1` | Backtest Signals | trading_lab_v1 | hourly | `{mode, grand_total: {trades, wins, losses, winrate_pct, avg_r, total_pnl}, by_channel: [...]}` | trades, wins, losses, winrate, avg_r, pnl |
| B2 | `backtest_export.v1` | Export Backtest | trading_lab_v1 | hourly | `{by_channel: [{channel, trades, wins, losses, winrate_pct, avg_r, pnl}]}` | per-channel summary |

---

## Query Reference — Data Keys

### Pour demander une donnée au resolver

```python
# Format: contract_class + symbol + data_key
resolve_and_publish("market_metrics.v1", "BTC/USDT", "price")
resolve_and_publish("vision_context.coinglass.v1", "BTCUSDT", "open_interest")
resolve_and_publish("fx_context.v1", "EUR/USD", "rate")
resolve_and_publish("macro_event.v1", "US", "FEDFUNDS")
resolve_and_publish("telegram_signal.v1", "XAU/USD", "entry_price")
```

### Data Keys disponibles par contrat

| Contract | Data Keys |
|---|---|
| `market_metrics.v1` | `price`, `price_change_24h_pct` |
| `pair_market_snapshot.v1` | `price`, `change_24h_pct` |
| `vision_context.coinglass.v1` | `open_interest`, `liquidations_long`, `liquidations_short`, `long_short_ratio`, `liquidation_heatmap_level` |
| `vision_analysis.v1` | `support_level`, `resistance_level`, `trend` |
| `telegram_signal.v1` | `signal_count`, `active_channels` |
| `fx_context.v1` | `rate`, `bid`, `ask` |
| `macro_event.v1` | `FEDFUNDS`, `GDP`, `CPIAUCSL`, `UNRATE`, `DGS10`, `T10Y2Y`, `VIXCLS` |
| `rates_context.v1` | `Fed Funds`, `10Y Yield`, `2Y Yield`, `10Y-2Y Spread` |
| `crypto_derivatives_state.v1` | `open_interest`, `liquidations_long`, `liquidations_short`, `long_short_ratio` |
| `source_score.v1` | `freshness`, `completeness`, `schema_validation`, `final_score` |

---

## Classification par domaine

| Domaine | Contrats | Count |
|---|---|---|
| 📊 Market | M1-M9 | 9 |
| 👁️ Vision | V1-V4 | 4 |
| 📡 Telegram | T1-T4 | 4 |
| ⚡ Runtime | R1-R4 | 4 |
| 🔗 Derivatives | D1-D2 | 2 |
| 🛡️ Quality | Q1-Q3 | 3 |
| 🧪 Backtest | B1-B2 | 2 |
| **Total** | | **28 contrats** |
