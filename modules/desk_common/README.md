# desk_common

Support commun de la suite Desk, actuellement centre sur les chemins runtime standardises et une facade de wrappers minimale.

## Role
- definir les chemins communs utilises par les surfaces Desk
- fournir une base legere partagee sans embarquer la logique produit Desk Pro complete

## Contenu
- `paths.py` : chemins `/opt/trading/desk/*`
- `scripts/` : wrappers generiques `cmd`, `menu`, `sanity`

## Statut
- actif mais mince
- module support, non entrypoint produit principal

## Notes de consolidation
- ce module a vocation a rester petit et partage
- toute logique metier ou UI Desk Pro doit rester dans `desk_pro` ou les modules `desk_pro_*`
- sa presence sans README etait source d'ambiguite dans la lecture de stack

## Statut de stack
- `desk_common` reste un support shared minimal
- il n'est ni un entrypoint produit, ni un survivant de stack
