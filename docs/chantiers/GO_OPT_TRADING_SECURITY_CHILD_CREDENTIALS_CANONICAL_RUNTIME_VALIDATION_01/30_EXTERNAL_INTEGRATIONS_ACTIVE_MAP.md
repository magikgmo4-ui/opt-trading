---
doc_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01_INTEGRATIONS
doc_type: integrations_map
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01
status: canonical
snapshot_at: 2026-06-03
---

# Cartographie intégrations externes actives

Valeurs jamais affichées — statuts SET/ABSENT/FUTURE uniquement.

## Légende

| Statut intégration | Sens |
|-------------------|------|
| `ACTIVE` | credentials SET, service utilisé en production |
| `CONFIGURED` | registre + rôle présents, credentials ABSENT — déployable sur demande |
| `PARTIAL` | certains credentials SET, d'autres ABSENT |
| `FUTURE` | phase 2 — credentials non requis actuellement |
| `SYSTEM` | gestion hors env vars (fichiers système) |

---

## Telegram

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| API ID | TELEGRAM_API_ID | ABSENT | .env |
| API Hash | TELEGRAM_API_HASH | ABSENT | .env |
| Bot Token | TELEGRAM_BOT_TOKEN | SET | .env |
| Session Path | TELEGRAM_SESSION_PATH | ABSENT | .env |
| Alert Chat ID | TELEGRAM_ALERT_CHAT_ID | ABSENT | .env |
| Channels Config | TELEGRAM_CHANNELS_CONFIG | ABSENT | .env |
| CHAT_ID_ALERTS | TELEGRAM_CHAT_ID_ALERTS | SET | role/telegram_collector |
| CHAT_ID_PIPELINE | TELEGRAM_CHAT_ID_PIPELINE | SET | role/telegram_collector |
| CHAT_ID_PUSH | TELEGRAM_CHAT_ID_PUSH | SET | role/telegram_collector |
| CHAT_ID_OPS | TELEGRAM_CHAT_ID_OPS | SET | role/telegram_collector |

**Statut intégration : PARTIAL**

- Notifications sortantes (BOT_TOKEN + CHAT_IDs) : **ACTIVE** — webhook_server, strict-workers alertent en Telegram
- Ingestion entrante (API_ID, API_HASH, SESSION_PATH) : **ABSENT** — telegram_ingestion / telegram_screener non opérationnels sans ces clés
- Update : `python3 scripts/credentials_form.py --provider Telegram`

---

## TradingView

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Webhook Key | TV_WEBHOOK_KEY | SET | .env |
| Webhook Secret | TV_WEBHOOK_SECRET | ABSENT | .env |

**Statut intégration : PARTIAL**

- `TV_WEBHOOK_KEY` est la clé active utilisée dans `webhook_server.py`
- `TV_WEBHOOK_SECRET` est l'alias legacy — non requis si TV_WEBHOOK_KEY est SET
- Intégration webhook TradingView → **ACTIVE**

---

## LLM Cloud

| Provider | Env Var | Statut | Storage |
|---------|---------|--------|---------|
| OpenAI | OPENAI_API_KEY | SET | openclaw |
| Anthropic | ANTHROPIC_API_KEY | SET | openclaw |
| Google Gemini | GEMINI_API_KEY | ABSENT | .env |
| Ollama (local) | OLLAMA_BASE_URL | ABSENT | .env |

**Statut intégration : PARTIAL**

- OpenAI + Anthropic : **ACTIVE** (via `openclaw configure`, confirmés SET)
- Gemini : CONFIGURED, clé absente dans .env
- Ollama : URL locale absente — inference locale désactivée

---

## Infrastructure

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| SSHFS Identity File | IDENTITY_FILE | SET | /etc/opt-trading/shared_sshfs_permanent.env |
| WireGuard Private Key | — | SET | /etc/wireguard/wg0.conf |
| Termux SSH Key | — | ABSENT | ~/.ssh/id_ed25519_termux |
| OPS Admin Key | OPS_ADMIN_KEY | ABSENT | .env |

**Statut intégration : PARTIAL**

- SSHFS + WireGuard : **ACTIVE** (system files présents)
- Termux : non généré sur cette machine
- OPS_ADMIN_KEY : requis par webhook_server pour endpoints /admin — ABSENT

---

## Binance

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| API Key | BINANCE_API_KEY | ABSENT | .env |

**Statut intégration : CONFIGURED**

- `collector_binance_spot` fonctionne sans clé (données publiques Binance)
- Clé requise uniquement pour données privées (ordres, portefeuille)
- Accès live trading Binance : non requis actuellement (SimEx uniquement)
- Update : `python3 scripts/credentials_form.py --provider Binance`

