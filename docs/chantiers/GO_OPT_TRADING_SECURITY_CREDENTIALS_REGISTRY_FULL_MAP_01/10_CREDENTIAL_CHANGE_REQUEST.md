---
doc_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01_CCR
doc_type: credential_change_request
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01
status: APPLIED
created_at: 2026-06-03
---

# CREDENTIAL_CHANGE_REQUEST — Registry Full Map

## Type : ADD (registry entries only — no secret values)

### Ajouts credentials.yaml

| ID | Provider | Env Var | Note |
|----|----------|---------|------|
| tv_webhook_key | tradingview | TV_WEBHOOK_KEY | Alias de TV_WEBHOOK_SECRET, utilisé dans webhook_server.py |
| ops_admin_key | internal | OPS_ADMIN_KEY | Clé admin interne |
| airtable_api_key | airtable | AIRTABLE_API_KEY | |
| airtable_base_id | airtable | AIRTABLE_BASE_ID | |
| deskpro_api_key | deskpro | DESKPRO_API_KEY | |
| deskpro_api_url | deskpro | DESKPRO_API_URL | |
| clickup_token | clickup | CLICKUP_TOKEN | aussi /tmp/clickup_token |
| figma_token | figma | FIGMA_TOKEN | future phase 2 |
| figma_file_key | figma | FIGMA_FILE_KEY | future phase 2 |
| sshfs_identity_file | internal | IDENTITY_FILE | fichier système |
| wireguard_private_key | internal | WG_PRIVATE_KEY | /etc/wireguard/, jamais git |
| termux_ssh_key | internal | null | ~/.ssh/id_ed25519_termux |

### Ajouts roles.yaml

| Rôle | Action | Credentials |
|------|--------|-------------|
| webhook_receiver | MODIFIED | + tv_webhook_key, + ops_admin_key |
| deskpro_user | MODIFIED | + deskpro_api_key, + deskpro_api_url |
| airtable_user | ADD | airtable_api_key, airtable_base_id |
| clickup_user | ADD | clickup_token |
| figma_designer | ADD (future) | figma_token, figma_file_key |
| infrastructure | ADD | sshfs_identity_file, wireguard_private_key, termux_ssh_key |

### Mapping machines.yaml (complet)

| Machine | Rôles actifs ajoutés |
|---------|---------------------|
| admin-trading | telegram_collector (promu), airtable_user, clickup_user, infrastructure |
| fantome | infrastructure |
| db-layer | inchangé |
| cursor-ai | inchangé |
| student | inchangé |

## Valeurs réelles

Aucune valeur réelle dans ce diff. Les valeurs réelles restent :
- `/opt/trading/.env` (TV_WEBHOOK_KEY, OPS_ADMIN_KEY)
- `/opt/trading/.secrets/` (Bitget)
- `/etc/opt-trading/env.d/roles/` (Telegram CHAT_IDs)
- `~/.openclaw/openclaw.json` (LLM keys via openclaw configure)
- Système `/etc/wireguard/`, `~/.ssh/` (infrastructure)
