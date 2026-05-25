---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_REGISTRY_ACTIONS
doc_type: registry_actions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - registry
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/40_ROLE_DECISION.md
---

# 50_REGISTRY_ACTIONS

## Invariant du lot

Aucune mutation de `registry/modules_registry.yaml` n'est executee dans ce GO.

## Gaps registry etablis

### Gap R1 - `desk_pro`

- absent de `modules_registry.yaml`
- alors qu'il porte le coeur partage et l'owner canonique de stack

### Gap R2 - `desk_pro_orchestrator`

- absent de `modules_registry.yaml`
- alors qu'il porte le backbone d'execution

### Gap R3 - `desk_common`

- absent de `modules_registry.yaml`
- alors qu'il reste un support shared explicite dans la stack

### Gap R4 - descriptions a realigner

Les modules deja presents devront etre relus pour mieux refleter la carte de roles :

- `desk_pro_runner`
- `desk_pro_dashboard`
- `desk_capture_inputs`
- `desk_analyze`
- `desk_state`
- `desk_snapshot_ingest`
- `desk_retention`

## Actions recommandees ensuite

1. ajouter `desk_pro` comme owner canonique de stack
2. ajouter `desk_pro_orchestrator` comme composant coeur d'execution
3. ajouter `desk_common` comme support shared minimal
4. requalifier les descriptions des autres modules pour distinguer coeur, facade et satellites

## GO suivant pour registry

`GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01`

## GO physique/runtime a differer

Un GO physique distinct pourra ensuite evaluer une absorption partielle de :

- `desk_pro_dashboard` dans `desk_pro`
- `desk_snapshot_ingest` dans une surface Desk Pro interne

Mais ce n'est pas requis pour valider la carte de roles actuelle.
