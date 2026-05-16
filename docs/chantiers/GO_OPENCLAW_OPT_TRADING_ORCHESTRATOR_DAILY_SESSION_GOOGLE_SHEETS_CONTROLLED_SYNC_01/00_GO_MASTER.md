---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_GOOGLE_SHEETS_CONTROLLED_SYNC_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #475  (Daily session journal — merged)
  - PR #478  (LocalCMS daily session history view — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_GOOGLE_SHEETS_CONTROLLED_SYNC_01

## Objectif

Ajouter une synchronisation contrôlée Google Sheets pour les sessions quotidiennes du pipeline dry-run.

## Contexte établi

- PR #475 daily session journal merged
- PR #478 LocalCMS daily session history view merged
- LocalCMS expose `/journal` et `/journal/{run_id}`
- Journal quotidien produit JSON dans `data/journal/daily/<run_id>.json`
- Journal quotidien produit CSV dans `data/journal/daily/<run_id>.csv`
- Dry-run par défaut, controlled-write via flag explicite

## Flux de synchronisation

```text
run_id quotidien
→ lire JSON journal
→ mapper colonnes Sheets
→ dry-run preview (diff)
→ [si --controlled-write] écrire ligne dans Google Sheets
→ log JSON de l'opération
→ status sync par run_id
→ closeout
```

## Colonnes Sheets

```text
run_id | date | signal | side | ticker | action | confidence | verdict
| exec_status | fill_price | outcome | net_pnl | datasheet_written
| bridge_status | brick_stored | tmux_before | tmux_after
| localcms_before_ok | localcms_after_ok | closeout_acknowledged
| duration_s | all_ok
```

## Livrables

1. `scripts/sheets/sync_daily_session.py` — script de synchronisation Google Sheets
2. `tests/e2e/test_sync_daily_session.py` — tests
3. `docs/chantiers/.../00_GO_MASTER.md` — documentation GO master

## Contraintes

- dry-run par défaut
- `--controlled-write` explicite seulement
- Aucune écriture automatique
- Pas de live trade
- Pas de Bitget order
- LocalCMS reste read-only
- Sheets API credentials hors repo (via env vars)
- Log JSON de chaque sync
- closeout obligatoire
