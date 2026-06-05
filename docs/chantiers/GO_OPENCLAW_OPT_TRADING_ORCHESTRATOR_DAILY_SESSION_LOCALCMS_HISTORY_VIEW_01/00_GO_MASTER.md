---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_LOCALCMS_HISTORY_VIEW_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #472  (E2E dry-run pipeline with LocalCMS view — merged)
  - PR #475  (Daily session journal — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_LOCALCMS_HISTORY_VIEW_01

## Objectif

Ajouter une vue LocalCMS historique des sessions quotidiennes du pipeline dry-run.

## Contexte établi

- PR #472 E2E dry-run pipeline with LocalCMS view merged
- PR #475 daily session journal merged
- LocalCMS expose déjà les endpoints JSON `/journal/daily` et `/journal/daily/{run_id}`
- Daily journal produit JSON/CSV/human summary dans `data/journal/daily/`

## Vue à produire

### Liste historique (`GET /journal`, HTML)

```text
- Tableau des run_id quotidiens
- Signal source (BUY/SELL, ticker)
- Proposition (action, confidence)
- Validation gate verdict (APPROVED/REJECTED)
- Trade executor status
- P&L paper (outcome, net_pnl)
- Learning feedback (bridge, brick)
- TMUX sessions count (before/after)
- LocalCMS endpoints ok
- Closeout acknowledged
- Filtre par date
```

### Détail par session (`GET /journal/{run_id}`, HTML)

```text
- run_id, session_id, dates
- Signal source détaillé
- Proposition complète
- Validation gate détail
- Trade executor détail
- Result tracker P&L paper
- Datasheet writer
- Learning feeder feedback
- TMUX before/after snapshot
- LocalCMS before/after snapshot
- Closeout status
```

## Livrables

1. `modules/localcms/app/main.py` — ajout des endpoints HTML `/journal` et `/journal/{run_id}`
2. `docs/chantiers/.../00_GO_MASTER.md` — documentation GO master
3. `tests/e2e/test_daily_session_journal_html.py` — tests des vues HTML

## Contraintes

- read-only
- Pas de live trade
- Pas de Bitget order
- Pas de restart depuis LocalCMS
- Aucun write depuis l'UI
- Toute donnée vient du JSON déjà produit par le daily session journal

## RISKS

- À qualifier.
