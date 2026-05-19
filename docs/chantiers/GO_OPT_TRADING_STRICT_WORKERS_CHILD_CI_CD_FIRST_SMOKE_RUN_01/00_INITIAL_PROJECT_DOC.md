# GO_OPT_TRADING_STRICT_WORKERS_CHILD_CI_CD_FIRST_SMOKE_RUN_01 — 00_INITIAL_PROJECT_DOC

## Objectif

Valider réellement les 3 workflows strict workers mergés par PR #601 en les déclenchant sur `sot/mainline`, observer les résultats, documenter les verdicts, et corriger les bugs prouvés.

## Travail effectué

1. Sync `sot/mainline` — les workflows #601 sont bien présents
2. Déclenchement manuel (`workflow_dispatch`) des 3 workflows
3. Observation des résultats et logs
4. Documentation des bugs
5. Correction des workflows (blocage prouvé)
