# 30_DATA_SOURCE_MAP — Sources de donnees par commande

## Sources primaires

| Source | Path | Format |
|---|---|---|
| vision_analysis | data/data_center/views/vision_analysis/by_symbol/{sym}.json | JSON: price, trend, direction, confidence, freshness_state |
| market_metrics | data/data_center/views/market_metrics/by_symbol/{sym}.json | JSON: vwap, volume_24h, rsi_14, price |
| signal_event | data/data_center/views/signal_event.v1/... | JSON: signal type, direction, invalidation |
| spacex_true_value | data/data_center/views/spacex_true_value.v1/by_symbol/{sym}.json | JSON: final_grade, true_value_score, confidence_score, hype_score, risk_score |
| crypto_derivatives | data/data_center/views/crypto_derivatives_state.v1/... | JSON: funding_rate, open_interest, long_short_ratio |
| fx_context | data/data_center/views/fx_context.v1/... | JSON: DXY, correlations |
| command_center | data/ipo/spacex/command_center/latest.json | JSON: price, vwap, gap_pct, top_setup, confidence, edge_score |
| snapshots | data/ipo/spacex/scored/latest_snapshot.json | JSON: scores, vwap_analysis, orderflow_score, ownership_score |
| perf_open | HTTP /perf/open (port 8010) | JSON: open trades list |
| perf_summary | HTTP /perf/summary (port 8010) | JSON: total_trades, winrate |
| deskpro_status | HTTP /desk/status (port 8010) | JSON: service health |
| deskpro_alerts | HTTP /desk/alerts (port 8010) | JSON: alert list |
| deskpro_snapshot | HTTP /desk/spacex/snapshot (port 8010) | JSON: full SPCX snapshot |
| telegram_signals | HTTP /cms/signals/summary (port 8010) | JSON: signal summary |
| localcms_menu | HTTP /cms/menu/state (port 8010) | JSON: menu state |
| daily_reports | outputs/stock_true_value/daily/*_report.md | Markdown: daily analysis |
| dc_registry | data/data_center/ | Repertoire: nombre de contrats v1 |

## Source par commande

| Commande | Sources lues |
|---|---|
| Etat systeme | HTTP deskpro + perf + localcms + memory + filesystem DC registry |
| Rapport marche | HTTP /read/spacex + filesystem vision_analysis + market_metrics |
| Analyse BTC | filesystem vision_analysis + market_metrics + signal_event + crypto_derivatives |
| Analyse Gold | filesystem vision_analysis + HTTP perf_open + fx_context |
| Resume SPCX | HTTP /read/spacex + filesystem command_center + spacex_true_value |
| Alertes Telegram | HTTP /read/alerts |
| Setups actifs | HTTP /read/setups |
| Setup BTC/Gold/SPCX | HTTP /read/setup + /read/setups |
| Score BTC/Gold/SPCX | filesystem spacex_true_value.v1 |
| Rapport quotidien | filesystem outputs/stock_true_value/daily/ |
| Priorites | HTTP /read/setups + /read/spacex + analysis_report + priority_engine |
| Attention | HTTP /read/setups + /read/spacex + alerts + priority_engine |
| Top movers | filesystem vision_analysis + market_metrics |
| Resume executif | HTTP /read/alerts + /read/setups + /read/spacex + analysis_report |
| Watchlist IA | filesystem spacex_true_value.v1 |
| Watchlist spatial | filesystem spacex_true_value.v1 |
