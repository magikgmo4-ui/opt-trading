# SPACEX_SOURCE_MAP — repo zip à jour

## Surfaces confirmées dans le repo

| Surface | Chemins | Usage SpaceX |
|---|---|---|
| Data Center | `modules/data_center/*` | vues canonicalisées, runtime registry, consumers |
| External Producers | `modules/data_center/external_data_producers.py` | pattern API/fallback pour Yahoo/Finnhub/FRED/TwelveData |
| Google Sheets | `modules/google_sheets_global_schema/*`, `modules/data_center/google_sheets_market_reporting_consumer.py` | export métriques |
| Desk Pro | `modules/desk_pro/*` | UI/aggregation/alerts existants |
| Perf/Webhook | `modules/perf/app.py`, `modules/perf/webhook.py`, `tradingview/*` | alertes TradingView JSON |
| Bot Vision Headless | `modules/bot_vision/headless_capture/*` | screenshots/OCR/analyse |
| Coinglass Vision | `modules/analysis_bundles/app/coinglass_squeeze.py`, `modules/bot_vision/headless_capture/profiles.coinglass.json` | funding/liquidation/OI contexte |
| Telegram Screener | `modules/telegram_screener/*` | signal/alert pipeline |
| Vision Telegram | `modules/vision/coinglass/telegram_sender.py` | pattern envoi Telegram |

## Sources externes à brancher

- SEC EDGAR submissions/companyfacts.
- Yahoo public chart quote.
- Yahoo RSS / Nasdaq / MarketWatch / CNBC / Benzinga selon disponibilité.
- TradingView alerts côté utilisateur.
- Bot Vision profiles pages SPCX/corrélés.
- ETF holdings ARKX/UFO si données publiques disponibles.

## Priorité immédiate

1. Yahoo chart public pour prix/corrélés.
2. SEC submissions pour filings.
3. News RSS général avec filtres SpaceX/SPCX/Starlink.
4. TradingView alert receiver via webhook existant.
5. Bot Vision profile JSON.
