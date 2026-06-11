# Credentials Fleet Inventory — 2026-06-11

Audit et synchronisation complète des credentials sur toute la fleet.

## Fleet

| Machine | OS | Rôle | `.env` path |
|---------|-----|------|-------------|
| db-layer | Ubuntu | operator UI / source de vérité | `/opt/trading/.env` + `/etc/opt-trading/env.d/roles/` |
| admin-trading | Ubuntu | backend / orchestration | `/opt/trading/.env` |
| student | Ubuntu | auxiliary AI | `/opt/trading/.env` |
| cursor-ai | Windows | dev station | `C:\Users\ghost\opt-trading\.env` |
| fantome | Ubuntu | auxiliary | `/home/fantome/opt-trading/.env` |

## Matrice credentials — état final

| Var | db-layer | admin-trading | student | cursor-ai | fantome | Note |
|-----|----------|---------------|---------|-----------|---------|------|
| `TV_WEBHOOK_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `OPS_ADMIN_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TV_WEBHOOK_SECRET` | — | — | — | — | — | legacy/optional |
| `TELEGRAM_BOT_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_API_ID` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_API_HASH` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_SESSION_PATH` | ✓ | ✓ | ✓ | — | ✓ | cursor-ai Windows N/A |
| `TELEGRAM_ALERT_CHAT_ID` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_CHANNELS_CONFIG` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_CHAT_ID_ALERTS` | ✓ | ✓ | ✓ | ✓ | ✓ | -5101027350 |
| `TELEGRAM_CHAT_ID_PIPELINE` | ✓ | ✓ | ✓ | ✓ | ✓ | -5137479305 |
| `TELEGRAM_CHAT_ID_PUSH` | ✓ | ✓ | ✓ | ✓ | ✓ | -5291206867 |
| `TELEGRAM_CHAT_ID_OPS` | ✓ | ✓ | ✓ | ✓ | ✓ | -4840490873 |
| `TELEGRAM_ALLOWED_CHAT_IDS` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `TELEGRAM_ALLOWED_USER_IDS` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `GH_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ | via `gh auth token` |
| `GOOGLE_SHEETS_SYNC_SHEET_ID` | ✓ | ✓ | ✓ | ✓ | ✓ | ADC auth |
| `GOOGLE_APPLICATION_CREDENTIALS` | ✓ | ✓ | ✓ | — | ✓ | cursor-ai Windows N/A |
| `OPENAI_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | récupéré depuis admin-trading/secrets/ |
| `OLLAMA_BASE_URL` | ✓ | ✓ | ✓ | ✓ | ✓ | http://localhost:11434 |
| `CLICKUP_TOKEN` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `AIRTABLE_API_KEY` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `AIRTABLE_BASE_ID` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `AIRTABLE_TABLE_GO_STATUS` | ✓ | ✓ | ✓ | ✓ | ✓ | |
| `IDENTITY_FILE` | ✓ | ✓ | ✓ | ✓ | ✓ | SSH SSHFS |

## Credentials décision explicite — non propagés

| Var | Décision |
|-----|----------|
| `ANTHROPIC_API_KEY` | skipped — Anthropic déclassé / non utilisé |
| `GEMINI_API_KEY` | skipped — Gemini CLI OAuth, pas de clé API |
| `BINANCE_API_KEY` | public-only/optional — endpoints publics ne requièrent pas de clé |
| `COINGLASS_API_KEY` | bot_vision/no-api — données via headless browser uniquement |
| `DESKPRO_API_KEY` / `DESKPRO_API_URL` | internal/no-runtime — module desk_pro local (port 8010), pas de SaaS |
| `DB_HOST` / `DB_USER` / `DB_PASSWORD` | skipped — DB distante non active |
| `WG_PRIVATE_KEY` | sys-file/not-in-env — `/etc/wireguard/`, jamais en `.env` |

## Score final

| Machine | Score actif |
|---------|-------------|
| db-layer | 24/24 |
| admin-trading | 24/24 |
| student | 24/24 |
| cursor-ai | 22/24 (2 N/A Windows) |
| fantome | 24/24 |
