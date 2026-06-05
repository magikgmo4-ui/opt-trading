# UI Registry — Data / Storage / Screenshots

## Stockages visibles déjà indexés précédemment
- `data/dashboard`
- `data/desk_runs`
- `data/perf`
- `data/journal`
- `desk/snapshots`
- `desk/inputs`
- `desk/state`
- `shared/`

## Direction validée
- **Garder les screenshots avec les analyses passées**.
- Ne pas jeter les captures/analyse utiles dans un nettoyage agressif.
- Les artefacts non critiques, intermédiaires, ou non reliés à une analyse peuvent ensuite être déplacés vers une routine quotidienne.

## Catégorie dédiée à créer / formaliser
### `ui/screenshots_analyses_passees`
Doit servir à cartographier :
- où sont stockées les captures,
- où vivent les analyses associées,
- quels modules lisent/produisent ces artefacts,
- quelles vues futures devront les exposer côté opérateur.

## Lecture initiale
Le pipeline `vision_bot` / `bot_vision` / `desk_capture_inputs` / `desk_analyze` est probablement le cœur de cette catégorie UI.

## RISKS

- À qualifier.
