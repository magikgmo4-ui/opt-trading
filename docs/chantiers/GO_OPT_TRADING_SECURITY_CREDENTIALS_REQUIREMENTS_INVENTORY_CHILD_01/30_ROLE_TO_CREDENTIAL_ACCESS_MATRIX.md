# Role to Credential Access Matrix

| Rôle | Credentials Autorisés |
|------|----------------------|
| `telegram_collector` | `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SESSION_PATH` |
| `webhook_receiver` | `TV_WEBHOOK_SECRET` |
| `google_sheets_writer` | `GOOGLE_SERVICE_ACCOUNT_JSON_PATH`, `GOOGLE_SHEETS_SPREADSHEET_ID` |
| `git_dev` | `GH_TOKEN`, `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL` |
| `market_data_readonly` | `BINANCE_API_KEY`, `COINGLASS_API_KEY` |
| `deskpro_user` | (Accès FS local) |
| `llm_local` | `OLLAMA_BASE_URL` |
| `llm_cloud` | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` |
| `datacenter` | `DB_HOST`, `DB_USER`, `DB_PASSWORD` |
