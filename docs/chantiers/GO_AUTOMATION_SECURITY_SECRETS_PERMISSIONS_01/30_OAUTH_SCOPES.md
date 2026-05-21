---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_OAUTH
doc_type: security_oauth
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
status: draft
---

# 30_OAUTH_SCOPES.md

## Scopes OAuth par application externe

| App | Auth method | Scopes requis | Justification |
|---|---|---|---|
| **Airtable** | PAT (Personal Access Token) | `data.records:read`, `data.records:write` | Lecture/écriture des bases de trading |
| **ClickUp** | API Token | `tasks:read`, `tasks:write`, `lists:read` | Gestion des tâches automation |
| **Botpress** | API Token | `bot:read`, `bot:write`, `conversations:read` | Configuration bot + logs |
| **Sheets** | OAuth 2.0 (service account) | `https://www.googleapis.com/auth/spreadsheets` | Mise à jour des sheets de trading |
| **Telegram** | Bot Token | `send_message`, `read_message` (API Bot native) | Alertes et commandes |
| **Gmail** | App Password | `https://mail.google.com/` | Envoi d'emails automation |
| **Calendar** | API Key | `https://www.googleapis.com/auth/calendar.readonly` | Lecture seule des events |
| **Drive** | API Key | `https://www.googleapis.com/auth/drive.readonly` | Lecture seule des fichiers partagés |
| **Figma** | PAT | `file:read`, `comments:read` | Lecture des maquettes |

## Principe

- Chaque app bridge n'utilise que les scopes nécessaires (least privilege)
- Les tokens sont chargés depuis les env vars au démarrage du worker
- Aucun scope d'écriture n'est autorisé sans confirmation humaine (L4+)
