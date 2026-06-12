---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_PARENT
doc_type: chantier_parent
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - directory
  - synthesis
  - repo
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Plan valide"
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/02_go_map.md
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

# GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01

## Classification
gouvernance + chantier parent + synthese repo-first par repertoire

## Role recommande
lecteur de surfaces canonique + cartographe repo + arbitre de decoupage des lots de synthese

## Besoin initial
Produire une synthese par repertoire du repo `opt-trading`, sans repartir dans une lecture file-by-file, sans melanger les surfaces actives et les caches locaux, et sans transformer la tache en chantier trop large pour etre exploitable.

## Cible finale
Disposer d'un chantier parent unique qui fixe :
- le decoupage integral de la synthese par blocs de repertoires
- la regle de lecture repo-first par surface top-level
- une synthese exploitable par repertoire, progressive et cumulable
- une distinction nette entre canonique, runtime, donnees/etat, support local et archive

## Source canonique
- Repo canonique : `opt-trading`
- Branche de travail dediee : `codex/repo-directory-synthesis-parent-01`

## ETABLI
- la racine du repo est stabilisee apres retrait du journal et reclassement des supports legacy
- `docs/architecture/REPO_SURFACES_MAP.md` fournit deja la carte canonique des surfaces top-level
- la demande courante porte sur une synthese par repertoire, pas sur un audit file-by-file
- le worktree contient deja d'autres modifications documentaires ; ce chantier doit s'y superposer sans les ecraser
- le bon niveau d'execution est un parent avec plan integral, puis des passes par blocs lisibles

## Regle de travail
- raisonner par repertoire top-level
- ne pas promouvoir caches, temporaires et archives au niveau des surfaces canoniques
- distinguer clairement :
  - surfaces canoniques de pilotage
  - surfaces runtime / operatoires
  - surfaces produit / donnees / etat
  - surfaces locales / archives / caches
- produire une synthese exploitable meme si tous les blocs ne sont pas encore deroules

## Plan valide

### Bloc A - Surfaces canoniques de pilotage
- `docs/`
- `registry/`
- `workflow_ai/`

But :
- figer les surfaces qui gouvernent la lecture du repo
- clarifier la relation entre gouvernance, index operatoires et doctrine d'execution

### Bloc B - Surfaces runtime et operatoires
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
- decrire les surfaces qui portent l'execution, les wrappers, les briques partagees et les outillages operatoires

### Bloc C - Surfaces produit, donnees et etat
- `data/`
- `state/`
- `student/`
- `tests/`
- `tradingview/`
- `contracts/`
- `audit/`

But :
- distinguer les sous-produits, l'etat persistant, les surfaces machine et les zones de preuve / validation

### Bloc D - Surfaces support, archive et local-only
- `_archive/`
- `tmp/`
- `__pycache__/`
- `.ruff_cache/`
- `.uv-cache/`
- `.uv-python/`
- `.secrets/`

But :
- borner ce qui releve du support local, de l'archive ou du cache
- eviter toute confusion avec les surfaces actives du repo

## Anti-cibles
Ne pas faire :
- synthese file-by-file de tout le repo dans ce parent
- reclassification physique opportuniste pendant la lecture
- reouverture de la doctrine des surfaces deja tranchee
- confusion entre support local et source canonique

## Gap restant
Il reste a produire :
1. un recap parent de synthese si la lecture doit etre gelée en un seul document
2. un arbre repo-level des references et dependances pour preparer les reclassements
3. un plan de classement optimal aligne sur cet arbre
4. un closeout parent si la profondeur atteinte est jugée suffisante
5. a defaut, un ou plusieurs lots enfants seulement si une cartographie interne plus fine devient necessaire

## GO suivants proposes

### GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_CANON_01
Bloc A : surfaces canoniques de pilotage.

### GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_RUNTIME_01
Bloc B : surfaces runtime et operatoires.

### GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_STATE_01
Bloc C : surfaces produit, donnees et etat.

### GO_OPT_TRADING_CHILD_DIRECTORY_SYNTHESIS_LOCAL_01
Bloc D : surfaces support, archive et local-only.

## TODO
- figer le plan integral
- verifier si la synthese top-level + Blocs A-D suffit
- produire un recap parent si utile
- n'ouvrir des enfants que si un besoin de profondeur supplementaire est prouve

## REPRISE
Point de reprise recommande :
`GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01`

Sequence :
synthese top-level -> Bloc A -> Bloc B -> Bloc C -> Bloc D -> recap parent ou closeout

## RISKS

- À qualifier.
