---
doc_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01_TARGET_REGISTRY_DELTA
doc_type: registry_delta
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
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01/00_INITIAL_PROJECT_DOC.md
---

# 10_TARGET_REGISTRY_DELTA

## Stack role map retenu

| Module | Role registry retenu |
| --- | --- |
| `gateway_openclaw` | runtime gateway owner |
| `openclaw_config_modulaire` | configuration structurelle modulaire |
| `configure_openclaw` | facade operateur de configuration live |
| `doctor_openclaw` | facade de diagnostic et health verification |
| `evidence_openclaw` | preuve et continuite documentaire |
| `install_module_openclaw` | point d'entree d'installation |
| `openclaw_operator_bridge` | contrat d'integration opt-trading -> OpenClaw |

## Choix de modelisation

- la suite `openclaw` est alignee comme stack complementaire
- `gateway_openclaw` est l'ancre runtime la plus critique
- `openclaw_config_modulaire` ne doit pas etre reduit a la facade `configure_openclaw`
- `openclaw_operator_bridge` reste distinct du runtime gateway: c'est le point de contact borne pour opt-trading
