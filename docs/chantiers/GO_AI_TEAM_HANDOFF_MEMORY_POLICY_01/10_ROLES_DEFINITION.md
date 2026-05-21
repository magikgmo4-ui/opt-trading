---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_ROLES
doc_type: roles_definition
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 10_ROLES_DEFINITION

## Manager agent

| Field | Value |
|---|---|
| role_id | team_ai_manager |
| model | gpt-5-nano (primary), kimi-k2.5 (fallback) |
| autonomy_max | A4 (HITL) |
| responsibility | Coordonne les spécialistes, décide affectation, valide les handoffs |
| human_validation | Obligatoire pour tout write ou action sur surface sensible |
| source | `10_ROLES_JOBS_TASKS_INVENTORY.md` |

## Specialist — raisonnement

| Field | Value |
|---|---|
| role_id | specialist_reasoning |
| model | qwen3.5-plus |
| autonomy_max | A2 |
| responsibility | Propositions, analyse, patch complexe |
| handoff_input | Proposition packet, analyse request |
| handoff_output | Analyse, patch draft, recommandation |

## Specialist — volume

| Field | Value |
|---|---|
| role_id | specialist_volume |
| model | minimax-m2.5 |
| autonomy_max | A2 |
| responsibility | Extraction, inventaire, documentation masse |
| handoff_input | Scope de collecte, pattern de recherche |
| handoff_output | Inventaire structuré, documentation bulk |

## Specialist — long contexte

| Field | Value |
|---|---|
| role_id | specialist_long_context |
| model | big-pickle |
| autonomy_max | A2 |
| responsibility | Code reading, inventaire commits, cherry-pick |
| handoff_input | Commits SHA, paths, scope d'analyse |
| handoff_output | Analyse de code, résumé de commits, cherry-pick draft |

## Specialist — flash/tri

| Field | Value |
|---|---|
| role_id | specialist_flash_triage |
| model | gpt-5-nano |
| autonomy_max | A1 |
| responsibility | Triage rapide, classification, formats courts |
| handoff_input | Élément à classifier, seuils de décision |
| handoff_output | Classification, score de confiance, recommandation |
