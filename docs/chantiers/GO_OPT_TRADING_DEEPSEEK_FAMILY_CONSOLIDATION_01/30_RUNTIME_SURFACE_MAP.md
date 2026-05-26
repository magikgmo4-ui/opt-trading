---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_RUNTIME_SURFACE_MAP
doc_type: runtime_surface_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - runtime
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/20_CALLERS_AUDIT.md
---

# 30_RUNTIME_SURFACE_MAP

## Logical map

```text
deepseek_hub
  -> unified menu/cmd
  -> patches deepseek_response + deepseek_thinking
  -> delegates some roadmap flows to deepseek_student

deepseek_response
  -> Ollama /api/chat response
  -> _student_archive/response

deepseek_thinking
  -> Ollama think=true
  -> _student_archive/thinking

deepseek_student
  -> transition surface
  -> points to scripts/student/ and student/scripts/
```

## Runtime classification

| Surface | Classification |
| --- | --- |
| `deepseek_hub` | hub operateur actif |
| `deepseek_response` | compatibilite operatoire active |
| `deepseek_thinking` | compatibilite operatoire active |
| `deepseek_student` | legacy/transitoire, usage limite |

## Structure retenue

La runtime family se lit comme un **hub de convergence** avec satellites, pas comme quatre surfaces equivalentes.
