---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_HANDOFF
doc_type: handoff_protocol
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 20_HANDOFF_PROTOCOL

## Handoff packet schema

```json
{
  "handoff_id": "uuid",
  "source_role": "manager | specialist_reasoning | specialist_volume | ...",
  "target_role": "manager | specialist_reasoning | specialist_volume | ...",
  "task_id": "ref to task",
  "packet_type": "request | response | escalation | completion",
  "payload": { ... },
  "context_ref": "memory key for shared context",
  "validation": {
    "required_fields": ["handoff_id", "source_role", "packet_type", "payload"],
    "reject_if_missing": ["handoff_id", "packet_type"]
  },
  "timestamp": "ISO8601",
  "ttl_minutes": 30
}
```

## Validation rules

- Rejeter tout packet sans `handoff_id`
- Rejeter tout packet sans `packet_type` valide (`request`, `response`, `escalation`, `completion`)
- Rejeter tout packet avec `source_role` inconnu du registry
- Rejeter tout packet avec `target_role` inconnu du registry
- Rejeter tout packet expiré (`ttl_minutes` dépassé)
- Logger tout rejet dans le ledger (G06)

## Escalation

Si un spécialiste ne peut pas traiter un handoff (timeout, erreur, doute) :
1. Le packet est marqué `escalation`
2. Routé vers le manager
3. Le manager décide : re-tenter, assigner autre spécialiste, ou escalader à l'humain

## Completion

- Tout handoff complété produit un `completion` packet
- Le completion contient le résultat ET le contexte mis à jour
- Le manager confirme la completion avant archivage
