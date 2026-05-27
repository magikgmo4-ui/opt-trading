---
doc_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01_DECISION_NOTES
doc_type: decision_notes
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - desk
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/40_ROLE_DECISION.md
---

# 30_DECISION_NOTES

## Decision structurante

Le registry modules doit decrire la stack Desk selon un partage de roles, pas comme un faux survivant unique.

## Notes de lecture

- `desk_pro` devient l'ancre canonique de stack dans la registry
- `desk_pro_runner` cesse d'etre decrit comme si lui seul portait l'execution
- `desk_pro_orchestrator` est explicitement visible comme coeur d'execution
- `desk_common` est reconnu comme support shared, sans sur-promesse produit
- les satellites `desk_*` sont conserves comme surfaces distinctes et utiles

## Risque residuel

Le registry reste une photo logique.
Il ne tranche pas encore les futures absorptions physiques possibles, notamment pour `desk_pro_dashboard` ou `desk_snapshot_ingest`.
