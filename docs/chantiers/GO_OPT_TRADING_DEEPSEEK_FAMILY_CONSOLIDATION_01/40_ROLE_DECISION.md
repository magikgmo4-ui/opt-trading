---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_ROLE_DECISION
doc_type: role_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - roles
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md
---

# 40_ROLE_DECISION

## Reponses tranchees

### 1. Owner canonique de la famille DeepSeek

- **`deepseek_hub`**

### 2. `deepseek_hub`

Verdict: **hub operateur + owner documentaire convergent**, mais pas encore owner runtime unique complet.

### 3. `deepseek_response`

Verdict: **runtime utile de compatibilite**, pas legacy pur, pas owner de famille.

### 4. `deepseek_student`

Verdict: **legacy de transition encore utilisable en mode limite**, lie a `student`/Ollama et a la migration vers `student/scripts/`.

### 5. `deepseek_thinking`

Verdict: **composant actif de raisonnement en compatibilite**, conserve sous `deepseek_hub`.

### 6. Nature de la famille

Verdict: **stack complementaire avec noyau convergent `deepseek_hub`**, pas lignee lineaire deja resolue.

## Classement final

| Surface | Classement |
| --- | --- |
| `deepseek_hub` | owner documentaire + hub operateur |
| `deepseek_response` | satellite de compatibilite actif |
| `deepseek_thinking` | satellite de compatibilite actif |
| `deepseek_student` | legacy/transitoire, usage limite |

## Verdict

**PASS**

La famille est clarifiee sans mutation runtime ni registry.
