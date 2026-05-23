# 00_INITIAL_PROJECT_DOC

## GO_ID

`GO_OPT_TRADING_AUTOMATION_NON_TRADING_WARN_BURN_DOWN_01`

## Type

Chantier enfant / follow-up post-rollout

## Parent

`GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01`

## Base

`sot/mainline` après merge PR #690 (commit `44225ba8`).

## Objectif

Fermer ou déclasser proprement les **13 WARN** issus du rollout non-trading (114 jobs, 0 FAIL) avant toute activation permanente du scheduler.

## Contexte

Le parent a exécuté 9 phases du registre canonique non-trading. 13 WARN ont été documentés par les gates des phases 01→09. Aucun FAIL n'a été rencontré, mais les WARN représentent des gaps contractuels, de sécurité, ou d'observabilité qui doivent être résolus avant de considérer le rollout comme stable pour activation permanente.

## Règles

- Non-trading only — aucun signal ni trading
- Pas de live order
- Pas de suppression de code existant
- Pas de write externe sans HITL / dual confirm
- Pas d'activation de scheduler permanent tant que les P0/P1 ne sont pas clos
- Chaque WARN doit finir en `CLOSED`, `DECLASSIFIED`, ou `CARRIED_FORWARD_WITH_REASON`

## Périmètre

| Scope | Hors scope |
|-------|-----------|
| 13 WARN listés dans le registre | Nouveaux WARN découverts |
| Correction locale et docs | Changement runtime/machine-side |
| Preuve par evidence | Activation scheduler permanent |
| .env permission audit | Live trading |

## Livrables

1. `10_WARN_REGISTER.md` — inventaire des 13 WARN
2. `20_BURN_DOWN_PLAN.md` — plan par priorité P0→P3
3. `30_EXECUTION_PACKETS.md` — packets d'exécution par WARN
4. `40_EVIDENCE_REQUIREMENTS.md` — preuves attendues par WARN
5. `BRANCH_STATE.md` — état de la branche
6. Résumé final `PASS` / `PARTIAL` / `BLOCKED`
