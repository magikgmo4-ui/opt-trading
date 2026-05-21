---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_HUMAN_GATE
doc_type: human_validation_gate
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 60_HUMAN_VALIDATION_GATE

## Quand la gate est requise

| Action | Gate | Délai max |
|---|---|---|
| Write sur repo (PATCH_DRAFT → commit) | human_approve | 24h |
| Write sur app externe (Airtable, ClickUp, etc.) | human_approve | 24h |
| Escalade depuis manager | human_review | 4h |
| Nouveau spécialiste non vérifié | human_approve | 48h |
| Handoff TTL dépassé sans réponse | human_notify | 1h |

## Format de la demande d'approbation

```json
{
  "approval_id": "uuid",
  "type": "human_approve | human_review | human_notify",
  "submitted_by": "manager | specialist_... | system",
  "task_ref": "task_id",
  "justification": "texte",
  "risks": ["risk1", "risk2"],
  "proposed_action": "description",
  "deadline": "ISO8601",
  "status": "pending | approved | rejected | expired"
}
```

## Comportement par défaut

- Si aucun humain ne répond dans le délai → l'action est REFUSÉE par défaut (deny-by-default)
- Le manager peut re-soumettre une demande avec plus de justification
- En cas d'urgence, le kill switch (G08) peut bypass toutes les gates en attente
