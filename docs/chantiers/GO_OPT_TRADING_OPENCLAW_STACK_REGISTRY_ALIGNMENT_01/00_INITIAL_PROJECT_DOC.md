---
doc_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01_INITIAL_PROJECT_DOC
doc_type: chantier_registry_realignement
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
  - stack
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv
  - modules/gateway_openclaw/README.md
  - modules/openclaw_config_modulaire/README.md
  - modules/openclaw_operator_bridge/README.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Aligner `registry/modules_registry.yaml` avec la stack `openclaw` du repo courant.

## Modules cibles

- `gateway_openclaw`
- `openclaw_config_modulaire`
- `configure_openclaw`
- `doctor_openclaw`
- `evidence_openclaw`
- `install_module_openclaw`
- `openclaw_operator_bridge`

## Delta vise

- sortir la famille `openclaw` de l'etat `review_missing_registry`
- representer explicitement le runtime gateway, la configuration, le diagnostic, la preuve, l'installation et le bridge d'integration

## Contraintes appliquees

- mutation limitee a `registry/modules_registry.yaml`
- aucun changement runtime
- aucun changement wrappers registry
- aucune doc globale hors dossier de GO
- `secrets/` hors perimetre

## Verdict attendu

`PASS`
