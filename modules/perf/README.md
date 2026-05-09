# perf

Surface canonique compatibilite-first pour la famille PERF.

## Role
- fournir des wrappers `cmd/menu/sanity` pour la surface Perf
- exposer une structure canonique sous `modules/perf/`
- conserver les anciens chemins runtime tant que la migration complete n'est pas validee

## Structure actuelle
- `scripts/cmd.sh`
- `scripts/menu.sh`
- `scripts/sanity_check.sh`
- `app.py` -> shim vers `perf/perf_app.py`
- `webhook.py` -> shim vers `adapters/webhook_to_perf.py`
- `engine/` -> shim vers `modules/perf_engine/`

## Integration
- le runtime canonique prefere est `uvicorn modules.perf.app:app`
- le runtime historique `uvicorn perf.perf_app:app` reste valide par compatibilite
- le moteur canonique prefere est `modules.perf.engine.app.perf_engine`
- le moteur historique `modules.perf_engine.app.perf_engine` reste valide par compatibilite

## Statut
- compatibilite non cassante active
- anciens chemins conserves
- nouvelle structure canonique disponible et referencee par les scripts mis a jour

## Notes de restructuration
- ne pas casser `desk_pro` pendant la convergence
- ne pas changer le chemin SQLite dans ce lot
- ne pas retirer les anciens chemins avant validation operatoire
