# 10_CURRENT_CREDENTIALS_INVENTORY

## Surfaces credentials identifiées

### 1. `/opt/trading/.env` — Secrets principaux du repo

| Variable | Usage | Méthode actuelle |
|----------|-------|-----------------|
| `TV_WEBHOOK_KEY` | Validation signature webhook TradingView | env file local, non versionné |
| `OPS_ADMIN_KEY` | Opérations admin | env file local, non versionné |
| `TELEGRAM_BOT_TOKEN` | Notifications Telegram | env file local, non versionné |
| `TELEGRAM_CHAT_ID` | Canal alerte principal | env file local, non versionné |
| `TELEGRAM_CHAT_ID_PIPELINE` | Canal pipeline (multi-canal) | env file local |
| `TELEGRAM_CHAT_ID_OPS` | Canal ops | env file local |
| `TELEGRAM_CHAT_ID_PUSH` | Canal push | env file local |

Template : `/opt/trading/.env.example` — versionné, valeurs vides.

---

### 2. `/opt/trading/.secrets/bitget.env` — Exchange credentials

| Variable | Usage |
|----------|-------|
| `BITGET_READONLY_MAIN_API_KEY` | API Bitget lecture seule |
| `BITGET_READONLY_MAIN_SECRET_KEY` | Secret key |
| `BITGET_READONLY_MAIN_PASSPHRASE` | Passphrase |

Template : `.secrets/bitget.env.example` — versionné. Fichier réel : gitignored.
Chargé via : `modules/auth/bitget_credentials.py` → lecture depuis env ou fichier local.

---

### 3. `/opt/trading/configs/env/roles/` — Rôles env modulaires

Fichiers `.example` versionnés, fichiers réels gitignorés.

| Fichier role | Credentials couverts |
|-------------|---------------------|
| `base.env.example` | LOG_LEVEL, DEBUG |
| `datacenter.env.example` | DB_HOST, DB_USER, DB_PASSWORD |
| `deskpro_cli.env.example` | DESKPRO_API_URL, DESKPRO_API_KEY |
| `git_dev.env.example` | GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL |
| `google_sheets.env.example` | GOOGLE_SERVICE_ACCOUNT_JSON_PATH, SPREADSHEET_ID |
| `llm_cloud.env.example` | OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY |
| `llm_local.env.example` | OLLAMA_BASE_URL, LOCAL_MODEL_NAME |
| `market_data_readonly.env.example` | BINANCE_API_KEY, COINGLASS_API_KEY |
| `telegram_collector.env.example` | TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, TELEGRAM_SESSION_PATH, TELEGRAM_ALERT_CHAT_ID, TELEGRAM_CHANNELS_CONFIG, TELEGRAM_CHAT_ID_ALERTS, TELEGRAM_CHAT_ID_PIPELINE, TELEGRAM_CHAT_ID_PUSH, TELEGRAM_CHAT_ID_OPS |
| `webhook_receiver.env.example` | TV_WEBHOOK_SECRET |

---

### 4. `/etc/opt-trading/shared_sshfs_permanent.env` — Mount SSHFS système

| Variable | Usage |
|----------|-------|
| REMOTE_HOST | Hôte admin-trading |
| REMOTE_USER | User SSH distant |
| REMOTE_PATH | Chemin distant |
| MOUNT_POINT | Point de montage local |
| SSH_PORT | Port SSH |
| IDENTITY_FILE | Clé SSH privée (chemin) |

Fichier système — non versionné, lecture root/group uniquement.
**Note :** `/etc/opt-trading/env.d/roles/` n'existe pas encore (pattern planifié, non déployé).

---

### 5. `/home/openclaw/.openclaw/openclaw.json` — Credentials OpenClaw

| Profile | Provider | Mode |
|---------|----------|------|
| `openai:default` | openai | api_key |
| `openai-codex:default` | openai-codex | oauth |

Modèles configurés : `openai/gpt-5.4`, `openrouter/qwen/*`, `openrouter/deepseek/deepseek-r1`

Stockage : JSON local dans `~/.openclaw/`, hors git.
Gestion : via `openclaw configure set` ou wizard — ne pas éditer manuellement.

---

### 6. GitHub Actions — Secrets CI

| Secret | Usage | Source |
|--------|-------|--------|
| `GITHUB_TOKEN` | Automatique GitHub | Injecté par runner |
| Aucun secret custom requis | Workflows read-only | Pas de secrets.yml supplémentaires |

Tous les workflows actuels (`strict-workers-smoke.yml`, `openclaw-mcp-policy-static-validator.yml`, etc.) sont `permissions: contents: read` — aucun secret externe requis.

---

## Résumé des méthodes actuelles

| Surface | Méthode | Gitignored | Documentée |
|---------|---------|------------|------------|
| `.env` | Fichier local | OUI | OUI (.env.example) |
| `.secrets/bitget.env` | Fichier local | OUI | OUI (.env.example) |
| `configs/env/roles/` | Role files | OUI (réels) | OUI (examples) |
| `/etc/opt-trading/` | Fichier système | N/A | Partiel |
| `~/.openclaw/` | Config JSON outil | N/A | Via openclaw cli |
| GitHub CI | Token auto | N/A | OUI |

## Gaps identifiés

- `/etc/opt-trading/env.d/roles/` planifié mais non créé
- `TELEGRAM_CHAT_ID_*` multi-canal dans `.env` mais pas dans `openclaw.json` channels
- `groupAllowFrom` vide dans openclaw.json → voir doc 40
- Pas de rotation policy documentée
- `modules/auth/secrets.py` pattern clean mais pas systématiquement utilisé partout
