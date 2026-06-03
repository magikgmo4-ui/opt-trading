# Telegram Credentials Scope

Les credentials suivants sont nécessaires pour le rôle `telegram_collector` :

| Credential ID | Env Var | Type | Description |
|---------------|---------|------|-------------|
| `telegram_api_id` | `TELEGRAM_API_ID` | `api_id` | Identifiant API Telegram (App ID). |
| `telegram_api_hash` | `TELEGRAM_API_HASH` | `api_hash` | Hash API Telegram. |
| `telegram_bot_token_main` | `TELEGRAM_BOT_TOKEN` | `bot_token` | Token du bot pour les notifications/alertes. |
| `telegram_session_path` | `TELEGRAM_SESSION_PATH` | `file_path` | Chemin vers le fichier `.session` de Telethon. |

## Variables Optionnelles
- `TELEGRAM_CHANNELS_CONFIG`: Chemin vers la configuration des canaux à surveiller.
- `TELEGRAM_ALERT_CHAT_ID`: ID du chat pour l'envoi d'alertes par le bot.

## Variables Multi-Canal (ajout PR #1063 — GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01)

| Credential ID | Env Var | Type | Description |
|---|---|---|---|
| `telegram_chat_id_alerts` | `TELEGRAM_CHAT_ID_ALERTS` | `chat_id` | Alertes système — cron WARN, kill switch, dead letter |
| `telegram_chat_id_pipeline` | `TELEGRAM_CHAT_ID_PIPELINE` | `chat_id` | Pipeline trading — signal, approbation, résultat |
| `telegram_chat_id_push` | `TELEGRAM_CHAT_ID_PUSH` | `chat_id` | Push contenu — bot_vision, coinglass, market data |
| `telegram_chat_id_ops` | `TELEGRAM_CHAT_ID_OPS` | `chat_id` | Commandes & tools — CLI, tmux, OpenClaw |

Fallback : si non définie → `TELEGRAM_CHAT_ID` (voir `shared/telegram_channels.py`).
