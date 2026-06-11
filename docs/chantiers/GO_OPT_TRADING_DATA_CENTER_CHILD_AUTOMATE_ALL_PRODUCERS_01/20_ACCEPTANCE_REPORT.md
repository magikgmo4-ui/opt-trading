# 20_ACCEPTANCE_REPORT — Full Automation

## Verdict: PASS ✅

Date: 2026-06-11 | Admin-trading live

### Pipeline horaire (11 producers)

| Step | Producer | Contract | Schedule |
|---|---|---|---|
| 1 | CoinGecko | market_metrics.v1 + pair_market_snapshot.v1 | hourly |
| 2 | Collector Telegram | (raw) | hourly |
| 3 | Bridge | telegram_signals + context + channel_stats | hourly |
| 4 | Source scoring | source_score.v1 | hourly |
| 5 | Signal events | signal_event.v1 | hourly |
| 6 | Telegram raw | telegram_raw.v1 | hourly |
| 7 | Runtime health | runtime_health.v1 | hourly |
| 8 | Position state | position_state.v1 | hourly |
| 9 | Crypto derivatives | crypto_derivatives_state.v1 + flow_positioning.v1 | hourly |
| 10 | Compliance | compliance_state.v1 | hourly |
| 11 | FX context (AlphaVantage) | fx_context.v1 | hourly (2 pairs/run) |

### Pipeline quotidien (5 producers, 02:00 UTC)

| Step | Producer | Contract |
|---|---|---|
| D1 | FRED | macro_event.v1 + rates_context.v1 |
| D2 | EIA | commodity_inventory.v1 |
| D3 | Yahoo Finance | fundamental_snapshot.v1 |
| D4 | Deribit | options_surface.v1 |
| D5 | Finnhub | news_event.v1 |

### Post-pipeline

| Step | Description |
|---|---|
| Backtest | --real mode with klines |
| Export | CSV + JSON for Google Sheets |
| Perf inject | events.jsonl + perf.db |

### Coverage finale

- **20/21 PROVEN** (P0 vendor excluded)
- **7 MISSING** (vendor/hors-scope)
- **16 producers automatisés**
- **0 manuels restants**
