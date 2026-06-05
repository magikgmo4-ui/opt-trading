---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_GO_MAP
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - directory
  - synthesis
  - go_map
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Sequence canonique"
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/11_synthese_bloc_a_canoniques.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/12_synthese_bloc_b_runtime.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/13_synthese_bloc_c_state.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/14_synthese_bloc_d_local.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/92_plan_classement_optimal.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/93_priorisation_reclassements.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/90_recap_parent.md
---

# GO_MAP — GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01

## Objet
Cartographier la sequence canonique de synthese du repo par repertoire, du plus structurant au plus local.

## Regle
Le present fichier fige le decoupage complet, mais seul le Bloc A est demarre dans ce lot.

## Sequence canonique

### Etape 1 - Synthese top-level
Livrable :
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md`

But :
- etablir la liste des repertoires top-level
- donner une qualification courte par surface
- figer le decoupage de travail

Etat :
- ouverte et demarree dans ce lot

### Etape 2 - Bloc A : pilotage canonique
GO futur propose :
- `GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_CANON_01`

Repertoires :
- `docs/`
- `registry/`
- `workflow_ai/`

But :
- decrire la gouvernance documentaire, les index operatoires et la doctrine d'execution

Etat :
- demarre dans ce lot via un premier livrable parent

### Etape 3 - Bloc B : runtime et operatoire
GO futur propose :
- `GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_RUNTIME_01`

Repertoires :
- `modules/`
- `scripts/`
- `shared/`
- `adapters/`
- `schemas/`
- `perf/`
- `tools/`
- `packages/`
- `deploy_module_multi_machine/`

But :
- cartographier les surfaces qui executent, relient ou pilotent le runtime

Etat :
- demarre dans ce lot via un livrable parent

### Etape 4 - Bloc C : produit, donnees, etat
GO futur propose :
- `GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_STATE_01`

Repertoires :
- `data/`
- `state/`
- `student/`
- `tests/`
- `tradingview/`
- `contracts/`
- `audit/`

But :
- separer preuves, etat, donnees, surfaces machine et contrats specialises

Etat :
- demarre dans ce lot via un livrable parent

### Etape 5 - Bloc D : local, archive, cache
GO futur propose :
- `GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_LOCAL_01`

Repertoires :
- `_archive/`
- `tmp/`
- `__pycache__/`
- `.ruff_cache/`
- `.uv-cache/`
- `.uv-python/`
- `.secrets/`

But :
- borner les surfaces locales, de cache ou d'archive

Etat :
- demarre dans ce lot via un livrable parent

### Etape 6 - Closeout parent
But :
- regrouper les syntheses par bloc
- figer un recap parent unique
- refermer le parent si tous les blocs utiles ont ete deroules

Etat :
- recap parent produit ; decision de closeout encore a arbitrer

## Conditions de passage
On ne passe a l'etape suivante que si :
- le bloc precedent a une synthese exploitable
- la distinction canonique / runtime / local reste claire
- aucun repertoire local-only n'est surpromu comme surface active
- tout reclassement propose est compatible avec les dependances repo-level verifiees

## RISKS

- À qualifier.
