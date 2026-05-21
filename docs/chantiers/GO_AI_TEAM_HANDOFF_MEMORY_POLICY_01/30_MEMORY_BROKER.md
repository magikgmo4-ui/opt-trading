---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_MEMORY
doc_type: memory_broker
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
status: draft
---

# 30_MEMORY_BROKER

## Stockage

Le memory broker stocke le contexte partagé entre agents :

| Storage | Usage | Rétention |
|---|---|---|
| `data/runtime_health/memory/` | Contexte de session actif | Durée de la session |
| Fichier JSON par clé | Contexte persistant (références, décisions) | 7 jours |
| Mémoire éphémère (dict runtime) | Handoff en cours, escalade | Jusqu'à completion |

## Structure d'une entrée mémoire

```json
{
  "key": "session_<uuid>",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "ttl_minutes": 1440,
  "context": {
    "active_tasks": [],
    "decisions": [],
    "references": [],
    "artifacts": []
  },
  "locked_by": null
}
```

## Rotation

- Entrée TTL expirée → archivée dans `data/runtime_health/memory/archive/`
- Archive rétention : 30 jours
- Rotation déclenchée par le manager à chaque fin de session

## Recovery

- Si le memory broker est inaccessible, les agents utilisent un fallback fichier local
- Le manager détecte l'inaccessibilité et replanifie les handoffs
- Les entrées verrouillées (`locked_by`) sont automatiquement déverrouillées après 5 min sans heartbeat
