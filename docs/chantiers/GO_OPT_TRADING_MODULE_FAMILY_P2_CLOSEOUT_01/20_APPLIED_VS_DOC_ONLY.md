---
doc_id: GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01_APPLIED_VS_DOC_ONLY
doc_type: applied_scope_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_MODULE_FAMILY_P2_CLOSEOUT_01
status: draft_for_review
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - modules
  - family
  - p2
  - applied
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-26
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/60_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01/40_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01/40_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01/40_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/60_REPRISE.md
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01/90_REPRISE_POINT.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01/20_ACCEPTANCE_REVIEW.md
---

# 20_APPLIED_VS_DOC_ONLY

## Classification

| GO | Domain | Nature |
| --- | --- | --- |
| `GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01` | `desk` | doc-only |
| `GO_OPT_TRADING_DESK_STACK_REGISTRY_REALIGNMENT_01` | `desk` | registry-applied |
| `GO_OPT_TRADING_OPENCLAW_STACK_REGISTRY_ALIGNMENT_01` | `openclaw` | registry-applied |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01` | `openclaw` | review/acceptance on code already landed |
| `GO_OPT_TRADING_REGISTRY_STACK_ROLE_MAP_01` | `registry` | doc-only |
| `GO_OPT_TRADING_REGISTRY_STACK_REALIGNMENT_IMPL_01` | `registry` | registry-applied |
| `GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01` | `deepseek` | doc-only |
| `GO_OPT_TRADING_DEEPSEEK_FAMILY_REGISTRY_REALIGNMENT_01` | `deepseek` | registry-applied |

## Interpretation

- `desk` et `deepseek` ont suivi le meme motif: lecture/decision d'abord, puis realignement registry ensuite.
- `registry` a suivi un motif equivalent mais a l'echelle transverse de la stack de registres.
- `openclaw` a depasse le simple realignement registry avec une acceptance review parent sur la chaine orchestrateur.

## Important boundary

Ce closeout P2 ne pretend pas que tout est maintenant physiquement consolide.

Il formalise plutot que:

- les lectures de roles P2 sont posees
- les realignements registry centraux les plus structurants sont appliques
- les nettoyages physiques/runtime restants doivent partir de ces decisions, pas les redefinir
