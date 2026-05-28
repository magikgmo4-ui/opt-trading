---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_JOBS_SPEC
doc_type: jobs_registry_spec
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
updated_at: 2026-05-28
---

# 20_JOBS_REGISTRY_SPEC

## Objectif

Définir le schéma du registre de jobs avant de l'alimenter.
Le registre réel est produit par `GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01`.

## Définition d'un "job"

Un job est toute unité d'exécution déclenchable :
- workflow GitHub Actions (`.github/workflows/*.yml`) ;
- script shell opérateur (`scripts/*.sh`, `modules/*/scripts/*.sh`) ;
- task AI worker (`scripts/ai/workers/job_packets/*.json`) ;
- runner Python autonome (`cmd.sh` + `app/__main__.py`) ;
- job OpenClaw (défini dans `tools.json5` ou `agents.json5`).

## Schéma du registre

| Champ | Type | Description |
|---|---|---|
| `job_id` | string | identifiant canonique unique |
| `path` | string | chemin relatif depuis repo root |
| `type` | enum | `gha / shell / python / openclaw / ai_worker` |
| `trigger` | enum | `push / pr / schedule / manual / webhook / openclaw_call` |
| `owner_surface` | string | module ou surface propriétaire |
| `inputs` | string | fichiers, variables, secrets requis |
| `outputs` | string | artefacts produits (fichiers, DB, logs, rapport) |
| `permissions` | string | secrets GHA, droits filesystem, réseau |
| `status` | enum | `active / candidate / experimental / deprecated / blocked` |
| `tests` | string | test ou smoke associé, ou `none` |
| `risk` | enum | `high / medium / low` |
| `next_action` | enum | `keep / add_test / merge_with / deprecate / delete_after_proof / blocked` |

## Types de jobs (enum)

| Type | Exemples |
|---|---|
| `gha` | `.github/workflows/gated-pr.yml` |
| `shell` | `scripts/smoke.sh`, `modules/*/scripts/cmd.sh` |
| `python` | `modules/risk_engine/app/risk_engine.py` (runner direct) |
| `openclaw` | jobs définis dans `tools.json5` |
| `ai_worker` | `scripts/ai/workers/job_packets/*.json` + `run_task.sh` |

## Triggers (enum)

| Trigger | Description |
|---|---|
| `push` | push sur branche définie |
| `pr` | pull_request vers branche cible |
| `schedule` | cron GHA ou tmux cron |
| `manual` | `workflow_dispatch` ou appel opérateur direct |
| `webhook` | POST TradingView ou autre |
| `openclaw_call` | invocation via OpenClaw agent |

## Statuts (enum)

| Statut | Signification |
|---|---|
| `active` | en production, consommé prouvé |
| `candidate` | opérationnel mais pas encore prouvé en production |
| `experimental` | test / prototype |
| `deprecated` | remplacé, à supprimer |
| `blocked` | consommateur inconnu ou permissions manquantes |

## Fichier cible

```text
docs/registry/JOBS_REGISTRY.md
```

Même emplacement que `CODE_REGISTRY.md`. Format Markdown + frontmatter YAML.

## Scope v1 du registre

| Famille | Entrées estimées |
|---|---|
| GHA workflows | 7 |
| AI workers job_packets | ~10-20 |
| Scripts opérateurs clés | ~15 |
| Modules cmd.sh (runner) | ~30 |
| OpenClaw jobs | à inventorier |

Total estimé v1 : 60-80 entrées.
