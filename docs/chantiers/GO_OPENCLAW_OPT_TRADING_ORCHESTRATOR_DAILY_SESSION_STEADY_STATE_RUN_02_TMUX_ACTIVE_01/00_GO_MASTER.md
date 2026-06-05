---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_RUN_02_TMUX_ACTIVE_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #483  (Daily session automation scheduler — merged)
  - PR #484  (Steady-state observation run 01 — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_RUN_02_TMUX_ACTIVE_01

## Objectif

Réexécuter une observation scheduler dry-run avec sessions TMUX actives
pour passer de `DEGRADED` (run 01) à `PASS`.

## Contexte établi

- PR #483 scheduler daily session merged
- PR #484 steady-state observation run 20260516 merged
- Observation #1 = `DEGRADED` car TMUX installé mais 0 session active
- LocalCMS OK (4/4 endpoints)
- Google Sheets sync dry-run OK
- Journal quotidien OK

## Périmètre de l'observation

```text
1. Démarrer sessions TMUX critiques (openclaw-core, screeners, strict-workers)
2. Lancer scheduler dry-run
3. Precheck TMUX (attendu: sessions actives détectées)
4. Precheck LocalCMS
5. Génération journal quotidien
6. Vérification LocalCMS /journal et /journal/{run_id}
7. Vérification Google Sheets sync en dry-run
8. Log scheduler
9. Statut final : PASS / DEGRADED / BLOCKED
```

## Critères d'évaluation

| Statut    | Condition                                                     |
| --------- | ------------------------------------------------------------- |
| PASS      | Scheduler run, journal produit, LocalCMS + TMUX OK, sync dry  |
| DEGRADED  | Scheduler run, journal produit, mais LocalCMS ou TMUX down    |
| BLOCKED   | Scheduler ne peut pas run (precheck critique échoué)          |

## Livrables

1. Rapport d'observation
2. Logs scheduler collectés
3. Vérification LocalCMS /journal endpoint

## Contraintes

- Aucune nouvelle feature
- Aucune modification de code
- dry-run only
- Pas de live trade / Pas de Bitget order
- Pas de write Sheets automatique
- LocalCMS read-only

## RISKS

- À qualifier.
