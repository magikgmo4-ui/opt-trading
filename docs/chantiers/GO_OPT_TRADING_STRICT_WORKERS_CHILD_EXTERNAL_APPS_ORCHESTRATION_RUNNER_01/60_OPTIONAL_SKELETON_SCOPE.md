# Optional Skeleton — Orchestration Runner

## Scope

Création d'un squelette non-exécutant dans `scripts/ai/workers/orchestration/`.

## Fichiers

| Fichier | Rôle |
|---|---|
| `README.md` | Présentation du dossier |
| `external_apps_orchestration_contract.json` | Contrat générique input/output (JSON Schema) |
| `sample_request.readonly.json` | Exemple de requête READ_ONLY (schedule hebdo) |
| `sample_response.pass.json` | Exemple de réponse PASS (READ_INVENTORY validé) |

## Ce qui n'est PAS dans ce squelette

- Aucun code d'exécution (Python, Bash, etc.)
- Aucun appel API réel
- Aucune modification des workflows CI
- Aucune modification des job packets existants
- Aucune modification de `tasks.index.json` ou `models.registry.json`
- Aucun secret, token ou credential

## Prochaine étape

L'implémentation réelle de l'adaptateur OpenClaw viendra dans un GO séparé :
`GO_OPT_TRADING_STRICT_WORKERS_CHILD_OPENCLAW_ADAPTER_IMPL_01`.
