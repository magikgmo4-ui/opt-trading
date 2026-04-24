# webhook

Couche interne de normalisation et de handling du flux webhook avant integration dans le serveur racine.

## Role
- parser un payload entrant vers un format stable
- appliquer le handling minimal autour de la validation, du lock et de la persistance d'evenement
- separer la logique reusable du gros entrypoint `webhook_server.py`

## Contenu
- `parse.py` : normalisation du payload entrant
- `schema.py` : types / schema webhook
- `handlers.py` : orchestration locale `parse -> require_key -> enforce_lock -> record_event`
- `scripts/` : wrappers `cmd`, `menu`, `sanity`

## Integration
- travaille en appui de `webhook_server.py`
- utilise `modules.auth.webhook_key` indirectement via la couche legacy passee au handler
- ecrit ensuite dans la chaine runtime qui alimente `state/` et eventuellement `perf/`

## Statut
- actif
- support runtime du bord d'entree webhook

## Notes de consolidation
- conserver la logique reusable ici plutot que dans `webhook_server.py` si la decomposition continue
- ne pas confondre cette surface avec le fichier racine `webhook_server.py`, qui reste l'entrypoint applicatif