---

## Coinglass

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| API Key | COINGLASS_API_KEY | ABSENT | .env |

**Statut intégration : CONFIGURED**

- Données acquises via headless browser (`modules/bot_vision/headless_capture/`) — pas d'API REST
- `COINGLASS_API_KEY` = futur REST adapter, **non prouvé runtime** (`coinglass=NOT_PROVEN_RUNTIME_ADAPTER`)
- Fonctionnel actuellement via capture Playwright

---

## Google (Sheets + Gemini)

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Service Account JSON | GOOGLE_SERVICE_ACCOUNT_JSON_PATH | ABSENT | .env |
| Spreadsheet ID | GOOGLE_SHEETS_SPREADSHEET_ID | ABSENT | .env |
| Gemini API Key | GEMINI_API_KEY | ABSENT | .env |

**Statut intégration : CONFIGURED**

- Rôle `google_sheets_writer` défini, clés ABSENT
- Session `apps-connectors` sur db-layer inclut Google Sheets
- Update : `vim /opt/trading/.env`

---

## GitHub

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Token | GH_TOKEN | ABSENT | .env |

**Statut intégration : PARTIAL**

- CLI `gh` utilise son propre mécanisme d'auth (keyring / `gh auth login`) — **opérationnel**
- `GH_TOKEN` dans .env est requis par les modules qui lisent `os.environ.get("GH_TOKEN")`
- Non bloquant actuellement si aucun module n'est en production

---

## Database

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Host | DB_HOST | ABSENT | .env |
| User | DB_USER | ABSENT | .env |
| Password | DB_PASSWORD | ABSENT | .env |

**Statut intégration : CONFIGURED**

- Rôle `datacenter` défini
- db-layer héberge la base mais la connexion est locale — variables peuvent rester optionnelles
- `perf/perf.db` est SQLite local, ne requiert pas DB_HOST

---

## Airtable

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| API Key | AIRTABLE_API_KEY | ABSENT | role/airtable_user |
| Base ID | AIRTABLE_BASE_ID | ABSENT | role/airtable_user |

**Statut intégration : CONFIGURED**

- Session `apps-connectors` sur db-layer
- Update : `scripts/env_role_sync.sh pull <machine> airtable_user`

---

## DeskPro

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| API Key | DESKPRO_API_KEY | ABSENT | role/deskpro_user |
| API URL | DESKPRO_API_URL | ABSENT | role/deskpro_user |

**Statut intégration : CONFIGURED**

- Update : `scripts/env_role_sync.sh pull <machine> deskpro_user`

---

## ClickUp

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Token | CLICKUP_TOKEN | ABSENT | role/clickup_user |

**Statut intégration : CONFIGURED**

- Runtime lit depuis `/tmp/clickup_token` (symlink ou copie)
- Update : `scripts/env_role_sync.sh pull <machine> clickup_user`

---

## Figma

| Credential | Env Var | Statut | Storage |
|-----------|---------|--------|---------|
| Token | FIGMA_TOKEN | FUTURE | role/figma_designer |
| File Key | FIGMA_FILE_KEY | FUTURE | role/figma_designer |

**Statut intégration : FUTURE** — phase 2 LocalCMS mobile

---

## Résumé

| Intégration | Statut | Blocage actuel |
|-------------|--------|----------------|
| Telegram notifications | ACTIVE | — |
| Telegram ingestion | CONFIGURED | API_ID + HASH + SESSION_PATH absents |
| TradingView webhook | ACTIVE | — |
| OpenAI / Anthropic | ACTIVE | — |
| Infrastructure SSH/WG | ACTIVE | Termux absent |
| OPS Admin | CONFIGURED | OPS_ADMIN_KEY absent |
| Binance (public) | ACTIVE | données publiques sans clé |
| Binance (privé) | CONFIGURED | clé absente |
| Coinglass | ACTIVE | via headless capture |
| Google Sheets | CONFIGURED | clés absentes |
| Gemini | CONFIGURED | clé absente |
| GitHub CLI | ACTIVE | gh auth (hors .env) |
| GitHub (module) | CONFIGURED | GH_TOKEN absent dans .env |
| Database SQLite | ACTIVE | perf.db local |
| Database externe | CONFIGURED | DB_* absents |
| Ollama | CONFIGURED | URL absente |
| Airtable | CONFIGURED | clés absentes |
| DeskPro | CONFIGURED | clés absentes |
| ClickUp | CONFIGURED | token absent |
| Figma | FUTURE | phase 2 |
