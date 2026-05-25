---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01_RISK
doc_type: risk_filters
---

# Risk Filters

## Niveaux de risque

| Niveau | Comportement OpenClaw |
|---|---|
| `low` | Autorisé sans confirmation |
| `medium` | Autorisé avec flag `--allow-medium-risk` |
| `high` | Refusé (bloqué en dur) |

## Surfaces autorisées

| Surface | Comportement |
|---|---|
| `github_actions` | Autorisé par défaut |
| `openclaw` | Autorisé avec flag `--allow-openclaw-surface` |

## Secrets

| requires_secret | Comportement |
|---|---|
| `false` | Autorisé |
| `true` | Nécessite `--allow-secrets` |

## Statut

| status | Comportement |
|---|---|
| `implemented_existing` | Autorisé |
| `implemented_child_go` | Autorisé |
| `planned_after_actions_pass` | Refusé (pas encore prêt) |
| `draft_opening_bundle` | Refusé (pas encore prêt) |
| autre / absent | Refusé |
