# scripts

Surface module legere pour exposer les wrappers standard autour d'un espace `scripts`.

## Role
- fournir un point d'entree module uniforme `cmd/menu/sanity`
- offrir une facade d'exploration locale sans se confondre avec la racine `scripts/`

## Contenu
- `scripts/cmd.sh` : commandes generiques `info`, `readme`, `ls`, `grep`, `menu`
- `scripts/menu.sh`, `scripts/install_shortcuts.sh`, `scripts/sanity_check.sh`

## Integration
- ce module n'est pas la racine `scripts/`
- il sert uniquement de surface module dans l'ecosysteme `modules/`
- sa valeur actuelle est surtout structurelle et operatoire

## Statut
- actif mais tres leger
- module wrapper, sans logique metier propre observee a ce stade

## Notes de consolidation
- a traiter avec les conventions `repo / tooling / authoring`, pas comme verticale produit
- candidat a une clarification forte de role avant tout move ou suppression
