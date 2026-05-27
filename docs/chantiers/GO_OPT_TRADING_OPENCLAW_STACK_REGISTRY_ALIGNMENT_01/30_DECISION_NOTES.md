---
doc_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01_DECISION_NOTES
doc_type: decision_notes
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - openclaw
  - registry
surface: registry
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - modules/gateway_openclaw/README.md
  - modules/openclaw_config_modulaire/README.md
  - modules/openclaw_operator_bridge/README.md
---

# 30_DECISION_NOTES

## Decision structurante

Le registry modules doit representer la suite `openclaw` comme une stack de roles, pas comme un seul module implicite.

## Notes de lecture

- `gateway_openclaw` porte le runtime explicite et reste distinct de `doctor_openclaw`
- `openclaw_config_modulaire` porte la securite de configuration et le rollback; `configure_openclaw` reste la facade operateur live
- `evidence_openclaw` est une surface documentaire utile, pas un composant runtime gateway
- `install_module_openclaw` ne doit pas etre confondu avec `install_module`
- `openclaw_operator_bridge` est une integration active d'opt-trading, deja prouvee operationnelle dans les docs recentes

## Limite assumee

Le champ `machine_target` reste grossier (`any`) car la registry courante n'exprime pas proprement la target `db-layer` / user `openclaw`.
Ce point pourra faire l'objet d'un GO registry transverse ulterieur.
