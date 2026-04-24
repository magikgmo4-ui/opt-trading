# perf

Facade module pour la surface Perf, avec wrappers generiques autour du sous-systeme applicatif.

## Role
- fournir des wrappers `cmd/menu/sanity` pour la surface Perf
- offrir un point d'entree module-compatible, meme si l'app principale vit hors `modules/`

## Contenu
- `scripts/cmd.sh`
- `scripts/menu.sh`
- `scripts/sanity_check.sh`

## Integration
- l'app principale reste `perf/perf_app.py`
- cette facade sert surtout a l'exposition operateur uniforme de la surface Perf

## Statut
- actif mais mince
- facade operatoire, pas source principale du code Perf

## Notes de consolidation
- ne pas dupliquer ici la logique de `perf/perf_app.py`
- si la surface Perf est consolidee plus tard, la question est surtout facade vs app, pas fusion de code
