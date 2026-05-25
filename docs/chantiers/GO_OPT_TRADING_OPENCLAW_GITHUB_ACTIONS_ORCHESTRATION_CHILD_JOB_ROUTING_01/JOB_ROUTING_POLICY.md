---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_JOB_ROUTING_01_POLICY
doc_type: policy
---

# Job Routing Policy

## Principe

Tout job GitHub Actions orchestré par OpenClaw doit passer par un routage contrôlé qui valide :
- L'existence du job dans le registry
- Le flag `orchestrable_by_openclaw=true`
- Un `workflow` non null
- Un `risk_level` autorisé
- Un `owner_surface` autorisé
- Le flag `requires_secret` avec confirmation explicite si true

## Filtres

| Filtre | Comportement |
|---|---|
| `job_id` | Sélection exacte |
| `role` | Correspondance exacte |
| `risk_level` | `low` autorisé par défaut ; `medium` sur confirmation ; `high` refusé |
| `owner_surface` | `github_actions` autorisé ; `openclaw` sur confirmation |
| `requires_secret` | `false` autorisé ; `true` nécessite `--allow-secrets` |
| `status` | `implemented_existing` ou `implemented_child_go` autorisé |

## Rejets

| Raison | Condition |
|---|---|
| NOT_ORCHESTRABLE | `orchestrable_by_openclaw != true` |
| NO_WORKFLOW | `workflow` est null ou vide |
| RISK_TOO_HIGH | `risk_level` > seuil autorisé |
| SURFACE_NOT_ALLOWED | `owner_surface` non autorisé |
| SECRET_REQUIRED | `requires_secret=true` sans `--allow-secrets` |
| STATUS_NOT_READY | `status` non autorisé |
