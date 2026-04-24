# desk_pro

Surface partagee Desk Pro pour l'API `/desk/*`, le rendu UI embarque et la logique de service associee.

## Role
- exposer les routes FastAPI Desk Pro
- fournir le montage UI dans une app hote
- centraliser les modeles et services utilises par la surface Desk Pro

## Structure
- `api/routes.py` : endpoints `/desk/*`
- `service/` : aggregation et scoring
- `ui/page.py` : rendu HTML
- `mount.py` : montage dans une app FastAPI
- `models.py` : schemas et modeles
- `scripts/` : wrappers `cmd`, `menu`, `sanity`

## Integration
- utilise par `perf/perf_app.py` via `modules.desk_pro.api.routes` et `modules.desk_pro.mount`
- sert de coeur commun pour `desk_pro_runner`, `desk_pro_dashboard` et la stack Desk Pro au sens large

## Statut
- actif
- centre de gravite fonctionnel de la suite Desk Pro
- a lire avec `modules/desk_pro_runner/README.md` et `modules/desk_pro_orchestrator/README.md`

## Notes de consolidation
- ne pas confondre cette surface partagee avec les facades operateur `desk_pro_runner` ou `desk_pro_dashboard`
- les frontieres `desk_pro` / `desk_common` / `desk_pro_*` doivent etre clarifiees avant tout move physique
