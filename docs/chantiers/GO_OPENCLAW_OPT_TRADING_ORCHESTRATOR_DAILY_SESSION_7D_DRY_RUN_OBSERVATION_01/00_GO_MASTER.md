---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_7D_DRY_RUN_OBSERVATION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #490  (3-run systemd steady-state review)
  - PR #491  (Production governance decision)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_7D_DRY_RUN_OBSERVATION_01

## Objectif

Installer le timer systemd et observer 7 runs dry-run quotidiens
pour valider la stabilité temporelle de la stack.

## Périmètre

1. Installer service + timer systemd
2. Exécuter 7 runs (simulation 7 jours)
3. Collecter pour chaque run : run_id, TMUX, LocalCMS, journal, Sheets
4. Vérifier LocalCMS /journal liste les 7 entries
5. Vérifier scheduler log
6. Produire comparaison J1-J7
7. Signaler anomalies éventuelles
8. Verdict PASS / DEGRADED / BLOCKED

## Critères

| Statut    | Condition                                                |
| --------- | -------------------------------------------------------- |
| PASS      | 7/7 runs OK, données cohérentes, aucune anomalie         |
| DEGRADED  | 5-6/7 OK, ou anomalies non-bloquantes                    |
| BLOCKED   | <5 runs OK, ou plantage système                          |

## Contraintes

- dry-run only
- no live trade / no Bitget order
- no automatic Sheets write
- controlled-write manuel seulement
- aucune nouvelle feature
- rollback après closeout

## RISKS

- À qualifier.
