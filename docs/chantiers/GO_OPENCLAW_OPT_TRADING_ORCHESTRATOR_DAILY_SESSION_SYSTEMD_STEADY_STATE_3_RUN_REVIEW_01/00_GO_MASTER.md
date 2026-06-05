---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_STEADY_STATE_3_RUN_REVIEW_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #488  (Cron/systemd integration GO)
  - PR #489  (Systemd first-run observation)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_STEADY_STATE_3_RUN_REVIEW_01

## Objectif

Observer 3 runs systemd/timer successifs en dry-run, comparer les résultats,
valider la reproductibilité du comportement steady-state.

## Périmètre

1. Installer service + timer
2. Exécuter 3 runs consécutifs (simulation 3 jours)
3. Collecter pour chaque run : run_id, journal, LocalCMS, logs, Sheets sync
4. Comparer les 3 runs (run_id, verdict, P&L, duration, dry_run, all_ok)
5. Vérifier LocalCMS /journal liste les 3 entries
6. Produire review + closeout
7. Rollback

## Critères

| Statut    | Condition                                                |
| --------- | -------------------------------------------------------- |
| PASS      | 3/3 runs OK, données cohérentes, LocalCMS liste tout     |
| DEGRADED  | 1-2 runs OK, écart non-bloquant                          |
| BLOCKED   | 0 run OK, ou plantage système                            |

## Contraintes

- Aucune nouvelle feature
- dry-run only
- No live trade / No Bitget order
- No automatic Sheets write
- Rollback obligatoire

## RISKS

- À qualifier.
