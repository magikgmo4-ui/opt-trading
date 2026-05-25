---
doc_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01_INITIAL_PROJECT_DOC
doc_type: chantier_registry_realignement
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/40_ROLE_DECISION.md
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/50_REGISTRY_ACTIONS.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Realigner `registry/modules_registry.yaml` avec la carte de roles de la stack `desk*` / `desk_pro*` actee par `GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01`.

## Delta vise

1. ajouter `desk_pro`
2. ajouter `desk_pro_orchestrator`
3. ajouter `desk_common`
4. requalifier les entrees `desk_*` et `desk_pro_*` deja presentes pour refleter coeur, facade et satellites

## Contraintes appliquees

- mutation limitee a `registry/modules_registry.yaml`
- aucun changement runtime
- aucun changement wrappers registry
- aucun changement docs globaux
- `secrets/` hors perimetre

## Verdict attendu

`PASS`
