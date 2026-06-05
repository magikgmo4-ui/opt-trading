---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_BLOC_B
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
  - bloc_b
  - runtime
  - operations
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/11_synthese_bloc_a_canoniques.md
  - docs/deploy_module_multi_machine_continuity.md
  - deploy_module_multi_machine/README.md
---

# Bloc B — surfaces runtime et operatoires

## `modules/`
Role :
- coeur fonctionnel du repo
- surface principale des modules durables, readers, wrappers specialises et briques metier

Lecture observee :
- familles produit / desk : `desk_*`, `desk_pro*`, `desk_snapshot_ingest`, `desk_state`
- familles trading / calcul : `decision_engine`, `execution_engine`, `portfolio_engine`, `position_engine`, `risk_engine`, `probability_engine`, `perf_engine`
- familles collecte / marche : `collector_*`, `marketdata`, `market_scanner`, `derivatives_*`, `liquidation_analyzer`
- familles gouvernance / support : `repo_hygiene`, `repo_local_artifacts`, `repo_ownership_guard`, `memory_bricks`, `naming_normalizer`, `install_module`
- familles registry / lecture declarative : `machines_registry_reader`, `modules_registry_reader`, `registry_meta_reader`, `wrappers_registry_reader`, `registry_router`, `ui_registry_msi`
- familles openclaw / Trae / agents : `*_openclaw`, `trae_module_validator`, `validated_prompt_factory`
- familles machine / transfert : `reseau_ssh*`, `winscp_transfer`, `shared_sshfs_permanent`, `shared_files_sftp`

Lecture retenue :
- `modules/` concentre l'essentiel du code durable exploitable
- la surface est large ; elle melange produit, support, readers, wrappers et satellites machine
- pour une lecture repo-first, `modules/` doit etre lu par familles, pas comme un bloc homogene

Limites :
- la presence d'un module ne prouve pas a elle seule son statut live
- certains modules sont centraux produit, d'autres servent surtout l'ops, la gouvernance ou l'integration
- une synthese plus fine de `modules/` meriterait un lot dedie si l'objectif devient la cartographie interne des familles

## `scripts/`
Role :
- surface operatoire directe de wrappers, helpers shell et points d'entree de verification / maintenance

Structure observable :
- sous-dossiers machine / usage : `admin_trading/`, `db_layer/`, `desk_bridge/`, `git_ops/`, `release_ops/`, `reseau_audit/`, `reseau_fix/`, `reseau_ssh/`, `student/`, `ui_debug/`
- fichiers racine nombreux, surtout centres sur `desk_pro`, installation, patching UI, verification, hygiene repo et automatisation shell

Lecture retenue :
- `scripts/` porte l'outillage operatoire immediat
- cette surface sert d'interface entre la doctrine (`workflow_ai`), les modules durables et les machines cibles
- la granularite est pragmatique : beaucoup de scripts sont specialises, voire ponctuels

Limites :
- `scripts/` n'est pas une couche de gouvernance
- plusieurs scripts sont contextuels ou historiques ; leur presence n'implique pas qu'ils soient tous des entrypoints canoniques
- les wrappers structurants doivent etre lus avec `registry/` et les README / runbooks associes

## `shared/`
Role :
- petites briques transverses reutilisables

Contenu observe :
- `logger.py`
- `telegram_notify.py`

Lecture retenue :
- surface simple, legere, support de reutilisation plus que centre de gravite fonctionnel

## `adapters/`
Role :
- adaptateurs de passage entre surfaces

Contenu observe :
- `webhook_to_perf.py`

Lecture retenue :
- surface mince mais importante conceptuellement : elle porte le couplage entre un input externe et un modele interne

## `schemas/`
Role :
- schemas de validation et contrats techniques ponctuels

Contenu observe :
- `webhook_event_v1.json`

Lecture retenue :
- surface de contrat technique, petite mais normative
- a lire avec `docs/SCHEMAS.md` et les adaptateurs qui l'utilisent

## `perf/`
Role :
- surface applicative Perf

Contenu observe :
- `perf_app.py`

Lecture retenue :
- `perf/` est un sous-systeme cible, plus qu'un simple helper
- il reste compact a l'echelle du repo top-level, mais sa fonction est centrale dans le flux webhook -> perf

## `tools/`
Role :
- utilitaires operatoires ponctuels et aides d'integration

Contenu observe :
- `bitget_feed.py`
- `bitget_probe.py`
- `bitget_to_tv_runner.py`
- `emit_tv_payload.py`
- `hermes_bridge/`

Lecture retenue :
- `tools/` sert de boite a outils pratique
- cette surface peut contenir des scripts utiles sans etre elle-meme une couche canonique de gouvernance

## `packages/`
Role :
- espace package / workspace code mutualise

Contenu observe :
- `collectors_core/`
  - `src/`
  - `tests/`
  - `README.md`

Lecture retenue :
- surface encore compacte
- probable noyau mutualisable pour les collectors, distinct de `modules/` tout en restant support actif

## `deploy_module_multi_machine/`
Role :
- outillage specialise de deploiement multi-machine depuis `admin-trading`

Lecture retenue :
- surface active et assumee hors `modules/`
- s'appuie sur `registry/` quand il est disponible, avec fallback si besoin
- couvre planification, preflight, deploiement, sanity distante et verrouillage de run

Limites :
- cible POSIX/Linux uniquement
- ne prouve pas a lui seul l'etat live de toutes les cibles
- reste un outil d'orchestration, pas une couche de gouvernance

## Synthese du Bloc B
- `modules/` est la surface durable la plus dense du repo
- `scripts/` porte l'ops immediate et les wrappers shell
- `shared/`, `adapters/`, `schemas/`, `tools/`, `packages/` sont des surfaces support plus fines mais structurellement utiles
- `perf/` et `deploy_module_multi_machine/` sont des surfaces speciales a forte valeur operatoire

## Suite
- bloc suivant recommande : Bloc C (`data/`, `state/`, `student/`, `tests/`, `tradingview/`, `contracts/`, `audit/`)

## RISKS

- À qualifier.
