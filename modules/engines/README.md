# engines

Registry et routeur minimal pour les moteurs de trading declares dans le repo.

## Role
- enregistrer les handlers d'engine
- exposer la liste des engines connus
- router un payload vers le handler correspondant
- fournir un point de compatibilite simple pour les moteurs legacy ou implicites

## Contenu
- `registry.py` : registre central des handlers et des noms d'engine
- `router.py` : routage vers le handler cible avec retour d'erreur standardise
- `__init__.py` : description courte de la surface
- `scripts/engines_cmd.sh` : commandes `list`, `test`, `sanity`
- `scripts/menu.sh`, `scripts/cmd.sh`, `scripts/sanity_check.sh`

## Integration
- importe par `modules.engines.router` et `modules.engines.registry`
- sert de couche de coordination legere pour les engines cites par `webhook_server.py`
- ne remplace pas les modules metier comme `decision_engine`, `risk_engine` ou `execution_engine`

## Statut
- actif
- module de coordination et de compatibilite, pas suite produit autonome

## Notes de consolidation
- a garder distinct des modules `*_engine` :
  - `engines` coordonne et route
  - les autres modules portent la logique metier specialisee
- relevant de `Step 06` pour durcir les contracts, pas pour une fusion physique rapide
