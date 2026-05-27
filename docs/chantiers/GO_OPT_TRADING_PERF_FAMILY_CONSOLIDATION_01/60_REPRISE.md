---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - modules
  - perf
  - reprise
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md
---

# 60_REPRISE

## Resume executif

- branche locale rebasee sur `origin/sot/mainline`
- lot Vision checkpointe et committe avant ouverture du lot Perf
- baseline `CURRENT_BASELINE_2026_05_20` confirmee disponible localement
- decision Perf fixee:
  - `perf` = owner canonique documentaire + runtime utile de famille
  - `perf_engine` = composant moteur historique encore actif

## Fichiers crees

- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/40_SURVIVOR_DECISION.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/60_REPRISE.md`

## Diff summary

- clarifie que `perf_engine` n'est plus le survivant canonique unique
- etabli `perf` comme facade canonique/runtime utile de famille
- preserve `perf_engine` comme moteur historique encore actif
- prepare un realignement registry separe sans mutation dans ce lot

## Commandes utiles de verification

```bash
rg -n "modules\.perf\.app|modules\.perf\.engine\.app\.perf_engine|modules\.perf_engine\.app\.perf_engine" .
rg -n "module_name: perf_engine|module_name: perf" registry/modules_registry.yaml
rg -n "CURRENT_BASELINE_2026_05_20|perf_engine,functional_candidate|perf,functional_candidate" docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01
```

## Resultats attendus

- le dossier chantier contient les 7 livrables attendus
- la decision `perf owner canonique / perf_engine moteur historique actif` est explicite
- aucune mutation runtime ni registry n'apparait dans le diff

## Rollback

1. supprimer `docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/`
2. verifier le worktree restant avant toute autre action

## Next GO recommandes

1. `GO_OPT_TRADING_PERF_FAMILY_REGISTRY_REALIGNMENT_01`
2. `GO_OPT_TRADING_PERF_ENGINE_PHYSICAL_ABSORPTION_CADRAGE_01`

## Objet du GO physique/runtime ensuite

Le GO physique/runtime a preparer ensuite doit trancher si :

- l'implementation de `modules/perf_engine/` est physiquement absorbee sous `modules/perf/engine/`, ou
- `perf_engine` reste un sous-module support officiellement conserve.

Ce lot doit rester distinct du present GO doc-only.
