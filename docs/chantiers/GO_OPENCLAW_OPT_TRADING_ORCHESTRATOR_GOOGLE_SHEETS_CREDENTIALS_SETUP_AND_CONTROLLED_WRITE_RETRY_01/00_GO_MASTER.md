---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_SETUP_AND_CONTROLLED_WRITE_RETRY_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #493  (7-day dry-run observation — merged)
  - PR #495  (Controlled-write pilot — merged DEGRADED)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_SETUP_AND_CONTROLLED_WRITE_RETRY_01

## Objectif

Configurer les credentials Google Sheets dans l'environnement puis
exécuter un controlled-write manuel vers Google Sheets.

## Prérequis (hors repo)

Avant de lancer ce GO, les variables d'environnement doivent être
définies :

```bash
export GOOGLE_SHEETS_CREDENTIALS_JSON='{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...@....iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}'
export GOOGLE_SHEETS_SYNC_SHEET_ID="your-google-sheet-id"
```

Ces valeurs ne doivent **jamais** être commitées dans le repo.

## Périmètre

1. Vérifier que les 2 variables env sont définies
2. Choisir le dernier run_id disponible comme cible
3. Dry-run preview avant écriture
4. Controlled-write avec `--controlled-write`
5. Vérifier la ligne dans Google Sheets (requête API)
6. Vérifier `data/journal/sync_log.jsonl`
7. Vérifier que LocalCMS est read-only (inchangé)
8. Produire rapport PASS / DEGRADED / BLOCKED

## Si credentials toujours absents

Ce GO reste ouvert et documente l'état d'attente. Aucune écriture
ne sera tentée sans les variables d'environnement.

## Contraintes

- Credentials jamais dans le repo
- Controlled-write manuel uniquement
- Aucune écriture automatique
- No live trade / No Bitget order
- LocalCMS read-only
