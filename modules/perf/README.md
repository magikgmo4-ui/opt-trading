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
- `scripts/perf_db_relocate.sh`
- `app.py` -> shim vers `perf/perf_app.py`
- `webhook.py` -> shim vers `adapters/webhook_to_perf.py`
- `engine/` -> shim vers `modules/perf_engine/`
- `data/` -> emplacement canonique candidat pour `perf.db`

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

## DB relocation tooling

Un outillage non destructif existe maintenant :

```bash
bash modules/perf/scripts/perf_db_relocate.sh status
bash modules/perf/scripts/perf_db_relocate.sh copy
bash modules/perf/scripts/perf_db_relocate.sh show-env
```

Ce script ne change pas le runtime par défaut. Il prépare seulement la copie
vers le chemin canonique candidat et affiche l'override `PERF_DB_PATH`.

## DB path switch behavior

Les launchers canoniques PERF preferent maintenant :

1. `PERF_DB_PATH` si deja exporte
2. `modules/perf/data/perf.db` si ce fichier existe
3. fallback legacy `perf/perf.db`

Le fallback legacy reste automatique.
