---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_BLOC_C
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
  - bloc_c
  - data
  - state
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - student/README.md
  - student/INDEX.md
---

# Bloc C — surfaces produit, donnees et etat

## `data/`
Role :
- stockage des sorties, artefacts et sous-produits metier par domaine

Structure observable :
- familles presentes : `dashboard`, `decision`, `derivatives`, `desk_runs`, `execution`, `journal`, `liquidation`, `perf`, `portfolio`, `position`, `probability`, `ranker`, `risk`, `scan`

Lecture retenue :
- `data/` n'est pas une surface canonique de gouvernance ; c'est une surface de matiere produite par le systeme
- la structure suit les domaines fonctionnels du repo
- `desk_runs/` apparait comme un sous-ensemble particulierement actif

Point d'attention :
- `data/journal/` existe encore, mais comme bucket de donnees (`journal_entries_*.json`), pas comme systeme de continuite documentaire
- il ne faut pas le confondre avec l'ancien `journal/` de racine qui a ete retire

## `state/`
Role :
- etat persistant leger et configurations runtime

Contenu observe :
- `positions.json`
- `risk_config.json`
- dossiers `vpf_*_2026-03-14/` contenant des prompts generes

Lecture retenue :
- `state/` stocke a la fois de la configuration de travail et des sorties persistantes liees a certains lots
- cette surface est plus proche du runtime et de la reprise technique que de la documentation canonique

Limites :
- les contenus dates dans `state/` peuvent etre utiles a la trace, mais ils ne remplacent pas les decisions ou les closeouts

## `student/`
Role :
- workspace canonique du perimetre `student`

Structure observable :
- `bin/`, `config/`, `docs/`, `exports/`, `scripts/`, `validation/`
- fichiers d'entree : `README.md`, `INDEX.md`

Lecture retenue :
- `student/` est une sous-surface machine quasi-produit a part entiere
- cette surface a sa propre structuration interne, ses raccourcis canoniques et sa documentation locale
- elle sert a la fois d'environnement operateur, de point de migration et de surface de validation

Points d'entree utiles :
- `student/README.md`
- `student/INDEX.md`
- `student/exports/kanban/*`

## `tests/`
Role :
- surface de tests repo-top-level

Contenu observe :
- uniquement `__pycache__/` a ce stade

Lecture retenue :
- il n'existe pas ici de couverture de test top-level riche
- la strategie de verification semble plutot distribuee entre modules, scripts de sanity et validations contextuelles

## `tradingview/`
Role :
- surface de compatibilite et d'integration TradingView

Contenu observe :
- `smartmoney_webhook_server_compat.pine`

Lecture retenue :
- surface etroite, specialisee, mais lisible
- sert de point de compatibilite cote TradingView plutot que de couche applicative large

## `contracts/`
Role :
- contrats metier specialises

Contenu observe :
- `schemas_marketdata/v1/market_snapshot_v1.txt`
- `schemas_marketdata/v1/pair_market_snapshot_v1.txt`

Lecture retenue :
- surface contractuelle minimale mais normative
- a lire comme extension specialisee de la logique schema/contrat du repo

## `audit/`
Role :
- conservation de packs de preuve et d'audits dates

Contenu observe :
- `2026-03-20/student_validation_pack_20260320.zip`

Lecture retenue :
- `audit/` est une surface de lecture et de preuve, pas une couche de pilotage
- sa valeur tient a la conservation des artefacts de validation

## Synthese du Bloc C
- `data/` et `state/` portent la matiere produite et l'etat persistant
- `student/` est une sous-surface machine forte, avec sa propre coherence interne
- `tests/` est faible au niveau top-level
- `tradingview/`, `contracts/` et `audit/` sont des surfaces etroites mais distinctes et utiles

## Suite
- bloc suivant recommande : Bloc D (`_archive/`, `tmp/`, caches et surfaces locales)
