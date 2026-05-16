---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CONTROLLED_WRITE_PILOT_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #493  (7-day dry-run observation — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CONTROLLED_WRITE_PILOT_01

## Objectif

Exécuter un premier pilot controlled-write manuel vers Google Sheets
en utilisant un run_id existant.

## Périmètre

1. Vérifier credentials Google Sheets dans l'environnement
2. Choisir un run_id existant (dernier journal)
3. Dry-run preview avant écriture
4. Controlled-write explicite avec `--controlled-write`
5. Vérifier la ligne écrite dans Sheets
6. Vérifier le sync log
7. Vérifier que LocalCMS reste read-only
8. Rapport PASS / DEGRADED / BLOCKED

## Contraintes

- Controlled-write manuel uniquement
- Aucune écriture automatique
- No live trade / No Bitget order
- LocalCMS read-only
- Credentials via env vars uniquement
