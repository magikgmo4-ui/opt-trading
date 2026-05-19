# GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01` |
| Objet | Définir l'architecture et le contrat du runner d'orchestration pour strict workers + apps externes |
| Déclencheur | CI chain validée (22/22 PASS) ; besoin de séparer validation GitHub Actions de l'orchestration réelle |
| Source | `run_task.sh`, `_validate_job.py`, `tasks.index.json`, `models.registry.json`, `strict-workers-*.yml`, bridges existants |
| Branche | `go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01` |

## Problème

GitHub Actions ne doit pas être l'orchestrateur principal des apps externes.
- `strict-workers-schedule.yml` valide/génère un prompt mais n'exécute pas l'IA worker
- Aucun modèle de langage ni accès API externe dans le runner GitHub
- Les bridges existants (airtable_bridge, ClickUp cockpit, Botpress gateway) n'ont pas de runner contract unifié

## Décision d'architecture

| Couche | Rôle |
|---|---|
| GitHub Actions | Valider les packets, lancer un smoke, vérifier qu'aucun fichier tracké n'est modifié |
| OpenClaw | Choisir le worker, orchestrer le job, appliquer les gates |
| OpenCode | Exécuter localement dans un environnement avec accès modèle/app contrôlé |
| App bridge | Écrire ou lire dans ClickUp, Airtable, Botpress, Telegram, Google Sheets |
| Repo opt-trading | Stocker preuves, logs, closeouts, outputs |
| Humain / modèle fort | Validation finale avant tout write durable |

## Périmètre de ce GO

- Définir le contrat du runner d'orchestration
- Documenter les gates par app bridge
- Définir les stop conditions
- Ne pas créer de code d'exécution
- Ne pas modifier les workflows, registry, index
