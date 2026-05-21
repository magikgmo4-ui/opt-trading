---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_INVENTORY
doc_type: security_inventory
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
status: draft
---

# 20_SENSITIVE_ITEMS_INVENTORY.md

## Inventaire des credentials et tokens

| Item | Type | Usage | Surface | Stockage | Rotation | Niveau risque |
|---|---|---|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot token | Communication Telegram | Telegram | `.env` | 90j | High |
| `AIRTABLE_PAT` | Personal Access Token | Airtable API | Airtable | `.env` | 90j | High |
| `OPENAI_API_KEY` | API key | LLM calls | Toutes LLM | `.env` | 30j | Critical |
| `GMAIL_APP_PASSWORD` | App password | Email bridge | Gmail | `.env` | 180j | Medium |
| `GITHUB_TOKEN` | Personal token | Git push/PR | GitHub | `.env` | 90j | High |
| `CLICKUP_API_TOKEN` | API token | ClickUp bridge | ClickUp | `.env` | 90j | Medium |
| `BOTPRESS_API_TOKEN` | API token | Botpress bridge | Botpress | `.env` | 90j | Medium |
| `GOOGLE_CALENDAR_API_KEY` | API key | Calendar bridge | Calendar | `.env` | 180j | Low |
| `GOOGLE_DRIVE_API_KEY` | API key | Drive bridge | Drive | `.env` | 180j | Low |
| `FIGMA_ACCESS_TOKEN` | Personal token | Figma bridge | Figma | `.env` | 90j | Medium |
| `SHEETS_API_CREDENTIALS` | Service account | Sheets bridge | Sheets | fichier JSON | 365j | Medium |

## Politique de stockage

1. **Aucun secret dans le code** — les fichiers `.env*`, `*SECRET*`, `*API_KEY*`, `*TOKEN*`, `*PASSWORD*` sont dans `.gitignore` (ligne 89)
2. **Template `.env.example`** — le fichier d'exemple contient les clés sans valeurs
3. **Variables d'environnement** — tous les secrets passés par env vars au runtime
4. **Fichiers JSON de service account** — stockés hors repo, exclus par `.gitignore`
5. **Rotation** — les tokens à risque Critical ont rotation 30j, High 90j, Medium 90j, Low 180j
