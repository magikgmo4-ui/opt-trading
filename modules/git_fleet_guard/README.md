# git_fleet_guard

Module durable OPT-TRADING pour auditer l'état Git sur plusieurs machines sans action destructive par défaut.

## Garanties V1
- lecture seule par défaut
- aucun reset automatique
- aucun rebase automatique
- aucun stash automatique
- aucun push automatique
- rapport JSON + Markdown à chaque audit

## Commandes
- `cmd-git_fleet_guard status`
- `cmd-git_fleet_guard audit`
- `cmd-git_fleet_guard audit --machines student,db-layer`
- `cmd-git_fleet_guard report`
- `menu-git_fleet_guard`

## Sorties
Les rapports sont écrits sous `modules/git_fleet_guard/reports/` :
- `latest.json`
- `latest.md`
- rapports horodatés

## Classification des écarts
- `utile_probable`
- `artefact_probable`
- `ambigu`
- `propre`

## Notes
- Le module peut faire un `git fetch origin` par défaut pour refléter l'état distant sans modifier l'arbre de travail.
- Utiliser `--no-fetch` si tu veux un audit 100% sans refresh des refs distantes.
