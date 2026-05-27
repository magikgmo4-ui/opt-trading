---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_REGISTRY_ACTIONS
doc_type: registry_actions
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - registry
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/40_ROLE_DECISION.md
---

# 50_REGISTRY_ACTIONS

## Invariant du lot

Aucune mutation registry n'est executee dans ce GO.

## Actions registry requises ensuite

1. ajouter `deepseek_hub` comme owner documentaire / hub operateur de la famille
2. ajouter `deepseek_response` et `deepseek_thinking` comme composants actifs de compatibilite
3. decider si `deepseek_student` doit etre :
   - explicitement note legacy/transitoire dans la registry, ou
   - laisse hors registry tant que la fermeture physique n'est pas traitee

## GO suivant naturel cote registry

- `GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01`

## GO physique/runtime distinct ensuite

- traiter la frontiere entre `modules/deepseek_student/`, `scripts/student/` et `student/scripts/`
- confirmer si `deepseek_hub` absorbe un jour totalement `response` et `thinking`
