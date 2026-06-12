---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_RECAP
doc_type: chantier_recap
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: recap
topic_keys:
  - opt-trading
  - directory
  - synthesis
  - recap
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/11_synthese_bloc_a_canoniques.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/12_synthese_bloc_b_runtime.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/13_synthese_bloc_c_state.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/14_synthese_bloc_d_local.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/91_arbre_references_dependances.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/92_plan_classement_optimal.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/93_priorisation_reclassements.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
---

# Recap parent — synthese par repertoire

## Objet
Regrouper la lecture du repo par grands blocs de repertoires, sans rebasculer dans une cartographie file-by-file.

## Noyau retenu
- `docs/`, `registry/`, `workflow_ai/` forment le noyau canonique de pilotage
- `modules/` et `scripts/` forment le coeur runtime / operatoire
- `shared/`, `adapters/`, `schemas/`, `tools/`, `packages/`, `perf/`, `deploy_module_multi_machine/` servent d'appui ou de sous-systemes specialises
- `data/`, `state/`, `student/`, `tests/`, `tradingview/`, `contracts/`, `audit/` portent la matiere produite, l'etat, les surfaces machine et les preuves
- `_archive/`, `tmp/`, caches et surfaces locales restent explicitement subordonnes

## Lecture structurante
1. pilotage canonique : `docs/` -> `registry/` -> `workflow_ai/`
2. execution et ops : `modules/` + `scripts/`
3. etat / donnees / machine : `data/`, `state/`, `student/`
4. supports specialises : `perf/`, `tools/`, `contracts/`, `tradingview/`, `audit/`
5. local / archive / cache : `_archive/`, `tmp/`, `__pycache__/`, `.ruff_cache/`, `.uv-cache/`, `.uv-python/`, `.secrets/`

## Points de vigilance
- `modules/` reste trop dense pour etre considere comme completement cartographie a ce niveau
- `scripts/` melange wrappers structurants et helpers contextuels
- `data/journal/` est un bucket de donnees, pas une reintroduction du systeme `journal/` supprime
- `tests/` est faible au niveau top-level ; la verification semble distribuee ailleurs

## Decision de profondeur
La profondeur actuelle suffit si l'objectif est :
- reprendre rapidement le repo par grandes surfaces
- distinguer canonique / runtime / etat / local
- savoir ou lire avant d'ouvrir un lot plus fin

Un lot enfant supplementaire n'est justifie que si l'objectif devient :
- cartographier les familles internes de `modules/`
- qualifier les entrypoints canoniques de `scripts/`
- separer plus finement les sous-surfaces de `data/` ou `student/`

## Point de reprise
- soit garder le parent ouvert comme synthese de reference
- soit produire un closeout parent si cette profondeur est jugee suffisante
- soit ouvrir un enfant cible sur `modules/` ou `scripts/` si un besoin plus fin est prouve

## RISKS

- À qualifier.
