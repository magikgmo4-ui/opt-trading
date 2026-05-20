---
doc_id: GO_PERF_ENGINE_STRATEGY_SCORE_01_METRICS_AND_GATES
doc_type: methodology
repo: opt-trading
go_id: GO_PERF_ENGINE_STRATEGY_SCORE_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_METRICS_AND_GATES

## Métriques standard (V1)

- `sample_size`: nombre d’events pour la stratégie
- `observation_days`: jours distincts observés
- `pass_rate`: ratio PASS/APPROVED sur events ayant un verdict
- `win_rate`: ratio win sur events ayant un outcome
- `pnl_cumulative`: somme `pnl_net` si présent
- `expectancy`: moyenne `pnl_net` sur events ayant un pnl
- `max_drawdown`: drawdown max sur série cumulative pnl (ordre temporel)

## Gates (V1, paramétrables)

Promotion gate (default thresholds):

- `min_sample_size` = 30
- `min_observation_days` = 14
- `min_pass_rate` = 0.80

Verdicts:

- `PROMOTE_RECOMMENDED` si tous les seuils sont atteints
- `INSUFFICIENT_SAMPLE` si sample/days insuffisants
- `BLOCKED_LOW_PASS_RATE` si pass_rate sous seuil

Retirement gate (placeholder V1):

- `KEEP_OBSERVING` par défaut (pas de règle auto tant que perf engine n’est pas branché à un consumer officiel)
