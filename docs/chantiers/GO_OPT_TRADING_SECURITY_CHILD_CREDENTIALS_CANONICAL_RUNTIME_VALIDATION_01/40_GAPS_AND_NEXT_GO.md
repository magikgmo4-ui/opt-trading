---
doc_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01
status: canonical
created_at: 2026-06-03
---

# Gaps identifiés + candidats GO suivants

## Gaps credentials (23 ABSENT / 33 actifs)

Classés par priorité opérationnelle.

### Priorité 1 — Bloque fonctionnalités critiques

| Gap | Credential(s) ABSENT | Impact |
|-----|---------------------|--------|
| G1 | OPS_ADMIN_KEY | Endpoints /admin du webhook_server inaccessibles |
| G2 | TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_PATH | telegram_ingestion + telegram_screener non opérationnels |
| G3 | TELEGRAM_ALERT_CHAT_ID, TELEGRAM_CHANNELS_CONFIG | Routing multi-canal incomplet (notifications actives via CHAT_ID_* mais pas via ALERT_CHAT_ID) |

### Priorité 2 — Bloque connecteurs apps

| Gap | Credential(s) ABSENT | Impact |
|-----|---------------------|--------|
| G4 | AIRTABLE_API_KEY, AIRTABLE_BASE_ID | Session apps-connectors — Airtable inopérant |
| G5 | CLICKUP_TOKEN | Session apps-connectors — ClickUp inopérant |
| G6 | DESKPRO_API_KEY, DESKPRO_API_URL | DeskPro connector inopérant |
| G7 | GOOGLE_SERVICE_ACCOUNT_JSON_PATH, GOOGLE_SHEETS_SPREADSHEET_ID | Google Sheets writer inopérant |

### Priorité 3 — Bloque market data enrichi

| Gap | Credential(s) ABSENT | Impact |
|-----|---------------------|--------|
| G8 | BINANCE_API_KEY | Données privées Binance (données publiques fonctionnent) |
| G9 | COINGLASS_API_KEY | REST adapter non prouvé, headless actif |
| G10 | GEMINI_API_KEY | Gemini LLM indisponible |
| G11 | OLLAMA_BASE_URL | Inference locale désactivée |

### Priorité 4 — Compléments config

| Gap | Credential(s) ABSENT | Impact |
|-----|---------------------|--------|
| G12 | TV_WEBHOOK_SECRET | Alias legacy TV_WEBHOOK_KEY, non bloquant |
| G13 | GH_TOKEN | Modules qui lisent la var directement (gh CLI fonctionne) |
| G14 | DB_HOST, DB_USER, DB_PASSWORD | Base externe — SQLite local actif |
| G15 | termux_ssh_key | Clé SSH Termux non générée sur db-layer |

## Action requise pour les gaps

Tous les gaps G1–G14 sont résolus par l'opérateur via :

```bash
python3 scripts/credentials_form.py          # menu interactif
python3 scripts/credentials_form.py --provider Telegram
scripts/env_role_sync.sh pull <machine> <role>
```

**Aucun code à écrire.** L'infrastructure de rotation est complète.

## Résumé architecture credentials — état final

```text
REGISTRY    = COMPLETE  (35 credentials / 13 rôles / 5 machines)
PANEL_UI    = COMPLETE  (GET /credentials + /credentials/json)
CLI_FORM    = COMPLETE  (scripts/credentials_form.py)
ROTATION    = COMPLETE  (env_role_sync.sh + credentials_form.py)
RUNBOOK     = COMPLETE  (60_ROTATION_RUNBOOK.md)
ANTI_LEAK   = ENFORCED  (git hooks + règles governance)
VALEURS     = 10/33 SET (30% — opérateur doit fournir les 23 restants)
```

## Candidats GO suivants

Ce chantier ne génère pas de nouveau code. Les GO suivants dépendent de l'opérateur.

### GO immédiats (opérateur)

```text
GO_CREDENTIALS_DEPLOY_TELEGRAM_INGESTION_01
  → Fournir TELEGRAM_API_ID + API_HASH + SESSION_PATH
  → Activer telegram_ingestion / telegram_screener

GO_CREDENTIALS_DEPLOY_APPS_CONNECTORS_01
  → Fournir Airtable + ClickUp + DeskPro + Google Sheets
  → Activer session apps-connectors sur db-layer
```

### GO techniques candidats

```text
GO_OPT_TRADING_CREDENTIALS_AUTO_ROTATION_CRON_01  (optionnel)
  → Alertes automatiques quand un credential passe de SET à ABSENT
  → Worker strict qui appelle /credentials/json et alerte si taux < seuil

GO_OPT_TRADING_LOCALCMS_CREDENTIALS_MULTI_MACHINE_01  (optionnel)
  → Étendre /credentials pour afficher l'état par machine (admin-trading, fantome)
  → Via env_role_sync.sh diff dans le panel
```

## Verdict chantier parent

```text
PARENT = GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01

Master target :
  "Registre canonique credentials complet + méthode de rotation opérationnelle"

Évaluation :
  REGISTRY     = COMPLETE  ✓
  ROLES        = COMPLETE  ✓
  MACHINES     = COMPLETE  ✓
  ENV_EXAMPLES = COMPLETE  ✓
  ROTATION_CLI = COMPLETE  ✓
  PANEL_UI     = COMPLETE  ✓
  RUNBOOK      = COMPLETE  ✓
  VALEURS SET  = 10/33     — dépend de l'opérateur, hors scope technique

MASTER_TARGET_STATUS = REACHED (infrastructure)
VALEURS_STATUS       = OPÉRATEUR_REQUIS

INDEX_GLOBAL_UPDATE_CANDIDATE:
  Le master target infrastructure est atteint.
  Les index globaux ne changent pas tant que les valeurs opérateur ne sont pas déployées.
  Recommandation : batch d'agrégation index globaux sur demande explicite.
```
