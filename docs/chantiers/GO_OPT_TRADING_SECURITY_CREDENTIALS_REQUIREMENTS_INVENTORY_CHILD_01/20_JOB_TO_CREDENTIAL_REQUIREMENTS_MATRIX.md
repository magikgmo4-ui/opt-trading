# Job to Credential Requirements Matrix

| Service | Job | Credentials Requis |
|---------|-----|-------------------|
| Telegram | `telegram_collect_channel` | `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SESSION_PATH` |
| TradingView | `tv_webhook_receive` | `TV_WEBHOOK_SECRET` |
| Google Sheets | `sheets_append_rows` | `GOOGLE_SERVICE_ACCOUNT_JSON_PATH`, `GOOGLE_SHEETS_SPREADSHEET_ID` |
| GitHub | `repo_ops` | `GH_TOKEN` |
| Market Data | `market_snapshot_fetch` | `BINANCE_API_KEY`, `BINANCE_SECRET_KEY`, `COINGLASS_API_KEY` |
| DeskPro | `deskpro_analysis` | (Chemins locaux, pas de secrets globaux) |
| LLM Local | `llm_local_inference` | `OLLAMA_BASE_URL` |
| LLM Cloud | `llm_cloud_inference` | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` |
| Data Center | `db_maintenance` | `DB_HOST`, `DB_USER`, `DB_PASSWORD` |
