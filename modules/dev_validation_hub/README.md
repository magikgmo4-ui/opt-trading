# dev_validation_hub

Surface de validation developpeur pour verifier l'etat du repo et executer un petit cycle de checks hors runtime.

## Role
- lire l'etat Git courant du repo
- creer et reutiliser un venv local de validation
- installer un minimum de dependances de tests HTTP
- executer des checks de validation cibles, notamment sur `memory_bricks`
- exposer un etat pre-PR simple

## Contenu
- `docs/README.md` : cadrage et cycle d'usage
- `docs/RUNBOOK.txt` : consignes operatoires
- `scripts/cmd.sh` : commandes `status`, `pre-pr`, `ensure-venv`, `install-http-test-deps`, `run-memory-bricks-http-tests`, `trading-lab-status`
- `scripts/sanity.sh`, `menu.sh`, `install_shortcuts.sh`

## Integration
- surface dev-only, orientee machine de validation locale
- peut appeler `modules/trading_lab_v1/scripts/cmd.sh status`
- n'ouvre aucun role runtime, reseau ou prod

## Statut
- actif
- module d'hygiene et de validation locale, pas module metier

## Notes de consolidation
- a traiter avec la famille `Repo / tooling / authoring`
- a garder distinct des modules runtime et des hubs operatoires prod
