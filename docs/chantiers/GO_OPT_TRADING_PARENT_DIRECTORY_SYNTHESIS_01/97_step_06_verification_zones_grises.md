---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_STEP_06_NOTE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - step-06
  - zones-grises
  - qualification
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
  - packages/collectors_core/README.md
  - student/README.md
  - student/INDEX.md
  - modules/desk_pro_dashboard/README.md
  - student/validation/HANDOFF.md
---

# Step 06 — verification des zones grises

## Statut
Complete.

## Objectif
Qualifier les surfaces encore grises du top-level sans ouvrir de refactor physique ni de lot enfant inutile.

## Scope
- `packages/`
- `tests/`
- `student/`
- `data/`
- `audit/`

## Verifications utilisees
- lecture du contenu reel des cinq surfaces
- lecture des entrypoints documentaires locaux quand ils existent
- recherche repo ciblee des references et consommateurs
- verification ciblee de chemins de preuve references dans `audit/`

## Decision par surface

### 1. `packages/`
Etat observe :
- `packages/collectors_core/` contient `src/`, `tests/` et `README.md`
- `collectors_core` se presente comme un package partage de concerns runtime transverses

References observees :
- `modules/collector_coingecko/*` importe `collectors_core` et injecte `packages/collectors_core/src` dans `PYTHONPATH`
- `modules/collector_binance_spot/*` fait de meme
- la doc collectors repo-level le traite comme fondation partagee

Decision :
- `packages/` est une surface top-level justifiee
- statut retenu : support runtime durable, distinct de `modules/`
- pas de besoin d'enfant dedie a ce stade

### 2. `tests/`
Etat observe :
- au top-level, `tests/` ne contient que `__pycache__/test_shared_explorer_api.cpython-314.pyc`
- aucun fichier source de test humainement maintenu n'est observe dans `tests/`

References observees :
- les tests reels observes vivent surtout dans `modules/*/tests` et `packages/collectors_core/tests`
- `packages/collectors_core/tests/README.md` indique meme que la strategie de test reste a figer pour ce package
- `modules/dev_validation_hub/scripts/*` pointe vers des tests sous `modules/memory_bricks/tests`

Decision :
- `tests/` top-level n'est pas aujourd'hui une vraie surface structurante
- statut retenu : faible / residuel / non pilotant
- ne pas promouvoir `tests/` comme surface canonique forte tant qu'il n'y a pas de contenu source reel

### 3. `student/`
Etat observe :
- surface riche avec `bin/`, `config/`, `docs/`, `exports/`, `scripts/`, `validation/`, plus `README.md` et `INDEX.md`
- les entrypoints canoniques declares sont `student_cmd.sh`, `student_menu.sh`, `student_sanity_check.sh`

References observees :
- `student/README.md` et `student/INDEX.md` fixent `/opt/trading/student` comme racine canonique
- `scripts/install_student_shortcuts.sh` cree `menu-student`, `cmd-student`, `sanity-student`
- `student/validation/*` porte une vraie couche operatoire et de preuve

Decision :
- `student/` est une surface machine distincte, pas un sous-bucket de donnees
- statut retenu : surface active contextuelle mais legitime au top-level
- ne pas la fusionner avec `data/` ni `audit/`

### 4. `data/`
Etat observe :
- `data/` contient des sous-buckets metier par domaine : `dashboard`, `decision`, `derivatives`, `desk_runs`, `execution`, `journal`, `liquidation`, `perf`, `portfolio`, `position`, `probability`, `ranker`, `risk`, `scan`
- les contenus observes sont principalement des artefacts dates et des repertoires de runs

References observees :
- `modules/desk_pro_dashboard/README.md` lit explicitement `data/desk_runs/`
- des scripts admin-trading lisent aussi `data/desk_runs`
- `data/journal/` contient des artefacts de donnees, pas une surface de continuite documentaire

Decision :
- `data/` reste un bucket downstream de sous-produits metier
- statut retenu : actif, mais non souverain
- ne pas le confondre avec `student/` ni avec des preuves `audit/`

### 5. `audit/`
Etat observe :
- `audit/2026-03-20/` ne contient qu'un seul fichier : `student_validation_pack_20260320.zip`

References observees :
- `student/validation/HANDOFF.md` et `LIVE_EXEC_HANDOFF.md` referencent des fichiers comme `audit/2026-03-20/92_student_canonical_surface.md`
- verification explicite : ces chemins `.md` n'existent pas dans l'arborescence observee
- inspection du zip `audit/2026-03-20/student_validation_pack_20260320.zip` : il contient un pack `student/validation/*`, pas les fichiers `audit/2026-03-20/*.md` cites par ces docs

Decision :
- `audit/` reste une surface de preuve top-level legitime
- statut retenu : archive active de preuves ponctuelles, non canonique
- point de vigilance : l'etat actuel est opaque, car la preuve est zippee alors que certaines docs pointent vers des fichiers non presents en clair
- ce point appelle une hygiene documentaire ciblee, pas une reclassification structurelle

## Frontieres retenues
- `packages/` = code mutualisable partage
- `tests/` = aujourd'hui non structurant au top-level
- `student/` = surface machine distincte
- `data/` = sorties et runs downstream
- `audit/` = preuves ponctuelles et packs d'audit

## Fichiers modifies
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md`

## Rollback
- revert doc-only de `94_plan_execution_step_by_step.md`
- suppression de cette note si le step est annule

## Resultat
Les cinq zones grises sont maintenant qualifiees sans ouvrir de nouveau lot de cartographie.

## Point de reprise
Passer a l'arbitrage enfant. Sauf nouveau besoin de profondeur, aucun enfant n'est justifie a ce stade.
