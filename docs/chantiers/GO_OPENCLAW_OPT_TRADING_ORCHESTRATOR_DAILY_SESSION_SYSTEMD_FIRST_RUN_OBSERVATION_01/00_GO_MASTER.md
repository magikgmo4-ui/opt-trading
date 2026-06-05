---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_FIRST_RUN_OBSERVATION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #483  (Daily session automation scheduler)
  - PR #487  (Steady-state closeout)
  - PR #488  (Cron/systemd integration GO)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_FIRST_RUN_OBSERVATION_01

## Objectif

Installer le service/timer systemd, exécuter le premier run en dry-run,
observer et valider le comportement complet.

## Périmètre

1. Implémenter les fichiers systemd et scripts d'install/uninstall/check
2. Installer le service et le timer
3. Enable le timer
4. Start manuel du service
5. Vérifier status
6. Vérifier logs (systemd + scheduler)
7. Vérifier journal quotidien
8. Vérifier LocalCMS /journal
9. Vérifier Sheets sync dry-run
10. Produire rapport PASS / DEGRADED / BLOCKED
11. Confirmer rollback path

## Contraintes

- DRY_RUN=1 hardcodé dans le service
- No automatic Sheets write
- No live trade / No Bitget order
- LocalCMS read-only
- Rollback obligatoire en fin d'observation

## RISKS

- À qualifier.
