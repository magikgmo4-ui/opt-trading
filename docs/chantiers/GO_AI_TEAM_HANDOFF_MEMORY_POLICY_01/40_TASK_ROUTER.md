---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_TASK_ROUTER
doc_type: task_router
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 40_TASK_ROUTER

## Règles d'affectation

| Task type | Spécialiste | Priorité | File |
|---|---|---|---|
| READ_INVENTORY | specialist_volume | P2 | volume_queue |
| PATCH_DRAFT | specialist_reasoning | P1 | reasoning_queue |
| DOC_DRAFT | specialist_volume | P2 | volume_queue |
| TESTPLAN | specialist_reasoning | P1 | reasoning_queue |
| CHERRY_PICK_INVENTORY | specialist_long_context | P2 | long_context_queue |
| FAST_TRIAGE | specialist_flash_triage | P0 (immédiat) | triage_queue |
| ENDPOINT_AUDIT | specialist_long_context | P2 | long_context_queue |
| WRITE_GATED | specialist_reasoning (→ manager) | P0 | reasoning_queue + human_approval |

## File de priorité

- P0 : immédiat (triage, write gated)
- P1 : prochain tour (patch, testplan)
- P2 : file d'attente normale (inventaire, doc, audit)

## Routage par défaut

Si aucun spécialiste n'est spécifié dans le handoff packet, le manager applique les règles d'affectation ci-dessus.

Si le spécialiste cible est indisponible :
1. Escalade P1/P2 vers un spécialiste de capacité proche
2. P0 : toujours vers le manager (qui décide)

## Rejet

- Tâche sans task_type reconnu → rejetée avec erreur `UNKNOWN_TASK_TYPE`
- Tâche avec modèle non vérifié → rejetée avec erreur `UNVERIFIED_MODEL`
- Tâche sans packet valide → rejetée avec erreur `INVALID_PACKET`
