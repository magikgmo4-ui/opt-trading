---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_REAL_BROKER_MEASUREMENT_01
status: CLOSED
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
---

# GO: Trading Lab Real Broker Measurement

## Objectif

Lancer `trading_lab_v1 run-with-outcomes` sur un export broker réel XAUUSD M1 placé localement dans `state/trading_lab_v1/inputs/` afin de produire une première mesure exploitable sans committer les données sensibles.

## Règles absolues

- Ne pas committer `state/` (gitignored)
- Ne pas committer d'export broker brut
- Ne pas promouvoir `perf_status` sans seuil de données suffisant
- Ne pas inventer de résultats si données absentes

## Verdict attendu

- `PASS_TRADING_LAB_REAL_BROKER_MEASUREMENT_01` si données présentes et mesure produite
- `BLOCKED_NO_BROKER_INPUT_TRADING_LAB_REAL_BROKER_MEASUREMENT_01` si données absentes
