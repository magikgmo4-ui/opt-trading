---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CONTROLLED_WRITE_EXECUTION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #495  (Controlled-write pilot — merged DEGRADED)
  - PR #496  (Credentials setup + retry plan — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CONTROLLED_WRITE_EXECUTION_01

## Objectif

Exécuter un controlled-write Google Sheets réel (première écriture)
et vérifier la ligne écrite.

## Prérequis

```bash
export GOOGLE_SHEETS_CREDENTIALS_JSON='{...service_account_json...}'
export GOOGLE_SHEETS_SYNC_SHEET_ID='...'
```

## Périmètre

1. Vérifier les 2 env vars
2. Dry-run preview avec le dernier run_id
3. Controlled-write avec `--controlled-write`
4. Vérifier la ligne via l'API Google Sheets
5. Vérifier `data/journal/sync_log.jsonl`
6. Confirmer LocalCMS inchangé
7. Rapport PASS / DEGRADED / BLOCKED

## Contraintes

- Credentials jamais dans le repo
- Controlled-write manuel uniquement
- Aucune écriture automatique
- No live trade / No Bitget order
- LocalCMS read-only
