---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - perf
  - consolidation
  - family
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Clarifier la frontiere entre `modules/perf` et `modules/perf_engine`, puis fixer si :

- `perf_engine` reste le survivant canonique de famille ;
- `perf` est une simple compatibilite ;
- ou si la famille a bascule vers une facade canonique `perf` avec `perf_engine` conserve pour compatibilite/runtime historique.

## Dependances verifiees

- le lot `GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01` est maintenant committe localement
- la branche locale a ete rebasee sur `origin/sot/mainline`
- les fichiers baseline modules demandes sont maintenant presents dans le checkout courant
- `CURRENT_BASELINE_2026_05_20 = 98` reste la baseline de travail

## Perimetre

- `modules/perf`
- `modules/perf_engine`

## Sources lues

- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md`
- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv`
- `docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/01_PERF_CLUSTER_INVENTORY.md`
- `docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/02_PERF_CONSOLIDATION_MAP.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01/01_IMPLEMENTATION_NOTES.md`
- `docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01/01_IMPLEMENTATION_NOTES.md`
- `modules/perf/README.md`
- `modules/perf_engine/README.md`
- `registry/modules_registry.yaml`

## Questions a trancher

1. Quels callers pointent vers `perf` ?
2. Quels callers pointent vers `perf_engine` ?
3. `perf_engine` est-il bien le survivant canonique ?
4. `perf` est-il legacy, compat, doc/gouv ou runtime utile ?
5. Quelle action registry est necessaire ?
6. Quel GO physique/runtime serait necessaire ensuite ?

## Contraintes appliquees

- mode `doc-only`
- aucune suppression
- aucun refactor runtime
- aucune mutation registry
- aucun index global ajoute
- machine_owner: `admin-trading`

## Hypothese de travail

Les lots anterieurs `PERF_MODULE_RESTRUCTURE_*` et `PERF_PATH_SWITCH_*` ont probablement deplace la canonicalite de chemin vers `modules/perf/*`, sans supprimer `modules/perf_engine/*` pour compatibilite.
