---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_BLOC_D
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
  - bloc_d
  - archive
  - local
  - cache
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/governance/REPO_ROOT_POLICY.md
---

# Bloc D — surfaces support, archive et local-only

## `_archive/`
Role :
- archive locale assumee

Structure observee :
- `legacy_modules/`
- `root_backups/`

Lecture retenue :
- surface d'archive explicite, hors perimetre actif
- utile pour conserver des backups racine et des variantes legacy sans les laisser polluer les surfaces actives

## `tmp/`
Role :
- temporaires locaux et bundles de travail

Contenu observe :
- bundles/documentation de travail (`GO_INDEX_ALIGNMENT_IDE_BUNDLE`, `journal_api_extraction_bundle_v1`)
- scripts ponctuels (`inject_init.py`, `test_bitget.py`)

Lecture retenue :
- surface de transit et de test local
- ne doit pas etre lue comme une couche canonique du produit

## `__pycache__/`
Role :
- cache Python

Lecture retenue :
- pure surface technique locale
- aucune valeur de gouvernance ou de runtime durable

## `.ruff_cache/`
Role :
- cache d'outillage lint

Lecture retenue :
- support local uniquement

## `.uv-cache/`
Role :
- cache de l'ecosysteme `uv`

Lecture retenue :
- support de build / resolution local
- non significatif pour la structure fonctionnelle du repo

## `.uv-python/`
Role :
- interpreteurs / runtimes Python locaux geres par `uv`

Lecture retenue :
- surface purement locale a l'environnement de travail

## `.secrets/`
Role :
- support local pour exemples / gabarits de secrets

Contenu observe :
- `bitget.env.example`

Lecture retenue :
- surface sensible par nature, meme si le contenu observe est un exemple
- a traiter comme support local, pas comme source declarative canonique

## Regle de lecture du Bloc D
- ces surfaces ne doivent pas guider la lecture produit ou gouvernance
- elles peuvent etre utiles pour comprendre un environnement local, une archive ou un cache
- elles doivent rester explicitement subordonnees aux surfaces canoniques et runtime

## Synthese du Bloc D
- `_archive/` conserve l'historique local assume
- `tmp/` sert de zone de transit locale
- `__pycache__/`, `.ruff_cache/`, `.uv-cache/`, `.uv-python/` relevent du cache outillage
- `.secrets/` est une surface locale sensible, meme quand elle ne contient qu'un exemple

## Suite
- le parent dispose maintenant des blocs A, B, C et D
- prochaine etape logique : produire un recap parent ou decider si la profondeur atteinte suffit
