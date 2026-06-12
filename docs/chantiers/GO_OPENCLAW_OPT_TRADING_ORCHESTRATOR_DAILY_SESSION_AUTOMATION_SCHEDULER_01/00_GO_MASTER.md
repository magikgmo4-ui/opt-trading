---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_AUTOMATION_SCHEDULER_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #475  (Daily session journal — merged)
  - PR #478  (LocalCMS daily session history view — merged)
  - PR #480  (Google Sheets controlled sync — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_AUTOMATION_SCHEDULER_01

## Objectif

Planifier l'exécution quotidienne du pipeline dry-run, sans activer d'écriture non contrôlée.

## Contexte établi

- PR #475 daily session journal merged
- PR #478 LocalCMS history view merged
- PR #480 Google Sheets controlled sync merged
- Sync Google Sheets dry-run par défaut
- controlled-write seulement avec flag explicite
- Aucun live trade, aucun Bitget order
- LocalCMS read-only

## Flux scheduler

```text
health precheck (TMUX + LocalCMS)
→ si OK : lancer daily_session_journal.py --no-closeout
→ journal JSON/CSV produit
→ [optionnel] sync Google Sheets --dry-run
→ log scheduler (date, status, run_id, duration)
```

## Livrables

1. `scripts/schedule/daily_session.sh` — script scheduler bash
2. `tests/e2e/test_daily_session_scheduler.sh` — tests du scheduler
3. `docs/chantiers/.../00_GO_MASTER.md` — documentation GO master

## Contraintes

- dry-run par défaut (pipeline + Sheets)
- controlled-write Sheets uniquement manuel
- Aucune écriture Sheets automatique
- Pas de live trade
- Pas de Bitget order
- LocalCMS read-only
- Aucune mutation runtime dangereuse
- Logs scheduler dans `data/logs/scheduler/`

## RISKS

- À qualifier.
