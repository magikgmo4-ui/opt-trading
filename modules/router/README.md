# router

Facade de wrappers pour operations de routage et inspection locale de module.

## Role
- exposer une interface shell uniforme `cmd/menu/sanity`
- servir de point d'entree leger pour une surface de routage sans logique Python dediee aujourd'hui

## Contenu
- `scripts/cmd.sh` : inspection locale (`info`, `readme`, `ls`, `grep`, `menu`)
- `scripts/menu.sh` : menu wrapper
- `scripts/sanity_check.sh` : verification de structure

## Statut
- actif mais minimal
- surface operatoire de wrapper plus que module metier

## Notes de consolidation
- ne pas surpromouvoir ce module comme coeur runtime
- si une vraie logique de routage Python apparait, il faudra clarifier sa frontiere avec `modules.engines.router` et `registry_router`
