---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_EXTERNAL_SETUP_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #495  (Controlled-write pilot — merged DEGRADED)
  - PR #496  (Credentials setup + retry plan — merged)
  - PR #497  (Controlled-write execution — merged BLOCKED)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_EXTERNAL_SETUP_01

## Objectif

Configurer l'environnement Google Sheets externe (Sheet + credentials)
pour débloquer le controlled-write, sans jamais exposer de secrets
dans le repo.

## Étapes

### 1. Créer le Google Sheet cible

- Créer un Google Sheet (ex: "OpenClaw Daily Session Log")
- Copier son ID depuis l'URL : `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit`
- Sheet ID = `GOOGLE_SHEETS_SYNC_SHEET_ID`

### 2. Créer un service account

Depuis Google Cloud Console :
- Projet : créer ou utiliser un projet existant
- APIs & Services > Credentials > Create Service Account
- Télécharger la clé JSON
- JSON complet = `GOOGLE_SHEETS_CREDENTIALS_JSON`

### 3. Partager le Sheet

- Ouvrir le Sheet > Share
- Ajouter l'email du service account (client_email dans le JSON)
- Rôle : Editor

### 4. Définir les variables d'environnement

```bash
export GOOGLE_SHEETS_CREDENTIALS_JSON='{...}'
export GOOGLE_SHEETS_SYNC_SHEET_ID='<sheet-id>'
```

### 5. Vérifier sans exposer les secrets

```bash
python3 -c "
import os, json
cj = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_JSON', '')
sid = os.environ.get('GOOGLE_SHEETS_SYNC_SHEET_ID', '')
print(f'CREDENTIALS: {\"SET\" if cj else \"NOT SET\"} ({len(cj)} chars)')
print(f'SHEET_ID: {\"SET\" if sid else \"NOT SET\"}')
if cj:
    d = json.loads(cj)
    print(f'client_email: {d.get(\"client_email\", \"N/A\")}')
    print(f'project_id: {d.get(\"project_id\", \"N/A\")}')
"
```

### 6. Dry-run preview

```bash
python scripts/sheets/sync_daily_session.py --run-id $(ls -t data/journal/daily/*.json | head -1 | grep -oP '\d+_\d+')
```

### 7. Retry controlled-write

Si dry-run OK, exécuter avec `--controlled-write`.

## Résultat attendu

- Sheet contient une ligne avec les 22 colonnes
- `data/journal/sync_log.jsonl` contient l'entrée
- LocalCMS inchangé

## Contraintes

- Aucun secret dans le repo
- Aucun secret dans les logs
- Controlled-write manuel uniquement
- Aucune écriture automatique
- No live trade / No Bitget order
- LocalCMS read-only
