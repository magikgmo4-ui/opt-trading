# Credentials Fleet Inventory — 2026-06-11

Audit, synchronisation et validation complète des credentials sur toute la fleet.

## Fleet

| Machine | OS | Rôle | `.env` path |
|---------|-----|------|-------------|
| db-layer | Ubuntu | operator UI / source de vérité | `/opt/trading/.env` + `/etc/opt-trading/env.d/roles/` |
| admin-trading | Ubuntu | backend / orchestration | `/opt/trading/.env` |
| student | Ubuntu | auxiliary AI | `/opt/trading/.env` |
| cursor-ai | Windows | dev station | `C:\Users\ghost\opt-trading\.env` |
| fantome | Ubuntu | auxiliary | `/home/fantome/opt-trading/.env` |

## Validation API live — 10/10 clés répondent HTTP 200 ✓

| Clé | Provider | Status |
|-----|----------|--------|
| `COINGECKO_API_KEY` | CoinGecko Demo | ✅ 200 |
| `ALPHAVANTAGE_API_KEY` | Alpha Vantage | ✅ 200 |
| `FRED_API_KEY` | FRED / St. Louis Fed | ✅ 200 |
| `EIA_API_KEY` | EIA | ✅ 200 |
| `FINNHUB_API_KEY` | Finnhub | ✅ 200 |
| `TWELVEDATA_API_KEY` | Twelve Data | ✅ 200 |
| `OPENAI_API_KEY` | OpenAI | ✅ 200 |
| `CLICKUP_TOKEN` | ClickUp | ✅ 200 |
| `GH_TOKEN` | GitHub | ✅ 200 |
| `AIRTABLE_API_KEY` | Airtable | ✅ 200 |

## Matrice complète — 43 vars — état final

| Var | db-layer | admin-trading | student | cursor-ai | fantome |
|-----|----------|---------------|---------|-----------|---------|
| `TV_WEBHOOK_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `OPS_ADMIN_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_BOT_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_API_ID` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_API_HASH` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_SESSION_PATH` | ✓ | ✓ | ✓ | — (Windows N/A) | ✓ |
| `TELEGRAM_ALERT_CHAT_ID` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_CHANNELS_CONFIG` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_CHAT_ID_ALERTS` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_CHAT_ID_PIPELINE` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_CHAT_ID_PUSH` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_CHAT_ID_OPS` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_ALLOWED_CHAT_IDS` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TELEGRAM_ALLOWED_USER_IDS` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `GH_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `IDENTITY_FILE` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `GOOGLE_APPLICATION_CREDENTIALS` | ✓ | ✓ | ✓ | — (Windows N/A) | ✓ |
| `AIRTABLE_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `AIRTABLE_BASE_ID` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `AIRTABLE_TABLE_GO_STATUS` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `OPENAI_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `OLLAMA_BASE_URL` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `CLICKUP_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `COINGECKO_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ALPHAVANTAGE_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `FRED_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `EIA_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `FINNHUB_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `TWELVEDATA_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_BINANCE_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_BYBIT_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_OKX_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_KRAKEN_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_COINBASE_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_DEFILLAMA_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_STOOQ_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_CFTC_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_SEC_EDGAR_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENABLE_GDELT_PUBLIC` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `BINANCE_API_KEY` | — | — | — | — | — |
| `BINANCE_API_SECRET` | — | — | — | — | — |
| `ENABLE_BINANCE_PRIVATE` | ✓ (=0) | ✓ (=0) | ✓ (=0) | ✓ (=0) | ✓ (=0) |

## Score final

| Machine | Score | Note |
|---------|-------|------|
| db-layer | **41/43** | 2 gaps intentionnels |
| admin-trading | **41/43** | 2 gaps intentionnels |
| student | **41/43** | 2 gaps intentionnels |
| cursor-ai | **39/43** | + 2 N/A Windows |
| fantome | **41/43** | 2 gaps intentionnels |

## Gaps explicites — non bloquants

| Var | Décision |
|-----|----------|
| `BINANCE_API_KEY` / `BINANCE_API_SECRET` | `ENABLE_BINANCE_PRIVATE=0` — désactivé jusqu'à besoin compte/trading |
| `TELEGRAM_SESSION_PATH` | cursor-ai Windows — chemin Linux N/A |
| `GOOGLE_APPLICATION_CREDENTIALS` | cursor-ai Windows — pas de gcloud |

## Credentials hors matrice — décision explicite

| Var | Décision |
|-----|----------|
| `ANTHROPIC_API_KEY` | skipped — déclassé / non utilisé |
| `GEMINI_API_KEY` | skipped — Gemini CLI OAuth |
| `COINGLASS_API_KEY` | bot_vision/no-api — données via headless browser |
| `DESKPRO_API_KEY` / `DESKPRO_API_URL` | internal/no-runtime — service local port 8010 |
| `DB_HOST` / `DB_USER` / `DB_PASSWORD` | skipped — DB distante non active |
| `WG_PRIVATE_KEY` | sys-file — `/etc/wireguard/`, jamais en `.env` |
