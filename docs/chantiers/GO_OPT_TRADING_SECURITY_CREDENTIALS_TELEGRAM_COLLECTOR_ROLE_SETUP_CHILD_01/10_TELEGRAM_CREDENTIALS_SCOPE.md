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
