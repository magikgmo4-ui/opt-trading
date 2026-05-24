---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_REGISTRY_ACTIONS
doc_type: registry_actions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - perf
  - registry
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
---

# 50_REGISTRY_ACTIONS

## Invariant du lot

Aucune mutation de `registry/modules_registry.yaml` n'est executee dans ce GO.

## Etat registry actuel

- `perf_engine` est present
- `perf` est absent

## Gap registry etabli

La registry ne reflete plus la canonicalite de chemins active :

- les launchers et l'orchestrateur ont bascule vers `modules/perf/*`
- mais seule la surface historique `perf_engine` est encore en registry

## Actions registry requises ensuite

### Action R1

Ajouter `perf` comme entree canonique de famille, avec role explicite : facade runtime/utilitaire de la famille PERF.

### Action R2

Conserver `perf_engine` en registry, mais requalifier sa description pour exprimer qu'il s'agit du moteur historique actif derriere la facade `perf`.

### Action R3

Verifier la couverture wrappers :

- `perf` expose `cmd/menu/sanity`
- `perf_engine` expose aussi ses wrappers historiques

La registry devra expliciter si `perf_engine` reste operator-visible ou seulement support/runtime.

## Actions registry a ne pas faire

- ne pas supprimer `perf_engine`
- ne pas reclassifier `perf` en legacy
- ne pas traiter `perf_engine` comme archive tant que l'implementation reelle n'a pas ete physiquement absorbee ou remplacee

## GO suivant necessaire pour mutation registry

`GO_OPT_TRADING_PERF_FAMILY_REGISTRY_REALIGNMENT_01`

Objet attendu:

- ajouter `perf`
- requalifier `perf_engine`
- aligner la registry avec la canonicalite de chemins et les wrappers reels
