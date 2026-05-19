# env

Module minimal de bootstrap environnement et repertoires runtime locaux.

## Role
- charger `.env` si `python-dotenv` est disponible
- exposer le `project_root`
- garantir l'existence de `tmp/` et `data/`

## Contenu
- `env.py` : `project_root()`, `load_env()`, `ensure_dirs()`, `get_setting()`
- `scripts/` : wrappers `cmd`, `menu`, `sanity`

## Integration
- `webhook_server.py` appelle `load_env()` et `ensure_dirs()`
- `perf/perf_app.py` appelle `load_env()` et `ensure_dirs()`

## Statut
- actif
- brique de bootstrap transverse

## Notes de consolidation
- garder ce module volontairement petit
- eviter d'y ajouter de la logique produit ou de secret management avance, qui releve plutot de `auth`
