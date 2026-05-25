---
doc_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01_APPLIED_REGISTRY_REALIGNMENT
doc_type: applied_change
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01
status: draft_for_review
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - modules
  - desk
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01/10_TARGET_REGISTRY_DELTA.md
---

# 20_APPLIED_REGISTRY_REALIGNMENT

## Fichier modifie

- `registry/modules_registry.yaml`

## Changements appliques

### Ajouts

- `desk_pro`
- `desk_pro_orchestrator`
- `desk_common`

### Requalifications de role

- `desk_pro_runner` -> facade operateur canonique
- `desk_pro_dashboard` -> dashboard/export des runs
- `desk_capture_inputs` -> extraction d'inputs
- `desk_analyze` -> analyse locale snapshot-driven
- `desk_state` -> state canonique lateral
- `desk_snapshot_ingest` -> ingest SFTP snapshots
- `desk_retention` -> hygiene des artefacts

### Ajustements de metadata

- `operator_visible`
- `ui_related`
- `wrappers_expected`
- `dependencies`
- `description`

## Ce qui n'a pas ete change

- aucun fichier runtime
- aucune entree `wrappers_registry.yaml`
- aucune doc globale hors dossier de GO
