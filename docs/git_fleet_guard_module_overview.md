# git_fleet_guard — module overview

## But
Créer une méthode durable et fidèle au workflow pour auditer l'état Git sur plusieurs machines, sans action destructive par défaut.

## Perimetre V1
- admin-trading
- student
- db-layer

## Modes
- `status`
- `audit`
- `report`
- `remediate`

## Garanties
- read-only par défaut
- aucun reset/rebase/push/stash automatique
- rapport JSON + Markdown
- classification des écarts par machine
- remédiation guidée uniquement ; aucune commande Git n'est exécutée automatiquement

## Rapport
Le module écrit :
- un rapport JSON détaillé
- un rapport Markdown lisible
- un `latest.*` pour reprise rapide
