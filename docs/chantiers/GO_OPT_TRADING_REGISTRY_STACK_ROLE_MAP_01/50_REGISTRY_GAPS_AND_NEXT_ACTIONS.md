---
doc_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01_REGISTRY_GAPS_AND_NEXT_ACTIONS
doc_type: gap_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - registry
  - gaps
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01/40_ROLE_DECISION.md
---

# 50_REGISTRY_GAPS_AND_NEXT_ACTIONS

## Gaps observes apres P1 + Desk + OpenClaw

### Gap G1 - readers absents de `modules_registry.yaml`

Le crosscheck baseline signalait encore hors registry :

- `modules_registry_reader`
- `machines_registry_reader`
- `wrappers_registry_reader`
- `registry_meta_reader`
- `registry_router`

Seul `ui_registry_msi` est deja present.

### Gap G2 - machine_target trop grossier

La stack registry melange des surfaces `admin_trading`, `msi_db_layer` et du `system-wide`.
Le modele courant de `modules_registry.yaml` reste trop grossier pour representer certaines surfaces mixtes sans approximation.

### Gap G3 - vocabulaire des descriptions

Certaines surfaces devront etre explicitement decrites comme :

- source de verite
- reader specialise
- facade de navigation
- surface UI operateur

pour eviter la confusion entre router et reader.

### Gap G4 - UI registry coherence

`ui_registry_msi` a un fallback local `config/ui_registry_seed.json`, ce qui est utile operatoirement mais cree un risque de divergence avec `registry/ui_surfaces_registry.yaml` si la gouvernance n'est pas explicite.

## Next actions recommandees

1. `GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01`
   - ajouter les readers manquants dans `modules_registry.yaml`
   - ajouter `registry_router`
   - requalifier `ui_registry_msi` si necessaire

2. `GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01`
   - expliciter la precedence entre fichiers centraux et fallbacks locaux
   - fixer les regles de derivation/export

3. `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01`
   - reprendre la suite P2 familles apres stabilisation de la couche registry

## Non-goal du present GO

- aucune mutation de `registry/modules_registry.yaml`
- aucune edition de `registry/meta_index.yaml`
- aucune fusion physique entre router et readers
