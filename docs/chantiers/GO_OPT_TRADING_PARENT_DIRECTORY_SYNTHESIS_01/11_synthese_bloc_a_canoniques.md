---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_BLOC_A
doc_type: chantier_synthese
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: active
lifecycle_stage: analyse
topic_keys:
  - opt-trading
  - directory
  - synthesis
  - bloc_a
  - canonical_surfaces
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - registry/README.md
  - workflow_ai/WORKFLOW.md
---

# Bloc A — surfaces canoniques de pilotage

## `docs/`
Role :
- surface canonique principale de gouvernance, continuite, architecture et chantiers

Structure observable :
- `architecture/` : cartographie et structure repo/runtime
- `chantiers/` : dossiers GO, parents, journaux techniques, decisions
- `governance/` : matrices, politiques, regles de lecture et continuite
- `index/` : surfaces operatoires de reprise (`GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `NEXT_GO_CANDIDATES`)
- `master_pack/` : ouverture de session, current state, mission starter pack
- `ot/` : closings, reports, kanban, Trae et surfaces OT specialisees
- sous-ensembles secondaires : `indexation_desk/`, `ui_indexation/`, `ui_screenshots/`, `product_targets/`, `project_management/`, `status/`, `trading/`, `opportunities/`, `simex/`, `hermes/`, `_backups/`

Lecture retenue :
- `docs/` porte la verite humaine versionnee du repo
- toutes les sous-surfaces n'ont pas le meme poids ; `governance/`, `index/`, `architecture/`, `master_pack/` et `ot/` structurent la lecture active
- `chantiers/` est la surface de travail documentaire par GO

Points d'entree utiles :
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` : matrice maitre souveraine
- `docs/index/GO_INDEX.md` : verite de liste des GO non clos
- `docs/index/REPRISE.md` : surface operatoire de reprise
- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` : ouverture de session canonique
- `docs/INDEX.md` : index de navigation utile, non souverain

Limites :
- `docs/` est une grande surface ; il faut distinguer les couches souveraines des annexes ou historiques
- `docs/INDEX.md` facilite la lecture, mais ne remplace ni la matrice maitre ni les index operatoires
- les closings, rapports et archives dans `docs/ot/` ou `_backups/` servent surtout la trace, pas la gouvernance courante

## `registry/`
Role :
- registre declaratif machine-readable du repo

Contenu observe :
- `machines_registry.yaml`
- `modules_registry.yaml`
- `ui_surfaces_registry.yaml`
- `wrappers_registry.yaml`
- `meta_index.yaml`
- `README.md`

Lecture retenue :
- `registry/` ne prouve pas le live, mais decrit le modele declaratif repo/package
- il complete `docs/` ; il ne remplace ni les preuves runtime ni les decisions de gouvernance
- sa valeur est forte pour les surfaces, wrappers et consommateurs automatises

Consommateurs explicites :
- `machines_registry.yaml` -> `modules/machines_registry_reader`
- `modules_registry.yaml` -> `modules/modules_registry_reader`
- `ui_surfaces_registry.yaml` -> `modules/ui_registry_msi`
- `wrappers_registry.yaml` -> `modules/wrappers_registry_reader`

Limites :
- la couverture `registry/` n'implique ni exhaustivite runtime ni installation prouvee
- certaines exceptions restent documentees dans `registry/README.md` plutot que de forcer une normalisation prematuree
- `registry/` est une couche de description ; l'arbitrage documentaire reste dans `docs/governance/*`

## `workflow_ai/`
Role :
- doctrine opposable d’execution IA

Structure observable :
- `WORKFLOW.md` : gates, validation, chaine de responsabilite, verdicts/statuts
- `templates/` : `specs.md`, `tasks.md`, `db_schema.md`, `api_contract.md`
- `prompts/` : prompts de support
- `scripts/` : wrappers et scripts d’installation/sanity
- fichiers de support : `.cursorrules`, `MANIFEST.json`, `ROLLBACK.md`, `CHANGELOG.md`

Lecture retenue :
- `workflow_ai/` n’est pas une doc generale du repo ; c’est la couche de conduite d’execution
- cette surface prime sur les anciens helpers Trae en cas de conflit de methode
- elle s’articule avec `docs/master_pack/mission_starter_pack/*` pour l’ouverture de session et avec `registry/` pour la description declarative

Artefacts directeurs :
- `WORKFLOW.md` : gates, roles, verdicts, conditions de cloture
- `templates/specs.md` : source de verite de mission / lot
- `templates/tasks.md` : plan atomique verifiable
- `ROLLBACK.md` : trame minimale de retour arriere

Limites :
- `workflow_ai/` ne decide pas a lui seul du produit, des priorites ou du statut des GO
- cette surface commence a l'execution ; elle ne remplace ni `GO_INDEX.md`, ni `REPRISE.md`, ni le starter pack
- les prompts et scripts de `workflow_ai/` sont des supports de conduite, pas des preuves runtime

## Articulation retenue
- `docs/` gouverne la lecture humaine, la continuite et la gouvernance
- `registry/` porte le modele declaratif machine-readable
- `workflow_ai/` gouverne la conduite d’execution

Regle pratique :
1. lire `docs/` pour savoir quoi faire et comment se rattacher au canon
2. lire `registry/` si la mission depend de surfaces, wrappers, machines ou modules declares
3. executer via `workflow_ai/` quand le lot entre en implementation ou en verification

## Gaps et points d'attention
- `docs/` reste large et heterogene ; il faut continuer a lire avec une hierarchie explicite
- `registry/` est actif, mais sa couverture ne remplace pas une preuve de terrain
- `workflow_ai/` est bien borne comme doctrine d'execution, mais reste volontairement incomplet pour la gouvernance produit

## Synthese du Bloc A
- `docs/` gouverne la lecture humaine et la continuite
- `registry/` porte le modele declaratif machine-readable
- `workflow_ai/` gouverne la conduite d’execution
- ces trois surfaces forment le noyau canonique de pilotage du repo

## Suite
- bloc suivant recommande : Bloc B (`modules/`, `scripts/`, `shared/`, `adapters/`, `schemas/`, `perf/`, `tools/`, `packages/`, `deploy_module_multi_machine/`)

## RISKS

- À qualifier.
