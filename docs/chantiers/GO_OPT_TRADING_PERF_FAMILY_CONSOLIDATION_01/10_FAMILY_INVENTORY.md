---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_FAMILY_INVENTORY
doc_type: family_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - perf
  - inventory
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md
---

# 10_FAMILY_INVENTORY

## Baseline family

| Module | Baseline current | Registry | Famille normalized |
| --- | --- | --- | --- |
| `perf` | oui | non | `perf` |
| `perf_engine` | oui | oui | `perf` |

Preuve baseline:

- `13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv` ligne 61: `perf,functional_candidate,no,review_missing_registry,perf`
- `13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv` ligne 62: `perf_engine,functional_candidate,yes,none,perf`

## Vue d'ensemble

| Module | Surface visible | Role constate | Statut retenu |
| --- | --- | --- | --- |
| `modules/perf/` | `README.md`, `app.py`, `webhook.py`, `engine/`, `scripts/`, `data/` | facade canonique de famille, shims Python, wrappers operateur, point d'entree FastAPI canonique | owner canonique documentaire + runtime utile + compat active |
| `modules/perf_engine/` | `app/`, `config/`, `scripts/`, `README.md` | moteur CLI historique encore consomme, noyau logique reel | composant runtime utile historique / compat active |

## Detail `modules/perf/`

### Surface Python

- `modules/perf/app.py`
  - shim vers `perf.perf_app:app`
  - expose `modules.perf.app:app` comme chemin canonique prefere
- `modules/perf/webhook.py`
  - shim vers `adapters.webhook_to_perf`
- `modules/perf/engine/app/perf_engine.py`
  - shim vers `modules.perf_engine.app.perf_engine`

### Surface shell

- wrappers `cmd/menu/sanity`
- `install_shortcuts.sh`
- `perf_db_relocate.sh`

### Lecture

`modules/perf/` n'est pas une documentation vide.
Il porte la famille canonique de chemins et plusieurs points d'entree actifs, meme si la logique metier reste deleguee.

## Detail `modules/perf_engine/`

- `modules/perf_engine/app/perf_engine.py`
  - contient la logique reelle du moteur de performance CLI
  - charge positions + execution JSON
  - derive les etats `TRACKING`, `WATCHLIST`, `BLOCKED`, `INACTIVE`
  - expose les commandes `status`, `sample`, `track`, `export`, `explain`
- `scripts/cmd.sh`
  - lance encore `python3 -m modules.perf_engine.app.perf_engine`
- `README.md`
  - presente le module comme moteur autonome

## Nature de la famille

La famille n'est plus un simple doublon.

Elle est composee de :

- une facade canonique de famille: `modules/perf/`
- un noyau logique historique encore reellement execute: `modules/perf_engine/`

## Inventaire decisionnel

- `perf` n'est ni doc-only ni legacy pur
- `perf_engine` n'est plus seul pour representer la famille canonique, puisque les chemins preferes ont ete bascules sous `modules/perf/*`
- la canonicalite de famille et la realite d'execution ne sont plus au meme endroit
