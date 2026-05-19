---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_DAILY_SESSION_JOURNAL_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #468  (TMUX Runtime Spine — merged)
  - PR #470  (LocalCMS central UI — merged)
  - PR #472  (E2E dry-run pipeline with LocalCMS view — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_DAILY_SESSION_JOURNAL_01

## Objectif

Transformer la preuve E2E ponctuelle en **session quotidienne traçable**.

## Contexte établi

- PR #468 TMUX Runtime Spine merged
- PR #470 LocalCMS central UI runtime view merged
- PR #472 E2E dry-run pipeline with LocalCMS view merged
- Pipeline dry-run complet prouvé : signal_router → learning_feeder → LocalCMS
- Aucun live trade, aucun Bitget order, LocalCMS read-only
- 86/86 tests PASS
- Branche stale dashboard supprimée, aucun code non voulu présent

## Pipeline journalier

```text
run_id quotidien (YYYYMMDD_NNN)
→ TMUX snapshot (before)
→ LocalCMS snapshot (before)
→ signal_router
→ proposition_engine
→ validation_gate
→ trade_executor (dry-run)
→ result_tracker (P&L paper)
→ datasheet_writer (dry-run ou controlled write)
→ learning_feeder (feedback)
→ TMUX snapshot (after)
→ LocalCMS snapshot (after)
→ JSON report → data/journal/daily/<run_id>.json
→ CSV summary → data/journal/daily/<run_id>.csv
→ Human-readable summary → stdout
→ Closeout acknowledgment
```

## Livrables

1. `scripts/e2e/daily_session_journal.py` — script Python principal
2. `scripts/e2e/daily_session_journal.sh` — wrapper bash (run / show / list / latest)
3. `data/journal/daily/<run_id>.json` — rapport JSON (créé à l'exécution)
4. `data/journal/daily/<run_id>.csv` — résumé CSV (créé à l'exécution)
5. Tests automatisés
6. Endpoint LocalCMS `/journal/daily` — liste les entrées du journal

## Contenu du journal

Chaque entrée inclut :

```text
- run_id quotidien
- signal source
- proposition (action, confidence)
- validation_gate verdict
- trade_executor dry-run status
- result_tracker P&L paper (outcome, net_pnl)
- datasheet_writer output (dry-run ou controlled write)
- learning_feeder feedback (bridge_status, brick_stored)
- TMUX health snapshot (before/after)
- LocalCMS state snapshot (before/after)
- JSON report (complet)
- CSV summary (1 ligne par run)
- Résumé humain (stdout)
- Closeout acknowledgment
```

## Contraintes

- dry-run only par défaut
- `--controlled-write` explicite pour datasheet_writer
- Pas de live trade
- Pas de Bitget order
- Pas de restart depuis LocalCMS
- Pas d'écriture non contrôlée
- closeout obligatoire (sauf `--no-closeout` pour automation)

## Tests

- `tests/e2e/test_daily_session_journal.py`
- Import clean
- Dry-run par défaut
- Champs présents dans le rapport
- Pas d'appels POST/PUT/DELETE/PATCH
