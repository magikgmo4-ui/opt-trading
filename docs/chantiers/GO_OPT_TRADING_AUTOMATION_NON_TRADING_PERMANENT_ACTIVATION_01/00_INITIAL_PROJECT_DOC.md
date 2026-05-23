# 00_INITIAL_PROJECT_DOC

## GO_ID

`GO_OPT_TRADING_AUTOMATION_NON_TRADING_PERMANENT_ACTIVATION_01`

## Type

Chantier d'activation permanente limitée

## Parent

`GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01`

## Base

`sot/mainline` après merge PR #690 (114 jobs, 0 FAIL) + PR #691 (13/13 WARN résolus).

## Contexte

Le rollout non-trading a validé l'infrastructure, les contrats, et les registres. Les WARN sont clos. Le prochain gap est l'activation réelle permanente limitée.

## Objectif

Activer uniquement les jobs non-trading déjà prouvés, avec scheduler contrôlé, ledger, kill switch, et exclusions explicites Gmail/Calendar/trading.

## Règles

- Non-trading only — aucun signal ni trading
- Drive seulement en WRITE_GATED avec approval manuelle
- Gmail et Calendar exclus du périmètre
- Aucun write externe autonome
- Aucune suppression
- Aucune modification de permissions externes
- Aucun .env commité
- Aucun secret dans les logs
- Rollback documenté et testé

## Jobs autorisés

- repo-status-check
- repo-diff-check
- repo-pr-audit
- ledger-heartbeat
- ledger-replay-check
- automation-health-status
- anti-leak-scan
- strict-worker-readonly-smoke
- capability-matrix-validate
- bridge-contract-validation
- hitl-scenarios-smoke
- localcms-status-sync
- Drive canary packet (WRITE_GATED / manual approve only)

## Périmètre interdit

- Gmail
- Calendar
- Signal/trading
- Broker/exchange/order
- Write externe autonome
- Scheduler permanent sur write-gated sans approval
