# git_fleet_guard

Module durable OPT-TRADING pour auditer l'état Git sur plusieurs machines sans action destructive par défaut.

## Garanties V1 / V1.1
- lecture seule par defaut
- aucun fetch par defaut
- aucun reset automatique
- aucun rebase automatique
- aucun stash automatique
- aucun push automatique
- aucune remediaton Git automatique
- rapport JSON + Markdown a chaque audit

## Commandes
- `cmd-git_fleet_guard status`
- `cmd-git_fleet_guard audit`
- `cmd-git_fleet_guard audit --machines student,db-layer`
- `cmd-git_fleet_guard audit --fetch`
- `cmd-git_fleet_guard report`
- `cmd-git_fleet_guard remediate`
- `menu-git_fleet_guard`

## Sorties
Les rapports sont écrits sous `modules/git_fleet_guard/reports/` :
- `latest.json`
- `latest.md`
- rapports horodatés

## Classification des écarts
- statut machine: `clean`, `review_required`, `inaccessible`
- tri des changements locaux: `utile_probable`, `artefact_probable`, `ambigu`, `propre`

## Notes
- branche cible par defaut: `origin/sot/mainline`
- machines V1: `admin-trading`, `student`, `db-layer`
- utiliser `--fetch` uniquement si un refresh explicite des refs distantes est voulu
- `remediate` lit `latest.json` par defaut et propose uniquement des commandes guidees a executer manuellement
