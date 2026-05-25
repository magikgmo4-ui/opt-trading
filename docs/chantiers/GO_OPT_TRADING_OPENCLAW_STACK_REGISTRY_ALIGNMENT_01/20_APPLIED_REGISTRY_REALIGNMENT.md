---
doc_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01_APPLIED_REGISTRY_REALIGNMENT
doc_type: applied_change
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - modules
  - openclaw
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01/10_TARGET_REGISTRY_DELTA.md
---

# 20_APPLIED_REGISTRY_REALIGNMENT

## Fichier modifie

- `registry/modules_registry.yaml`

## Entrees ajoutees

- `gateway_openclaw`
- `openclaw_config_modulaire`
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `install_module_openclaw`
- `openclaw_operator_bridge`

## Metadata posees

- `domain: operator_tools`
- `machine_target: any`
- `wrappers_expected: ["cmd", "menu", "sanity"]`
- priorites et dependances minimales coherentes avec les README modules

## Ce qui n'a pas ete change

- aucun wrapper dans `registry/wrappers_registry.yaml`
- aucun script runtime
- aucune doc hors dossier GO
